from django.test import TestCase
import pika
import os
# Create your tests here.

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



