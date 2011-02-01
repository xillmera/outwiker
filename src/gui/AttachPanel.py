# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Fri May 21 19:25:30 2010

import os.path
import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

from core.controller import Controller
from core.factory import FactorySelector
import core.commands
from core.tree import RootWikiPage
import core.system

class AttachPanel(wx.Panel):
	def __init__(self, *args, **kwds):
		self.ID_ATTACH = wx.NewId()
		self.ID_REMOVE = wx.NewId()
		self.ID_PASTE = wx.NewId()
		self.ID_EXECUTE = wx.NewId()

		#self.__createToolBar()

		# begin wxGlade: AttachPanel.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.toolbar = self.__createToolBar(self, -1)
		self.attachList = wx.ListCtrl(self, -1, style=wx.LC_LIST|wx.SUNKEN_BORDER)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

		self.Bind(wx.EVT_MENU, self.onAttach, id=self.ID_ATTACH)
		self.Bind(wx.EVT_MENU, self.onRemove, id=self.ID_REMOVE)
		self.Bind(wx.EVT_MENU, self.onPaste, id=self.ID_PASTE)
		self.Bind(wx.EVT_MENU, self.onOpen, id=self.ID_EXECUTE)

		self.currentPage = None

		Controller.instance().onPageSelect += self.onPageSelect
		Controller.instance().onPageUpdate += self.onPageUpdate

		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onPaste, self.attachList)
	

	def __createToolBar (self, parent, id):
		imagesDir = core.system.getImagesDir()

		toolbar = wx.ToolBar (parent, id, style=wx.TB_DOCKABLE)

		toolbar.AddLabelTool(self.ID_ATTACH, 
				_(u"Attach Files..."), 
				wx.Bitmap(os.path.join (imagesDir, "attach.png"),
					wx.BITMAP_TYPE_ANY),
				wx.NullBitmap, 
				wx.ITEM_NORMAL,
				_(u"Attach Files..."), 
				"")

		toolbar.AddLabelTool(self.ID_REMOVE, 
				_(u"Remove Files..."), 
				wx.Bitmap(os.path.join (imagesDir, "delete.png"),
					wx.BITMAP_TYPE_ANY),
				wx.NullBitmap, 
				wx.ITEM_NORMAL,
				_(u"Remove Files..."), 
				"")

		toolbar.AddSeparator()

		toolbar.AddLabelTool(self.ID_PASTE, 
				_(u"Paste"), 
				wx.Bitmap(os.path.join (imagesDir, "paste.png"),
					wx.BITMAP_TYPE_ANY),
				wx.NullBitmap, 
				wx.ITEM_NORMAL,
				_(u"Paste"), 
				"")

		toolbar.AddLabelTool(self.ID_EXECUTE, 
				_(u"Execute"), 
				wx.Bitmap(os.path.join (imagesDir, "execute.png"),
					wx.BITMAP_TYPE_ANY),
				wx.NullBitmap, 
				wx.ITEM_NORMAL,
				_(u"Execute"), 
				"")

		toolbar.Realize()
		return toolbar


	def __set_properties(self):
		# begin wxGlade: AttachPanel.__set_properties
		self.attachList.SetMinSize((-1, 100))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: AttachPanel.__do_layout
		attachSizer_copy = wx.FlexGridSizer(2, 1, 0, 0)
		buttonsSizer_copy = wx.BoxSizer(wx.VERTICAL)
		attachSizer_copy.Add(self.toolbar, 1, wx.EXPAND, 0)
		attachSizer_copy.Add(self.attachList, 1, wx.ALL|wx.EXPAND, 2)
		attachSizer_copy.Add(buttonsSizer_copy, 1, wx.EXPAND, 0)
		self.SetSizer(attachSizer_copy)
		attachSizer_copy.Fit(self)
		attachSizer_copy.AddGrowableRow(1)
		attachSizer_copy.AddGrowableCol(0)
		# end wxGlade

		attachSizer_copy.Fit(self)
		self.SetAutoLayout(True)

		#attachSizer_copy.Add (self.toolbar, 1, wx.ALL|wx.EXPAND, 2)


	def onPageSelect (self, page):
		self.currentPage = page
		self.updateAttachments (page)


	def onPageUpdate (self, page):
		if self.currentPage != None and self.currentPage == page:
			self.updateAttachments (page)


	def updateAttachments (self, page):
		"""
		Обновить список прикрепленных файлов
		"""
		self.attachList.ClearAll()
		if page != None:
			files = page.attachment
			files.reverse()

			for fname in files:
				if not os.path.basename(fname).startswith("__") or not os.path.isdir (fname):
					self.attachList.InsertImageStringItem (0, os.path.basename (fname), 0)


	def getSelectedFiles (self):
		files = []

		item = self.attachList.GetNextItem (-1, state = wx.LIST_STATE_SELECTED)

		while item != -1:
			fname = self.attachList.GetItemText (item)
			files.append (fname)

			item = self.attachList.GetNextItem (item, state = wx.LIST_STATE_SELECTED)

		return files


	def onAttach(self, event): # wxGlade: AttachPanel.<event_handler>
		if self.currentPage != None:
			core.commands.attachFilesWithDialog (self, self.currentPage)


	def onRemove(self, event): # wxGlade: AttachPanel.<event_handler>
		if self.currentPage != None:
			files = self.getSelectedFiles ()

			if wx.MessageBox (_(u"Remove selected files?"), 
					_(u"Remove files?"),
					wx.YES_NO  | wx.ICON_QUESTION) == wx.YES:
				try:
					self.currentPage.removeAttach (files)
				except IOError as e:
					wx.MessageBox (unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)
	

	def onPaste(self, event): # wxGlade: AttachPanel.<event_handler>
		"""
		Сгенерировать сообщение о том, что пользователь хочет вставить ссылку на приаттаченные файлы
		"""
		files = self.getSelectedFiles ()
		Controller.instance().onAttachmentPaste (files)


	def onOpen(self, event): # wxGlade: AttachPanel.<event_handler>
		if self.currentPage != None:
			files = self.getSelectedFiles()

			for file in files:
				fullpath = os.path.join (self.currentPage.path, RootWikiPage.attachDir, file)
				try:
					core.system.getOS().startFile (fullpath)
				except OSError:
					text = _(u"Can't execute file '%s'") % file
					wx.MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)

# end of class AttachPanel


