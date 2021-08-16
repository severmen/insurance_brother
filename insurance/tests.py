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
        def pika_connect():
            '''
            устонавливает соединение с брокером ссобщений
            '''
            credentials = pika.PlainCredentials(os.environ["RabbitMQ_USERNAME"], os.environ["RabbitMQ_PASSWORD"])
            return pika.BlockingConnection(
                pika.ConnectionParameters(host=os.environ["RabbitMQ_HOST"],
                                          credentials=credentials))
        def send():
            """
            отправляем тестовый запрос в брокер
            """
            connection = pika_connect()

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
            connection = pika_connect()
            channel = connection.channel()
            channel.basic_consume(queue='test_queue',
                                  auto_ack=True,
                                  on_message_callback=worker)
            channel.start_consuming()
        def setUp():
            '''
            подготовка данных перед тестами
            '''
            send()
            get()

        setUp()
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
            '''
            создаём тестового юзера
            '''
            nonlocal user
            user = User(username = "test",
                    password = "test")
            user.save()

        def create_companies():
            '''
            создаём тестовую компанию
            '''
            nonlocal company
            company = Insurance_companies(autor = user,
                            name = "тестовая компания",
                            expert_rating="A",
                            customer_base=1,
                            general_refusal=1.1,
                            date_of_creation=datetime.datetime.now())
            company.save()

        def creaete_type():
            '''
            создаём тестовый тип услуги
            '''
            nonlocal type
            type = Type_services(name = "тестовый тип сервиса")
            type.save()

        def crete_service():
            '''
            создаём тестовую услугу
            '''
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
            '''
            создём тестовый запрос
            '''
            nonlocal request
            request = Request_for_a_call(name = "Тестовое имя",
                                         phone_number="12345",
                                         services = service,
                                         comment = "тестовый комментарий")
            request.save()


        def SetUp():
            '''
            подготовка данных перед тестами
            '''
            create_user()
            create_companies()
            creaete_type()
            crete_service()
            crete_request()

        SetUp()
        self.assertEqual(request.name, "Тестовое имя")
        self.assertEqual(service.name, "Название тестового сервиса")
        self.assertEqual(type.name, "тестовый тип сервиса")
        self.assertEqual(company.name, "тестовая компания")
        self.assertEqual(user.username, "test")





