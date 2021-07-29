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


class PasswordRecovery(SuccessMessageMixin, FormView):
    template_name = 'insurance/password_recover.html'
    form_class = PasswordRecoverForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        try:
            User.objects.get(username  = form.data.get("login"))
            messages.add_message(self.request, messages.INFO, 'Письмо с дальнейшей инструкцией отправлено на почту')
        except:
            self.success_url = reverse_lazy("password_recovery")
            messages.add_message(self.request, messages.INFO, 'Пользователь не найден')

        return super().form_valid(form)

class RegistrationConfirmations(RedirectView):
    '''
    потверждение регистрации
    '''
    url = reverse_lazy('admin:index')
    def get_redirect_url(self, *args, **kwargs):
        '''
        функция проверет правильность и актуальность URL адреса потверждения
        формирует сообщение о статусе
        '''
        try:
            one_user_info = User.objects.get(id = args[0],is_staff = False)
            if one_user_info.is_staff == True:
                raise Exception()
            hash = hashlib.sha1(
                (str(one_user_info.id) + one_user_info.first_name + one_user_info.password).encode('utf-8')).hexdigest()
            if hash == args[1]:
                one_user_info.is_staff = True
                one_user_info.save()

            messages.add_message(self.request, messages.INFO, 'Пользователь успешно активирован')

        except:
            messages.add_message(self.request, messages.ERROR, 'Ссылка не действительна')
        return super().get_redirect_url(*args, **kwargs)
