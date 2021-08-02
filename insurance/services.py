import pika
import json
import hashlib
import os
import time

class MaintenanceServices:
    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.environ["RabbitMQ_HOST"]))
        self.channel = connection.channel()
    def send_new_request(self, request_info):
        '''
        Функция отправляет сообщение в очередь
        для отправки на почту сообщения о новом запросе
        '''
        self.channel.queue_declare(queue='send_new_request')
        self.email = request_info.services.insurance_companies.autor.email
        self.channel.basic_publish(exchange='', routing_key='send_new_request', body=json.dumps({
            "email":request_info.services.insurance_companies.autor.email,
            'name':request_info.name,
            'phone_number':str(request_info.phone_number),
            'services':request_info.services.name,
            'comment':request_info.comment,
            'data_time':{"day":str(request_info.data_time.day)+"."+str(request_info.data_time.month),
                "time":str(request_info.data_time.hour)+":"+str(request_info.data_time.minute),
            },
            'company':request_info.services.insurance_companies.name,
        }))

    def send_confirmation(self, new_user):
        '''
        Функция отравляет сообщение в очередь
        для подтверждения регистрации
        '''
        self.channel.queue_declare(queue='send_confirmation_queue')
        hash = hashlib.sha1((str(new_user.id) +new_user.first_name+new_user.password).encode('utf-8')).hexdigest()
        self.channel.basic_publish(exchange='', routing_key='send_confirmation_queue', body=json.dumps({
            "id":str(new_user.id),
            "name":new_user.first_name,
            "surname":new_user.last_name,
            "email":new_user.email,
            "hash":hash,

        }))

    def password_recovery(self, **kwargs):
        '''
        Функция отравляет сообщение в очередь
        для востановления пароля
        '''
        self.channel.queue_declare(queue='password_recovery_queue')
        second_time = time.time()
        self.channel.basic_publish(exchange='', routing_key='password_recovery_queue', body=json.dumps({
            "subject": kwargs.get("subject"),
            "body": kwargs.get("body"),
            "email":kwargs.get("email")
        }))