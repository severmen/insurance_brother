import os
import re

from elasticsearch import Elasticsearch

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User, Group
from django.forms import Textarea
from django.template import loader

from .models import Insurance_companies, Services, Request_for_a_call, Type_services
from .services import MaintenanceServices


class RegisterForm(UserCreationForm):
    '''
    форма регистрации
    '''
    first_name = forms.CharField(label = "Имя",required=True, max_length=150)
    last_name = forms.CharField(label = "Фамилийя",required=True, max_length=150)
    email = forms.EmailField(required=True, max_length=150)

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email','password1','password2',)



    def save(self, commit=True):
        '''
        функция проводит валидацию и добавлет пользователя в группу
        '''
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_staff = False
            #добаляем в группу
            user.save()
            group = Group.objects.get(id=1)
            group.user_set.add(user)
        #ставим в очередь
        service = MaintenanceServices()
        service.send_confirmation(user)
        return user


class Request_for_a_call_Form(forms.Form):
    '''
    Форма для реботы и добавления запроса в БД
    '''
    class Meta:
        model = Request_for_a_call
        fields = ('name','phone_number','services', 'comment')

    @property
    def errors(self):
        '''
        Функция проверки коректности ввода запроса на зваонок
        '''
        """Return an ErrorDict for the data provided for the form."""
        self._errors = {}
        #проверка имени
        if len(re.findall(r"[A-zА-я]",self.data.get('name'))) <= 2:
            self.data._mutable = True
            self.data['name'] = "Имя не определил"
        #проверка номер телефона
        if len(re.findall(r"[0-9]",self.data.get('phone_number'))) <= 4 or len(re.findall(r"[0-9]",self.data.get('phone_number'))) >=12:
            self._errors['phone_number'] = "Недопустимы номер телефона"
        #проверка id
        try:
            Services.objects.get(id = int(self.data.get('id')))
        except Exception:
            self._errors['other'] = "Недопустимый формат"
        #проверка коментария
        if len(re.findall(r"[A-zА-я]",self.data.get('comment'))) <= 2:
            self.data['comment'] = "не отпределил"
        self.data._mutable = False

    def save(self):
        '''
        Функция сохранет запрос на звонок
        '''
        one_request =Request_for_a_call(name = self.data.get('name'),
                                         phone_number = self.data.get('phone_number'),
                                         services = Services.objects.get(id = int(self.data.get('id'))),
                                         comment = self.data.get('comment'))
        one_request.save()
        service = MaintenanceServices()
        service.send_new_request(one_request)
        services = MaintenanceServices()


class Search_Services(forms.Form):
    '''
    Форма для работы с поиском
    '''

    def add_the_all_field_for_selection( list_of_elections):
        '''
        Фукция добовляет в начало списка выбора  "Все"
        '''
        final_result = [("Все", "Все")]
        for one_choice in list_of_elections:
            final_result.append(one_choice)
        return final_result

    type = forms.ChoiceField(label = "тип сервиса",
                             choices = add_the_all_field_for_selection(list(map(lambda one_services: (one_services.name, one_services.name), Type_services.objects.all()))) )
    rating = forms.ChoiceField(label = "экспертный рейтинг",
                               choices=add_the_all_field_for_selection(Insurance_companies.RATING_CHOICES))
    customer_base = forms.IntegerField(label = "Клиентская база не менее тыщь. чел", min_value = 1,
                                       required=False)
                                       #widget=forms.IntegerField(attrs={'placeholder': 'весь диапазон'})

    price = forms.ChoiceField(label = "Сортировка по цене страхования",
                                     choices = [("по возрастанию", "по возрастанию"), ("по убыванию", "по убыванию")])
    text = forms.CharField(label="Поиск по имени услуги и описании", required=False)

    class Meta:
        model = Services
        fields = ('insurance_companies','description','insurance_cost', 'amount_of_payments',"terms_of_insurance",)

    def filter(self, qs):
        '''
        Фильтрация по параметрам для главной страницы
        '''


        def query_constructor():
            '''
            формирует тело запроса для elastik search
            '''
            result = {"must": [

                    ]
            }
            must = result.get("must")
            #тип сервиса
            if not(self.data.get('type') in [None, "", "Все"]):
                must.append({"match":{
								"type_service":{
									"query":self.data.get('type'),
									"operator":"and"
								}
							}
                         })
            # экспертный рейтинг
            if not (self.data.get('rating') in [None, "", "Все"]):
                must.append({"match": {
                    "expert_rating": {
                        "query": self.data.get('rating')
                    }
                }
                })
            # клиентская база
            if not (self.data.get('customer_base') in [None, "", 0, "0"]):
                must.append({"range": {
                    "customer_base": {
                        "gte": self.data.get('customer_base')
                    }
                }
                })
            # слова
            if not (self.data.get('text') in [None, ""]):
                must.append({"multi_match": {
                    "query": self.data.get('text') ,
                    "fields": ["name", "description"],
                    "type": "best_fields",
                    "operator": "and"
                        }
                    })


            return result


        def Elasticsearch_seacrh():
            '''
            функция выполняет  запрос на Elasticsearch для быстрого поиска
            потом по id-шникам формирует QuerySet и сортирует его
            '''
            nonlocal self
            nonlocal qs
            es = Elasticsearch([{'host': os.environ["Elasticsearch_HOST"], 'port': 9200}])
            query_es = es.search(index='services', body=  {"query": {
                                                    "bool":  query_constructor()
                                                } })
            qs = qs.none()
            for result in query_es["hits"]["hits"]:
                qs = qs | Services.objects.filter(id=result.get("_id"))

            #сортировка
            if self.data.get('price') == "по убыванию":
                return qs.order_by("-insurance_cost")
            else:
                return qs.order_by("insurance_cost")

        ############################
        ### потом уберу старый код #
        ############################
        '''
        #экспертный рейтинг
        def rating():
            nonlocal self
            nonlocal qs
            try:
                if self.data.get('rating') != 'Все' and self.data.get('rating') != None:
                    all_companies = Insurance_companies.objects.filter(expert_rating = self.data.get('rating'))
                    for id, one_filter_qs in enumerate(copy.copy(qs)):
                        if id == 0:
                            qs = qs.none()
                        x = (True for x in all_companies if one_filter_qs.insurance_companies == x)
                        if next(x,None) == True:
                            qs = qs | Services.objects.filter(id = one_filter_qs.id)
            except Exception as E:
                pass

        # клинеская база
        def base():
            nonlocal self
            nonlocal qs
            if self.data.get('customer_base') != None and  self.data.get('customer_base') != "":
                number = int(self.data.get('customer_base'))
                sorted_base = list((x for x in copy.copy(qs) if x.insurance_companies.customer_base > number))
                for id, one_good_qs in enumerate(sorted_base):
                    if id == 0:
                        qs = qs.filter(id=-1)
                    qs = qs | Services.objects.filter(id = one_good_qs.id)
                if len(sorted_base) == 0:
                    qs = qs.none()

        #сортировка
        def sortirovka():
            nonlocal self
            nonlocal qs
            if self.data.get('price') == "по возрастанию":
                return qs.order_by("insurance_cost")
            else:
                return qs.order_by("-insurance_cost")
        
        '''
        return Elasticsearch_seacrh()


class MyPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Ставим в очередь на отправку сообщение для востановления пароля
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        #отправлем на поток
        services = MaintenanceServices()
        services.password_recovery(subject = subject, body = body, email = to_email)

class ElasticSearchForm(forms.Form):
    name = forms.CharField(label = "",required=True, max_length=350)