# Sample_one_a.py

"""

Author : Jan Bodnar
Website : zetcode.com

"""

import wx

# class MyFrame
# class MyApp

#---------------------------------------------------------------------------

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,
                          wx.DefaultPosition, wx.Size(500, 480))

        self.SetIcon(wx.Icon('./icons/wxwin.ico', wx.BITMAP_TYPE_ICO))

        #------------
        
        panel1 = wx.Panel(self, -1, style=wx.WANTS_CHARS)
        panel2 = wx.Panel(self, -1, style=wx.WANTS_CHARS)
        panel2.SetBackgroundColour('#c4c4c4')
        
        #------------
        
        self.tree = wx.TreeCtrl(panel1, 1,
                                wx.DefaultPosition,
                                wx.DefaultSize,
                                wx.TR_HIDE_ROOT |
                                wx.TR_HAS_BUTTONS)
        self.tree.SetBackgroundColour('#cce8ff')
        
        root = self.tree.AddRoot('Programmer')
        
        os = self.tree.AppendItem(root, 'Operating Systems')
        pl = self.tree.AppendItem(root, 'Programming Languages')
        tk = self.tree.AppendItem(root, 'Toolkits')

        cl = self.tree.AppendItem(pl, 'Compiled languages')
        sl = self.tree.AppendItem(pl, 'Scripting languages')

        self.tree.AppendItem(os, 'Linux')
        self.tree.AppendItem(os, 'FreeBSD')
        self.tree.AppendItem(os, 'OpenBSD')
        self.tree.AppendItem(os, 'NetBSD')
        self.tree.AppendItem(os, 'Solaris')
        self.tree.AppendItem(cl, 'Java')
        self.tree.AppendItem(cl, 'C++')
        self.tree.AppendItem(cl, 'C')
        self.tree.AppendItem(cl, 'Pascal')
        self.tree.AppendItem(sl, 'Python')
        self.tree.AppendItem(sl, 'Ruby')
        self.tree.AppendItem(sl, 'Tcl')
        self.tree.AppendItem(sl, 'PHP')
        self.tree.AppendItem(tk, 'Qt')
        self.tree.AppendItem(tk, 'MFC')
        self.tree.AppendItem(tk, 'wxPython')
        self.tree.AppendItem(tk, 'GTK+')
        self.tree.AppendItem(tk, 'Swing')

        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
        #------------
        
        self.display = wx.StaticText(panel2, -1, '', (10, 10), style=wx.ALIGN_CENTRE)

        #------------
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        vbox.Add(self.tree, 1, wx.EXPAND)

        hbox.Add(panel1, 1, wx.EXPAND)
        hbox.Add(panel2, 1, wx.EXPAND)

        panel1.SetSizer(vbox)
        self.SetSizer(hbox)

        #------------
        
        self.Centre()

    #-----------------------------------------------------------------------

    def OnSelChanged(self, event):
        self.item = event.GetItem()
        self.display.SetLabel(self.tree.GetItemText(self.item))
        self.tree.GetItemText(self.item)

        event.Skip()
        

    def OnCloseWindow(self, event):
        self.Destroy()
        
#---------------------------------------------------------------------------

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'wx.TreeCtrl (wx.Panel)')
        frame.Show(True)
        self.SetTopWindow(frame)
        
        return True

#---------------------------------------------------------------------------

if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()

