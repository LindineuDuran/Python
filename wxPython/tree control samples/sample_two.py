# sample_two.py

"""

Author : Rahul Sabharwal
https://www.geeksforgeeks.org/wxpython-treectrl/

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
        self.tree.SetBackgroundColour('#d9f3fa')
        
        # Add root to tree 
        self.root = self.tree.AddRoot('Root ')
        
        # Add item to root 
        self.tree.AppendItem(self.root, 'Child 1') 
        self.tree.AppendItem(self.root, 'Child 2') 
        self.tree.AppendItem(self.root, 'Child 3') 
        self.tree.AppendItem(self.root, 'Child 4') 
        self.tree.AppendItem(self.root, 'Child 5') 
        self.tree.AppendItem(self.root, 'Child 6') 
        self.tree.AppendItem(self.root, 'Child 7') 
        self.tree.AppendItem(self.root, 'Child 8')
        
        # Expand tree 
        self.tree.Expand(self.root) 

        #------------
        
        # Show frame 
        self.Show() 
  
#---------------------------------------------------------------------------
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'wx.TreeCtrl')
        frame.Show(True)
        self.SetTopWindow(frame)
        
        return True

#---------------------------------------------------------------------------
    
app = MyApp(0)
app.MainLoop()
