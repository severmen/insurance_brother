import pika
import json
import os
import django
import sys
import datetime

from django.core.mail import send_mail


sys.path.insert(1, os.getcwd()+"/..")
os.chdir(os.getcwd()+"/..")


from project.settings import EMAIL_HOST_USER
from project.settings import pika_channel as channel

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")


django.setup()


def worker(ch, method, properties, body):

    '''
    отправлет на email сообщение, что пришла новая заявка
    '''
    body = json.loads(body)
    subject = "Новый отклик на ваш сервис"
    time = body.get('data_time')
    message = "Добрый день \r\n "\
              +"Недавно "+str(time.get('day')) + " в "+str(time.get('time')) \
              +".\r\n " +"Пользователь "+body.get('name') +" оставил отклик на вашу услугу " +body.get('services')+" компании "+body.get('company') +".\r\n " \
              +"Его номер "+body.get('phone_number')+", коментарий "+body.get('comment')+"\r\n " \
              +"C уважением сервис застрахуй братуху"
    send_mail(subject, 
            message, EMAIL_HOST_USER, [body.get('email')], fail_silently = False)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Запрос на услугу получен и обработан "+str(datetime.datetime.now()))


channel.queue_declare(queue='send_new_request')

channel.basic_consume(queue='send_new_request',
                      auto_ack=False,
                      on_message_callback=worker)

print ( '[*] Ожидание сообщений.' )
channel.start_consuming ()


