# -*- coding: utf-8 -*-

import os.path
from typing import List

import wx

from outwiker.core.commands import MessageBox, attachFiles, showError
from outwiker.core.system import getOS, getBuiltinImagePath
from outwiker.core.attachment import Attachment
from outwiker.actions.attachfiles import AttachFilesAction
from outwiker.actions.openattachfolder import OpenAttachFolderAction
from .guiconfig import AttachConfig
from .dropfiles import BaseDropFilesTarget


class AttachPanel(wx.Panel):
    def __init__(self, parent, application):
        super().__init__(parent)
        self._application = application
        self.ID_ATTACH = None
        self.ID_REMOVE = None
        self.ID_PASTE = None
        self.ID_EXECUTE = None
        self.ID_OPEN_FOLDER = None

        self.__toolbar = self.__createToolBar(self, -1)
        self.__attachList = wx.ListCtrl(self,
                                        -1,
                                        style=wx.LC_LIST | wx.SUNKEN_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.__fileIcons = getOS().fileIcons
        self.__attachList.SetImageList(self.__fileIcons.imageList,
                                       wx.IMAGE_LIST_SMALL)
        self._dropTarget = DropAttachFilesTarget(self._application, self)

        self.__bindGuiEvents()
        self.__bindAppEvents()

    def SetBackgroundColour(self, colour):
        super().SetBackgroundColour(colour)
        self.__attachList.SetBackgroundColour(colour)

    def SetForegroundColour(self, colour):
        super().SetForegroundColour(colour)
        self.__attachList.SetForegroundColour(colour)

    def __bindGuiEvents(self):
        self.Bind(wx.EVT_LIST_BEGIN_DRAG,
                  self.__onBeginDrag, self.__attachList)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.__onDoubleClick,
                  self.__attachList)

        self.Bind(wx.EVT_MENU, self.__onAttach, id=self.ID_ATTACH)
        self.Bind(wx.EVT_MENU, self.__onRemove, id=self.ID_REMOVE)
        self.Bind(wx.EVT_MENU, self.__onPaste, id=self.ID_PASTE)
        self.Bind(wx.EVT_MENU, self.__onExecute, id=self.ID_EXECUTE)
        self.Bind(wx.EVT_MENU, self.__onOpenFolder, id=self.ID_OPEN_FOLDER)
        self.Bind(wx.EVT_CLOSE, self.__onClose)

    def __unbindGuiEvents(self):
        self.Unbind(wx.EVT_LIST_BEGIN_DRAG,
                    handler=self.__onBeginDrag,
                    source=self.__attachList)

        self.Unbind(wx.EVT_LIST_ITEM_ACTIVATED,
                    handler=self.__onDoubleClick,
                    source=self.__attachList)

        self.Unbind(wx.EVT_MENU, handler=self.__onAttach, id=self.ID_ATTACH)
        self.Unbind(wx.EVT_MENU, handler=self.__onRemove, id=self.ID_REMOVE)
        self.Unbind(wx.EVT_MENU, handler=self.__onPaste, id=self.ID_PASTE)
        self.Unbind(wx.EVT_MENU, handler=self.__onExecute, id=self.ID_EXECUTE)

        self.Unbind(wx.EVT_MENU, handler=self.__onOpenFolder,
                    id=self.ID_OPEN_FOLDER)

        self.Unbind(wx.EVT_CLOSE, handler=self.__onClose)

    @property
    def attachList(self):
        return self.__attachList

    @property
    def toolBar(self):
        return self.__toolbar

    def __bindAppEvents(self):
        self._application.onPageSelect += self.__onPageSelect
        self._application.onAttachListChanged += self.__onAttachListChanged
        self._application.onWikiOpen += self.__onWikiOpen

    def __unbindAppEvents(self):
        self._application.onPageSelect -= self.__onPageSelect
        self._application.onAttachListChanged -= self.__onAttachListChanged
        self._application.onWikiOpen -= self.__onWikiOpen

    def __onClose(self, _event):
        self._dropTarget.destroy()
        self.__unbindAppEvents()
        self.__unbindGuiEvents()
        self.toolBar.ClearTools()
        self.attachList.ClearAll()
        self.__fileIcons.clear()
        self.Destroy()

    def __createToolBar(self, parent, toolbar_id):
        toolbar = wx.ToolBar(parent, toolbar_id, style=wx.TB_DOCKABLE)
        self.ID_ATTACH = toolbar.AddTool(
            wx.ID_ANY,
            _(u"Attach Files…"),
            wx.Bitmap(getBuiltinImagePath("attach.png"),
                      wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Attach Files…"),
            ""
        ).GetId()

        self.ID_REMOVE = toolbar.AddTool(
            wx.ID_ANY,
            _(u"Remove Files…"),
            wx.Bitmap(getBuiltinImagePath("delete.png"),
                      wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Remove Files…"),
            ""
        ).GetId()

        toolbar.AddSeparator()

        self.ID_PASTE = toolbar.AddTool(
            wx.ID_ANY,
            _(u"Paste"),
            wx.Bitmap(getBuiltinImagePath("paste.png"),
                      wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Paste"),
            ""
        ).GetId()

        self.ID_EXECUTE = toolbar.AddTool(
            wx.ID_ANY,
            _(u"Execute"),
            wx.Bitmap(getBuiltinImagePath("execute.png"),
                      wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Execute"),
            ""
        ).GetId()

        self.ID_OPEN_FOLDER = toolbar.AddTool(
            wx.ID_ANY,
            _(u"Open Attachments Folder"),
            wx.Bitmap(getBuiltinImagePath("folder.png"),
                      wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Open Attachments Folder"),
            ""
        ).GetId()

        toolbar.Realize()
        return toolbar

    def __set_properties(self):
        self.__attachList.SetMinSize((-1, 100))

    def __do_layout(self):
        attachSizer_copy = wx.FlexGridSizer(2, 1, 0, 0)
        attachSizer_copy.Add(self.__toolbar, 1, wx.EXPAND, 0)
        attachSizer_copy.Add(self.__attachList, 1, wx.ALL | wx.EXPAND, 2)
        self.SetSizer(attachSizer_copy)
        attachSizer_copy.Fit(self)
        attachSizer_copy.AddGrowableRow(1)
        attachSizer_copy.AddGrowableCol(0)

        attachSizer_copy.Fit(self)
        self.SetAutoLayout(True)

    def __onWikiOpen(self, _wiki):
        self.updateAttachments()

    def __onPageSelect(self, _page):
        self.updateAttachments()

    def __sortFilesList(self, files_list):
        result = sorted(files_list, key=str.lower, reverse=True)
        result.sort(key=Attachment.sortByType)
        return result

    def updateAttachments(self):
        """
        Обновить список прикрепленных файлов
        """
        self.__attachList.Freeze()
        self.__attachList.ClearAll()
        if self._application.selectedPage is not None:
            files = Attachment(self._application.selectedPage).attachmentFull
            files = self.__sortFilesList(files)

            for fname in files:
                if (not os.path.basename(fname).startswith("__") or
                        not os.path.isdir(fname)):
                    # Отключим уведомления об ошибках во всплывающих окнах
                    # иначе они появляются при попытке прочитать
                    # испорченные иконки
                    # На результат работы это не сказывается,
                    # все-равно бракованные иконки отлавливаются.
                    wx.Log.EnableLogging(False)

                    imageIndex = self.__fileIcons.getFileImage(fname)

                    # Вернем всплывающие окна с ошибками
                    wx.Log.EnableLogging(True)

                    self.__attachList.InsertItem(
                        0,
                        os.path.basename(fname),
                        imageIndex)

        self.__attachList.Thaw()

    def __getSelectedFiles(self):
        files = []

        item = self.__attachList.GetNextItem(-1, state=wx.LIST_STATE_SELECTED)

        while item != -1:
            fname = self.__attachList.GetItemText(item)
            files.append(fname)

            item = self.__attachList.GetNextItem(item,
                                                 state=wx.LIST_STATE_SELECTED)

        return files

    def __onAttach(self, _event):
        self._application.actionController.getAction(
            AttachFilesAction.stringId).run(None)

    def __onRemove(self, _event):
        if self._application.selectedPage is not None:
            files = self.__getSelectedFiles()

            if len(files) == 0:
                showError(self._application.mainWindow,
                          _(u"You did not select a file to remove"))
                return

            if MessageBox(_(u"Remove selected files?"),
                          _(u"Remove files?"),
                          wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
                try:
                    Attachment(
                        self._application.selectedPage).removeAttach(files)
                except IOError as e:
                    showError(self._application.mainWindow, str(e))

                self.updateAttachments()

    def __pasteLink(self):
        """
        Сгенерировать сообщение о том, что пользователь хочет вставить
        ссылку на приаттаченные файлы
        """
        files = self.__getSelectedFiles()
        if len(files) == 0:
            showError(self._application.mainWindow,
                      _(u"You did not select a file to paste"))
            return

        self._application.onAttachmentPaste(files)

    def __executeFile(self):
        if self._application.selectedPage is not None:
            files = self.__getSelectedFiles()

            if len(files) == 0:
                showError(self._application.mainWindow,
                          _(u"You did not select a file to execute"))
                return

            for file in files:
                fullpath = os.path.join(Attachment(
                    self._application.selectedPage).getAttachPath(), file)
                try:
                    getOS().startFile(fullpath)
                except OSError:
                    text = _(u"Can't execute file '%s'") % file
                    showError(self._application.mainWindow, text)

    def __onPaste(self, _event):
        self.__pasteLink()

    def __onOpenFolder(self, _event):
        self._application.actionController.getAction(
            OpenAttachFolderAction.stringId).run(None)

    def __onExecute(self, _event):
        self.__executeFile()

    def __onDoubleClick(self, _event):
        config = AttachConfig(self._application.config)
        if config.doubleClickAction.value == AttachConfig.ACTION_INSERT_LINK:
            self.__pasteLink()
        elif config.doubleClickAction.value == AttachConfig.ACTION_OPEN:
            self.__executeFile()

    def __onBeginDrag(self, _event):
        selectedFiles = self.__getSelectedFiles()
        if not selectedFiles:
            return

        data = wx.FileDataObject()
        attach_path = Attachment(
            self._application.selectedPage).getAttachPath()

        for fname in self.__getSelectedFiles():
            data.AddFile(os.path.join(attach_path, fname))

        dragSource = wx.DropSource(data, self)
        dragSource.DoDragDrop()

    def __onAttachListChanged(self, page, _params):
        if page is not None and page == self._application.selectedPage:
            self.updateAttachments()

    def SetFocus(self):
        self.__attachList.SetFocus()

        if (self.__attachList.GetItemCount() != 0 and
                self.__attachList.GetFocusedItem() == -1):
            self.__attachList.Focus(0)
            self.__attachList.Select(0)


class DropAttachFilesTarget(BaseDropFilesTarget):
    """
    Класс для возможности перетаскивания файлов
    между другими программами и панелью с прикрепленными файлами.
    """

    def OnDropFiles(self, x: int, y: int, files: List[str]) -> bool:
        correctedFiles = self.correctFileNames(files)

        if (self._application.wikiroot is not None and
                self._application.wikiroot.selectedPage is not None):
            attachFiles(self._application.mainWindow,
                        self._application.wikiroot.selectedPage,
                        correctedFiles)
            return True

        return False
