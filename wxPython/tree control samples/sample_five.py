# sample_five.py

"""

Author : Rahul Sabharwal
https://www.geeksforgeeks.org/wxpython-clearfocuseditem-method-in-wx-treectrl/?ref=rp

"""

import wx

# class MyTree
# class MyFrame
# class MyApp

#---------------------------------------------------------------------------
  
class MyTree(wx.Panel): 
  
    def __init__(self, parent): 
        wx.Panel.__init__(self, parent) 
  
        # create Tree Control in frame 
        self.tree = wx.TreeCtrl(self, wx.ID_ANY,
                                wx.DefaultPosition,
                                wx.DefaultSize,
                                wx.TR_HAS_BUTTONS) 
        self.tree.SetBackgroundColour('#fddef5')
        
        # Create root for Tree Control 
        self.root = self.tree.AddRoot('Root') 
  
        # Add item to root 
        item = self.tree.AppendItem(self.root, 'Item 1') 
        item = self.tree.AppendItem(self.root, 'Item 2')
        item = self.tree.AppendItem(self.root, 'Item 3') 
        item = self.tree.AppendItem(self.root, 'Item 4') 
        item = self.tree.AppendItem(self.root, 'Item 5') 
        item = self.tree.AppendItem(self.root, 'Item 6') 
        item = self.tree.AppendItem(self.root, 'Item 7')
        item = self.tree.AppendItem(self.root, 'Item 8') 
        
        # Clear focused item 
        self.tree.ClearFocusedItem() 
  
        # expand tree 
        self.tree.Expand(self.root) 

        #------------
        
        sizer = wx.BoxSizer(wx.VERTICAL) 
        sizer.Add(self.tree, 1, wx.EXPAND) 
        self.SetSizer(sizer) 

#---------------------------------------------------------------------------
        
class MyFrame(wx.Frame):
    """
    Main root frame for tree control.
    """
    def __init__(self, parent, id, title): 
        wx.Frame.__init__(self, parent, -1, title)  

        self.SetIcon(wx.Icon('./icons/wxwin.ico', wx.BITMAP_TYPE_ICO))

        #------------
        
        panel = MyTree(self) 

        #------------
        
        # Show frame 
        self.Show()
        
#---------------------------------------------------------------------------
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'wx.TreeCtrl (ClearFocusedItem)')
        frame.Show(True)
        self.SetTopWindow(frame)
        
        return True

#---------------------------------------------------------------------------
    
app = MyApp(0)
app.MainLoop()
