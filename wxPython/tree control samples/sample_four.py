# sample_four.py

"""

Author : Rahul Sabharwal
https://www.geeksforgeeks.org/wxpython-collapse-method-wx-treectrl/?ref=rp

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
  
        # Create tree control 
        self.tree = MyTree(self, wx.ID_ANY,
                           wx.DefaultPosition,
                           wx.DefaultSize,
                           wx.TR_HAS_BUTTONS) 
        self.tree.SetBackgroundColour('#f8f094')
        
        # Add root to self.tree 
        self.root = self.tree.AddRoot('Root') 

        # Add item to self.root 
        item = self.tree.AppendItem(self.root, 'Item 1') 
        item = self.tree.AppendItem(self.root, 'Item 2')
        item = self.tree.AppendItem(self.root, 'Item 3') 
        item = self.tree.AppendItem(self.root, 'Item 4') 
        item = self.tree.AppendItem(self.root, 'Item 5')
        item = self.tree.AppendItem(self.root, 'Item 6') 
        item = self.tree.AppendItem(self.root, 'Item 7')         
        item = self.tree.AppendItem(self.root, 'Item 8')

        # Expand whole tree 
        self.tree.Expand(self.root)
        
        #------------
        
        # Add button in panel 
        self.btn = wx.Button(self, 1, "&Collapse")
        
        # Bind event with self.btn 
        self.btn.Bind(wx.EVT_BUTTON, self.OnClick) 

        #------------
        
        sizer = wx.BoxSizer(wx.VERTICAL) 
        sizer.Add(self.tree, 1, wx.EXPAND) 
        sizer.Add(self.btn, 0, wx.EXPAND) 
        self.SetSizer(sizer) 

    #-----------------------------------------------------------------------  

    def OnClick(self, event): 
        # Collapse root 
        self.tree.Collapse(self.root) 

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
        frame = MyFrame(None, -1, 'wx.TreeCtrl (Collapse)')
        frame.Show(True)
        self.SetTopWindow(frame)
        
        return True

#---------------------------------------------------------------------------
    
app = MyApp(0)
app.MainLoop()
