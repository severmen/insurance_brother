import pika
import json
import os
import django

from django.core.mail import send_mail


print("fgdg---"+os.getcwd())
#os.chdir(os.getcwd()+"/../")

from project.settings import EMAIL_HOST_USER

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")


django.setup()


def send_new_request(ch, method, properties, body):
    body = json.loads(body)
    subject = "Подтверждение регистрации"
    url = os.environ["URL_AT_THE_MOMENT"] + "/registration_confirmations/"+body.get("id")+"/"+body.get("hash")
    message = "Добрый день "+body.get('surname') + "<br> "\
              +body.get('name') +"!<br>" +"для подтверждение регистрации на сервисе застрахуй братуху перейдите по <a href = \""+url+" \">ссылке</a><br>"   \
              +"C уважением сервис застрахуй братуху"
    send_mail(subject = subject,
              message = "Cooбщение",
              html_message= message,
              from_email = EMAIL_HOST_USER,
              recipient_list= [body.get('email')],
              fail_silently=False,
              )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Сообщение отправлено")


connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["RabbitMQ_HOST"], '5672'))
channel = connection.channel()
channel.queue_declare(queue='send_confirmation_queue')

channel.basic_consume(queue='send_confirmation_queue',
                      auto_ack=False,
                      on_message_callback=send_new_request)

print ( '[*] Ожидание сообщений.' )
channel.start_consuming ()


#send_confirmation_queue

