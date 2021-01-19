# Add check box to frame : CheckBox « wxPython « Python Tutorial
# http://www.java2s.com/Tutorial/Python/0380__wxPython/Addcheckboxtoframe.htm
import wx

class CheckBoxFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Checkbox Example', size=(150, 200))
        panel = wx.Panel(self, -1)
        wx.CheckBox(panel, -1, "A", (35, 40), (150, 20))
        wx.CheckBox(panel, -1, "B", (35, 60), (150, 20))
        wx.CheckBox(panel, -1, "C", (35, 80), (150, 20))

app = wx.App()
CheckBoxFrame().Show()
app.MainLoop()
