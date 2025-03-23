#! /usr/bin/env python


class Apotheken:
    """Notdienst-Apotheken"""
    def __init__(self, xmlEntry):
        self.name   = xmlEntry.find('name').text
        self.tel    = xmlEntry.find('phone').text
        self.loc    = [xmlEntry.find('location').text,
                       xmlEntry.find('subLocation').text]
        self.plz    = xmlEntry.find('zipCode').text
        self.str    = xmlEntry.find('street').text
        self.offen  = [datetime.strptime(re.sub('(.000)?[+-]0[0-9]:00$','',xmlEntry.find('from').text),
                                         '%Y-%m-%dT%H:%M:%S'),
                       datetime.strptime(re.sub('(.000)?[+-]0[0-9]:00$','',xmlEntry.find('to').text),
                                         '%Y-%m-%dT%H:%M:%S')]
        self.gpsList= [float(xmlEntry.find('lat').text),
                       float(xmlEntry.find('lon').text)]
    def gps(self):
        return list(self.gpsList)

    def open(self,Datum):
        Datum = Datum.replace(hour=12)
        dO = Datum-self.offen[0]
        dC = self.offen[1] - Datum
        if dO.total_seconds()>0 and dC.total_seconds()>0:
            return True
        else:
            return False
    def getLoc(self):
        if self.loc[1] and self.loc[1].strip():
            return self.loc[0] + '-' + self.loc[1]
        else:
            return self.loc[0]

