import pika
import json
import hashlib
import os
class MaintenanceServices:
    def send_new_request(self, request_info):
        '''
        Функция
        '''
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.environ["RabbitMQ_HOST"]))
        channel = connection.channel()
        channel.queue_declare(queue='send_new_request')
        email = request_info.services.insurance_companies.autor.email
        channel.basic_publish(exchange='', routing_key='send_new_request', body=json.dumps({
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
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.environ["RabbitMQ_HOST"]))
        channel = connection.channel()
        channel.queue_declare(queue='send_confirmation_queue')
        hash = hashlib.sha1((str(new_user.id) +new_user.first_name+new_user.password).encode('utf-8')).hexdigest()
        channel.basic_publish(exchange='', routing_key='send_confirmation_queue', body=json.dumps({
            "id":str(new_user.id),
            "name":new_user.first_name,
            "surname":new_user.last_name,
            "email":new_user.email,
            "hash":hash,

        }))

