__author__ = 'fritz'
from pubsub.database.utils import is_remote_model, get_remote_model_id
from aqt import mw
from .Field import Field
from .Template import Template


class Model():
    def __init__(self, name,
                 tags, usn, fields, sortf,
                 templates, latex_post, latex_pre, type, css, remote_id=None, local_id=None):
        self.name = name
        self.tags = tags
        self.usn = usn
        self.fields = fields
        self.sortf = sortf
        self.templates = templates
        self.latex_post = latex_post
        self.latex_pre = latex_pre
        self.type = type
        self.css = css
        self.deck = None
        self.remote_id = remote_id
        self.local_id = local_id

    @classmethod
    def from_anki(cls, local_id):
        if is_remote_model(local_id):
            remote_id = get_remote_model_id(local_id)
        else:
            remote_id = None
        anki_model = mw.col.models.get(local_id)
        name = anki_model.get('name')
        tags = anki_model.get('tags')
        usn = anki_model.get('usn')
        # req = anki_model.get('req')
        fields = []
        for field in anki_model.get('flds'):
            fields.append(Field(field.get('size'),
                          field.get('name'),
                          field.get('rtl'),
                          field.get('ord'),
                          field.get('font'),
                          field.get('sticky')))
        sortf = anki_model.get('sortf')
        templates = []
        for template in anki_model.get('tmpls'):
            templates.append(Template(template.get('name'),
                                      template.get('afmt'),
                                      template.get('qfmt'),
                                      template.get('did'),
                                      template.get('ord'),
                                      template.get('bafmt'),
                                      template.get('bqfmt')))
        latex_post = anki_model.get('latexPost')
        latex_pre = anki_model.get('latexPre')
        type = anki_model.get('type')
        css = anki_model.get('css')

        return cls(name, tags, usn, fields, sortf, templates, latex_post, latex_pre, type, css, remote_id, local_id)






