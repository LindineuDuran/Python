import wx
from ExtractorFrame import ExtractorFrame
# from ExtractorTextoCompletoFrame import ExtractorTextoCompletoFrame

class main(wx.App):
    def OnInit(self):
        frm = ExtractorFrame(parent=None, id=-1, title='Pdf Extractor')
        # frm = ExtractorTextoCompletoFrame(parent=None, id=-1, title='Pdf Extractor')
        frm.Show()
        return True

app = main()
app.MainLoop()