# -*- coding: UTF-8 -*-

import os.path

import wx
import wx.grid

from outwiker.core.system import getImagesDir


class IconButton (object):
    """
    Button with single icons
    """
    _invalidFileName = os.path.join (getImagesDir(), u'cross.png')

    # Оформление
    _normalBackground = wx.Colour (255, 255, 255)
    _selectedBackground = wx.Colour (160, 190, 255)
    _borderColor = wx.Colour (0, 0, 255)


    def __init__ (self, parent, fname, width, height):
        self._parent = parent
        self.fname = fname
        self._width = width
        self._height = height

        self._x = 0
        self._y = 0
        self.image = None

        # Выбрана ли данная иконка?
        self.__selected = False


    def _createImage (self, fname):
        # Disable wxPython message about the invalid picture format
        wx.Log_EnableLogging(False)
        image = wx.Bitmap (fname)
        wx.Log_EnableLogging(True)

        if not image.IsOk():
            print _(u'Invalid icon file: {}').format (fname)
            image = wx.Bitmap (self._invalidFileName)

        return image


    def paint (self):
        if self.image is None:
            self.image = self._createImage (self.fname)

        assert self.image.IsOk()

        dc = wx.PaintDC (self._parent)

        dc.SetBrush (wx.Brush (self._selectedBackground
                               if self.selected
                               else self._normalBackground))

        dc.SetPen(wx.TRANSPARENT_PEN)

        dc.DrawRectangle (self._x,
                          self._y,
                          self._width,
                          self._height)

        posx = self._x + (self._width - self.image.GetWidth()) / 2
        posy = self._y + (self._height - self.image.GetHeight()) / 2

        dc.DrawBitmap(self.image, posx, posy, True)

        if self.selected:
            dc.SetPen (wx.Pen (self._borderColor))
            dc.SetBrush (wx.TRANSPARENT_BRUSH)
            dc.DrawRectangle (self._x,
                              self._y,
                              self._width,
                              self._height)


    @property
    def selected (self):
        return self.__selected


    @selected.setter
    def selected (self, value):
        if value != self.__selected:
            self.__selected = value


    def SetPosition (self, x, y):
        self._x = x
        self._y = y


    @property
    def x (self):
        return self._x


    @x.setter
    def x (self, value):
        self._x = value


    @property
    def y (self):
        return self._y


    @y.setter
    def y (self, value):
        self._y = value


    @property
    def width (self):
        return self._width


    @property
    def height (self):
        return self._height


    def __getToolTipText (self, fname):
        """
        Return the text of the tooltip with file name
        """
        text = os.path.basename (fname)

        # Отбросим расширение файла
        dotPos = text.rfind (".")
        if dotPos != -1:
            text = text[: dotPos]

        if text == "__icon":
            text = _(u"Curent icon")
        elif text == u"_page":
            text = _(u"Default icon")

        return text


