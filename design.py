# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designcnClDI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.16
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(779, 535)
        Form.setAutoFillBackground(False)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.functionList = QListWidget(Form)
        self.functionList.setObjectName(u"functionList")

        self.horizontalLayout.addWidget(self.functionList)

        self.outputText = QTextEdit(Form)
        self.outputText.setObjectName(u"outputText")
        self.outputText.setReadOnly(True)

        self.horizontalLayout.addWidget(self.outputText)

        self.sourceText = QTextEdit(Form)
        self.sourceText.setObjectName(u"sourceText")
        self.sourceText.setReadOnly(True)

        self.horizontalLayout.addWidget(self.sourceText)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi