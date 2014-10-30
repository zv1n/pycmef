import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

from pycmef.utils.page import EnhancedPage

"""
  Based on Window class from:
    http://agateau.com/2012/pyqtwebkit-experiments-part-2-debugging/
  Allows for F12 debugging of JS/HTML/CSS.
"""
class EnhancedBrowser(QWidget):
  def __init__(self):
    super(EnhancedBrowser, self).__init__()
    self.view = QWebView(self)
    self.view.setPage(EnhancedPage())
    for f in self.view.actions():
      print f

    self.setupInspector()

    self.splitter = QSplitter(self)
    self.splitter.setOrientation(Qt.Vertical)

    layout = QVBoxLayout(self)
    layout.setMargin(0)
    layout.addWidget(self.splitter)

    self.splitter.addWidget(self.view)
    self.splitter.addWidget(self.webInspector)

  def load(self, page):
    self.view.load(page)

  def setJsObject(self, name, obj):
    self.view.page().mainFrame().addToJavaScriptWindowObject(name, obj)

  def setupInspector(self):
    page = self.view.page()
    page.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
    self.webInspector = QWebInspector(self)
    self.webInspector.setPage(page)

    shortcut = QShortcut(self)
    shortcut.setKey(Qt.Key_F12)
    shortcut.activated.connect(self.toggleInspector)
    self.webInspector.setVisible(False)

  def toggleInspector(self):
    self.webInspector.setVisible(not self.webInspector.isVisible())
