from django.contrib.auth import logout
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, CreateView
from .models import Services
from .form import RegisterForm,Search_Services,Request_for_a_call_Form
from django.views.decorators.csrf import csrf_exempt
from .templates_filter import get_next_url



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


class Register(CreateView):
    template_name = 'insurance/register.html'
    form_class = RegisterForm
    success_url = "/admin"

def user_logout(request):
    '''
    выполет выход из системы
    '''
    logout(request)
    return redirect("/")


