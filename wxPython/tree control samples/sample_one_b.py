# Sample_one_b.py

"""

Author : Adil Hasan
https://wiki.wxpython.org/AnotherTutorialTreeCtrlComment

"""

import wx

# class MyTree
# class MyFrame
# class MyApp

#---------------------------------------------------------------------------

class MyTree(wx.TreeCtrl):
    """
    Our customized TreeCtrl class.
    """
    def __init__(self, parent, id, position, size, style):
        """
        Initialize our tree.
        """
        wx.TreeCtrl.__init__(self, parent, id, position, size, style)
       
        root = self.AddRoot('Programmer')
        
        os = self.AppendItem(root, 'Operating Systems')
        pl = self.AppendItem(root, 'Programming Languages')
        tk = self.AppendItem(root, 'Toolkits')
           
        cl = self.AppendItem(pl, 'Compiled languages')
        sl = self.AppendItem(pl, 'Scripting languages')

        self.AppendItem(os, 'Linux')
        self.AppendItem(os, 'FreeBSD')
        self.AppendItem(os, 'OpenBSD')
        self.AppendItem(os, 'NetBSD')
        self.AppendItem(os, 'Solaris')        
        self.AppendItem(cl, 'Java')
        self.AppendItem(cl, 'C++')
        self.AppendItem(cl, 'C')
        self.AppendItem(cl, 'Pascal')
        self.AppendItem(sl, 'Python')
        self.AppendItem(sl, 'Ruby')
        self.AppendItem(sl, 'Tcl')
        self.AppendItem(sl, 'PHP')
        self.AppendItem(tk, 'Qt')
        self.AppendItem(tk, 'MFC')
        self.AppendItem(tk, 'wxPython')
        self.AppendItem(tk, 'GTK+')
        self.AppendItem(tk, 'Swing')

#---------------------------------------------------------------------------
        
class MyFrame(wx.Frame):
    """
    Our customized window class.
    """
    def __init__(self, parent, id, title):
        """
        Initialize our window.
        """
        wx.Frame.__init__(self, parent, id, title,
                          wx.DefaultPosition, wx.Size(500, 480))

        self.SetIcon(wx.Icon('./icons/wxwin.ico', wx.BITMAP_TYPE_ICO))

        #------------
        
        # Create a splitter window.
        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE)
        
        # Create the left panel.
        leftPanel = wx.Panel(self.splitter, -1)
        
        # Create our tree and put it into the left panel.
        self.tree = MyTree(leftPanel, 1,
                           wx.DefaultPosition,
                           wx.DefaultSize,
                           wx.TR_HIDE_ROOT |
                           wx.TR_HAS_BUTTONS)
        self.tree.SetBackgroundColour('#d8f0d4')

        # Bind the OnSelChanged method to the tree.
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)

        # Create the right panel.
        rightPanel = wx.Panel(self.splitter, -1, style=wx.SUNKEN_BORDER)
        rightPanel.SetBackgroundColour('#f0d4e9')
        
        # Create a widget to display static text 
        # and store it in the right panel.
        self.display = wx.StaticText(rightPanel, -1, '',
                                     style=wx.ALIGN_LEFT)
        
        # Put the left and right panes into the split window.
        self.splitter.SplitVertically(leftPanel, rightPanel, 200)

        # Minimum size of subwindow.
        self.splitter.SetMinimumPaneSize(1)         

        #------------

        # Create a box sizer that will contain the left panel contents.
        leftBox = wx.BoxSizer(wx.VERTICAL)
        
        # Add the tree to the box sizer.
        leftBox.Add(self.tree, 1, wx.EXPAND)
        
        # Set the size of the right panel to that required by the tree.
        leftPanel.SetSizer(leftBox)
        
        # Create the right box sizer that will contain the panel's contents.
        rightBox = wx.BoxSizer(wx.VERTICAL)
        
        # Add the display widget to the right panel.
        rightBox.Add(self.display, 0, wx.ALL, 10)

        # Set the size of the right panel to that 
        # required by the display widget.
        rightPanel.SetSizer(rightBox)
        
        #------------
        
        # Create the window in the centre of the screen.
        self.Centre()

    #-----------------------------------------------------------------------
        
    def OnSelChanged(self, event):
        """
        Method called when selected item is changed.
        """
        
        # Get the selected item object.
        item =  event.GetItem()
        
        # Display the selected item text in the text widget.
        self.display.SetLabel(self.tree.GetItemText(item))

#---------------------------------------------------------------------------
        
class MyApp(wx.App):
    """
    Our application class.
    """
    def OnInit(self):
        """
        Initialize by creating the split window with the tree.
        """
        
        frame = MyFrame(None, -1, 'wx.TreeCtrl (wx.SplitterWindow)')
        frame.Show(True)
        self.SetTopWindow(frame)
        
        return True

#---------------------------------------------------------------------------
    
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
