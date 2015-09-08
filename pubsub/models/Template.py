__author__ = 'fritz'
import json
from pubsub.database.models import db, AnkiPubSubTemplate
from copy import deepcopy


class Template():
    def __init__(self,
                 name,
                 answer_format,
                 question_format,
                 deck,
                 ord,
                 back_answer_format,
                 back_question_format):
        try:
            db.connect()
            expression = (AnkiPubSubTemplate.answer_format == answer_format) & \
                         (AnkiPubSubTemplate.name == name) & \
                         (AnkiPubSubTemplate.question_format == question_format) & \
                         (AnkiPubSubTemplate.ord == ord) & \
                         (AnkiPubSubTemplate.back_answer_format == back_answer_format) & \
                         (AnkiPubSubTemplate.back_question_format == back_question_format)
            template = AnkiPubSubTemplate.select().where(expression).get()
            self.remote_id = template.remote_id
        except AnkiPubSubTemplate.DoesNotExist:
            self.remote_id = None
        finally:
            db.close()
        self.answer_format = answer_format
        self.name = name
        self.question_format = question_format
        # self.deck = deck
        self.ord = int(ord)
        self.back_answer_format = back_answer_format
        self.back_question_format = back_question_format

    def json(self):
        dic = deepcopy(self.__dict__)
        dic.update({"remote_id": str(self.remote_id)})
        return json.dumps(dic)

    def save(self):
        db.connect()
        template, created = AnkiPubSubTemplate.get_or_create(remote_id=self.remote_id,
                                                             answer_format=self.answer_format,
                                                             name=self.name,
                                                             question_format=self.question_format,
                                                             ord=self.ord,
                                                             back_answer_format=self.back_answer_format,
                                                             back_question_format=self.back_question_format)
        db.close()
