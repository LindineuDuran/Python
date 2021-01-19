import random
import wx

########################################################################
class MyPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        self.username = wx.StaticText(self, label="username")
        self.online_status = wx.StaticText(self, label="offline")
        self.dialing_status = wx.StaticText(self, label="no dial tone")

        btn = wx.Button(self, label="Update")
        btn.Bind(wx.EVT_BUTTON, self.onUpdate)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.username, 0, wx.ALL, 5)
        sizer.Add(self.online_status, 0, wx.ALL, 5)
        sizer.Add(self.dialing_status, 0, wx.ALL, 5)
        sizer.Add(btn, 0, wx.ALL, 5)
        self.SetSizer(sizer)

    #----------------------------------------------------------------------
    def update_text(self, info):
        """"""
        index = {
            "username":self.username,
            "online status":self.online_status,
            "dial status":self.dialing_status
            }
        text = index[info[0]]
        data = info[1]
        append = info[2]
        if append:
            current = text.GetLabel()
            text.SetLabel(current + " " + data)
        else:
            text.SetLabel(data)

    #----------------------------------------------------------------------
    def onUpdate(self, event):
        """"""
        info = random.choice(
            [("username", "mork89", 1),
             ("online status", "online", 0),
             ("dial status", "dialing", 1)
             ])
        self.update_text(info)

########################################################################
class MainFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Dynamic StaticText")
        panel = MyPanel(self)
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
