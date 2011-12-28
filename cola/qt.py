def create_button(text='', layout=None, tooltip=None, icon=None):
    if text:
        button.setText(tr(text))
        self.label = label = QtGui.QLabel()
        self.corner_layout = QtGui.QHBoxLayout()
        self.corner_layout.setMargin(0)
        self.corner_layout.setSpacing(defs.spacing)

        layout.addLayout(self.corner_layout)
    def set_title(self, title):
        self.label.setText(title)

    def add_corner_widget(self, widget):
        self.corner_layout.addWidget(widget)

    def __init__(self, parent, provider=None):
        self._model = GitRefModel(parent, provider=provider)
    def __init__(self, parent=None, provider=None):
        self.refcompleter = GitRefCompleter(self, provider=provider)
        self.refcompleter.popup().installEventFilter(self)

    def eventFilter(self, obj, event):
        """Fix an annoyance on OS X

        The completer popup steals focus.  Work around it.
        This affects dialogs without QtCore.Qt.WindowModal modality.

        """
        if obj == self.refcompleter.popup():
            if event.type() == QtCore.QEvent.FocusIn:
                return True
        return False

    def mouseReleaseEvent(self, event):
        super(GitRefLineEdit, self).mouseReleaseEvent(event)
        self.refcompleter.complete()


class GitRefDialog(QtGui.QDialog):
    def __init__(self, title, button_text, parent, provider=None):
        super(GitRefDialog, self).__init__(parent)
        self.setWindowTitle(title)

        self.label = QtGui.QLabel()
        self.label.setText(title)

        self.lineedit = GitRefLineEdit(self, provider=provider)
        self.setFocusProxy(self.lineedit)

        self.ok_button = QtGui.QPushButton()
        self.ok_button.setText(self.tr(button_text))
        self.ok_button.setIcon(qtutils.apply_icon())

        self.close_button = QtGui.QPushButton()
        self.close_button.setText(self.tr('Close'))

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.setMargin(0)
        self.button_layout.setSpacing(defs.button_spacing)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.close_button)

        self.main_layout = QtGui.QVBoxLayout()
        self.main_layout.setMargin(defs.margin)
        self.main_layout.setSpacing(defs.spacing)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.lineedit)
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

        qtutils.connect_button(self.ok_button, self.accept)
        qtutils.connect_button(self.close_button, self.reject)

        self.connect(self.lineedit, SIGNAL('textChanged(QString)'),
                     self.text_changed)

        self.setWindowModality(QtCore.Qt.WindowModal)
        self.ok_button.setEnabled(False)

    def text(self):
        return unicode(self.lineedit.text())

    def text_changed(self, txt):
        self.ok_button.setEnabled(bool(self.text()))

    @staticmethod
    def ref(title, button_text, parent, provider=None):
        dlg = GitRefDialog(title, button_text, parent, provider=provider)
        dlg.show()
        dlg.raise_()
        dlg.setFocus()
        if dlg.exec_() == GitRefDialog.Accepted:
            return dlg.text()
        else:
            return None


class GitRefProvider(QtCore.QObject):
    def __init__(self, pre=None):
        super(GitRefProvider, self).__init__()
        if pre:
            self.pre = pre
        else:
            self.pre = []
        self.model = model = cola.model()
        msg = model.message_updated
        model.add_observer(msg, self.emit_updated)

    def emit_updated(self):
        self.emit(SIGNAL('updated()'))

    def matches(self):
        model = self.model
        return self.pre + model.local_branches + model.remote_branches + model.tags

    def dispose(self):
        self.model.remove_observer(self.emit_updated)
    def __init__(self, parent, provider=None):

        if provider is None:
            provider = GitRefProvider()
        self.provider = provider
        self.connect(self.provider, SIGNAL('updated()'),
                     self.update_matches)

        self.provider.dispose()
        for match in self.provider.matches():
        diff_old_rgx = TERMINAL(r'^--- ')
        diff_new_rgx = TERMINAL(r'^\+\+\+ ')
        diff_hd4_rgx = TERMINAL(r'^deleted file mode')
                          diff_hd4_rgx,     diff_head,