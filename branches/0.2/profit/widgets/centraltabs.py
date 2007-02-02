#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2007 Troy Melhase
# Distributed under the terms of the GNU General Public License v2
# Author: Troy Melhase <troy@gci.net>

from PyQt4.QtGui import QTabWidget, QWidget

from profit.lib import Signals
from profit.widgets.brokerwidget import BrokerWidget
from profit.widgets.tickerdisplay import TickerDisplay


class CentralTabs(QTabWidget):
    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)
        self.connect(self.window(), Signals.sessionItemClicked,
                     self.on_sessionItemClicked)
        self.brokerTab = None
        self.session = None
        self.connect(self.window(), Signals.sessionCreated, self.on_sessionCreated)

    def on_sessionCreated(self, session):
        self.session = session
    
    def on_sessionItemClicked(self, item, col):
        value = str(item.text(0))
        call = getattr(self, 'on_session%sClicked' % value.capitalize(), None)
        if call:
            call(item)
        

    def on_sessionAccountClicked(self, item):
        pass

    def on_sessionTickersClicked(self, item):
        idx = self.addTab(TickerDisplay(self.session, self), item.text(0))
        self.setCurrentIndex(idx)
        
    def on_sessionBrokerClicked(self, item):
        if not self.brokerTab:
            self.brokerTab = BrokerWidget(self.session, self)
            self.addTab(self.brokerTab, item.text(0))
        self.setCurrentWidget(self.brokerTab)