class PDFfile:
    def __init__(self, filename):
        self.canvas = canvas.Canvas(filename, pagesize=A4)
        self.paperW, self.paperH = A4
        self.tableW = (127-6)*mm
        self.tableH = 0
        self.fontSize =15
        self.currentRow = -1
        self.currentPage = 0
        self.rows = 0

    def drawTable(self):
        self.currentPage = self.currentPage + 1
        if self.currentPage % 2 > 0:
            self.rows = 4
            self.tableH = 399/7*self.rows*mm
            self.canvas.setFont('Helvetica', 12)
            self.canvas.rotate(90)
            self.canvas.drawString(30*mm,-30*mm,'Bitte ausschneiden und mit naechster Seite zusammenkleben. Beim Drucken unter "Seite anpassen" Option "Tatsächliche Größe" wählen.')
            self.canvas.rotate(270)
            self.canvas.setFont('Helvetica', self.fontSize)
        else:
            self.rows = 3
            self.tableH = 399/7*self.rows*mm
            self.canvas.setFont('Helvetica', 12)
            self.canvas.rotate(90)
            self.canvas.drawString(30*mm,-30*mm,'Bitte ausschneiden und mit voriger Seite zusammenkleben. Beim Drucken unter "Seite anpassen" Option "Tatsächliche Größe" wählen.')
            self.canvas.rotate(270)
            self.canvas.setFont('Helvetica', self.fontSize)
        self.canvas.setLineWidth(.3)
        self.canvas.setFont('Helvetica', self.fontSize)
        paperOffsetW = self.paperW/2-self.tableW/2
        paperOffsetH = self.paperH/2-self.tableH/2
        
        
        """Anrisslinien"""
        self.canvas.line(paperOffsetW,15*mm,paperOffsetW,25*mm)
        self.canvas.line(self.paperW-paperOffsetW,15*mm,self.paperW-paperOffsetW,25*mm)
        self.canvas.line(paperOffsetW,self.paperH-15*mm,paperOffsetW,self.paperH-25*mm)
        self.canvas.line(self.paperW-paperOffsetW,self.paperH-15*mm,self.paperW-paperOffsetW,self.paperH-25*mm)
        
        self.canvas.line(15*mm,paperOffsetH,25*mm,paperOffsetH)
        self.canvas.line(self.paperW-15*mm,paperOffsetH,self.paperW-25*mm,paperOffsetH)
        self.canvas.line(15*mm,self.paperH-paperOffsetH,25*mm,self.paperH-paperOffsetH)
        self.canvas.line(self.paperW-15*mm,self.paperH-paperOffsetH,self.paperW-25*mm,self.paperH-paperOffsetH)
        
        """Tabelle zeichnen"""
        self.canvas.translate(paperOffsetW, paperOffsetH)
        self.canvas.line(0,0,0,self.tableH)
        self.canvas.line(self.tableW,0,self.tableW,self.tableH)
        for iRow in range(0,self.rows+1):
            self.canvas.line(0,iRow*self.rowH(), self.tableW, iRow*self.rowH())
        self.canvas.translate(0,self.tableH)
        self.currentRow = 0

    def nextRow(self):
        if self.currentPage < 1:
            self.drawTable()
        else:
            self.canvas.translate(0,-self.rowH())
            self.currentRow = self.currentRow + 1
            if self.currentRow+1 > self.rows:
                self.canvas.showPage()
                self.drawTable()

    def fillRow(self,apos,Datum):
        self.canvas.rotate(90)
        self.canvas.setFont('Helvetica', 12)
        self.canvas.drawCentredString(-self.rowH()/2-self.fontSize/2-2*mm,-self.fontSize*2,Datum.strftime('%A, %x'))
        self.canvas.setFont('Helvetica', self.fontSize)
        self.canvas.rotate(270)
        l = []
        for apo in apos:
            if apo.open(Datum):
                l.append(apo)
        if 0 == len(l):
            return #skip past days
        offsetW = (self.rowH() - self.fontSize*8)/2*self.tableW/self.rowH()
        offsetH =-(self.rowH() - self.fontSize*8)/2-self.fontSize*0.8 - 4*mm
        if len(l)>=1 and l[0].name == "Charlotten-Apotheke Stuttgart":
            self.canvas.setFont('Helvetica-Bold', self.fontSize*2)
            self.canvas.drawString(offsetW,offsetH-self.fontSize*4,"DIENSTBEREIT")
            self.canvas.setFont('Helvetica', self.fontSize/2)
        else:
            for iApo in range(0,2): #there are 4, but we want only 2//len(l)):
                self.canvas.setFont('Helvetica-Bold', self.fontSize)
                offsetW = (self.rowH() - self.fontSize*8)/2*self.tableW/self.rowH()
                offsetH =-(self.rowH() - self.fontSize*8)/2-self.fontSize*0.8 - 4*mm
                """Schilder sind nicht zentriert!"""
                self.canvas.drawString(offsetW,offsetH-self.fontSize*(4*iApo+0),l[iApo].name)
                self.canvas.setFont('Helvetica', self.fontSize)
                self.canvas.drawString(offsetW+5*mm,offsetH-self.fontSize*(4*iApo+1),l[iApo].str)
                self.canvas.drawString(offsetW+5*mm,offsetH-self.fontSize*(4*iApo+2),l[iApo].plz + " " + l[iApo].getLoc())
                self.canvas.drawString(offsetW+5*mm,offsetH-self.fontSize*(4*iApo+3),"Tel.: " + l[iApo].tel)

    def rowH(self):
        return self.tableH/self.rows

    def save(self):
        self.canvas.save()


from xml.etree.ElementTree import parse
from datetime import datetime
from datetime import timedelta
import re
import codecs
import os
import locale
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import tempfile
import sys
import subprocess

locale.setlocale(locale.LC_ALL, 'de_DE')

t = parse('lak.xml')
r = t.getroot()
apos = []
for apo in r.findall("entries/entry"):
    apos.append(Apotheken(apo))

f = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')

Monday = datetime.today() - timedelta(days=datetime.today().weekday())
for arg in sys.argv:
    if "next" in arg:
        Monday = Monday + timedelta(days=7)

pdf = PDFfile(f.name)
for iDay in range(0,7):
    pdf.nextRow()
    pdf.fillRow(apos,Monday+timedelta(days=iDay))
pdf.save()

#pdf = PDFfile("Plan_naechste_Woche.pdf")
#for iDay in range(0,7):
#    pdf.nextRow()
#    pdf.fillRow(apos,Monday+timedelta(days=iDay+7))
#pdf.save()


if sys.platform.startswith('linux'):
    subprocess.call(["xdg-open", f.name])
else:
    os.startfile(f.name)
