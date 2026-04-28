import wx

class ImageService:

    def load(self, path):
        return wx.Image(path)

    def scale(self, img, factor):
        w = int(img.GetWidth() * factor)
        h = int(img.GetHeight() * factor)
        return img.Scale(w, h)

    def rotate(self, img, angle):
        center = wx.Point(img.GetWidth()//2, img.GetHeight()//2)
        return img.Rotate(angle, center)