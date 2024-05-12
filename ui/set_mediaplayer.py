from PyQt5.QtCore import QUrl
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class SetMediaPlayer:
    def __init__(self, ui_class):
        self.ui = ui_class
        self.set()

    def set(self):
        self.ui.videoWidget = QVideoWidget(self.ui)
        self.ui.videoWidget.setGeometry(0, 0, 1403, 763)
        self.ui.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.ui.mediaPlayer.setVideoOutput(self.ui.videoWidget)
        self.ui.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile('./ui/intro.mp4')))
        # noinspection PyUnresolvedReferences
        self.ui.mediaPlayer.stateChanged.connect(self.ui.VideoWidgetClose)
        if self.ui.dict_set['인트로숨김']:
            self.ui.videoWidget.setVisible(False)
        else:
            self.ui.mediaPlayer.play()
