# sample_six.py

"""

Author : Rahul Sabharwal
https://www.geeksforgeeks.org/wxpython-collapseallchildren-method-in-wx-treectrl/?ref=rp

"""

import wx

# class MyTree
# class MyTreePanel
# class MyFrame
# class MyApp

#---------------------------------------------------------------------------
  
class MyTree(wx.TreeCtrl): 
    def __init__(self, parent, id, pos, size, style): 
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style) 
  
#---------------------------------------------------------------------------
        
class MyTreePanel(wx.Panel):  
    def __init__(self, parent): 
        wx.Panel.__init__(self, parent) 
  
        # Create Tree Control 
        self.tree = MyTree(self, wx.ID_ANY,
                           wx.DefaultPosition,
                           wx.DefaultSize,
                           wx.TR_HAS_BUTTONS) 
        self.tree.SetForegroundColour('#ffffff')
        self.tree.SetBackgroundColour('#000000')
        
        # Add root to Tree Control 
        self.root = self.tree.AddRoot('Root') 
  
        # Add item to root 
        self.itm = self.tree.AppendItem(self.root, 'Item') 
  
        # Add item to 'itm' 
        self.itm2 = self.tree.AppendItem(self.itm, "Sub Item") 
  
        # Add child item to itm2 
        self.itm3 = self.tree.AppendItem(self.itm2, "Another Item") 
        self.itm4 = self.tree.AppendItem(self.itm2, "Another Item")
        self.itm5 = self.tree.AppendItem(self.itm2, "Another Item") 
        self.itm6 = self.tree.AppendItem(self.itm2, "Another Item")
        self.itm7 = self.tree.AppendItem(self.itm2, "Another Item")
        self.itm8 = self.tree.AppendItem(self.itm2, "Another Item") 
        self.itm9 = self.tree.AppendItem(self.itm2, "Another Item")
        
        # Expand whole tree 
        self.tree.Expand(self.root) 

        #------------
        
        # Add button in frame 
        self.btn = wx.Button(self, 1, "Collapse") 

        # Bind event function with button 
        self.btn.Bind(wx.EVT_BUTTON, self.OnClick) 
        
        #------------
        
        sizer = wx.BoxSizer(wx.VERTICAL) 
        sizer.Add(self.tree, 1, wx.EXPAND) 
        sizer.Add(self.btn, 0, wx.EXPAND)
        self.SetSizer(sizer) 
  
    #-----------------------------------------------------------------------
  
    def OnClick(self, event): 
        # Collapse all children of itm recursively 
        self.tree.CollapseAllChildren(self.itm) 

#---------------------------------------------------------------------------
        
class MyFrame(wx.Frame):
    def __init__(self, parent, id, title): 
        wx.Frame.__init__(self, parent, -1, title)  

        self.SetIcon(wx.Icon('./icons/wxwin.ico', wx.BITMAP_TYPE_ICO))

        #------------
        
        panel = MyTreePanel(self) 

        #------------
        
        # Show frame 
        self.Show()
        
#---------------------------------------------------------------------------
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'wx.TreeCtrl (CollapseAllChildren)')
        frame.Show(True)
        self.SetTopWindow(frame)
        
        return True

#---------------------------------------------------------------------------
    
app = MyApp(0)
app.MainLoop()
