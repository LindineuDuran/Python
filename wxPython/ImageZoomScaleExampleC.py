# Original code downloaded from:
#  http://stackoverflow.com/questions/602557/image-viewer-standard-gui-controls-bottom-up-or-what
#  [author: kanem]
import wx, os, string
from PIL import Image
"""
  Purpose: display images (*.jpg, *.jpeg, *.png, *.gif, *.bmp) and
           manipulate them (zoom, pan, and rotate images)

    Usage:
	* Mouse wheel forward (backward) and "+" ("-") key, zooms in (out). [similar to Google Earth]
	* "f" key toggles full screen.
	* "r" key rotates image in CW direction by 90 degree increments.
    * "m" key changes PIL mode from normal quality (fast) to high quality (slow).
    * Images less than 1000 x 1000 (w x h in pixels) will have high quality rendering.
    * Middle mouse button down while dragging, pans image, as do arrow keys, if image
      is larger than window).                                           [similar to Google Earth]
    * Click on left (right) mouse button for next (previous) image in image list.
  Note:
   1. The IMAGE_DIRECTORY should be assigned to the directory where your image files are located.
   2. Key codes can be obtained with KeyEvents in the wxPython demo.
   3. This code could almost surely be improved --- I leave that to you.

   Vers. 2014.03.05.01
   Contact: vs@it.uu.se

"""

# The following directories contain PNG files on my computers
#IMAGE_DIRECTORY = 'C:/FRA/ri220b/AVI_01/'   # DT
IMAGE_DIRECTORY = 'C:\\Users\\lindineu.duran\\Documents\\Python\\wxPython\\'   # LT
# The following are the character codes for a Swedish keyboard
M_KEY     = 77
F_KEY     = 70
R_KEY     = 82
PLUS_KEY  = 43
MINUS_KEY = 45

class ImageFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,title = "Image Viewer")
        self.Centre()
        self.Size = (500,500)

        self.imageBox = wx.Window(self)

        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.CreateStatusBar(5)
        self.SetStatusWidths([-1, 70, 50, 50, 30])

        self.cursor     = wx.Cursor( wx.CURSOR_ARROW)  # single arrow pointer
        self.moveCursor = wx.Cursor(wx.CURSOR_SIZING)  # N,E,S,W arrows (when panning)

        self.vbox.Add(self.imageBox,proportion=1,flag = wx.EXPAND)
        self.SetSizer(self.vbox)
        self.Show()

        self.sbm       = 0
        self.imageList = []
        self.imageIndx = 0
        self.numImages = 0
        self.factor    = 1
        self.rotation  = 0
        self.width     = 0
        self.height    = 0
        self.size      = 0
        self.count     = 0
        self.mc        = False        # change mouse cursor
        self.fs        = False        # toggle fullscreen
        self.mode      = 0            # rendering quality
        self.SetStatusText(str(self.mode), 4)

        self.loadDirectory(IMAGE_DIRECTORY)
        # Ok, ready to process this image
        self.processPicture()
        self.imageBox.SetBackgroundColour((0,0,0,0))
        # Define event handlers
        self.imageBox.Bind(wx.EVT_SIZE, lambda evt: self.rescale(evt,1))
        self.imageBox.Bind(wx.EVT_MOUSEWHEEL,       self.zoom)
        self.imageBox.Bind(wx.EVT_KEY_DOWN,         self.keyEvent)
        self.imageBox.Bind(wx.EVT_MIDDLE_UP,        self.endDrag)
        self.imageBox.Bind(wx.EVT_LEFT_DOWN,        self.next)
        self.imageBox.Bind(wx.EVT_RIGHT_DOWN,       self.prev)

    def processPicture(self, factor = 0):
        """
         Purpose: get image, define geometric parameters, scale,
                  show information in status bar, and display it.
        """
        fileName = self.imageList[self.imageIndx]
        img = Image.open(IMAGE_DIRECTORY+fileName)
        self.width  = img.size[0]
        self.height = img.size[1]
        ogHeight    = self.height
        ogWidth     = self.width
        xWin        = self.imageBox.Size[0]
        yWin        = self.imageBox.Size[1]
        winRatio    = 1.0*xWin/yWin
        imgRatio    = 1.0*self.width/self.height

        self.factor = factor*self.factor
        if factor == 0:
            self.factor = 1

        # Mode toggle
        mode = 0
        if (ogWidth <=1000 and ogHeight <= 1000) or self.mode == 1:
            mode = 1
        if imgRatio >= winRatio:
            # Match widths
            self.width  = self.factor*xWin
            self.height = self.factor*xWin/imgRatio
        else:
            # Match heights
            self.height = self.factor*yWin
            self.width  = self.factor*yWin*imgRatio
        img = img.resize((int(self.width),int(self.height)),mode)

        # Update information in status bar
        label = str(int(100*self.width/ogWidth))  # scale (percent)
        self.SetStatusText(self.imageList[self.imageIndx], 0)
        self.SetStatusText(str(ogWidth) + 'x' + str(ogHeight), 1)
        self.SetStatusText(label + '%', 2)
        self.SetStatusText(str(self.imageIndx+1) + '/' + str(self.numImages), 3)
        # Check for rotation of image
        if self.rotation % 360 != 0:
            img         = img.rotate(self.rotation)
            self.width  = img.size[0]
            self.height = img.size[1]

        # Clear the image window
        wximg = wx.Image(img.size[0],img.size[1])

        wximg.SetData(img.convert("RGB").tobytes())
        wximg.SetAlpha(img.convert("RGBA").tobytes()[3::4])

        self.showPicture(wximg)

    def showPicture(self,img):
        """
         Purpose: get bitmap, setup event handlers, and show image (refresh window).
        """
        bmp = wx.Bitmap(img)
        x = (self.imageBox.Size[0] -  self.width)/2.0
        y = (self.imageBox.Size[1] - self.height)/2.0

        tmp = wx.StaticBitmap(self.imageBox,wx.ID_ANY,bmp,(round(x),round(y)))

        tmp.Bind(wx.EVT_LEFT_DOWN,    self.next   )
        tmp.Bind(wx.EVT_RIGHT_DOWN,   self.prev   )
        tmp.Bind(wx.EVT_MOTION,       self.drag   )
        tmp.Bind(wx.EVT_MIDDLE_UP,    self.endDrag)
        tmp.SetBackgroundColour((180,180,180,180))

        if self.sbm:
            self.sbm.Destroy()
        self.sbm = tmp
        self.imageBox.Refresh()

    def loadDirectory(self,dir):
        """
         Purpose: create a list of all image files that can be displayed
                  in the dir directory.
        """
        self.imageList = []
        for image in os.listdir(dir):
            if image.lower().endswith(    'jpg') \
               or image.lower().endswith( 'png') \
               or image.lower().endswith('jpeg') \
               or image.lower().endswith( 'gif') \
               or image.lower().endswith( 'bmp'):
                self.imageList.append(image)
        self.numImages = len(self.imageList)

    def next(self,event):
        """
         Purpose: process next image in image list.
        """
        if self.imageIndx == self.numImages-1:
            self.imageIndx = -1
        self.imageIndx += 1
        self.rotation = 0
        self.processPicture()

    def prev(self,event):
        """
         Purpose: process previous image in image list.
        """
        if self.imageIndx == 0:
            self.imageIndx = self.numImages
        self.imageIndx += -1
        self.rotation = 0
        self.processPicture()

    def rescale(self,event,factor):
        """
         Purpose: rescale image.
        """
        if self.GetStatusBar():
            self.processPicture(factor)

    def zoom(self,event):
        """
         Purpose: mouse wheel forward zooms in and mouse
                  wheel backwards zooms out.
        """
        factor = 1.25
        if event.GetWheelRotation() < 0:
            factor = 0.8
        self.rescale(event,factor)

    def keyEvent(self,event):
        """
         Purpose: process keys for control of image.
        """
        code = event.GetKeyCode()
        if code   == PLUS_KEY  or code == wx.WXK_NUMPAD_ADD:
            self.rescale(event,1.25)
        elif code == MINUS_KEY or code == wx.WXK_NUMPAD_SUBTRACT:
            self.rescale(event,0.8)
        elif code == R_KEY:
            # Rotation in CW direction by 90 degrees
            self.rotation = self.rotation + 90
            self.processPicture(1)
        elif code == F_KEY:
            self.toggleFS()
        elif (code in [wx.WXK_LEFT, wx.WXK_UP, wx.WXK_RIGHT, wx.WXK_DOWN]) and self.sbm:
            # Process arrow keys
            self.scroll(code)
        elif code == M_KEY:
            if self.mode == 0:
                self.mode = 1
            else:
                self.mode = 0
            self.SetStatusText(str(self.mode), 4)
            self.processPicture(1)

    def scroll(self,code):
        """
         Purpose: pan image with "arrow" keys.
        """
        boxPos = self.imageBox.GetScreenPositionTuple()
        imgPos = self.sbm.GetScreenPositionTuple()
        delta = 20  # initialize pan translation

        if code == wx.WXK_LEFT and self.width > self.imageBox.Size[0]:
            compare = boxPos[0] - imgPos[0]
            if compare <= delta:
                delta = max(compare,0)
            self.imageBox.ScrollWindow(delta,0)

        if code == wx.WXK_UP and self.height > self.imageBox.Size[1]:
            compare = boxPos[1] - imgPos[1]
            if compare <= delta:
                delta = max(compare,0)
            self.imageBox.ScrollWindow(0,delta)

        if code == wx.WXK_RIGHT and self.width > self.imageBox.Size[0]:
            compare =  imgPos[0] + self.sbm.Size[0] - boxPos[0] - self.imageBox.Size[0]
            if compare <= delta:
                delta = max(compare,0)
            self.imageBox.ScrollWindow(-delta,0)

        if code == wx.WXK_DOWN and self.height > self.imageBox.Size[1]:
            compare =  imgPos[1] + self.sbm.Size[1] - boxPos[1] - self.imageBox.Size[1]
            if compare <= delta:
                delta = max(compare,0)
            self.imageBox.ScrollWindow(0,-delta)

    def drag(self,event):
        """
         Purpose: pan image with middle mouse button down.
        """
        if event.MiddleIsDown():
            if not self.mc:
                self.SetCursor(self.moveCursor)
                self.mc = True
            boxPos = self.imageBox.GetScreenPosition()
            imgPos = self.sbm.GetScreenPosition()
            if self.count == 0:
                self.x = event.GetX()
                self.y = event.GetY()
            self.count +=  1
            if self.count > 1:
                deltaX = event.GetX() - self.x
                deltaY = event.GetY() - self.y
                if imgPos[0] >= boxPos[0] and deltaX > 0:
                    deltaX = 0
                if imgPos[0] + self.width <= boxPos[0] + self.imageBox.Size[0] and deltaX < 0:
                    deltaX = 0
                if imgPos[1] >= boxPos[1] and deltaY > 0:
                    deltaY = 0
                if imgPos[1] + self.height <= boxPos[1] + self.imageBox.Size[1] and deltaY < 0:
                    deltaY = 0
                self.imageBox.ScrollWindow(2*deltaX,2*deltaY)
                self.count = 0

    def endDrag(self,event):
        """
          Purpose: clean-up after panning.
        """
        self.count = 0
        self.SetCursor(self.cursor)
        self.mc = False

    def toggleFS(self):
        """
         Purpose: toggle between fullscreen and previous size.
        """
        if self.fs:
            self.ShowFullScreen(False)
            self.fs = False
        else:
            self.ShowFullScreen(True)
            self.fs = True

##-------------------------------------------------------------------------------
app = wx.App(redirect = False)
frame = ImageFrame()
app.MainLoop()
