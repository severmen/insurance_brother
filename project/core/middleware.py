import re
from django.contrib import messages
from django.contrib.messages.constants import *
from django.shortcuts import render

class CheckAttack:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        '''
        проверка безопасностей сайтов
        '''
        self.XSS(request)
        if request._messages.added_new and request._messages.level == 20:
            return render(request, 'insurance/error.html')
        response = self.get_response(request)
        return response

    def XSS(self,request):
        '''
        функция проверяет все формы если, на наличие JS кода
        '''
        def check_script(one_entry):
            '''
            функция проверяет есть ли в поле JS код
            '''
            if len(re.findall(r"(<script>|</script>|&lt;script&gt;|&lt;/script&gt;)", str(one_entry))) != 0:
                messages.add_message(request, messages.WARNING, 'Была попытка XSS атаки, но мы вас поймали')
        def GET():
            '''
            проверка всех полей в GET запросе
            '''
            list(map(check_script, request.GET.values()))
        def POST():
            '''
               проверка всех полей в POST запросе
            '''
            list(map(check_script, request.POST.values()))

        GET()
        POST()

