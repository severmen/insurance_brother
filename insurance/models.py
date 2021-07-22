from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.




class Insurance_companies(models.Model):
    RATING_CHOICES = (
        ('AAA', 'AAA'),
        ('AA', 'AA'),
        ('A', 'A'),
        ('BBB', 'BBB'),
        ('BB', 'BB'),
        ('B', 'B'),
        ('CCC', 'CCC'),
        ('CC', 'CC'),
        ('C', 'C'),
        ('RD', 'RD'),
        ('D','D')
    )
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name="Название компании")
    expert_rating = models.CharField(max_length=50, choices=RATING_CHOICES, verbose_name="Рейтинг эксперта")
    image = models.ImageField(verbose_name = "Логотип компании")
    customer_base = models.IntegerField(verbose_name="Клиентская база тыщ. чел.")
    general_refusal = models.DecimalField(max_digits = 5, decimal_places = 2, validators=[MinValueValidator(0.00), MaxValueValidator(100)], verbose_name="Общий отказ в обращении")
    date_of_creation = models.DateField(verbose_name="Дата создания компании")

    class Meta:
        verbose_name_plural = 'компании'
        verbose_name = 'компания'
        ordering = ['-name']

    def __str__(self):
        return self.name
    def get_date_year(self):
        today = datetime.today()
        def get_month(year, mounts): #int
            if year == 0:
                return mounts
            if mounts == 0:
                return year * 12
            return (year *12)+ mounts
        age_mount = get_month(int(today.year), int(today.month))-get_month(int(self.date_of_creation.year), int(self.date_of_creation.month))
        result = ""
        # год
        if age_mount >= 12:
            age_year = int(round(age_mount / 12, 0))
            if age_year <= 10  or age_year > 20:
                buffer = list(str(age_year))
                z = int(buffer[len(buffer) - 1])
                if int(buffer[len(buffer) - 1]) == 1:
                    result += str(age_year) + " год "
                elif int(buffer[len(buffer)-1]) <= 4:
                    result += str(age_year) + " года "
                else:
                    result += str(age_year) + " лет "
            else:
                result += str(age_year)+" лет "
        #месяц
        result += str(age_mount%12)+" мес. "
        return result

    @staticmethod
    def get_user(self):
        self.save()



class Services(models.Model):
    insurance_companies = models.ForeignKey('Insurance_companies', on_delete=models.CASCADE)
    type_services = models.ForeignKey('Type_services', on_delete=models.CASCADE)
    name = models.CharField(max_length=400, verbose_name="Название услуги")
    description = RichTextUploadingField(verbose_name="Краткое описание услуги", config_name="default")
    insurance_cost = models.IntegerField(verbose_name="Стоймость страхования от в рублях")
    amount_of_payments = models.IntegerField(verbose_name="Сумма выплат до")
    terms_of_insurance = models.CharField(max_length=200, verbose_name="Сроки страхования")

    class Meta:
        verbose_name_plural = 'услуги'
        verbose_name = 'услуга'
        ordering = ['-description']

    def __str__(self):
        return self.description
class Type_services(models.Model):
    name = models.CharField(max_length=200, verbose_name="Тип страхования")

    class Meta:
        verbose_name_plural = 'типы услуг'
        verbose_name = 'тип услуги'

    def __str__(self):
        return self.name

class Request_for_a_call(models.Model):
    name = models.CharField(max_length=400, verbose_name="имя кого, кто делал запрос")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    services = models.ForeignKey('Services', on_delete=models.CASCADE)
    comment = models.CharField(max_length=600, verbose_name="Коментарий к запросу")
    data_time = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Дата время")
    class Meta:
        verbose_name_plural = 'заявки'
        verbose_name = 'заявка'

    def __str__(self):
        return self.comment
