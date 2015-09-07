__author__ = 'fritz'


def drawTable(f):
    table = f.ui.tableWidget
    decks = util.getAllAnkiPubSubDecks()
    table.setRowCount(len(decks))
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(['Deck', 'Deck Remote ID', ''])
    table.setColumnWidth(0, 160)
    table.setColumnWidth(1, 200)
    table.setColumnWidth(2, 120)

    for (i, deck) in enumerate(decks):
        did = deck[1]

        deck = AnkipubSubDeck.fromLocalID(did)
        deckRemoteID = deck.getRemoteID()
        widget = QWidget(table)
        btnDelete = QPushButton(widget)
        btnDelete.setGeometry(0, 0, 30, 30)

        btnDelete.setIcon(QIcon('../../addons/pubsub/images/Delete-Resized.jpg'))
        btnDelete.setIconSize(QSize(25, 25))
        btnDelete.clicked.connect(partial(deleteAnkiPubSubDeck,form=f, remoteID=deckRemoteID))
        btnDownload = QPushButton(widget)
        btnDownload.setGeometry(30, 0, 30, 30)
        # TODO FIX TO PARTIAL
        btnDownload.clicked.connect(
            partial(download, did,
                    mw.col.conf.get('ankipubsubServer',
                                    "http://144.76.172.187:5000/v0"),
                    mw.col.conf.get('pubSubName', ""),
                    mw.col.conf.get('pubSubPassword', "")))
        btnDownload.setIcon(QIcon('../../addons/pubsub/images/Download-Resized.jpg'))
        btnDownload.setIconSize(QSize(25, 25))

        btnUpload = QPushButton(widget)
        btnUpload.setGeometry(60, 0, 30, 30)
        btnUpload.setIcon(QIcon('../../addons/pubsub/images/Upload-Resized.jpg'))
        btnUpload.setIconSize(QSize(25, 25))
        btnUpload.clicked.connect(
            partial(upload, did,
                    mw.col.conf.get('ankipubsubServer',
                                    "http://144.76.172.187:5000/v0"),
                    mw.col.conf.get('pubSubName', ""),
                    mw.col.conf.get('pubSubPassword', "")))

        btnSettings = QPushButton(widget)
        btnSettings.setGeometry(90, 0, 30, 30)
        btnSettings.setIcon(QIcon('../../addons/pubsub/images/Settings-Resized.jpg'))
        btnSettings.setIconSize(QSize(25, 25))
        btnSettings.clicked.connect(partial(ankiDeckSettings, did=deckRemoteID))
        table.setCellWidget(i, 2, widget)
        table.setItem(i, 0, QTableWidgetItem(str(deck.getName())))
        table.setItem(i, 1, QTableWidgetItem(str(deck.getRemoteID())))