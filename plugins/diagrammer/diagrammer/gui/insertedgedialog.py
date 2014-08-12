# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod

import wx

from outwiker.gui.testeddialog import TestedDialog

from ..i18n import get_
from .propertyfactory import PropertyFactory


class InsertEdgeDialog (TestedDialog):
    """
    Диалог для выбора параметров ребра
    """
    def __init__ (self, parent):
        global _
        _ = get_()

        super (InsertEdgeDialog, self).__init__ (parent,
                                                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME)

        self.SetTitle (_(u"Insert edge"))

        self.__createGui()
        self.Fit()
        self.Center(wx.CENTRE_ON_SCREEN)

        self.Bind (wx.EVT_COLLAPSIBLEPANE_CHANGED, self.__onPaneChanged)


    def __createGui (self):
        self._paramsPanel = wx.CollapsiblePane (self,
                                                label = _(u"Options"),
                                                style = wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE)

        mainSizer = wx.FlexGridSizer (cols = 1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (1)

        nameSizer = wx.FlexGridSizer (cols=2)
        nameSizer.AddGrowableCol (1)
        nameSizer.AddGrowableRow (0)

        self._firstName = PropertyFactory.createText (self,
                                                      self,
                                                      nameSizer,
                                                      _(u"First node name"),
                                                      "firstName")

        self._secondName = PropertyFactory.createText (self,
                                                       self,
                                                       nameSizer,
                                                       _(u"Second node name"),
                                                       "secondName")
        mainSizer.Add (nameSizer,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2)

        optionsSizer = wx.FlexGridSizer (cols=2)
        optionsSizer.AddGrowableCol (0)
        optionsSizer.AddGrowableCol (1)

        PropertyFactory.createText (self,
                                    self._paramsPanel.GetPane(),
                                    optionsSizer,
                                    _(u"Label"),
                                    "label")

        PropertyFactory.createStyle (self,
                                     self._paramsPanel.GetPane(),
                                     optionsSizer,
                                     _(u"Line style"))

        PropertyFactory.createArrowStyle (self,
                                          self._paramsPanel.GetPane(),
                                          optionsSizer,
                                          _(u"Arrow style"))

        PropertyFactory.createColor  (self,
                                      self._paramsPanel.GetPane(),
                                      optionsSizer,
                                      _(u"Set line color"),
                                      "black",
                                      "lineColor",
                                      "isLineColorChanged")

        self._paramsPanel.GetPane().SetSizer (optionsSizer)

        mainSizer.Add (self._paramsPanel,
                       flag = wx.EXPAND | wx.ALL,
                       border = 2)

        PropertyFactory.createOkCancelButtons (self, mainSizer)

        self.SetSizer (mainSizer)
        self._firstName.SetFocus()


    def __onPaneChanged (self, event):
        self.Fit()



class InsertEdgeControllerBase (object):
    __metaclass__ = ABCMeta

    def __init__ (self, dialog):
        self._dialog = dialog


    @abstractmethod
    def getEdge (self):
        """
        Метод должен возвращать строку, описывающую связь узлов (ребро): "--", "->", "<-", "<->"
        """
        pass


    def showDialog (self):
        result = self._dialog.ShowModal()
        return result


    def getResult (self):
        """
        Возвращает строку для создания ребра в соответствии с параметрами, установленными в диалоге.
        Считается, что этот метод вызывают после того, как showDialog вернул значение wx.ID_OK
        """
        firstname = self._getFirstName (self._dialog).strip()
        if len (firstname) == 0:
            firstname = _(u"Node1")

        secondname = self._getSecondName (self._dialog).strip()
        if len (secondname) == 0:
            secondname = _(u"Node2")

        edge = self.getEdge()
        params = self._getParamString (self._dialog).strip()

        if len (params) == 0:
            return u"{firstname} {edge} {secondname}".format (firstname = firstname,
                                                              secondname = secondname,
                                                              edge = edge)
        else:
            return u"{firstname} {edge} {secondname} [{params}]".format (firstname = firstname,
                                                                         secondname = secondname,
                                                                         edge = edge,
                                                                         params = params)


    def _getParamString (self, dialog):
        params = []
        params.append (self._getLabelParam (dialog))
        params.append (self._getLineStyleParam (dialog))
        params.append (self._getArrowStyleParam (dialog))
        params.append (self._getLineColorParam (dialog))

        return u", ".join ([param for param in params if len (param.strip()) != 0])


    def __getNameNotation (self, name):
        if u" " in name:
            return u'"{}"'.format (name)

        return name


    def _getFirstName (self, dialog):
        return self.__getNameNotation (dialog.firstName)


    def _getSecondName (self, dialog):
        return self.__getNameNotation (dialog.secondName)


    def _getLabelParam (self, dialog):
        return u'label = "{}"'.format (dialog.label) if len (dialog.label) != 0 else u""


    def _getLineStyleParam (self, dialog):
        """
        Возвращает строку с параметром, задающим стиль линии
        """
        style = dialog.style.lower().strip().replace (u" ", u"")

        if len (style) == 0:
            return u""

        if style[0].isdigit():
            return u'style = "{}"'.format (style)

        return u"style = {}".format (style)


    def _getArrowStyleParam (self, dialog):
        """
        Возвращает строку с параметром, задающим стиль линии
        """
        style = dialog.arrowStyle.lower().strip().replace (u" ", u"")

        if len (style) == 0:
            return u""

        if style[0].isdigit():
            return u'hstyle = "{}"'.format (style)

        return u"hstyle = {}".format (style)


    def _getLineColorParam (self, dialog):
        return u'color = "{}"'.format (dialog.lineColor) if dialog.isLineColorChanged else u""



class InsertEdgeControllerNone (InsertEdgeControllerBase):
    def getEdge (self):
        return u"--"



class InsertEdgeControllerLeft (InsertEdgeControllerBase):
    def getEdge (self):
        return u"<-"



class InsertEdgeControllerRight (InsertEdgeControllerBase):
    def getEdge (self):
        return u"->"



class InsertEdgeControllerBoth (InsertEdgeControllerBase):
    def getEdge (self):
        return u"<->"
