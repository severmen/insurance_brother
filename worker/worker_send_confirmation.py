import datetime
import pika
import json
import os
import django
import sys

from django.core.mail import send_mail


sys.path.insert(1, os.getcwd()+"/..")
os.chdir(os.getcwd()+"/..")

from project.settings import EMAIL_HOST_USER
from project.settings import pika_channel as channel

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()


def worker(ch, method, properties, body):
    '''
    отправлет email сообщение с сылкой для потдверждения
    '''
    body = json.loads(body)
    subject = "Подтверждение регистрации"
    url = os.environ["URL_AT_THE_MOMENT"] + "/registration_confirmations/"+body.get("id")+"/"+body.get("hash")
    message = "Добрый день "+body.get('surname') +" "+ body.get('name') +"!<br> "\
              +"для подтверждение регистрации на сервисе застрахуй братуху перейдите по <a href = \""+url+" \">ссылке</a><br>"   \
              +"C уважением сервис застрахуй братуху"
    send_mail(subject = subject,
              message = "Cooбщение",
              html_message= message,
              from_email = EMAIL_HOST_USER,
              recipient_list= [body.get('email')],
              fail_silently=False,
              )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Запрос на потверждение почты получен и обработан "+str(datetime.datetime.now()))



channel.queue_declare(queue='send_confirmation_queue')

channel.basic_consume(queue='send_confirmation_queue',
                      auto_ack=False,
                      on_message_callback=worker)

print ( '[*] Ожидание сообщений.' )
channel.start_consuming ()

