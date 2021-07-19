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
        # original qs
        Search_Services(data = self.request.GET)
        qs = super().get_queryset()
        return qs
        # filter by a variable captured from url, for example
        return qs.filter(name__startswith=self.kwargs['name'])


    def get_context_data(self, **kwargs):
        context = super(main, self).get_context_data(**kwargs)
        context['form'] = Search_Services(data = self.request.GET)
        return context
@csrf_exempt
def add_request_for_a_call(request):
    form = Request_for_a_call_Form(request.POST)
    if form.is_valid():
        student = form.save()
        return HttpResponse("Спасибо мы организатор свяжентся с вами в ближайшее свободное время")
    else:
        return HttpResponse("Ошибки в формате данных")




