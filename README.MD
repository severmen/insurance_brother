Застрахуй братуху
Биржа продажи услуг страховых компаний.

Основные возможности:
Для страховых компаний (авторизованные пользователи):
Админ панель с возможностью создания несколько страховых организации, продуктов
и редактирования своих продуктов с различными параметрами
удобная поля для ввода описания своеё услуги
Просмотр откликов пользователей на свои продукты
Для покупателей (неавторизованные пользователи):
Просмотр услуг от страховых компаний с возможностью фильтрации по различным параметрам
Возможность оставлять отклики на продукты страховых компаний
возможность зарегистрироваться(подвердить регистрацию) и зарегистрировать свои компании и услуги соответсвенно
если реководитель компании забыло пароль то он по email легко может востановить его

Сборка проекта
    Запуск Elasticsearch
        -docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.4
    Сборка БД
        -docker-compose build
        -docker-compose up
        Далее необходимо запустить CLI приложения db и выполнить импорт БД командой
        PGPASSWORD="1234" psql -f db.dump -h localhost -U admin insurance_brother
    Запуск RabbitMQ
        -docker-compose build
        -docker-compose up
        Далее необходимо запустить CLI приложение и создать пользователя
        -rabbitmqctl add_user username password
        -rabbitmqctl set_user_tags username administrator
        -rabbitmqctl set_permissions -p / username ".*" ".*" ".*"
    Запуск MongoDB
        -docker-compose build
        -docker-compose up
    Сборка приложения и запуск воркеров
        -docker-compose build
        -docker-compose up
		Для индексирования и CLI переходим в папку script
        -python *
        Для запуска воркеров переходим в CLI и в папку worker
        -python worker_send_confirmation.py
        -python worker_send_new_request.py
        -python worker_password_recovery.py
        


Доступ к сайту
http://127.0.0.1:8008

Запуск тестов(они ещё не все написаны, но некоторые есть)
	python manage.py test

TO-DU
-дописать тесты
