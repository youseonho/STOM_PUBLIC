class SetLogTap:
    def __init__(self, ui_class, wc):
        self.ui = ui_class
        self.wc = wc
        self.set()

    def set(self):
        self.ui.sst_textEditttt_01 = self.wc.setTextEdit(self.ui.lg_tab, vscroll=True)
        self.ui.cst_textEditttt_01 = self.wc.setTextEdit(self.ui.lg_tab, vscroll=True)
        self.ui.src_textEditttt_01 = self.wc.setTextEdit(self.ui.lg_tab, vscroll=True)
        self.ui.crc_textEditttt_01 = self.wc.setTextEdit(self.ui.lg_tab, vscroll=True)

        self.ui.sst_textEditttt_01.setGeometry(7, 10, 668, 367)
        self.ui.cst_textEditttt_01.setGeometry(680, 10, 668, 367)
        self.ui.src_textEditttt_01.setGeometry(7, 382, 668, 367)
        self.ui.crc_textEditttt_01.setGeometry(680, 382, 668, 367)
