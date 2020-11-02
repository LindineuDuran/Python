import plotly.offline as po
import plotly.offline as py
import plotly.graph_objs as go

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore, QtWidgets
import sys

import pandas as pd

# habilita o modo offline
from plotly.offline import plot, iplot
# plotly.offline>init_notebook_mode(connected=True)


df=pd.read_csv("PETR4.SA.csv")

def show_qt(fig):
    raw_html = '<html><head><meta charset="utf-8" />'
    raw_html += '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>'
    raw_html += '<body>'
    raw_html += po.plot(fig, include_plotlyjs=False, output_type='div')
    raw_html += '</body></html>'

    fig_view = QWebEngineView()
    # setHtml has a 2MB size limit, need to switch to setUrl on tmp file
    # for large figures.
    fig_view.setHtml(raw_html)
    fig_view.show()
    fig_view.raise_()
    return fig_view

Close = go.Scatter(
                    x=df.Date,
                    y=df.Close,
                    name="PETR4 High",
                    line=dict(color='#17BECF'),
                    opacity=0.8
                  )

trace = go.Candlestick(
                         x=df['Date'],
                         open=df['Open'],
                         high=df['High'],
                         low=df['Low'],
                         close=df['Close']
                       )

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    data = [trace]
    layout = dict(
                    title = "Série com Rangeslider e Botões",
                    title_x = 0.5,
                    xaxis = dict(
                                   rangeselector = dict(
                                                         buttons = list([
                                                                          dict(
                                                                                count = 1,
                                                                                label = '1m',
                                                                                step = 'month',
                                                                                stepmode = 'backward'
                                                                              ),
                                                                           dict(
                                                                                count = 6,
                                                                                label = '6m',
                                                                                step = 'month',
                                                                                stepmode = 'backward'
                                                                              ),
                                                                           dict(
                                                                                step = 'all'
                                                                              )
                                                                       ])
                                                       ),
                                  rangeslider = dict(visible = True),
                                  type = 'date'
                                )
                 )
    fig = go.Figure(data, layout = layout)
    fig_view = show_qt(fig)
    sys.exit(app.exec_())
