from anki.hooks import wrap
from aqt.deckbrowser import DeckBrowser
from pubsub.gui.setup import anki_deck_manager_setup
from pubsub.gui.buttons import ankiPubSubOptionsButton


def connect_anki_pub_sub_link_handler(self, url, **kwargs):
    """
    wrap around the normal Link Handler.

    It checks for the signals we expect for the buttons we placed in the gui
    if it cant find a single that it needs to trigger on it passes
    it to the normal _linkHandler function.
    """
    if ":" in url:
        (cmd, arg) = url.split(":")
    else:
        cmd = url

    if cmd == "ankipubsubDeckManager":
        anki_deck_manager_setup()
    else:
        kwargs.get('_old')(self, url)

# We are adding buttons to the anki gui right here
DeckBrowser._drawButtons = wrap(DeckBrowser._drawButtons,
                                ankiPubSubOptionsButton)

# Here we hook into the anki link handler to wire up our button
DeckBrowser._linkHandler = wrap(DeckBrowser._linkHandler,
                                connect_anki_pub_sub_link_handler,
                                pos='around')
