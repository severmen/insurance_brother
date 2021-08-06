import os
import django
import sys
import requests
from bs4 import BeautifulSoup

sys.path.insert(1, os.getcwd()+"/..")
os.chdir(os.getcwd()+"/..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from insurance.models import Services

def create_index():
    requests.put("http://"+os.environ["Elasticsearch_HOST"]+":9200/services", json = {
                                                    "mappings": {
                                                        "properties": {
                                                            "type_service":{"type":"text"},
                                                            "name": {"type": "text"},
                                                            "description": {"type": "text"},
                                                            "expert_rating":{"type":"text"},
                                                            "customer_base":{"type":"integer"},
                                                            "insurance_cost":{"type":"integer"}
                                                        }
                                                    }
                                                })

def add_info():
    b = 4
    for one_service in Services.objects.all():
        requests.put("http://"+os.environ["Elasticsearch_HOST"]+":9200/services/_doc/"+str(one_service.id), json={
                    "type_service":one_service.type_services.name,
                    "name": one_service.name,
                    "description":BeautifulSoup(markup = one_service.description).get_text(),
                    "expert_rating":one_service.insurance_companies.expert_rating,
                    "customer_base":str(one_service.insurance_companies.customer_base),
                    "insurance_cost":str(one_service.insurance_cost)
                    })

create_index()
add_info()



