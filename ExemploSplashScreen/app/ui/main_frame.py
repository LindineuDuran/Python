
import wx
from app.ui.components.progress_bar import ProgressBar
from app.ui.panels.preview_panel import PreviewPanel

class FileDrop(wx.FileDropTarget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    def OnDropFiles(self,x,y,files):
        for f in files:
            if f.endswith(".pdf"):
                self.callback(f)

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None,title="PDF OCR PRO V2",size=(800,600))
        panel=wx.Panel(self)
        vbox=wx.BoxSizer(wx.VERTICAL)

        self.preview=PreviewPanel(panel)
        self.progress=ProgressBar(panel)
        btn=wx.Button(panel,label="Selecionar PDF")

        vbox.Add(self.preview,1,wx.EXPAND|wx.ALL,10)
        vbox.Add(self.progress,0,wx.EXPAND|wx.ALL,10)
        vbox.Add(btn,0,wx.CENTER|wx.ALL,10)

        panel.SetSizer(vbox)
        panel.SetDropTarget(FileDrop(self.process))

        btn.Bind(wx.EVT_BUTTON,self.select)

    def set_controller(self,c): self.controller=c

    def select(self,e):
        with wx.FileDialog(self,"PDF",wildcard="*.pdf") as dlg:
            if dlg.ShowModal()==wx.ID_OK:
                self.process(dlg.GetPath())

    def process(self,path):
        self.controller.process_pdf(path)

    def update_progress(self,val):
        wx.CallAfter(self.progress.SetValue,val)

    def show_preview(self,path):
        wx.CallAfter(self.preview.show_image,path)

    def on_complete(self):
        wx.CallAfter(wx.MessageBox,"Concluído")
