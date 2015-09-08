__author__ = 'fritz'
from peewee import *

db = SqliteDatabase('/home/fritz/code/ankipubsub_client/ankipubsub.db')
db.connect()


class AnkiPubSubNote2AnkiNote(Model):
    remote_id = CharField()
    local_id = IntegerField()

    class Meta:
        database = db


class AnkiPubSubModel2AnkiModel(Model):
    remote_id = CharField()
    local_id = IntegerField()

    class Meta:
        database = db


class AnkiPubSubField(Model):
    remote_id = CharField(unique=True)
    size = IntegerField()
    name = CharField()
    rtl = BooleanField()
    order = IntegerField()
    font = CharField()
    sticky = BooleanField()

    class Meta:
        database = db


class AnkiPubSubTemplate(Model):
    remote_id = CharField(unique=True)
    answer_format = TextField()
    name = CharField()
    question_format = TextField()
    ord = IntegerField()
    back_answer_format = TextField()
    back_question_format = TextField()

    class Meta:
        database = db


class AnkiPubSubUser(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db


class AnkiPubSubDeck(Model):
    uuid = CharField(unique=True)
    author = CharField(null=True)
    creation_date = DateTimeField(null=True)
    last_updated = DateTimeField(null=True)

    class Meta:
        database = db


class DeckSettings(Model):
    deck = ForeignKeyField(AnkiPubSubDeck)
    base_url = CharField()
    read_password = CharField()
    write_password = CharField()

    class Meta:
        database = db


class AnkiPubSubDeck2AnkiDeck(Model):
    remote_deck = ForeignKeyField(AnkiPubSubDeck)
    local_id = IntegerField()

    class Meta:
        database = db

'''db.create_tables([AnkiPubSubDeck2AnkiDeck,
                  AnkiPubSubNote2AnkiNote,
                  AnkiPubSubModel2AnkiModel,
                  AnkiPubSubField,
                  AnkiPubSubTemplate,
                  AnkiPubSubUser,
                  DeckSettings,
                  AnkiPubSubDeck])'''