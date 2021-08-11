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
    '''
    body = json.loads(body)
    send_mail(subject=body.get("subject"),
              message=body.get("body"),
              from_email=EMAIL_HOST_USER,
              recipient_list=[body.get('email')],
              fail_silently=False,
              )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Сообшение для сменя пароля отправлено "+str(datetime.datetime.now()))


channel.queue_declare(queue='password_recovery_queue')

channel.basic_consume(queue='password_recovery_queue',
                      auto_ack=False,
                      on_message_callback=worker)

print ( '[*] Ожидание сообщений.' )
channel.start_consuming ()

