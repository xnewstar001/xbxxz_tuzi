# uncompyle6 version 3.9.3
# -*- coding: utf-8 -*-
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.13.15 (tags/v3.13.15:4061bc4, Aug  5 2026, 13:05:39) [MSC v.1944 64 bit (AMD64)]
# Embedded file name: browser.py
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class BrowserDialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8('Dialog'))
        Dialog.resize(1024, 768)
        self.qwebview = QWebView(Dialog)
        self.qwebview.setGeometry(QtCore.QRect(0, 50, 1020, 711))
        self.qwebview.setObjectName(_fromUtf8('kwebview'))
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 20, 1000, 25))
        self.lineEdit.setObjectName(_fromUtf8('lineEdit'))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        return

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate('Browser', 'Browser', None))
        return
