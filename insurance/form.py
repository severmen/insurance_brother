import copy
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

from .models import Insurance_companies, Services, Request_for_a_call, Type_services


class RegisterForm(UserCreationForm):
    '''
    форма регистрации
    '''
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','password1','password2',)


    def save(self, commit=True):
        '''
        функция проводит валидацию и добовлет пользователя в группу
        '''
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_staff = True
            #добаляем в группу
            user.save()
            group = Group.objects.get(id=1)
            group.user_set.add(user)
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

    class Meta:
        model = Services
        fields = ('insurance_companies','description','insurance_cost', 'amount_of_payments',"terms_of_insurance",)

    def filter(self, qs, ):
        '''
        Фильтрация по параметрам для главной страницы
        '''
        #тип
        try:
            if self.data.get('type') != 'Все':
                qs = qs.filter(type_services = Type_services.objects.get(name = self.data.get('type')))
        except Exception:
            pass
        #экспертный рейтинг
        try:
            if self.data.get('rating') != 'Все' and self.data.get('rating') != None:
                all_companies = Insurance_companies.objects.filter(expert_rating = self.data.get('rating'))
                for id, one_filter_qs in enumerate(copy.copy(qs)):
                    if id == 0:
                        qs = qs.filter(id = -1)
                    x = (True for x in all_companies if one_filter_qs.insurance_companies == x)
                    if next(x,None) == True:
                        qs = qs | Services.objects.filter(id = one_filter_qs.id)
        except Exception as E:
            pass
        #клинеская база
        if self.data.get('customer_base') != None and  self.data.get('customer_base') != "":
            number = int(self.data.get('customer_base'))
            sorted_base = list((x for x in copy.copy(qs) if x.insurance_companies.customer_base > number))
            for id, one_good_qs in enumerate(sorted_base):
                if id == 0:
                    qs = qs.filter(id=-1)
                qs = qs | Services.objects.filter(id = one_good_qs.id)
            if len(sorted_base) == 0:
                qs = qs.filter(id=-1)
        #сортировка
        if self.data.get('price') == "по возрастанию":
            return qs.order_by("insurance_cost")
        else:
            return qs.order_by("-insurance_cost")