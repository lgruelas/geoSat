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

import datetime
import MySQLdb as mariadb
from PySide import QtCore, QtGui, QtSql

class Datos:
    
    def __init__(self):
        self.temperatura = []
        self.presion = []
        self.altitud = []
        self.contador = 1

    def ingresarDatos(self, temp, pre, alt):
        self.temperatura.append(temp)
        self.presion.append(pre)
        self.altitud.append(alt)
    
    def guardarEnArchivo(self, hora_recibido, nombre='salida.txt'):
        archivo = open(nombre, 'a')
        archivo.write('Altura: %f\tTemperatura: %f\t Presion: %f\t Fecha: %s\t Hora: %s\n' % (self.altitud[-1], self.temperatura[-1], self.presion[-1], str(datetime.datetime.utcnow().date()), hora_recibido))
        archivo.close()
        
    def ingresarBaseDatos(self, hora_recibido):
        self.DB_HOST = 'localhost' 
        self.DB_USER = 'root' 
        self.DB_PASS = ''
        self.DB_NAME = 'DATOS_CANSAT' 
        self.login = mariadb.connect(self.DB_HOST, self.DB_USER, self.DB_PASS, self.DB_NAME)
        
        self.cursor = self.login.cursor()
        self.query = "INSERT INTO datos VALUES (%f,%f,%f,'%s','%s');" % (self.altitud[-1], self.temperatura[-1], self.presion[-1],str(datetime.datetime.utcnow().date()), hora_recibido)
        self.cursor.execute(self.query)
        self.login.commit()
        
    def agregarTableWidget(self, tabla, hora_recibido):
        tabla.insertRow(self.contador)
        self.nuevoTemperatura = QtGui.QTableWidgetItem()
        self.nuevoTemperatura.setText(str('%.1f' % self.temperatura[-1]))
        tabla.setItem(self.contador,0,self.nuevoTemperatura)
        self.nuevoPresion = QtGui.QTableWidgetItem()
        self.nuevoPresion.setText('%.2f' % self.presion[-1])
        tabla.setItem(self.contador,1,self.nuevoPresion)
        self.nuevoAltura = QtGui.QTableWidgetItem()
        self.nuevoAltura.setText('%.2f' % self.altitud[-1])
        tabla.setItem(self.contador,2,self.nuevoAltura)
        self.nuevoTiempo = QtGui.QTableWidgetItem()
        self.nuevoTiempo.setText('%s' % hora_recibido)
        tabla.setItem(self.contador,3,self.nuevoTiempo)
        self.contador+=1
        tabla.repaint()
        tabla.scrollToBottom()