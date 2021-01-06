import wx
import wx.lib.scrolledpanel

class CheckBoxPanel(wx.lib.scrolledpanel.ScrolledPanel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent, sizePanel, posPanel):
        """Constructor"""
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, size=sizePanel, pos=posPanel, style=wx.SIMPLE_BORDER)
        self.number_of_buttons = 0
        self.text_list = list()
        self.process_list = list()
        self.frame = parent

        self.widgetSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.widgetSizer)

    #----------------------------------------------------------------------
    def setTextList(self, text_list):
        self.text_list = text_list

    #----------------------------------------------------------------------
    def getTextList(self):
        return self.text_list

    #----------------------------------------------------------------------
    def setProcessList(self, process_list):
        self.process_list = process_list

    #----------------------------------------------------------------------
    def getProcessList(self):
        return self.process_list

    #----------------------------------------------------------------------
    def createCheckBoxesList(self):
        """"""
        if self.number_of_buttons > 0: self.destroyCheckBoxesList()

        chkAll = wx.CheckBox(self, label='Selecionar todos', name='chkAll', pos=(10, 10))
        chkAll.Bind(wx.EVT_CHECKBOX, self.changeState)
        self.widgetSizer.Add(chkAll, 0, wx.ALL, 5)

        pos_y = 20
        for item in self.text_list:
                self.addWidget(item, pos_y)
                pos_y += 20

    #----------------------------------------------------------------------
    def addWidget(self, texto, pos_y):
        """"""
        self.number_of_buttons += 1
        name = "chk%s" % self.number_of_buttons
        cb = wx.CheckBox(self, label=texto, name=name, pos=(10, pos_y))
        cb.Bind(wx.EVT_CHECKBOX, self.update)
        self.widgetSizer.Add(cb, 0, wx.ALL, 5)

    #----------------------------------------------------------------------
    def changeState(self, e):
        """"""
        sender = e.GetEventObject()
        isChecked = sender.GetValue()
        nome = sender.GetLabel()

        if isChecked:
            # print('Insere item: ', nome)
            children = self.widgetSizer.GetChildren()
            for child in children:
                widget = child.GetWindow()

                if(widget.GetName() != 'chkAll' and widget.GetValue() == False):
                    # print('Nome:', widget.GetName(), '- Texto:', widget.GetLabel(), '- State:', widget.GetValue())
                    widget.SetValue(True)
                    self.process_list.append( widget.GetLabel())
        else:
            # print('Remolve item: ', nome)
            children = self.widgetSizer.GetChildren()
            for child in children:
                widget = child.GetWindow()

                if(widget.GetName() != 'chkAll' and widget.GetValue() == True):
                    # print('Nome:', widget.GetName(), '- Texto:', widget.GetLabel(), '- State:', widget.GetValue())
                    widget.SetValue(False)
                    if widget.GetLabel() in self.process_list: self.process_list.remove(widget.GetLabel())

        # print(self.process_list)

    #----------------------------------------------------------------------
    def update(self, e):
        """"""
        sender = e.GetEventObject()
        isChecked = sender.GetValue()
        nome = sender.GetLabel()

        if isChecked:
            # print('Insere item: ', nome)
            self.process_list.append(nome)
        else:
            # print('Remolve item: ', nome)
            if nome in self.process_list: self.process_list.remove(nome)

    #----------------------------------------------------------------------
    def destroyCheckBoxesList(self):
        """"""
        while(self.number_of_buttons > 0):
            self.removeWidget()

        if self.widgetSizer.GetChildren():
            self.widgetSizer.Hide(0)
            self.widgetSizer.Remove(0)

    #----------------------------------------------------------------------
    def removeWidget(self):
        """"""
        if self.widgetSizer.GetChildren():
            self.widgetSizer.Hide(self.number_of_buttons-1)
            self.widgetSizer.Remove(self.number_of_buttons-1)
            self.number_of_buttons -= 1
