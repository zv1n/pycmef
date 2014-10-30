import logging

from PyQt4.QtWebKit import *

class EnhancedPage(QWebPage):
  """
  Makes it possible to use a Python logger to print javascript console messages
  """
  def __init__(self, logger=None, parent=None):
    super(EnhancedPage, self).__init__(parent)
    if not logger:
      logger = logging
    self.logger = logger

  def javaScriptConsoleMessage(self, msg, lineNumber, sourceID):
    self.logger.warning("JsConsole(%s:%d): %s" % (sourceID, lineNumber, msg))