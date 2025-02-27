#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.1.0a2 on Sun Mar 31 13:41:39 2024
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((846, 430))
        self.SetTitle("frame")

        # Menu Bar
        self.pyrequest_menubar = wx.MenuBar()
        self.SetMenuBar(self.pyrequest_menubar)
        # Menu Bar end

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.window_1 = wx.SplitterWindow(self.panel_1, wx.ID_ANY)
        self.window_1.SetMinimumPaneSize(20)
        sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)

        self.window_1_pane_1 = wx.Panel(self.window_1, wx.ID_ANY)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        self.tree_ctrl_1 = wx.TreeCtrl(self.window_1_pane_1, wx.ID_ANY, style=wx.BORDER_SUNKEN | wx.TR_HAS_BUTTONS | wx.TR_NO_BUTTONS | wx.TR_SINGLE)
        sizer_2.Add(self.tree_ctrl_1, 1, wx.EXPAND, 0)

        self.window_1_pane_2 = wx.Panel(self.window_1, wx.ID_ANY)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)

        self.window_2 = wx.SplitterWindow(self.window_1_pane_2, wx.ID_ANY)
        self.window_2.SetMinimumPaneSize(20)
        sizer_3.Add(self.window_2, 1, wx.EXPAND, 0)

        self.window_2_pane_1 = wx.Panel(self.window_2, wx.ID_ANY)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)

        self.combo_box_1 = wx.ComboBox(self.window_2_pane_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        sizer_4.Add(self.combo_box_1, 0, 0, 0)

        self.window_2_pane_2 = wx.Panel(self.window_2, wx.ID_ANY)

        self.window_2_pane_1.SetSizer(sizer_4)

        self.window_2.SplitVertically(self.window_2_pane_1, self.window_2_pane_2)

        self.window_1_pane_2.SetSizer(sizer_3)

        self.window_1_pane_1.SetSizer(sizer_2)

        self.window_1.SplitVertically(self.window_1_pane_1, self.window_1_pane_2)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        # end wxGlade

# end of class MyFrame

class MyApp(wx.App):
    def OnInit(self):
        self.pyrequest = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.pyrequest)
        self.pyrequest.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
