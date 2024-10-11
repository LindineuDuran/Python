# sample_three.py

"""

Author : Rahul Sabharwal
https://www.geeksforgeeks.org/wxpython-assignimagelist-method-in-wx-treectrl/?ref=rp

"""

import wx

# class MyFrame
# class MyApp

#---------------------------------------------------------------------------
  
class MyFrame(wx.Frame): 
    def __init__(self, parent, id, title): 
        wx.Frame.__init__(self, parent, -1, title) 

        self.SetIcon(wx.Icon('./icons/wxwin.ico', wx.BITMAP_TYPE_ICO))

        #------------
        
        # Tree control 
        self.tree = wx.TreeCtrl(self, wx.ID_ANY,
                                wx.DefaultPosition,
                                wx.DefaultSize) 
        self.tree.SetBackgroundColour('#f1f2f2')
        
        # Create imagelist 
        il = wx.ImageList(16, 16) 
  
        # Add images to image list 
        one = il.Add(wx.Image('./bitmaps/plus.png', wx.BITMAP_TYPE_PNG).Scale(16, 16).ConvertToBitmap()) 
        two = il.Add(wx.Image('./bitmaps/close.png').Scale(16, 16).ConvertToBitmap()) 
  
        # Asign image list to tree 
        self.tree.AssignImageList(il) 
  
        # Add a root node to tree 
        self.root = self.tree.AddRoot('Root ', 0) 
  
        # Add item to self.root 
        self.tree.AppendItem(self.root, 'Item 1', 1) 
        self.tree.AppendItem(self.root, 'Item 2', 1)  
        self.tree.AppendItem(self.root, 'Item 3', 1)  
        self.tree.AppendItem(self.root, 'Item 4', 1)  
        self.tree.AppendItem(self.root, 'Item 5', 1)  
        self.tree.AppendItem(self.root, 'Item 6', 1)  
        self.tree.AppendItem(self.root, 'Item 7', 1) 
        self.tree.AppendItem(self.root, 'Item 8', 1) 
        
        # Expand tree 
        self.tree.Expand(self.root) 

        #------------
        
        # Show frame 
        self.Show()
        
#---------------------------------------------------------------------------
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'wx.TreeCtrl (AssignImageList)')
        frame.Show(True)
        self.SetTopWindow(frame)
        
        return True

#---------------------------------------------------------------------------
    
app = MyApp(0)
app.MainLoop()
