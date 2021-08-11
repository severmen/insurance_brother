from project.settings import *
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponse, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    FormView
)
from project.settings import collection_mongoDB_statistics_serivice

from .models import (Services,
                    CommentService,)
from .form import (RegisterForm,
                   Search_Services,
                   Request_for_a_call_Form,
                   MyPasswordResetForm,
                   CommentForm,)
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

class AboutServices(DetailView,FormView):
    model = Services
    template_name = 'insurance/about.html'
    context_object_name = "service"
    form_class = CommentForm
    success_url = "#"

    def get_object(self):
        #
        query = get_object_or_404(Services, id=self.kwargs.get('pk'))
        if collection_mongoDB_statistics_serivice.count_documents({"id":self.kwargs.get('pk')}) == 0:
            #создаём индекс
            index = {
                "id": self.kwargs.get('pk'),
                "count": 0
            }
            collection_mongoDB_statistics_serivice.insert_one(index)
        else:
            collection_mongoDB_statistics_serivice.update_one({"id":self.kwargs.get('pk')},
                                                              {'$inc':{'count':1}})
        return query

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save(self.request.POST, self.kwargs.get('pk'))
        return super().form_valid(form)



class ServiceComment(ListView):
    model = CommentService
    template_name = 'insurance/comment.html'
    paginate_by = 2
    context_object_name = 'comment'

    def get_queryset(self):
        return CommentService.objects.filter(services=Services.objects.get(id = self.kwargs.get('pk')))

