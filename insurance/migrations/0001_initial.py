# Generated by Django 3.2.4 on 2021-07-13 18:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance_companies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название компании')),
                ('expert_rating', models.CharField(choices=[('AAA', 'AAA'), ('AA', 'AA'), ('A', 'A'), ('BBB', 'BBB'), ('BB', 'BB'), ('B', 'B'), ('CCC', 'CCC'), ('CC', 'CC'), ('C', 'C'), ('RD', 'RD'), ('D', 'D')], max_length=50, verbose_name='Рейтинг эксперта')),
                ('image', models.ImageField(upload_to='', verbose_name='Логотип компании')),
                ('customer_base', models.IntegerField(verbose_name='Клиентская база тыщ. чел.')),
                ('general_refusal', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100)], verbose_name='Общий отказ в обращении')),
                ('date_of_creation', models.DateField(verbose_name='Дата создания компании')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'компания',
                'verbose_name_plural': 'компании',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Type_services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Тип страхования')),
            ],
            options={
                'verbose_name': 'тип услуги',
                'verbose_name_plural': 'типы услуг',
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=400, verbose_name='Краткое описание услуги')),
                ('insurance_cost', models.IntegerField(verbose_name='Стоймость страхования от в рублях')),
                ('amount_of_payments', models.IntegerField(verbose_name='Сумма выплат до')),
                ('terms_of_insurance', models.CharField(max_length=200, verbose_name='Сроки страхования')),
                ('insurance_companies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.insurance_companies')),
                ('type_services', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.type_services')),
            ],
            options={
                'verbose_name': 'услуга',
                'verbose_name_plural': 'услуги',
                'ordering': ['-description'],
            },
        ),
        migrations.CreateModel(
            name='Request_for_a_call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400, verbose_name='имя кого, кто делал запрос')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер телефона')),
                ('comment', models.CharField(max_length=600, verbose_name='Коментарий к запросу')),
                ('services', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance.services')),
            ],
        ),
    ]
