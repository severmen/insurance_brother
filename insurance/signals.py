import os
import requests

from bs4 import BeautifulSoup
from django.db.models import signals
from elasticsearch import Elasticsearch

from .models import Services

def reindexing_elasticsearch(**kwargs):
    '''
    выпоняет запрос на индексацию в elasticsearch
    при удалении, обновлении и добавлении
    '''
    es = Elasticsearch([{'host': os.environ["Elasticsearch_HOST"], 'port': 9200}])
    if kwargs.get("created") in [True, False]:
        requests.put("http://" + os.environ["Elasticsearch_HOST"] + ":9200/services/_doc/" + str(kwargs["instance"].id), json={
            "type_service": kwargs["instance"].type_services.name,
            "name": kwargs["instance"].name,
            "description": BeautifulSoup(markup=kwargs["instance"].description).get_text(),
            "expert_rating": kwargs["instance"].insurance_companies.expert_rating,
            "customer_base": str(kwargs["instance"].insurance_companies.customer_base),
            "insurance_cost": str(kwargs["instance"].insurance_cost)
        })
    else:
        requests.post("http://" + os.environ["Elasticsearch_HOST"] + ":9200/services/_delete_by_query/" ,   json=  {"query": {
                   "match": {
                        "_id": str(kwargs["instance"].id)
                   } }
                     })
signals.post_save.connect(receiver=reindexing_elasticsearch, sender=Services)
signals.post_delete.connect(receiver=reindexing_elasticsearch, sender=Services)


