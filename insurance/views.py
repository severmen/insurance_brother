import hashlib

from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, CreateView, FormView, RedirectView
from .models import Services
from .form import RegisterForm,Search_Services,Request_for_a_call_Form,PasswordRecoverForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse_lazy
from .templates_filter import get_next_url
from .services import MaintenanceServices
from django.contrib.auth.models import User


class Main(ListView):
    '''
    Главная страница
    '''
    model = Services
    template_name = 'insurance/index.html'
    context_object_name = 'Services'
    paginate_by = 2

    def get_queryset(self):
        '''
        производит филтрацию во выбранным параметрам
        '''
        filter = Search_Services(data=self.request.GET)
        return filter.filter(super().get_queryset())

    def get_context_data(self, **kwargs):
        '''
        Добовляет форму для филтрации
        '''
        context = super(Main, self).get_context_data(**kwargs)
        context['form'] = Search_Services(data = self.request.GET)
        return context

@csrf_exempt
def add_request_for_a_call(request):
    '''
    Волидиурет запрос на звонок и добовлет в БД
    '''
    form = Request_for_a_call_Form(request.POST)
    if form.is_valid():
        student = form.save()
        return HttpResponse("Спасибо мы организатор свяжентся с вами в ближайшее свободное время")
    else:
        return HttpResponse("Ошибки в формате данных")


class Register(SuccessMessageMixin, CreateView):
    template_name = 'insurance/register.html'
    form_class = RegisterForm
    success_url = "/admin"
    success_message = "Пользователь успешно зарегистрирован, небходимо потвердить email, для дальнейшего использования"

def user_logout(request):
    '''
    выполняет выход из системы
    '''
    logout(request)
    return redirect("/")


class PasswordRecovery(FormView):
    template_name = 'insurance/password_recover.html'
    form_class = PasswordRecoverForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #channel = pika_connect()
        #email.send_new_request()
        return super().form_valid(form)

class registration_confirmations(RedirectView):
    #url = "http://localhost:8000/"
    url = reverse_lazy('admin:index')
    def get_redirect_url(self, *args, **kwargs):
        try:
            one_user_info = User.objects.get(id = args[0])
            if one_user_info.is_staff == True:
                raise Exception()
            hash = hashlib.sha1(
                (str(one_user_info.id) + one_user_info.first_name + one_user_info.password).encode('utf-8')).hexdigest()
            if hash == args[1]:
                one_user_info.is_staff = True
                one_user_info.save()
            else:
                raise Exception()

            messages.add_message(self.request, messages.ERROR, 'Пользователь успешно активирован')

        except:
            messages.add_message(self.request, messages.INFO, 'Ссылка не действительна')
        #article = get_object_or_404(Article, pk=kwargs['pk'])
        #article.update_counter()
        return super().get_redirect_url(*args, **kwargs)
