# -*- coding: utf-8 -*-
# Author ideas from KarJa, with many helps from StackOverflow, GeeksforGeeks, and many more.
# Sorry i cannot mention all, as i move along building this app, i looked up in website, 
# and did not save the website. 
# Many apologize from me. 
# Thank you all so much for all, for your dedication making website the source of sharing.
# I dedicate this app as well for learning and free to be use and copied for better.
# Copyright © kakkarja (K A K)

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog, messagebox
import calendar as cal
import pandas as pd
import datetime as dt
import time

class ChoCal:
    """Creating Calendar engine."""
    
    def __init__(self, year = dt.date.today().year , 
                 month =  dt.date.today().month, 
                 day = dt.date.today().day):
        self.year = year
        self.month = month
        self.day = day
    
    def createcal(self):
        cal.setfirstweekday(cal.SUNDAY)
        cm = [cal.monthcalendar(self.year,i+1) for i in range(12)]            
        monthy = self.month-1
        dayth = self.day
        mo = [i for i in cal.month_name if i != '']
        monthdict = { i:d for i, d in zip(mo,cm)}
        days = cal.weekheader(2).split()
        df = pd.DataFrame(monthdict[mo[monthy]],
        index = [f'Week {i+1}' for i in range(len(monthdict[mo[monthy]]))],
        columns= days)
        df = df.replace(0, '')
        df.index.name = f'{mo[monthy]} {self.year}'
        return df

    @staticmethod
    def monrang(year, month):
        return cal.monthrange(year, month)[1]
    
    @staticmethod
    def mds():
        return cal.mdays[1:]
    
    @staticmethod
    def caldays(ye: int, mo: int, da: int):
        y = dt.datetime.today().year
        m = dt.datetime.today().month
        d = dt.datetime.today().day
        r = str(dt.date(ye, mo, da) - dt.date(y,m,d))[:-9]
        if r:
            return r