class IconListCtrl (wx.ScrolledWindow):
    """
    Control with icons for pages
    """
    def __init__ (self, parent, multiselect=False):
        wx.ScrolledWindow.__init__ (self, parent, style = wx.BORDER_THEME)
        self._canvas = wx.Panel (self)
        self._canvas.SetSize ((0, 0))
        self._canvas.SetBackgroundColour (IconButton._normalBackground)
        self._canvas.Bind (wx.EVT_PAINT, handler=self.__onPaint)
        self._canvas.Bind (wx.EVT_LEFT_DOWN, handler=self.__onCanvasClick)

        self.cellWidth = 32
        self.cellHeight = 32
        self.margin = 1
        self.multiselect = multiselect

        # Path to current page icon
        self._currentIcon = None

        self._lastClickedButton = None

        self.SetScrollRate (0, 0)
        self.SetBackgroundColour (wx.Colour (255, 255, 255))

        # Список картинок, которые хранятся в окне
        self.buttons = []
        self._iconFileNames = []

        self.defaultIcon = os.path.join (getImagesDir(), "page.png")

        self.Bind (wx.EVT_SIZE, self.__onSize)


    def __onSize (self, event):
        self.__layout()


    def __onPaint (self, event):
        for button in self.buttons:
            button.paint()


    def clear (self):
        """
        Remove old buttons with icons.
        """
        self.buttons = []
        self._iconFileNames = []
        self._lastClickedButton = None
        self.Scroll (0, 0)


    def setIconsList (self, iconFileNames):
        self.clear()
        self._iconFileNames = iconFileNames

        for fname in reversed (iconFileNames):
            self.__addButton (fname)

        if len (self.buttons) != 0:
            self.__selectSingleButton (self.buttons[0])

        self.__layout()
        self.Scroll (0, 0)


    def __addButton (self, fname):
        """
        Add the button with icons fname (full path)
        """
        try:
            button = IconButton (self._canvas, fname, self.cellWidth, self.cellHeight)
        except ValueError:
            return

        self.buttons.insert (0, button)
        return button


    def _getButtonByCoord (self, x, y):
        for button in self.buttons:
            if (x >= button.x and
                    x <= button.x + button.width and
                    y >= button.y and
                    y <= button.y + button.height):
                return button


    def __onCanvasClick (self, event):
        ctrl = wx.GetKeyState (wx.WXK_CONTROL)
        shift = wx.GetKeyState (wx.WXK_SHIFT)

        button = self._getButtonByCoord (event.GetPosition()[0],
                                         event.GetPosition()[1])

        if button is None:
            return

        if not self.multiselect or (not ctrl and not shift):
            self.__selectSingleButton (button)
        elif ctrl:
            self.__toggleSelectionButton (button)
        elif shift and self._lastClickedButton is not None:
            self.__selectFromTo (self._lastClickedButton, button)

        self._refreshCanvas()


    def _refreshCanvas (self):
        self._canvas.Refresh()


    def __selectSingleButton (self, selectedButton):
        for button in self.buttons:
            if button is selectedButton:
                button.selected = True
                self._lastClickedButton = button
            else:
                button.selected = False


    def __toggleSelectionButton (self, button):
        button.selected = not button.selected
        self._lastClickedButton = button


    def __selectFromTo (self, fromButton, toButton):
        fromIndex = -1
        toIndex = -1

        for index, button in enumerate (self.buttons):
            if button is fromButton:
                fromIndex = index

            if button is toButton:
                toIndex = index

        assert fromIndex != -1
        assert toIndex != -1

        minIndex = min (fromIndex, toIndex)
        maxIndex = max (fromIndex, toIndex)

        for button in self.buttons[minIndex: maxIndex + 1]:
            button.selected = True
            self._lastClickedButton = button


    def __layout (self):
        currx = 0
        curry = 0
        windowWidth = self.GetClientSizeTuple()[0]

        # Row size in cells (columns count)
        colsCount = (windowWidth - self.margin) // (self.cellWidth + self.margin)
        rowsCount = len (self.buttons) // colsCount + 1

        for n, button in enumerate (self.buttons):
            row = n // colsCount
            col = n % colsCount

            currx = self.margin + col * (self.cellWidth + self.margin)
            curry = self.margin + row * (self.cellHeight + self.margin)

            button.x = currx
            button.y = curry

        self.Scroll (0, 0)
        self._canvas.SetSizeWH (windowWidth,
                                rowsCount * (self.cellHeight + self.margin))

        self.SetScrollbars (self.cellWidth,
                            self.cellHeight + self.margin,
                            1,
                            rowsCount)
        self._refreshCanvas()


    def getSelection (self):
        """
        Return list of the selected icons
        """
        return [button.fname for button in self.buttons if button.selected]


    def setCurrentIcon (self, fname):
        """
        Add the icon and make it selected default
        """
        self._currentIcon = fname
        if self._currentIcon is None:
            return

        self._iconFileNames.insert (0, fname)
        self.__addButton (self._currentIcon)
        self.__layout()
        self.__selectSingleButton (self.buttons[0])
