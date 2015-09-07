__author__ = 'fritz'
from aqt import mw


def is_remote_deck(local_id):
    return False


def get_remote_deck_id(local_id):
    return 0


def is_remote_model(local_id):
    return False


def get_remote_model_id(local_id):
    return 0


def is_remote_note(local_id):
    return False


def get_remote_note_id(local_id):
    return 0


def is_remote_template(local_id):
    return False


def get_remote_template_id(local_id):
    return 0


def is_remote_field(local_id):
    return False


def get_remote_field_id(local_id):
    return 0


def get_note_ids_for_deck_id(local_id):
    result = mw.col.db.all("SELECT DISTINCT nid FROM cards WHERE did = ?", local_id)
    result = [int(i[0]) for i in result]  # convert list of tuples to int list
    return result