class CalGui:
    """This is calendar that built with tkinter.
       From the year 1800 to 2300."""
    
    SELF = True
    RUN = False
    TOP = None
    
    def __init__(self, root):
        self.root = root
        self.sd = []
        self.rdr =[]
        self.txfile =''
        
        self.wwidth = self.root.winfo_reqwidth()
        self.wheight = self.root.winfo_reqheight()
        self.pwidth = int(self.root.winfo_screenwidth()/17 - self.wwidth/17)
        self.pheight = int(self.root.winfo_screenheight()/17 - self.wheight/17)
        self.root.geometry(f"+{self.pwidth}+{self.pheight}")
        self.root.overrideredirect(True)
        self.root.config(background = 'teal')
        self.root.bind_all('<Left>', self.mlr)
        self.root.bind_all('<Right>', self.mlr)
        self.root.bind_all('<Up>',self. mlr)
        self.root.bind_all('<Down>', self.mlr)
        self.root.bind_all('<Control-Left>', self.mtc)
        self.root.bind_all('<Control-Right>', self.mtc)
        self.root.bind_all('<Shift-Left>', self.dtc)
        self.root.bind_all('<Shift-Right>', self.dtc)
        self.root.bind_all('<Alt-Left>', self.yrc)
        self.root.bind_all('<Alt-Right>', self.yrc)
        self.bt = {}
        self.sc1 = Scale(self.root, from_=1800, to=2300, orient = HORIZONTAL, 
                    command = self.ccal, background = 'gold')
        self.sc1.set(dt.datetime.today().year)
        self.sc1.pack(pady = 3, padx = 3 , fill = 'both')
        self.bt['sc1'] = self.sc1
        self.sc2 = Scale(self.root, from_=1, to=12, orient = HORIZONTAL, 
                    command = self.ccal, background = 'gold')
        self.sc2.set(dt.datetime.today().month)
        self.sc2.pack(pady = 2, padx = 3 , fill = 'both')
        self.bt['sc2'] = self.sc2
        self.sc3 = Scale(self.root, from_=1, to=31, orient = HORIZONTAL, 
                    command = self.ccal, background = 'gold')
        self.sc3.set(dt.datetime.today().day)
        self.sc3.pack(pady = 3, padx = 3 , fill = 'both')
        self.bt['sc3'] = self.sc3
        self.text = Text(self.root, font = 'courier 20 bold', width = 48, height = 8, background ='light blue', foreground='indigo', relief = SUNKEN)
        self.text.tag_add('bd', '1.0', END)
        self.text.tag_config('bd', justify = 'center')
        self.text.tag_config('thg', background = 'dark orange', foreground = 'black')
        self.text.tag_config('hg', background = 'dark slate blue', foreground = 'white')
        self.text.pack(pady = 2, fill = 'x')
        self.bt['text'] = self.text
        self.gset = IntVar()
        self.cb = Checkbutton(self.root, text = 'Set date', variable = self.gset, command=self.scald,
                         background = 'teal', highlightthickness = 0, bd = 0,
                         fg = 'black', activebackground = 'teal', activeforeground = 'white')
        self.cb.bind_all('<Control-k>', self.setcb)
        self.cb.pack(pady = 5)
        self.bt['cb'] = (self.cb, '<Control-k>', self.setcb)
        self.lvar = StringVar()
        self.label = ttk.Label(root, textvariable = self.lvar, font = 'verdana 20 bold', 
                          background = 'teal', foreground = 'white' )
        self.label.pack(pady = 5)
        self.frb = ttk.Frame(self.root)
        self.frb.pack(pady = 7)
        self.lb = Button(self.frb, text = 'Load Set Date', command = self.loaddat, 
                         bg = 'yellow', fg = 'black',
                         activebackground = 'green', activeforeground = 'white',
                         highlightthickness = 0, bd = 0)
        self.lb.bind_all('<Control-l>', self.loaddat)
        self.lb.pack(side = LEFT)
        self.bt['lb'] = (self.lb, '<Control-l>', self.loaddat)
        self.stb = Button(self.frb, text = 'Current Date/Set', command = self.sdat, 
                          bg = 'yellow', fg = 'black', activebackground = 'green', 
                          activeforeground = 'white',highlightthickness = 0, bd = 0)
        self.stb.bind_all('<Control-c>', self.sdat)
        self.stb.pack(side = LEFT, padx=2)
        self.bt['stb'] = (self.stb, '<Control-c>', self.sdat)
        self.entry = Button(self.frb, text = 'Reminder', command = self.rem, 
                            bg = 'yellow', fg = 'black', activebackground = 'green', 
                            activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.entry.bind_all('<Control-m>', self.rem)
        self.entry.pack(side = LEFT)
        self.bt['entry'] = (self.entry, '<Control-m>', self.rem)
        self.cdb = Button(self.frb, text = 'Calculate', command = self.calcd, 
                          bg = 'yellow', fg = 'black', activebackground = 'green', 
                          activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.cdb.bind_all('<Control-equal>', self.calcd)
        self.cdb.pack(side = LEFT, padx=2)
        self.bt['cdb'] = (self.cdb, '<Control-equal>', self.calcd)
        self.stob = Button(self.frb, text = 'Run Color', command = self.colrun, 
                           bg = 'yellow', fg = 'black', activebackground = 'green', 
                           activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.stob.bind_all('<Control-r>', self.colrun)
        self.stob.pack(side = LEFT)
        self.bt['stob'] = (self.stob, '<Control-r>', self.colrun)
        self.recb = Button(self.frb, text = 'Record Set Date', command = self.recdat, 
                         bg = 'yellow', fg = 'black', activebackground = 'green', 
                         activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.recb.bind_all('<Control-e>', self.recdat)
        self.recb.pack(side = LEFT, padx=2)
        self.bt['recb'] = (self.recb, '<Control-e>', self.recdat)
        self.hcbb = Button(self.frb, text = 'Highlight', command = self.colorh, 
                           bg = 'yellow', fg = 'black', activebackground = 'green', 
                           activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.hcbb.bind_all('<Control-h>', self.colorh)
        self.hcbb.pack(side = LEFT)
        self.bt['hcbb'] = (self.hcbb, '<Control-h>', self.colorh)
        self.clbcb = Button(self.frb, text = 'Cal Bg Color', command = self.calbg, 
                            bg = 'yellow', fg = 'black', activebackground = 'green', 
                            activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.clbcb.bind_all('<Control-b>', self.calbg)
        self.clbcb.pack(side = LEFT, padx=2)
        self.bt['clbcb'] = (self.clbcb, '<Control-b>', self.calbg)
        self.setb = Button(self.frb, text = 'Saving Colors', command = self.savs, 
                           bg = 'yellow', fg = 'black', activebackground = 'green', 
                           activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.setb.bind_all('<Control-s>', self.savs)
        self.setb.pack(side = LEFT)
        self.bt['setb'] = (self.setb, '<Control-s>', self.savs)
        self.but = Button(self.frb, text = 'Close', command = self.root.destroy, 
                         bg = 'blue', fg = 'white', activebackground = 'black', 
                         activeforeground = 'white',highlightthickness = 1, bd = 0)
        self.but.pack(side = LEFT)
        self.bt['but'] = self.but
        
    def mlr(self, event = None):
        # Moving the app's window to any position on the screen.
        
        if not CalGui.TOP:
            if event.keysym == 'Left':
                self.pwidth = self.pwidth - 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Right':
                self.pwidth = self.pwidth + 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Down':
                self.pheight = self.pheight + 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
            elif event.keysym == 'Up':
                self.pheight = self.pheight - 10
                self.root.geometry(f"+{self.pwidth}+{self.pheight}")
                
    def dtc(self, event = None):
        # Moving the scale of the day.
        
        if event.keysym == 'Right':
            ad = self.sc3.get()+1
            self.sc3.set(ad)
        else:
            ad = self.sc3.get()-1
            self.sc3.set(ad)
            
    def mtc(self, event = None):
        # Moving the scale of the month.
        
        if event.keysym == 'Right':
            ad = self.sc2.get()+1
            self.sc2.set(ad)
        else:
            ad = self.sc2.get()-1
            self.sc2.set(ad)
            
    def yrc(self, event = None):
        # Moving the scale of the year.
        
        if event.keysym == 'Right':
            ad = self.sc1.get()+1
            self.sc1.set(ad)
        else:
            ad = self.sc1.get()-1
            self.sc1.set(ad)    
            
    def ccal(self, event = None):
        #Creating Calendar according to the scales of the years, months and days.
        
        self.label.config(font = 'verdana 20 bold')
        cc = ChoCal(self.sc1.get(), self.sc2.get(), self.sc3.get())
        self.sc3.config(to = cc.monrang(self.sc1.get(), self.sc2.get()))
        self.text.config(state = 'normal')
        self.text.delete('1.0', END)
        self.text.insert(END, cc.createcal(), 'bd')
        self.tdcol()
        sch1 = self.text.search(str(self.sc3.get()),'3.6',END)
        sch2 = f'{sch1}+{len(str(self.sc3.get()))}c'
        gt = self.text.get(sch1,sch2)
        self.text.delete(sch1, sch2)
        self.text.insert(sch1, gt, ('hg'))
        self.text.config(state = 'disabled')
        if self.cald():
            self.lvar.set(self.cald())
        else:
            self.tn()

    def tdcol(self):
        #Highlight Color of today's date.
        
        if self.sc2.get() == dt.date.today().month and self.sc1.get() == dt.date.today().year:
            sch1 = self.text.search(str(dt.datetime.today().day),'3.6',END)
            sch2 = f'{sch1}+{len(str(dt.datetime.today().day))}c'
            gt = self.text.get(sch1,sch2)
            self.text.delete(sch1, sch2)
            self.text.insert(sch1,gt, ('thg'))
    
    def cald(self, event = None):
        #Calculation between two dates for how many days left.
        
        if self.sd:
            c = str(dt.date(self.sc1.get(),
                    self.sc2.get(), self.sc3.get()) - dt.date(self.sd[0], 
                    self.sd[1], self.sd[2]))[:-9]
            if c:
                f, _ = c.split()
                if int(f) < 0:
                    return f'The range are {c}, before this day {dt.date(self.sd[0], self.sd[1], self.sd[2])}'
                elif int(f) > 0:
                    return f'The range are {c}, after this day {dt.date(self.sd[0], self.sd[1], self.sd[2])}'  
        else:
            c = ChoCal.caldays(self.sc1.get(), self.sc2.get(), self.sc3.get())
            if c:
                f, _ = c.split()
                if int(f) < 0:
                    return f'{c} have passed to today {dt.date.isoformat(dt.datetime.today())}'
                elif int(f) > 0:
                    return f'{c} to go from today {dt.date.isoformat(dt.datetime.today())}' 

    
    def tn(self):
        #Running the seconds display and colored them.
        
        import random
        if CalGui.RUN:
            colors = [str(i) for i in range(10)] + ['a','b','c','d','e','f']
            ctk = '#'
            if self.cald() == None:
                for i in range(6):
                    ctk += ''.join(random.choice(colors))
                self.label.config(foreground = ctk)
                self.lvar.set(f'Today is {str(dt.datetime.today())[:-7]}')
                self.root.after(1000,self.tn)
        else:
            if self.cald() == None:
                self.lvar.set(f'Today is {str(dt.datetime.today())[:-7]}')
                self.root.after(1000,self.tn)
    
    def colrun(self, event = None):
        #Dedicated button for running random color on the seconds running
        
        self.sdat()
        if CalGui.RUN:
            self.stob.configure(text = 'Run Color')
            CalGui.RUN = False
        else:
            self.stob.configure(text = 'Stop Color')
            CalGui.RUN = True

    def setcb(self, event = None):
        # This for key event binding only. On checkbox set date.
        
        if not self.gset.get():
            self.gset.set(1)
        else:
            self.gset.set(0)
        self.scald()
        
    def scald(self, event = None):
        #Setting year, month and day as default on set date check button.
         
        self.label.config(font = 'verdana 20 bold')
        if self.gset.get():
            self.sd.clear()
            self.sd.extend((self.sc1.get(), self.sc2.get(), self.sc3.get()))        
            if self.cald():
                self.lvar.set(self.cald())
            else:
                self.tn()
        else:
            self.sd.clear()
            if self.cald():
                self.lvar.set(self.cald())
            else:
                self.tn()
                
    def sdat(self, event = None):
        #Set the scale to default values of year, month and day.
        
        if self.gset.get():
            self.sc1.set(self.sd[0])    
            self.sc2.set(self.sd[1])
            self.sc3.set(self.sd[2])
        else:
            self.sc1.set(dt.date.today().year)    
            self.sc2.set(dt.date.today().month)
            self.sc3.set(dt.date.today().day)

    def recdat(self, event = None):
        #Saving event for specific date that has been set, and recorded.
        
        import os
        dirc = os.getcwd()
        if 'Caldata' == dirc[dirc.rfind("\\")+1:]:
            file = simpledialog.askstring('CalGui', 'File name create?')
            if file:
                if f'{file}.txt' in os.listdir():
                    if self.sd:
                        ev = simpledialog.askstring('CalGui', 'Events?')
                        if ev:
                            with open(f'{file}.txt', 'a') as wr:
                                wr.write(f'{(self.sd, ev)}\n')
                        else:
                            messagebox.showinfo('CalGui', 'Must write event!')
                    else:
                        messagebox.showwarning('CalGui', 'No Set Date found!')
                else:
                    if self.sd:
                        ev = simpledialog.askstring('CalGui', 'Events?')
                        if ev:
                            with open(f'{file}.txt', 'w') as wr:
                                wr.write(f'{(self.sd, ev)}\n')
                        else:
                            messagebox.showinfo('CalGui', 'Must write event!')
                    else:
                        messagebox.showwarning('CalGui', 'No Set Date found!')
            else:
                messagebox.showwarning('CalGui', 'Saving Event aborted!')
        else:
            messagebox.showwarning('CalGui', 'Nothing found!!!')
            
    def loaddat(self, event = None):
        #Load a date base on the event that has been saved.
        
        if CalGui.TOP is None:
            import os
            dirc = os.getcwd()
            if 'Caldata' == dirc[dirc.rfind("\\")+1:]:
                fi = ''
                files = [i for i in os.listdir() if '.' in i]
                if files:
                    def chosenfile(event = None):
                        if ev.get():
                            o=[]
                            self.txfile = ev.get()
                            with open(f'{self.txfile}', 'r') as rd:
                                lg = rd.readlines()
                            for i,j in enumerate(lg):
                                o.append(f'{i+1}: {eval(j[:-1])[1]}')
                            cbbx.config(state = 'normal')
                            cbbx.delete(0,END)
                            cbbx['values'] = o
                            cbbx.current(0)
                            cbbx.config(state = 'readonly')
                            butcho.config(state = 'disable')
                            tl.unbind_all('<c>')
                            buteve.config(state = 'normal')
                            tl.bind_all('<c>', chosenevent)
                            
                    def chosenevent(event = None):
                        ask = messagebox.askyesno('CalGui', '"Yes" show event date, "No" delete event/file')
                        if ask:
                            for i in self.bt:
                                if isinstance(self.bt[i], tuple):
                                    self.bt[i][0].config(state = 'normal')
                                    self.bt[i][0].bind_all(self.bt[i][1], self.bt[i][2])
                                else:
                                    if i != 'text':
                                        self.bt[i].config(state = 'normal')                            
                            with open(f'{self.txfile}', 'r') as rd:
                                lg = rd.readlines()
                            chdat = eval(ev.get()[:ev.get().find(':')])
                            if self.gset.get():
                                self.gset.set(0)
                                self.scald()
                            self.sd = eval(lg[chdat-1][:-1])[0]
                            self.sc3.config(to = ChoCal.monrang(self.sd[0], self.sd[1]))
                            self.gset.set(1)
                            self.sdat()
                            self.gset.set(0)
                            self.scald()
                            y, m, d =eval(lg[chdat-1][:-1])[0]
                            messagebox.showinfo(f'{self.txfile[:-4]}: {dt.date(y,m,d)}',
                                                f'{eval(lg[chdat-1][:-1])[1]}')                                
                            for i in self.bt:
                                if isinstance(self.bt[i], tuple):
                                    self.bt[i][0].config(state = 'disable')
                                    self.bt[i][0].unbind_all(self.bt[i][1])
                                else:
                                    self.bt[i].config(state = 'disable')
                        else:
                            ask = messagebox.askyesno('CalGui', '"Yes"Remove event, "No" remove file')
                            if ask:
                                with open(f'{self.txfile}', 'r') as rd:
                                    lg = rd.readlines()
                                if lg:
                                    chdat = eval(ev.get()[:ev.get().find(':')])
                                    del lg[chdat-1]
                                    if lg:
                                        o = []
                                        for i,j in enumerate(lg):
                                            o.append(f'{i+1}: {eval(j[:-1])[1]}')
                                        cbbx.config(state = 'normal')
                                        cbbx.delete(0,END)
                                        cbbx['values'] = o
                                        cbbx.current(0)
                                        cbbx.config(state = 'readonly')                                
                                        with open(f'{self.txfile}', 'w') as wr:
                                            wr.writelines(lg)
                                    else:
                                        try:
                                            os.remove(f'{self.txfile}')
                                            files = [i for i in os.listdir() if '.' in i]
                                            cbbx.config(state = 'normal')
                                            cbbx.delete(0,END)
                                            cbbx['values'] = files
                                            cbbx.current(0)
                                            cbbx.config(state = 'readonly')                                
                                            buteve.config(state = 'disable')
                                            tl.unbind_all('<c>')
                                            butcho.config(state = 'normal')
                                            tl.bind_all('<c>', chosenfile)
                                        except:
                                            chc()                                        
                            else:
                                try:
                                    os.remove(f'{self.txfile}')
                                    files = [i for i in os.listdir() if '.' in i]
                                    cbbx.config(state = 'normal')
                                    cbbx.delete(0,END)
                                    cbbx['values'] = files
                                    cbbx.current(0)
                                    cbbx.config(state = 'readonly')                                
                                    buteve.config(state = 'disable')
                                    tl.unbind_all('<c>')
                                    butcho.config(state = 'normal')
                                    tl.bind_all('<c>', chosenfile)
                                except:
                                    chc()
                                    
                    def chc(event = None):
                        CalGui.TOP = None
                        tl.unbind_all("<q>")
                        tl.unbind_all("<Q>")
                        tl.unbind_all('<f>')
                        tl.unbind_all('<c>')
                        for i in self.bt:
                            if isinstance(self.bt[i], tuple):
                                self.bt[i][0].config(state = 'normal')
                                self.bt[i][0].bind_all(self.bt[i][1], self.bt[i][2])
                            else:
                                if i != 'text':
                                    self.bt[i].config(state = 'normal')             
                        tl.destroy()
                        
                    def cbf(event = None):
                        cbbx.focus_set()
                            
                    for i in self.bt:
                        if isinstance(self.bt[i], tuple):
                            self.bt[i][0].config(state = 'disable')
                            self.bt[i][0].unbind_all(self.bt[i][1])
                        else:
                            self.bt[i].config(state = 'disable')
                    tl = Toplevel()
                    tl.resizable(False, False)
                    tl.wm_attributes("-topmost", 1)
                    tl.title('Choose Event')
                    tl.overrideredirect(True)
                    tl.bind_all("<q>",chc)
                    tl.bind_all("<Q>",chc)
                    tl.bind_all('<c>', chosenfile)
                    label = Label(tl, text = 'Please select recorded event')
                    label.pack(pady = 5)
                    ev = StringVar()
                    cbbx = ttk.Combobox(tl, textvariable = ev, font= 'Helvetica 12 bold')
                    cbbx['values'] = files
                    cbbx.current(0)
                    cbbx.config(state = 'readonly')
                    cbbx.pack(padx = 5)
                    tl.bind_all('<f>', cbf)
                    fr = Frame(tl)
                    fr.pack()
                    butcho = Button(fr, text = 'Choose File', command = chosenfile)
                    butcho.pack(side = LEFT, pady = 5)
                    buteve = Button(fr, text = 'Choose event', command = chosenevent)
                    buteve.pack(side = RIGHT, pady = 5)
                    buteve.config(state = 'disable')
                    CalGui.TOP = tl
                    cbbx.focus_set()
                else:
                    messagebox.showwarning('CalGui', 'No Record!!!')
            else:
                messagebox.showwarning('CalGui', 'Nothing found!!!')
                    
    def rem(self, event = None):
        #Making reminder like alarm, but a window will pop-up.
        
        if not self.rdr:
            self.entry.config(background = 'green', foreground = 'white')
            remi = simpledialog.askstring("Reminder",'What to remind?')
            wak = simpledialog.askinteger("Reminder", 'Interval?(in seconds)')
            if remi and wak:
                set = dt.datetime.timestamp(dt.datetime.now().replace(microsecond=0)) + wak
                self.rdr.extend((remi,set))
                self.root.after(1000,self.rem)
            else:
                self.entry.config(background = 'yellow', foreground = 'black')
                messagebox.showinfo("Reminder", 'Reminder is aborted!!!')    
        else:
            import winsound
            tm = dt.datetime.timestamp(dt.datetime.today().replace(microsecond=0))
            if tm >= self.rdr[1]:
                winsound.Beep(800,350)
                messagebox.showinfo("Reminder", 
                                    f'{dt.datetime.fromtimestamp(tm)}\nReminder:\n{self.rdr[0]}')
                self.entry.config(background = 'yellow', foreground = 'black')
                self.rdr = []
            else:
                self.root.after(1000,self.rem)

    def calcd(self, event = None):
        #Calculate the days left that represent years, months, weeks, and days.
        
        if CalGui.SELF:
            CalGui.SELF = False
            self.label.config(font = 'verdana 15 bold')
            if self.sd:
                de = dt.date(self.sc1.get(), 
                self.sc2.get(), self.sc3.get()) - dt.date(self.sd[0], 
                self.sd[1], self.sd[2])
            else:
                de = dt.date(self.sc1.get(), self.sc2.get(), self.sc3.get()) - dt.date.today()
            td = de.days
            pt = {365:0, 30:0, 7:0, 1:0}
            te = 0
            for i in pt:
                if td//i:
                    pt[i]=td//i
                    td = td-(i*pt[i])
            td = sum([k*l for k,l in pt.items()])
            
            assert td == de.days
            
            if td:
                nt = ['years', 'months', 'weeks', 'days']
                tm = list(pt)
                pt = {nt[i]:pt[tm[i]] for i in range(4) if pt[tm[i]]}
                if td >= 7 or td < -1:
                    sent = f"{td} days left and equal to: "
                    for i , j in pt.items():
                        if j > 1 or j < -1:
                            sent += ''.join(f'{j} {i}, ')
                        else:
                            sent += ''.join(f'{j} {str(i)[:-1]}, ')
                    self.lvar.set(sent[:-2]+'.')
                else:
                    if td > 1:
                        self.lvar.set(f"{td} days left.")
                    else:
                        self.lvar.set(f"{td} day left.")
            else:
                self.label.config(font = 'verdana 20 bold')
                messagebox.showinfo('CalGui', 'No days left!')
            
        else:
            CalGui.SELF = True
            self.label.config(font = 'verdana 20 bold')
            self.lvar.set(self.cald())
            

    def colorh(self, event = None):
        #Changing color on the highlight and the foreground.
        
        from CreateColors import create_colors as cco
        import os
        if not CalGui.TOP:    
            if not 'tkcols.txt' in os.listdir():
                cco()
                with open('tkcols.txt') as cols:
                    lc = eval(cols.read())
            else:
                with open('tkcols.txt') as cols:
                    lc = eval(cols.read())
                
            def high(event = None):
                try:
                    if not rt1.get():
                        spb.configure(background = lc[lc.index(spb.get())])
                        self.text.tag_config('hg', background = lc[lc.index(spb.get())])
                    else:
                        spb.configure(foreground = lc[lc.index(spb.get())])
                        self.text.tag_config('hg', foreground = lc[lc.index(spb.get())])
                except:
                    pass
                
            def chc(event = None):
                CalGui.TOP = None
                cco()
                tl.unbind_all("<q>")
                tl.unbind_all("<Q>")
                tl.unbind_all('<f>')
                tl.unbind_all('<Control-t>')
                tl.unbind_all('<Control-g>')
                for i in self.bt:
                    if isinstance(self.bt[i], tuple):
                        self.bt[i][0].config(state = 'normal')
                        self.bt[i][0].bind_all(self.bt[i][1], self.bt[i][2])
                    else:
                        if i != 'text':
                            self.bt[i].config(state = 'normal')                
                tl.destroy()
            
            def fcs(event = None):
                if event.keysym == 'f':
                    spb.focus()
                elif event.keysym == 't':
                    rt1.set(False)
                elif event.keysym == 'g':
                    rt1.set(True)
                    
            for i in self.bt:
                if isinstance(self.bt[i], tuple):
                    self.bt[i][0].config(state = 'disable')
                    self.bt[i][0].unbind_all(self.bt[i][1])
                else:
                    self.bt[i].config(state = 'disable')            
            tl = Toplevel()
            tl.resizable(False, False)
            tl.wm_attributes("-topmost", 1)
            tl.title('Color Highlight')
            tl.overrideredirect(True)
            tl.bind_all("<q>",chc)
            tl.bind_all("<Q>",chc)
            tl.bind_all('<f>', fcs)
            tl.bind_all('<Control-t>', fcs)
            tl.bind_all('<Control-g>', fcs)            
            spb = Spinbox(tl, command= high, values=lc, font= 'Helvetica 20 bold')
            spb.pack(side = LEFT, padx = 5)
            rt1 = BooleanVar()
            rbt1 = ttk.Radiobutton(tl, text = 'H', variable = rt1, value = False)
            rbt2 = ttk.Radiobutton(tl, text = 'F', variable = rt1, value = True)
            rbt1.pack(pady = 2, padx = 5)
            rbt2.pack(pady = 2, padx = 5)
            CalGui.TOP = tl
            spb.focus_set()
 
    def calbg(self, event = None):
        #Changing colors for the Calendar background and foreground(the text).
        
        from CreateColors import create_colors as cco
        import os
        if not CalGui.TOP:
            if not 'tkcols.txt' in os.listdir():
                cco()
                with open('tkcols.txt') as cols:
                    lc = eval(cols.read())
            else:
                with open('tkcols.txt') as cols:
                    lc = eval(cols.read())
                    
            def clc(event = None):
                try:
                    if not rt2.get():
                        spb2.configure(background = lc[lc.index(spb2.get())])
                        self.text.config(background = lc[lc.index(spb2.get())])
                    else:
                        spb2.configure(foreground = lc[lc.index(spb2.get())])
                        self.text.configure(foreground = lc[lc.index(spb2.get())])
                except:
                    pass
            
            def chc(event = None):
                CalGui.TOP = None
                cco()
                tl.unbind_all("<q>")
                tl.unbind_all("<Q>")
                tl.unbind_all('<f>')
                tl.unbind_all('<Control-t>')
                tl.unbind_all('<Control-g>')
                tl.grab_release()
                for i in self.bt:
                    if isinstance(self.bt[i], tuple):
                        self.bt[i][0].config(state = 'normal')
                        self.bt[i][0].bind_all(self.bt[i][1], self.bt[i][2])
                    else:
                        if i != 'text':
                            self.bt[i].config(state = 'normal')                
                tl.destroy()
            
            def fcs(event = None):
                if event.keysym == 'f':
                    spb2.focus()
                elif event.keysym == 't':
                    rt2.set(False)
                elif event.keysym == 'g':
                    rt2.set(True)
            
            for i in self.bt:
                if isinstance(self.bt[i], tuple):
                    self.bt[i][0].config(state = 'disable')
                    self.bt[i][0].unbind_all(self.bt[i][1])
                else:
                    self.bt[i].config(state = 'disable')
            tl = Toplevel()
            tl.resizable(False, False)
            tl.wm_attributes("-topmost", 1)
            tl.title('Color Background')
            tl.overrideredirect(True)
            tl.bind_all("<q>", chc)
            tl.bind_all("<Q>", chc)
            tl.bind_all('<f>', fcs)
            tl.bind_all('<Control-t>', fcs)
            tl.bind_all('<Control-g>', fcs)
            spb2 = Spinbox(tl, values = lc, command= clc, font= 'Helvetica 20 bold')
            spb2.pack(side = LEFT, padx = 5)
            rt2 = BooleanVar()
            cbr1 = ttk.Radiobutton(tl, text = 'B', variable = rt2, value = False)
            cbr2 = ttk.Radiobutton(tl, text = 'F', variable = rt2, value = True)
            cbr1.pack(pady = 2, padx = 5)
            cbr2.pack(pady = 2, padx = 5)
            CalGui.TOP = tl
            spb2.focus_set()
            
    def savs(self, event = None):
        #Saving the color theme that has been set.
        
        import json
        import os
        
        dirc = os.getcwd()
        if 'Calset' in os.listdir():
            os.chdir('Calset')
        else:
            os.mkdir('Calset')
            os.chdir('Calset')            
        ask = messagebox.askyesno('CalGui', 'Save setting color?')
        if ask:
            if 'stc.txt' in os.listdir():
                ask = messagebox.askyesno('CalGui', 'Adding more setting?')
                if ask:
                    std = {}
                    with open('stc.txt') as sett:
                        gj  = json.load(sett)
                        std = {'Highlight': self.text.tag_cget("hg","background"),
                               'Foreground': self.text.tag_cget("hg","foreground"),
                               'Label': str(self.label.cget('foreground')),
                               'CB': str(self.text.cget('background')),
                               'CF': str(self.text.cget('foreground'))
                               }
                        gj['stc'].append(std)
                    with open('stc.txt', 'w') as sett:
                        json.dump(gj,sett)
                    os.chdir(dirc)
                    
                else:
                    os.chdir(dirc)
                    messagebox.showinfo('CalGui', 'Saving setting aborted!')
            else:
                std = {}
                with open('stc.txt', 'w') as sett:
                    std['stc'] = []
                    std['stc'].append({'Highlight': self.text.tag_cget("hg","background"),
                           'Foreground': self.text.tag_cget("hg","foreground"),
                           'Label': str(self.label.cget('foreground')),
                           'CB': str(self.text.cget('background')),
                           'CF': str(self.text.cget('foreground'))
                           })
                    json.dump(std, sett)
                os.chdir(dirc)
        else:
            if 'stc.txt' in os.listdir():
                with open('stc.txt') as sett:
                    gj = json.load(sett)
                    
                def cbf(event = None):
                    cbbx.focus_set()
                
                def chosensett(event = None):
                    rw = int(ev.get()[:ev.get().find(':')])
                    with open('stc.txt') as sett:
                        rd = json.load(sett)
                    std = rd['stc'][rw]
                    for i in self.bt:
                        if isinstance(self.bt[i], tuple):
                            self.bt[i][0].config(state = 'normal')
                            self.bt[i][0].bind_all(self.bt[i][1], self.bt[i][2])
                        else:
                            if i != 'text':
                                self.bt[i].config(state = 'normal')                    
                    self.text.tag_config('hg', background = std['Highlight'], 
                                         foreground= std['Foreground'])
                    self.text.config(background = std['CB'], foreground= std['CF'])
                    self.label.config(foreground = std['Label'])
                    for i in self.bt:
                        if isinstance(self.bt[i], tuple):
                            self.bt[i][0].config(state = 'disable')
                            self.bt[i][0].unbind_all(self.bt[i][1])
                        else:
                            self.bt[i].config(state = 'disable')
                    hback = self.text.tag_cget("hg","background")
                    hfore = self.text.tag_cget("hg","foreground")
                    labc = self.label.cget("foreground")
                    cback = self.text.cget("background")
                    cfore = self.text.cget("foreground")
                    messagebox.showinfo('Info setting Now', 
                    f'Highlight: {hback}\nForeground: {hfore}\nLabel Color: {labc}\nCalBackground: {cback}\nCalForeground: {cfore}')
                
                def delsett(event = None):
                    rw = int(ev.get()[:ev.get().find(':')])
                    with open('stc.txt') as sett:
                        rd = json.load(sett)
                    if len(rd['stc']) > 1:
                        del rd['stc'][rw]
                        with open('stc.txt', 'w') as sett:
                            json.dump(rd, sett)
                        cbbx.config(state = 'normal')
                        cbbx.delete(0, END)
                        cbbx['values'] = [f'{i}: {rd["stc"][i]}' for i in range(len(rd['stc']))]
                        cbbx.current(0)
                        cbbx.config(state = 'readonly')
                    else:
                        os.remove('stc.txt')
                        chc()
                        
                def chc(event = None):
                    CalGui.TOP = None
                    tl.unbind_all("<q>")
                    tl.unbind_all("<Q>")
                    tl.unbind_all('<f>')
                    tl.unbind_all('<c>')
                    tl.unbind_all('<d>')
                    for i in self.bt:
                        if isinstance(self.bt[i], tuple):
                            self.bt[i][0].config(state = 'normal')
                            self.bt[i][0].bind_all(self.bt[i][1], self.bt[i][2])
                        else:
                            if i != 'text':
                                self.bt[i].config(state = 'normal')
                    os.chdir(dirc)
                    tl.destroy()
                
                for i in self.bt:
                    if isinstance(self.bt[i], tuple):
                        self.bt[i][0].config(state = 'disable')
                        self.bt[i][0].unbind_all(self.bt[i][1])
                    else:
                        self.bt[i].config(state = 'disable')
                        
                tl = Toplevel()
                tl.resizable(False, False)
                tl.wm_attributes("-topmost", 1)
                tl.title('Choose Event')
                tl.overrideredirect(True)
                tl.bind_all("<q>", chc)
                tl.bind_all("<Q>", chc)
                tl.bind_all('<c>', chosensett)
                tl.bind_all('<d>', delsett)
                label = Label(tl, text = 'Please select recorded Setting')
                label.pack(pady = 5)
                ev = StringVar()
                cbbx = ttk.Combobox(tl, textvariable = ev, font= 'Helvetica 12 bold')
                cbbx['values'] = [f'{i}: {gj["stc"][i]}' for i in range(len(gj['stc']))]
                cbbx.current(0)
                cbbx.config(state = 'readonly')
                cbbx.pack(padx = 5)
                tl.bind_all('<f>', cbf)
                fr = Frame(tl)
                fr.pack()
                butcho = Button(fr, text = 'Select setting', command = chosensett)
                butcho.pack(side = LEFT, pady = 5)
                buteve = Button(fr, text = 'Delete setting', command = delsett)
                buteve.pack(side = RIGHT, pady = 5)
                CalGui.TOP = tl
                cbbx.focus_set()
            else:
                messagebox.showinfo('CalGui', 'No colors saved yet!')
                os.chdir(dirc)
                
def main():
    #Starting the app.
    
    import os
    if 'Caldata' in os.listdir():
        os.chdir('Caldata')
    else:
        os.mkdir('Caldata')
        os.chdir('Caldata')
    root =  Tk()
    start = CalGui(root)
    root.update()   
    root.mainloop()
    
if __name__ == "__main__":
    main()