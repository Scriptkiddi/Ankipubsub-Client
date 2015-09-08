__author__ = 'fritz'
from pubsub.models.Deck import Deck
from pubsub.models.Field import Field
from pubsub.models.Template import Template
from pubsub.models.Model import Model
from pubsub.models.Note import Note
import pubsub.requests as requests
import pubsub.models as models

def create_on_server(obj, settings):
    if isinstance(obj, Deck):
        url_extension = "decks/"
    elif isinstance(obj, Model):
        url_extension = "models/"
    elif isinstance(obj, Field):
        url_extension = "fields/"
    elif isinstance(obj, Template):
        url_extension = "templates/"
    elif isinstance(obj, Note):
        url_extension = "notes/"
    obj_json = obj.json()
    header = {"content-type": "application/json"}
    r = requests.post(settings.server_url+url_extension, data=obj_json, headers=header)
    if r.status_code == requests.codes.created:
        r = r.json()
        if isinstance(obj, Deck):
            obj.author = r.get('author')
        return r.get('id')
    r.raise_for_status()
