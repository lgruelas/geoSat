#! /usr/bin/python
# -*- coding: utf-8 -*-

#Copyright (C) 2015  Luis Germán Ruelas Luna gruelas@cieco.unam.mx

#This file is part or GeoSat Viewer

#GeoSat Viewer is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import time

class miGrafica(pg.GraphicsLayout):
    def __init__(self,border=(100,100,100), parent=None):
        pg.graphicsItems.GraphicsLayout.GraphicsLayout.__init__(self, parent)
        self.l2 = self.addLayout(colspan=3, border=(50,0,0))
        self.l2.setContentsMargins(10, 10, 10, 10)
        self.l2.addLabel("GeoSat", colspan=3)
        self.l2.nextRow()
        self.l2.addLabel('Temperatura', angle=-90, rowspan=1)
        self.ptemp = self.l2.addPlot()
        self.ptemp.setContentsMargins(10, 10, 10, 10)
        self.ptemp.setYRange(0,50)
        self.l2.nextRow()
        self.l2.addLabel(u'Presión', angle=-90, rowspan=1)
        self.ppre = self.l2.addPlot()
        self.ppre.setContentsMargins(10,10,10,10)
        self.ppre.setYRange(0,50)
        self.l2.nextRow()
        self.l2.addLabel('Altitud', angle=-90, rowspan=1)
        self.palt = self.l2.addPlot()
        self.palt.setContentsMargins(10,10,10,10)
        self.palt.setYRange(0,50)
        self.a = time.time()

        # Share the bottom axis
        #self.ptemp.hideAxis('bottom')
        self.ptemp.hideButtons()
        self.ppre.hideButtons()
        self.palt.hideButtons()
        self.ptemp.enableAutoRange(enable=True)
        self.palt.enableAutoRange(enable=True)
        self.ppre.enableAutoRange(enable=True)
        self.ppre.showGrid(x=True ,y=True)
        self.palt.showGrid(x=True ,y=True)
        self.ptemp.showGrid(x=True ,y=True)
        #self.ppre.hideAxis('bottom')
    
        self.x_list = [time.time()-self.a]
    def update(self, temperatura, presion, altitud):
        pent = pg.mkPen(color=0, width=2)
        penp = pg.mkPen(color=3, width=2)
        pena = pg.mkPen(color='b', width=2)
        self.x_list.append(time.time()-self.a)
        self.ptemp.plot(x = self.x_list, y = temperatura, clear=True, pen=pent)
        self.ppre.plot(x = self.x_list, y = presion, clear=True, pen=penp)
        self.palt.plot(x = self.x_list, y = altitud, clear=True, pen=pena)
        #QtGui.QApplication.processEvents()