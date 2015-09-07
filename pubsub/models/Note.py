__author__ = 'fritz'
from anki.utils import stripHTMLMedia
from aqt import mw
from pubsub.database.utils import is_remote_note, get_remote_note_id


class Note():
    def __init__(self, tags, fields, model_id, sfld, remote_id=None, local_id=None):
        self.tags = tags
        self.fields = fields
        self.model_id = model_id
        self.model = None
        self.sfld = sfld
        self.deck = None
        self.remote_id = remote_id
        self.local_id = local_id

    @classmethod
    def from_anki(cls, local_id):
        if is_remote_note(local_id):
            remote_id = get_remote_note_id(local_id)
        else:
            remote_id = None
        anki_note = mw.col.getNote(local_id)
        tags = anki_note.tags
        fields = anki_note.joinedFields()
        model_id = anki_note.mid
        sfld = stripHTMLMedia(anki_note.fields[anki_note.col.models.sortIdx(anki_note._model)])
        return cls(tags, fields, model_id, sfld, remote_id, local_id)
