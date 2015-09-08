__author__ = 'fritz'
import json
from pubsub.database.models import db, AnkiPubSubField
from copy import deepcopy

class Field():
    def __init__(self, size, name, rtl, order, font, sticky):
        try:
            db.connect()
            expression = (AnkiPubSubField.size == size) & \
                         (AnkiPubSubField.name == name) & \
                         (AnkiPubSubField.rtl == rtl) & \
                         (AnkiPubSubField.order == order) & \
                         (AnkiPubSubField.font == font) & \
                         (AnkiPubSubField.sticky == sticky)
            field = AnkiPubSubField.select().where(expression).get()
            self.remote_id = field.remote_id
        except AnkiPubSubField.DoesNotExist:
            self.remote_id = None
        finally:
            db.close()
        self.size = int(size)
        self.name = str(name)
        self.rtl = bool(rtl)
        self.order = int(order)
        self.font = str(font)
        self.sticky = bool(sticky)

    def json(self):
        dic = deepcopy(self.__dict__)
        dic.update({"remote_id": str(self.remote_id)})
        return json.dumps(dic)

    def save(self):
        db.connect()
        field, created = AnkiPubSubField.get_or_create(remote_id=self.remote_id,
                                                       size=self.size,
                                                       name=self.name,
                                                       rtl=self.rtl,
                                                       order=self.order,
                                                       font=self.font,
                                                       sticky=self.sticky)
        db.close()
