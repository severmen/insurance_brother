from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponse, redirect
from django.views.generic import (
    ListView,
    CreateView,
)

from .models import Services
from .form import (RegisterForm,
                   Search_Services,
                   Request_for_a_call_Form,
                   MyPasswordResetForm,
                   ElasticSearchForm,)
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy

# импорты не которые не нуужны в view, но используються в проекте!
from .templates_filter import get_next_url
from .signals import *


class Main(ListView):
    '''
    Главная страница
    '''
    model = Services
    template_name = 'insurance/index.html'
    context_object_name = 'Services'
    paginate_by = 4

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



class MyPasswordResetView(SuccessMessageMixin, PasswordResetView):
    """
    востановление пароля
    """
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('main_insurance')
    success_message = "Мы отправили вам инструкцию по установке нового пароля на указанный адрес "\
                       + "электронной почты (если в нашей базе данных есть такой адрес). Вы должны "\
                       +"получить ее в ближайшее время"


