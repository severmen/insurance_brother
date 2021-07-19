from django import forms
from .models import *
import re
class Request_for_a_call_Form(forms.Form):

    class Meta:
        model = Request_for_a_call
        fields = ('name','phone_number','services', 'comment')

    @property
    def errors(self):
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
        return self._errors

    def save(self):
        one_request =Request_for_a_call(name = self.data.get('name'),
                                         phone_number = self.data.get('phone_number'),
                                         services = Services.objects.get(id = int(self.data.get('id'))),
                                         comment = self.data.get('comment'))
        one_request.save()
        return 0