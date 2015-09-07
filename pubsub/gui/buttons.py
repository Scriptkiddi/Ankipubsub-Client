__author__ = 'fritz'
from .draw import drawTable
from aqt.utils import showInfo, shortcut


def addRemoteDeckButton(form):
    remoteID = form.ui.remoteDeckId.text()
    if not len(remoteID) == 24:
        showInfo('This seems is not a valid Remote Deck ID please try again')
        return
    readPassword = form.ui.readPW.text()
    form.ui.writePW.text()
    addRemoteDeck(remoteID, "http://144.76.172.187:5000/v0",
                  mw.col.conf.get('pubSubName', ""),
                  mw.col.conf.get('pubSubPassword', ""),
                  readPassword)
    drawTable(form)


def ankiPubSubOptionsButton(self):
    links = [
        ["", "ankipubsubDeckManager", _("AnkiPubSub")],
        ["", "shared", _("Get Shared")],
        ["", "create", _("Create Deck")],
        ["Ctrl+I", "import", _("Import File")],
    ]
    buf = ""
    for b in links:
        if b[0]:
            b[0] = _("Shortcut key: %s") % shortcut(b[0])
        buf += """
<button title='%s' onclick='py.link(\"%s\");'>%s</button>""" % tuple(b)
    self.bottom.draw(buf)
    # todo find out what ismac was for
    #if isMac:
    #    size = 28
    #else:
    size = 36 + self.mw.fontHeightDelta*3
    self.bottom.web.setFixedHeight(size)
    self.bottom.web.setLinkHandler(self._linkHandler)