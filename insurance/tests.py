from django.test import TestCase
import pika
import os
import datetime
from .models import Insurance_companies,Type_services,Services,Request_for_a_call
from django.contrib.auth.models import User


class baseSystemTest(TestCase):

    def test_RabbitMQ(self):
        '''
        тест раотоспособности бокера сообщений
        '''
        RabbitMQ_request_result = None
        def send():
            """
            отправляем тестовый запрос в брокер
            """
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host="localhost"))
            channel = connection.channel()
            channel.queue_declare(queue='test_queue')
            channel.basic_publish(exchange='', routing_key='test_queue', body="test message")

        def get():
            '''
            проверяем сообщение и записывет результат
            '''
            def worker(ch, method, properties, body):
                nonlocal RabbitMQ_request_result
                RabbitMQ_request_result = body.decode("utf-8")
                channel.close()
            connection = pika.BlockingConnection(pika.ConnectionParameters("localhost", '5672'))
            channel = connection.channel()
            channel.basic_consume(queue='test_queue',
                                  auto_ack=True,
                                  on_message_callback=worker)
            channel.start_consuming()

        send()
        get()
        self.assertEqual(RabbitMQ_request_result, "test message")

    def test_models(self):
        '''
        тест заполлнения моделей
        '''
        user = None
        company = None
        type = None
        service = None
        request = None
        def create_user():
            nonlocal user
            user = User(username = "test",
                    password = "test")
            user.save()

        def create_companies():
            nonlocal company
            company = Insurance_companies(autor = user,
                            name = "тестовая компания",
                            expert_rating="A",
                            customer_base=1,
                            general_refusal=1.1,
                            date_of_creation=datetime.datetime.now())
            company.save()

        def creaete_type():
            nonlocal type
            type = Type_services(name = "тестовый тип сервиса")
            type.save()

        def crete_service():
            nonlocal service
            service = Services(
                insurance_companies=company,
                type_services = type,
                name = "Название тестового сервиса",
                description="Описание тестовго сервиса",
                insurance_cost= 100,
                amount_of_payments=110,
                terms_of_insurance = "много" )
            service.save()

        def crete_request():
            nonlocal request
            request = Request_for_a_call(name = "Тестовое имя",
                                         phone_number="12345",
                                         services = service,
                                         comment = "тестовый комментарий")
            request.save()

        create_user()
        create_companies()
        creaete_type()
        crete_service()
        crete_request()

        self.assertEqual(request.name, "Тестовое имя")
        self.assertEqual(service.name, "Название тестового сервиса")
        self.assertEqual(type.name, "тестовый тип сервиса")
        self.assertEqual(company.name, "тестовая компания")
        self.assertEqual(user.username, "test")





