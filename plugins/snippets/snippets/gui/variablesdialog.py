# -*- coding: UTF-8 -*-

import cgi
from collections import namedtuple

import wx

from outwiker.core.event import Event
from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.system import getOS

from snippets.snippetparser import SnippetParser


FinishDialogParams = namedtuple('FinishDialogParams', ['text'])


class VariablesDialog(TestedDialog):
    def __init__(self, parent):
        super(TestedDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self._width = 700
        self._height = 400
        self._createGUI()

    def _createGUI(self):
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(0)

        self._htmlRender = getOS().getHtmlRender(self)
        self._varPanel = VaraiblesPanel(self)

        self.ok_button = wx.Button(self, wx.ID_OK)
        self.ok_button.SetDefault()

        btn_sizer = self.CreateStdDialogButtonSizer(wx.CANCEL)
        btn_sizer.Add(self.ok_button)

        mainSizer.Add(self._htmlRender, 1, flag=wx.ALL | wx.EXPAND, border=2)
        mainSizer.Add(self._varPanel, 1, flag=wx.ALL | wx.EXPAND, border=2)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(btn_sizer,
                      flag=wx.ALL | wx.ALIGN_RIGHT,
                      border=2)

        self.SetSizer(mainSizer)
        self.SetClientSize((self._width, self._height))

    def setTemplate(self, text, basepath):
        self._htmlRender.SetPage(text, basepath)

    def prepare(self, variables):
        pass


class VariablesDialogController(object):
    def __init__(self, application):
        self._application = application

        self.onFinishDialog = Event()
        self._dialog = None
        self._parser = None
        self._selectedText = u''

        self._htmlTemplate = u'''<!DOCTYPE html>
<html>
<head>
</head>
<body>{text}</body>
</html>
        '''

    def _setDialogTemplate(self, template):
        text = cgi.escape(template)
        text = text.replace(u'\n', u'<br/>\n')
        result = self._htmlTemplate.format(text=text)
        self._dialog.setTemplate(result,
                                 self._application.selectedPage.path)

    def ShowDialog(self, selectedText, template):
        if self._application.selectedPage is None:
            return

        if self._dialog is None:
            self._dialog = VariablesDialog(self._application.mainWindow)
            self._dialog.ok_button.Bind(wx.EVT_BUTTON, handler=self._onOk)

        self._selectedText = selectedText
        self._parser = SnippetParser(template, self._application)
        variables = sorted([var for var
                            in self._parser.getVariables()
                            if not var.startswith('__')])

        self._setDialogTemplate(template)
        self._dialog.prepare(variables)

        if variables:
            self._dialog.Show()
        else:
            self._finishDialog()

    def destroy(self):
        self.onFinishDialog.clear()
        if self._dialog is not None:
            self._dialog.ok_button.Unbind(wx.EVT_BUTTON,
                                          handler=self._onOk)
            self._dialog.Close()
            self._dialog = None

    def _finishDialog(self):
        if self._application.selectedPage is not None:
            text = self._parser.process(self._selectedText,
                                        self._application.selectedPage)
            self.onFinishDialog(FinishDialogParams(text))
        self._dialog.Close()
        self._dialog = None

    def _onOk(self, event):
        self._finishDialog()


class VaraiblesPanel(wx.ScrolledWindow):
    def __init__(self, parent):
        super(VaraiblesPanel, self).__init__(parent)
        self.SetMinSize((1, 1))
