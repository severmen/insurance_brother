import re
import datetime
import os
import schedule

from django.contrib import messages
from django.contrib.messages.constants import *
from django.shortcuts import render

from project.settings import current_DB

class CheckAttack:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        '''
        проверка безопасностей сайтов
        '''
        self.XSS(request)
        self.brute_force(request)

        if request._messages.added_new and request._messages.level == 20:
            return render(request, 'insurance/error.html')
        response = self.get_response(request)
        return response

    def XSS(self,request):
        '''
        функция проверяет все формы если, на наличие JS кода
        в случие наличии фиксирует его
        '''
        def check_script(one_entry):
            '''
              функция проверяет есть ли в поле JS код
              с случае наличии фиксирует в БД
            '''
            def add_attack_in_DB():
                '''
                функция фиксирует факт попытки атаки в БД
                который может прсмаотривать только админ
                '''
                def get_user_info():
                    nonlocal request
                    '''
                    функция получает информацию об текущем пользователе
                    '''
                    if request.user.is_authenticated:
                        return {"username":request.user.username}
                    else:
                        return "Uset is not authenticated"

                collection_mongoDB_for_admin_statistics_serivice = current_DB["for_admin"]
                index = {
                    "type": "XSS",
                    "user":get_user_info(),
                    "data_time": datetime.datetime.now(),
                    "ip":request.META.get('REMOTE_ADDR')
                }
                collection_mongoDB_for_admin_statistics_serivice.insert_one(index)

            if len(re.findall(r"(<script>|</script>|&lt;script&gt;|&lt;/script&gt;)", str(one_entry))) != 0:
                add_attack_in_DB()
                messages.add_message(request, messages.WARNING, 'Была попытка XSS атаки, но мы вас поймали')

        def GET():
            #проверка всех полей в GET запросе
            list(map(check_script, request.GET.values()))
        def POST():
            #проверка  всех   полей  в  POST  запросе
            list(map(check_script, request.POST.values()))

        GET()
        POST()

    def brute_force(self, request):
        '''
        функция проверяет и ограничивает время попытки для каждого логина
        проверка ведёться только для стараницы авторизации и поля username
        ненужные поля автоматический удаляються
        '''
        if request.path_info == os.environ["Login_URL"] and not(request.POST.get('username') in [None, ""]):
            collection_mongoDB_for_admin_statistics_serivice = current_DB["last_authorized_users"]
            if str(collection_mongoDB_for_admin_statistics_serivice.index_information().keys()).find("last_login_time") == -1 :
                collection_mongoDB_for_admin_statistics_serivice.ensure_index("last_login_time",
                                                                              expireAfterSeconds=60)

            #получаем последнию запись для определённого логина
            last_entry_for_user = list(collection_mongoDB_for_admin_statistics_serivice.find({"username":request.POST.get('username')}).sort([("last_login_time", -1)]).limit(1))
            if len(last_entry_for_user) != 0:
                last_entry_for_user = last_entry_for_user.pop()
                if (datetime.datetime.utcnow() - last_entry_for_user['last_login_time']).total_seconds() < int(os.environ["Login_time_out"]):
                    messages.add_message(request, messages.WARNING, 'Превышен лимит попытки входа в аккаунт, повторите попытку позже')

            utc_timestamp = datetime.datetime.utcnow()
            collection_mongoDB_for_admin_statistics_serivice.insert({'username': request.POST.get('username'),
                                                                         "last_login_time": utc_timestamp,})




