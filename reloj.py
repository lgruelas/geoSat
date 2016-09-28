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

from PySide import QtCore, QtGui, QtSql

class RelojDigital(QtGui.QLCDNumber):
    
    def __init__(self, parent=None, utc = False):
        
        QtGui.QLCDNumber.__init__(self, parent)
        self.setDigitCount(8)
        self.utc = utc

    @QtCore.Slot()
    def showTime(self):
        #Show Current Time in "hh:mm:ss" format
        if self.utc:
            self.display(QtCore.QDateTime.currentDateTime().toTimeSpec(QtCore.Qt.UTC).time().toString(("hh:mm:ss")))
        else:
            self.display(QtCore.QTime.currentTime().toString(("hh:mm:ss")))
    
    def setUtc(self, value):
        self.utc = value
    
    def isUtc(self):
        return self.utc
    
class RelojUltimaCaida(QtGui.QLCDNumber):
    
    def __init__(self, parent=None, utc = False):
        
        QtGui.QLCDNumber.__init__(self, parent)
        self.setDigitCount(8)
        
    def actualizar_hora(self,hora):
        hora = hora.split(':')
        self.display(hora[1]+':'+hora[2][:-3])
        
class RelojDatosPorSegundo(QtGui.QLCDNumber):
    def __init__(self, parent=None, utc = False):
        QtGui.QLCDNumber.__init__(self, parent)
        self.setDigitCount(8)
        self.lenUltimos = 0
        self.lenPasados = 0
        
    def setLenNuevosDatos(self, nuevos):
        self.lenUltimos=nuevos
        
    @QtCore.Slot()
    def showTime(self):
        self.display(self.lenUltimos - self.lenPasados)
        self.lenPasados = self.lenUltimos
        
class RelojExtremo(QtGui.QLCDNumber):
    def __init__(self, parent=None):
        QtGui.QLCDNumber.__init__(self, parent)
        self.setDigitCount(8)
        self.anterior = 0
        self.modify = False
        
    def setAnterior(self, nuevo):
        self.anterior = nuevo
        
    def getAnterior(self):
        return self.anterior
    
    def changeModify(self):
        self.modify=True
        
    def getModify(self):
        return self.modify
        
    def actualizar(self):
        self.display(self.anterior)