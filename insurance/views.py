from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, CreateView
from .models import *
from .form import *
from django.views.decorators.csrf import csrf_exempt

class main(ListView):
    model = Services
    template_name = 'insurance/index.html'
    context_object_name = 'Services'
    def get_queryset(self):
        a = Services.objects.all()
        return a
@csrf_exempt
def add_request_for_a_call(request):
    form = Request_for_a_call_Form(request.POST)
    if form.is_valid():
        student = form.save()
        return HttpResponse("Спасибо мы организатор свяжентся с вами в ближайшее свободное время")
    else:
        return HttpResponse("Ошибки в формате данных")




