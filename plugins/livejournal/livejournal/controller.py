# -*- coding: utf-8 -*-

import os.path

import wx

from .i18n import get_
from .ljcommand import LjUserCommand, LjCommunityCommand
from .comboboxdialog import ComboBoxDialog
from .dialogcontroller import UserDialogController, CommunityDialogController


class Controller (object):
    def __init__ (self, application):
        self._application = application
        self.__toolbarCreated = False

        self.ID_TOOLBAR = u"Plugin_livejournal"
        self.ID_LJUSER = u"PLUGIN_LIVEJOURNAL_LJUSER_ID"
        self.ID_LJCOMMUNITY = u"PLUGIN_LIVEJOURNAL_LJCOMMUNITY_ID"


    def initialize(self):
        """
        Инициализация плагина
        """
        global _
        _ = get_()

        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy

        if self._isWikiPage(self._application.selectedPage):
            self.__onPageViewCreate (self._application.selectedPage)


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy

        self.__destroyToolBar()


    def __onWikiParserPrepare (self, parser):
        """
        Добавление команд в википарсер
        """
        parser.addCommand (LjUserCommand (parser))
        parser.addCommand (LjCommunityCommand (parser))


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None

        if self._isWikiPage(page):
            self.__createToolBar()

    def __createToolBar(self):
        """
        Создание панели с кнопками, если она еще не была создана
        """
        mainWnd = self._application.mainWindow

        if mainWnd is not None and not self.__toolbarCreated:
            mainWnd.toolbars.createToolBar(
                self.ID_TOOLBAR,
                _('Livejournal')
            )

            pageView = self._getPageView()
            # pageView.addTool (pageView.commandsMenu,
            #                   self.ID_LJUSER,
            #                   self.__onLJUser,
            #                   _(u"Livejournal User (:ljuser ...:)"),
            #                   _(u"Livejournal User (:ljuser ...:)"),
            #                   self._getImagePath ("ljuser.gif"),
            #                   False,
            #                   panelname=self.ID_TOOLBAR)
            #
            # pageView.addTool (pageView.commandsMenu,
            #                   self.ID_LJCOMMUNITY,
            #                   self.__onLJCommunity,
            #                   _(u"Livejournal Community (:ljcomm ...:)"),
            #                   _(u"Livejournal Community (:ljcomm ...:)"),
            #                   self._getImagePath ("ljcommunity.gif"),
            #                   False,
            #                   panelname=self.ID_TOOLBAR)

            self.__toolbarCreated = True


    def __onPageViewDestroy (self, page):
        """
        Обработчик события выбора новой страницы
        """
        if self._isWikiPage(page):
            self.__destroyToolBar()

    def _isWikiPage(self, page):
        return page is not None and page.getTypeString() == u"wiki"

    def __insertCommand (self, title, controllerType):
        assert self._application.mainWindow is not None

        with ComboBoxDialog (self._application.mainWindow,
                             title,
                             title,
                             wx.CB_DROPDOWN | wx.CB_SORT) as dlg:
            editor = self._getPageView().codeEditor

            selText = editor.GetSelectedText()

            controller = controllerType (dlg, self._application, selText)
            if controller.showDialog () == wx.ID_OK:
                editor.replaceText (controller.result)


    def __onLJUser (self, event):
        """
        Обработчик нажатия кнопки для вставки ЖЖ-пользователя
        """
        assert self._application.mainWindow is not None
        self.__insertCommand (_(u"Livejournal user"), UserDialogController)


    def __onLJCommunity (self, event):
        """
        Обработчик нажатия кнопки для вставки ЖЖ-сообщества
        """
        assert self._application.mainWindow is not None
        self.__insertCommand (_(u"Livejournal community"), CommunityDialogController)


    def __destroyToolBar (self):
        """
        Уничтожение панели с кнопками
        """
        if self._application.mainWindow is not None and self.__toolbarCreated:
            self._application.mainWindow.toolbars.destroyToolBar (self.ID_TOOLBAR)
            self.__toolbarCreated = False


    def _getImagePath (self, fname):
        imagedir = os.path.join (os.path.dirname (__file__), "images")
        return os.path.join (imagedir, fname)


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView
