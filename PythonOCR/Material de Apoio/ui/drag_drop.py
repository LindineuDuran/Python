import wx
import os

class FileDropTarget(wx.FileDropTarget):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def OnDropFiles(self, x, y, files):
        self.callback(files)
        return True