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

import sys
import serial
import datetime
from PySide import QtCore, QtGui, QtSql
import grafica as gf
import pyqtgraph as pg
import datos as dt
import reloj as rj

class Ventana(QtGui.QMainWindow):
    def __init__(self, parent=None):
        
        QtGui.QMainWindow.__init__(self, parent)
        self.resize(1366,768)
        self.move(QtGui.QApplication.desktop().screen().rect().center()- self.rect().center())
        self.tabla = dt.Datos()
        self.setStyleSheet("background-color: white;")
        
        #####################################################################################´
        #TABLA
        #####################################################################################'
        
        self.table = QtGui.QTableWidget(self)
        self.table.setGeometry(703,120,450,300)
        self.table.setColumnCount(4)
        self.table.setRowCount(1)
        self.temperatura = QtGui.QTableWidgetItem()
        self.temperatura.setText('Temperatura:')
        self.table.setItem(0,0,self.temperatura)
        self.presion = QtGui.QTableWidgetItem()
        self.presion.setText('Presion:')
        self.table.setItem(0,1,self.presion)
        self.altitud = QtGui.QTableWidgetItem()
        self.altitud.setText('Altura:')
        self.table.setItem(0,2,self.altitud)
        self.tiempo = QtGui.QTableWidgetItem()
        self.tiempo.setText('Tiempo:')
        self.table.setItem(0,3,self.tiempo)
        self.table.setStyleSheet("background-image: url(./IGUM2.png); background-repeat: no-repeat; background-position: center;")
        self.table.show()
        
        #####################################################################################´
        #IMAGENES
        #####################################################################################´   
        self.label_banner = QtGui.QLabel(self)
        self.label_banner.setPixmap(QtGui.QPixmap("banner2.png"))
        self.label_banner.setGeometry(703,10,653,100)
        #powered
        self.label_f = QtGui.QLabel(self)
        self.label_f.setPixmap(QtGui.QPixmap("f.png"))
        self.label_f.setGeometry(1054,595,36,53)     
        self.label_q = QtGui.QLabel(self)
        self.label_q.setPixmap(QtGui.QPixmap("q.png"))
        self.label_q.setGeometry(1100,595,36,36)   
        self.label_p = QtGui.QLabel(self)
        self.label_p.setPixmap(QtGui.QPixmap("p.png"))
        self.label_p.setGeometry(1146,595,100,40)   
        self.label_m = QtGui.QLabel(self)
        self.label_m.setPixmap(QtGui.QPixmap("m.png"))
        self.label_m.setGeometry(1256,595,100,34)
        #logos escuela
        self.label_utm = QtGui.QLabel(self)
        self.label_utm.setPixmap(QtGui.QPixmap("ut.png"))
        self.label_utm.setGeometry(1214,517,142,68)
        self.label_enes = QtGui.QLabel(self)
        self.label_enes.setPixmap(QtGui.QPixmap("en.png"))
        self.label_enes.setGeometry(1054,517,109,68)
        self.label_igum = QtGui.QLabel(self)
        self.label_igum.setPixmap(QtGui.QPixmap("unam.png"))
        self.label_igum.setGeometry(703,517,341,122)
        
        pixmap = QtGui.QPixmap('icono.png')
        self.setWindowIcon(QtGui.QIcon(pixmap))
        self.style = self.style()
        
        ###################################################################'
        #Boton de iniciarCansat
        self.iniciar = QtGui.QPushButton("Comenzar", self)
        self.iniciar.setGeometry(703,443,135,27)
        self.connect(self.iniciar, QtCore.SIGNAL('clicked()'), self.iniciarCansat)
        self.check_salir = QtGui.QCheckBox(self)
        self.check_salir.setGeometry(QtCore.QRect(848, 443, 31, 31))
    
        self.graficota = QtGui.QPushButton('Expandir grafica', self)
        self.graficota.setGeometry(703, 480, 135,27)
        self.connect(self.graficota, QtCore.SIGNAL('clicked()'), self.expandirGrafica)
                
        #####################################################################'
        #RELOJES
        #####################################################################'
        #lcd
        self.timer = QtCore.QTimer(self)
        self.relojlocal = rj.RelojDigital(self)
        self.relojlocal.setGeometry(1163,147,193,40)
        self.relojlocal.connect(self.timer,QtCore.SIGNAL("timeout()"),self.relojlocal,QtCore.SLOT("showTime()"))
        self.relojutc = rj.RelojDigital(self, utc=True)
        self.relojutc.setGeometry(1163,214,193,40)
        self.relojutc.connect(self.timer,QtCore.SIGNAL("timeout()"),self.relojutc,QtCore.SLOT("showTime()"))
        self.datospersecond = rj.RelojDatosPorSegundo(self)
        self.datospersecond.setGeometry(1163,367,193,40)
        self.datospersecond.connect(self.timer,QtCore.SIGNAL("timeout()"),self.datospersecond,QtCore.SLOT("showTime()"))
        self.relojultima = rj.RelojUltimaCaida(self)
        self.relojultima.setGeometry(1163,291,193,40)
        self.timer.start(1000)
        #labels
        self.horalocal = QtGui.QLabel('Hora Local:', self)
        self.horalocal.setGeometry(1163,120,91,27)
        self.horautc = QtGui.QLabel('Tiempo Universal Coordinado:', self)
        self.horautc.setGeometry(1163,187,191,27)
        self.horainicia = QtGui.QLabel('Datos por segundo:', self)
        self.horainicia.setGeometry(1163,341,180,27)
        self.horaultima = QtGui.QLabel('Ultimo dato recibido:', self)
        self.horaultima.setGeometry(1163,264,180,27)
        
        ################################################################################################'
        #MAXIMOS Y MINIMOS
        ################################################################################################'
        #labels
        self.label_maximo = QtGui.QLabel("Maximo:", self)
        self.label_maximo.setGeometry(877,443,54,27)
        self.label_minimo = QtGui.QLabel("Minimo:", self)
        self.label_minimo.setGeometry(877,480,54,27)
        self.label_temperatura = QtGui.QLabel("Temperatura",self)
        self.label_temperatura.setGeometry(931,415,135,27)
        self.label_presion = QtGui.QLabel(u"Presión",self)
        self.label_presion.setGeometry(1076,415,135,27)
        self.label_altura = QtGui.QLabel("Altitud",self)
        self.label_altura.setGeometry(1221,415,135,27)
        #relojes
        self.reloj_maximo_temperatura = rj.RelojExtremo(self)
        self.reloj_maximo_temperatura.setGeometry(931,443,135,27)        
        self.reloj_minimo_temperatura = rj.RelojExtremo(self)
        self.reloj_minimo_temperatura.setGeometry(931,480,135,27)        
        self.reloj_maximo_presion = rj.RelojExtremo(self)
        self.reloj_maximo_presion.setGeometry(1076,443,135,27)    
        self.reloj_minimo_presion = rj.RelojExtremo(self)
        self.reloj_minimo_presion.setGeometry(1076,480,135,27)        
        self.reloj_maximo_altitud = rj.RelojExtremo(self)
        self.reloj_maximo_altitud.setGeometry(1221,443,135,27)        
        self.reloj_minimo_altitud = rj.RelojExtremo(self)
        self.reloj_minimo_altitud.setGeometry(1221,480,135,27)    
        
        #################################################################################################´
        #GRAFICA
        self.view = pg.GraphicsView(self)
        self.l = gf.miGrafica()
        self.view.setCentralItem(self.l)
        self.view.show()
        self.view.setWindowTitle('Muestra en tiempo real de los datos')
        self.view.setGeometry(10,10,683,630)

        self.regresar = QtGui.QPushButton('<', self)
        self.regresar.setGeometry(1329, 613, 27,27)
        self.connect(self.regresar, QtCore.SIGNAL('clicked()'), self.regresarGrafica)
        self.regresar.hide()
    

    def iniciarCansat(self):
        try:
            self.ser = serial.Serial(port='/dev/ttyUSB0',baudrate=57600, timeout=1.0)
        except OSError:
            self.ser = serial.Serial(port='/dev/ttyUSB1',baudrate=57600, timeout=1.0)
            
        self.ser.close()
        self.ser.open()

        while True:
            self.a = self.ser.readline().split()

            try:
                try:
                    self.tabla.ingresarDatos(float(self.a[1]),float(self.a[0]),float(self.a[2]))
                except ValueError:
                    continue
                if len(self.tabla.
                    temperatura)>=1 and len(self.tabla.presion)>=1 and len(self.tabla.altitud)>=1:
                    if self.tabla.temperatura[-1] > 100 and abs(self.tabla.presion[-2] - self.tabla.presion[-1]) > 200:
                        continue
                    self.hora_recibido = str(datetime.datetime.utcnow().time())
                    self.tabla.guardarEnArchivo(self.hora_recibido)
                    self.tabla.agregarTableWidget(self.table, self.hora_recibido)
                    self.l.update(self.tabla.temperatura, self.tabla.presion, self.tabla.altitud)
                    self.relojultima.actualizar_hora(self.hora_recibido)
                    self.tabla.ingresarBaseDatos(self.hora_recibido)
                    self.checarMaxMin(self.tabla.temperatura[-1], self.tabla.presion[-1], self.tabla.altitud[-1])
                    self.datospersecond.setLenNuevosDatos(len(self.tabla.presion))
                    QtGui.QApplication.processEvents()
                    if self.check_salir.isChecked():
                        break
            except IndexError or ValueError:
                continue
            
        self.ser.close()
        
    def expandirGrafica(self):
        self.view.setGeometry(10,10,1346,630)
        self.regresar.show()
        self.label_f.hide()
        
    def regresarGrafica(self):
        self.view.setGeometry(10,10,683,630)
        self.regresar.hide()
        self.label_f.show()
        
    def checarMaxMin(self, temp, pre, alt):
        if temp > self.reloj_maximo_temperatura.getAnterior():
            self.reloj_maximo_temperatura.setAnterior(temp)
            self.reloj_maximo_temperatura.actualizar()
        if not self.reloj_minimo_temperatura.getModify():
            self.reloj_minimo_temperatura.setAnterior(temp)
            self.reloj_minimo_temperatura.actualizar()
            self.reloj_minimo_temperatura.changeModify()
        elif temp < self.reloj_minimo_temperatura.getAnterior():
            self.reloj_minimo_temperatura.setAnterior(temp)
            self.reloj_minimo_temperatura.actualizar()
        if pre > self.reloj_maximo_presion.getAnterior():
            self.reloj_maximo_presion.setAnterior(pre)
            self.reloj_maximo_presion.actualizar()
        if not self.reloj_minimo_presion.getModify():
            self.reloj_minimo_presion.setAnterior(pre)
            self.reloj_minimo_presion.actualizar()
            self.reloj_minimo_presion.changeModify()
        elif pre < self.reloj_minimo_presion.getAnterior():
            self.reloj_minimo_presion.setAnterior(pre)
            self.reloj_minimo_presion.actualizar()
        if alt > self.reloj_maximo_altitud.getAnterior():
            self.reloj_maximo_altitud.setAnterior(alt)
            self.reloj_maximo_altitud.actualizar()
        if not self.reloj_minimo_altitud.getModify():
            self.reloj_minimo_altitud.setAnterior(alt)
            self.reloj_minimo_altitud.actualizar()
            self.reloj_minimo_altitud.changeModify()
        elif alt < self.reloj_minimo_altitud.getAnterior():
            self.reloj_minimo_altitud.setAnterior(alt)
            self.reloj_minimo_altitud.actualizar()
            
app = QtGui.QApplication(sys.argv)

status = QtGui.QStatusBar()
status.addWidget(QtGui.QLabel("Autor: Equipo GeoSat gruelas@cieco.unam.mx"),5)
status.addWidget(QtGui.QLabel("Software Version 1.2 License GNU GPL v3"),5)
status.addWidget(QtGui.QLabel(u"Copyright © Germán Ruelas"),5)

main = Ventana()
main.setWindowTitle("Observacion de los datos del CanSat")
app.setWindowIcon(QtGui.QIcon('icono.png'))
main.setStatusBar(status)
main.show()

sys.exit(app.exec_())