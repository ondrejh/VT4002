#! /usr/bin/env python3

from tkinter import *
from VT4002 import *


#system configuration
PortName = 'COM3'


#application class
class runapp_gui(Frame):
	''' gui for VT4002 (using chamber_temp.py module) '''
	
	def __init__(self,master=None):
		self.root = Tk()
		self.root.title('VT4002 ({})'.format(PortName))
		Frame.__init__(self,master)
		self.createWidgets()
		self.readCycle()
	
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
		self.btnRead.grid(row=0,sticky=W+E,pady=1)
		#start button
		self.btnStart = Button(self.frmButtons, text="Start", command=self.startClick)
		self.btnStart.grid(row=1,sticky=W+E,pady=1)
		#stop button
		self.btnStop = Button(self.frmButtons, text="Stop", command=self.stopClick)
		self.btnStop.grid(row=2,sticky=W+E,pady=1)

		#settings frame
		self.frmSettings = Frame(self.root,bd=3)
		self.frmSettings.pack(fill=X)
		self.frmSettings.grid_columnconfigure(0,weight=1)
		#autoread radiobutton
		self.boolAutoRead = BooleanVar()
		self.chbAutoRead = Checkbutton(self.frmSettings,text="Auto Read",variable=self.boolAutoRead,onvalue=True,offvalue=False,command=self.autoreadClick)
		self.chbAutoRead.grid(row=0,column=0,sticky=W)
		self.strAutoReadTime = StringVar()
		self.strAutoReadTime.set("60")
		self.spbAutoReadTime = Spinbox(self.frmSettings,textvariable=self.strAutoReadTime,from_=10,to=120,width=8)
		self.spbAutoReadTime.grid(row=0,column=1,sticky=E)
		labAutoReadTimeUnit = Label(self.frmSettings,text="sec")
		labAutoReadTimeUnit.grid(row=0,column=2,sticky=W+E)
		#autooff radiobutton
		self.boolAutoOff = BooleanVar()
		self.chbAutoOff = Checkbutton(self.frmSettings,text="Auto Off",variable=self.boolAutoOff,onvalue=True,offvalue=False,command=self.autooffClick)
		self.chbAutoOff.grid(row=1,column=0,sticky=W)
		self.strAutoOffTime = StringVar()
		self.strAutoOffTime.set("120")
		self.spbAutoOffTime = Spinbox(self.frmSettings,textvariable=self.strAutoOffTime,from_=1,to=600,width=8)
		self.spbAutoOffTime.grid(row=1,column=1,sticky=E)
		labAutoOffTimeUnit = Label(self.frmSettings,text="min")
		labAutoOffTimeUnit.grid(row=1,column=2,sticky=W)

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
					self.strActualTemp.set('{:.1f}'.format(answ[1]))
					self.strSettedTemp.set('{:.1f}'.format(answ[0]))
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
						self.strStatus.set('{}'.format(answ[1]))
						self.strSettedTemp.set('{:.1f}'.format(answ[0]))
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
		self.setTemp('OFF')

	def readCycle(self):
		if self.boolAutoRead.get() == True:
			if self.boolAutoOff.get() == False:
				self.readClick()
			self.after(int(self.strAutoReadTime.get())*1000,self.readCycle)

	def autoreadClick(self):
		if self.boolAutoRead.get() == True:
			self.btnRead.config(state=DISABLED)
			self.btnStart.config(state=DISABLED)
			self.btnStop.config(state=DISABLED)
			self.readCycle()
		else:
			if self.boolAutoOff.get() == False:
				self.btnRead.config(state=NORMAL)
				self.btnStart.config(state=NORMAL)
				self.btnStop.config(state=NORMAL)

	def autooffClick(self):
		if self.boolAutoOff.get() == True:
			self.intAutoOffTime = int(self.strAutoOffTime.get()) + 1
			self.btnRead.config(state=DISABLED)
			self.btnStart.config(state=DISABLED)
			self.btnStop.config(state=DISABLED)
			self.autooffTimeTick()
		else:
			if self.boolAutoRead.get() == False:
				self.btnRead.config(state=NORMAL)
				self.btnStart.config(state=NORMAL)
				self.btnStop.config(state=NORMAL)

	def autooffTimeTick(self):
		if self.boolAutoOff.get() == True:
			if self.boolAutoRead.get() == True:
				self.readClick()
			if self.intAutoOffTime>=0:
				self.intAutoOffTime = self.intAutoOffTime - 1
				if self.intAutoOffTime<0:
					self.stopClick()
					self.strStatusBar.set('Air conditioning is stopped')
				else:
					self.strStatusBar.set('Stop in {} minutes'.format(self.intAutoOffTime))
			else:
				self.strStatusBar.set('Air conditioning is stopped')
			self.after(60000,self.autooffTimeTick)
	
#run application
app = runapp_gui()
app.mainloop()
