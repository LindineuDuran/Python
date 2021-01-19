import os
import wx
import time
from threading import *

# Define Buttons
ID_START = 100
ID_STOP = 101

# Define notification event for thread completion
EVT_RESULT_ID = 100


def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)


class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""

    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data


class ThreadTest(Thread):
    def __init__(self, main_window):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self._main_window = main_window
        self.want_abort = 0
        self.start()

    def run(self):
        self._main_window.pg_bar.SetValue(0)
        for k in range(10, 110, 10):
            if self.want_abort:
                # Use a result of None to acknowledge the abort
                wx.PostEvent(self._main_window, ResultEvent(None))
                return

            self._main_window.pg_bar.SetValue(k)
            print(k)
            wx.Yield()
            time.sleep(1)
        wx.PostEvent(self._main_window, ResultEvent(1))

    def abort(self):
        """abort worker thread."""
        # Method for use by main thread to signal an abort
        self.want_abort = 1


class CopierFrame(wx.Frame):
    def __init__(self, parent):
        # Define the main Frame
        wx.Frame.__init__(self, parent, wx.ID_ANY, "Gauge Test", size=(600, 400),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetBackgroundColour(wx.WHITE)

        self.pg_bar = wx.Gauge(self, wx.ID_ANY, 100, (10, 10), (550, 15))

        btn = wx.Button(self, ID_START, "Push Me", (10, 30))
        btn2 = wx.Button(self, ID_STOP, "Stop", (250, 30))
        btn.Bind(wx.EVT_BUTTON, self.start_copy, id=ID_START)
        btn2.Bind(wx.EVT_BUTTON, self.stop_copy, id=ID_STOP)

        # Set up event handler for any worker thread results
        EVT_RESULT(self, self.on_result)

        # No threads at start
        self.thread = None

    def start_copy(self, event):
        if not self.thread:
            self.thread = ThreadTest(self)

    def stop_copy(self, event):
        """Stop any task."""
        # Flag the worker thread to stop if running
        if self.thread:
            self.thread.abort()

    def on_result(self, event):
        if event.data is None:
            # Thread aborted (using our convention of None return)
            print("Aborted")
        else:
            print("Finished")
        # In either event, the worker is done
        self.thread = None


class main(wx.App):

    def OnInit(self):
        frm = CopierFrame(None)
        frm.Show()
        return True


app = main()
app.MainLoop()
