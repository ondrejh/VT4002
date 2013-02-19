#! /usr/bin/env python3

from tkinter import *
from chamber_temp import *


#system configuration
PortName = 'COM8'


#application class
class runapp_gui(Frame):
	''' gui for VT4002 (using chamber_temp.py module) '''
	
	def __init__(self,master=None):
		self.root = Tk()
		self.root.title('VT4002 ({})'.format(PortName))
		Frame.__init__(self,master)
		self.createWidgets()
	
	def createWidgets(self):
		#values and button frame
		self.frmValBtns = Frame(self.root, height=2, bd=3)
		self.frmValBtns.pack(side=TOP)
		
		#values frame
		self.frmTempValues = Frame(self.frmValBtns, height=2, bd=3)
		self.frmTempValues.pack(side=LEFT)
		#actual temperature entry (read only)
		self.lblActualTemp = Label(self.frmTempValues,text='Actual temperature:')
		self.lblActualTemp.grid(row=0, column=0, sticky=E, pady=3)
		self.strActualTemp = StringVar()
		self.entActualTemp = Entry(self.frmTempValues,
				       textvariable=self.strActualTemp,
				       width=10,
				       justify=RIGHT,
				       state=DISABLED)
		self.entActualTemp.grid(row=0, column=1)
		self.lblActualTempU = Label(self.frmTempValues,text='°C')
		self.lblActualTempU.grid(row=0, column=2, sticky=W)
		#setted temperature entry
		self.lblSettedTemp = Label(self.frmTempValues,text='Setted temperature:')
		self.lblSettedTemp.grid(row=1, column=0, sticky=E, pady=3)
		self.strSettedTemp = StringVar()
		self.entSettedTemp = Entry(self.frmTempValues,
					   textvariable=self.strSettedTemp,
					   width=10,
					   justify=RIGHT)
		self.entSettedTemp.grid(row=1, column=1)
		self.lblSettedTempU = Label(self.frmTempValues,text='°C')
		self.lblSettedTempU.grid(row=1, column=2, sticky=W)
		#status entry (read only)
		self.lblStatus = Label(self.frmTempValues,text='Status:')
		self.lblStatus.grid(row=2,column=0, sticky=E, pady=3)
		self.strStatus = StringVar()
		self.entStatus = Entry(self.frmTempValues,
				       textvariable=self.strStatus,
				       width=10,
				       justify=RIGHT,
				       state=DISABLED)
		self.entStatus.grid(row=2,column=1)

		#buttons frame
		self.frmButtons = Frame(self.frmValBtns, height=2, bd=3)
		self.frmButtons.pack(side=TOP)
		#read button
		self.btnRead = Button(self.frmButtons, text="Read", command=self.readClick)
		self.btnRead.grid(row=0,sticky=W+E)
		#start button
		self.btnStart = Button(self.frmButtons, text="Start", command=self.startClick)
		self.btnStart.grid(row=1,sticky=W+E)
		#stop button
		self.btnStop = Button(self.frmButtons, text="Stop", command=self.stopClick)
		self.btnStop.grid(row=2,sticky=W+E)

		#status bar frame
		self.frmStatusBar = Frame(self.root)
		self.frmStatusBar.pack(side=BOTTOM,fill=X)
		#status entry (read only)
		self.strStatusBar = StringVar()
		self.entStatusBar = Entry(self.frmStatusBar,
					  textvariable=self.strStatusBar,
					  justify=CENTER,
					  state=DISABLED)
		self.entStatusBar.pack(fill=X)

	def sayReadError(self,text):
		self.strActualTemp.set('---')
		self.strSettedTemp.set('---')
		self.strStatus.set('---')
		self.strStatusBar.set('Read temperature: {} !!!'.format(text))

	def readClick(self):
		try:
			answ = read_temp(PortName,verbose=False)
			if len(answ)>0:
				if answ[0]=='E':
					self.sayReadError('ERROR')
				else:
					self.strActualTemp.set('{:.1f}'.answ[1])
					self.strSettedTemp.set('{:.1f}'.answ[0])
					self.strStatus.set(answ[2])
					self.strStatusBar.set('Temperature read OK')
			else:
				self.sayReadError('No answer')
		except:
			self.sayReadError('Raised exception')

	def saySetError(self,text):
		self.strSettedTemp.set('???')
		self.strStatusBar.set('Set temperature: {} !!!'.format(text))

	def setTemp(self,status):
		setTemp = None
		try:
			setTemp=float(self.strSettedTemp.get())
		except:
			self.saySetError('Syntax error')
		finally:
			try:
				answ = set_temp(PortName,setTemp,status,verbose=False)
				if len(answ)>0:
					if answ[0]!='E':
						self.strStatus.set('{}'.answ[1])
						self.strSettedTemp.set('{:.1f}'.answ[0])
						self.strStatusBar.set('Temperature set OK')
					else:
						self.saySetError('ERROR')
				else:
					self.saySetError('No answer')
			except:
				self.saySetError('Raised exception')
			
	def startClick(self):
		self.setTemp('ON')

	def stopClick(self):
		self.setTemp('ON')
		
#run application
app = runapp_gui()
app.mainloop()
