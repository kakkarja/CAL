# Author ideas from KarJa, with many helps from StackOverflow, GeeksforGeeks, and many more.
# Sorry i cannot mention all, as i move along building this app, i looked up in website, 
# and did not save the website. 
# Many apologize from me. 
# Thank you all so much for all, for your dedication making website the source of sharing.
# I dedicate this app as well for learning and free to be use and copied for better. 

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog, messagebox
from tkinter.font import Font
import calendar as cal
import pandas as pd
import datetime as dt
import time
from CreateColors import create_colors as cco

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
        mo = list(i for i in list(cal.month_name) if i != '')
        monthdict = { i:d for i, d in zip(mo,cm)}
        days = list(i for i in list(cal.weekheader(1)) if i != ' ')
        df = pd.DataFrame(monthdict[mo[monthy]],
        index = [f'Week {i+1}' for i in range(len(monthdict[mo[monthy]]))],
        columns= days)
        df = df.replace(0, ' ')
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
        
        #This geometry is to set fit in my tablet, which div by 17.
        self.wwidth = self.root.winfo_reqwidth()
        self.wheight = self.root.winfo_reqheight()
        self.pwidth = int(self.root.winfo_screenwidth()/17 - self.wwidth/17)
        self.pheight = int(self.root.winfo_screenheight()/17 - self.wheight/17)
        self.root.geometry(f"+{self.pwidth}+{self.pheight}")
        self.root.overrideredirect(True)
        self.root.config(background = 'teal')
        
        self.sc1 = Scale(self.root, from_=1800, to=2300, orient = HORIZONTAL, length = 2293, 
                    command = self.ccal, background = 'gold')
        self.sc1.set(dt.datetime.today().year)
        self.sc1.pack(pady = 5)
        self.sc2 = Scale(self.root, from_=1, to=12, orient = HORIZONTAL, length = 2293, 
                    command = self.ccal, background = 'gold')
        self.sc2.set(dt.datetime.today().month)
        self.sc2.pack(pady = 5)
        self.sc3 = Scale(self.root, from_=1, to=31, orient = HORIZONTAL, length = 2293, 
                    command = self.ccal, background = 'gold')
        self.sc3.set(dt.datetime.today().day)
        self.sc3.pack(pady = 5)
        self.text = Text(self.root, width = 48, height = 8, font = 'courier 20 bold', 
                    background ='light blue', foreground='indigo', relief = RAISED)
        self.text.tag_add('bd', '1.0', END)
        self.text.tag_config('bd', justify = 'center')
        self.text.tag_config('thg', background = 'dark orange', foreground = 'black')
        self.text.tag_config('hg', background = 'dark slate blue', foreground = 'white')
        self.text.pack(pady = 3)
        self.gset = IntVar()
        self.cb = Checkbutton(self.root, text = 'Set date', variable = self.gset, command=self.scald,
                         background = 'teal', highlightthickness = 0, bd = 0,
                         fg = 'blue', activebackground = 'teal', activeforeground = 'white')
        self.cb.pack(pady = 5)
        self.lvar = StringVar()
        self.label = ttk.Label(root, textvariable = self.lvar, font = 'times 20 bold', 
                          background = 'teal', foreground = 'white' )
        self.label.pack(pady = 5)
        
        self.frb = ttk.Frame(self.root)
        self.frb.pack(pady = 7)
        self.lb = Button(self.frb, text = 'Load Set Date', command = self.loaddat, 
                         bg = 'yellow', fg = 'black',
                         activebackground = 'green', activeforeground = 'white',
                         highlightthickness = 0, bd = 0)
        self.lb.pack(side = LEFT)
        self.stb = Button(self.frb, text = 'Current Date/Set', command = self.sdat, 
                          bg = 'yellow', fg = 'black', activebackground = 'green', 
                          activeforeground = 'white',highlightthickness = 0, bd = 0)
        self.stb.pack(side = LEFT)
        self.entry = Button(self.frb, text = 'Reminder', command = self.rem, 
                            bg = 'yellow', fg = 'black', activebackground = 'green', 
                            activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.entry.pack(side = LEFT)
        self.cdb = Button(self.frb, text = 'Calculate', command = self.calcd, 
                          bg = 'yellow', fg = 'black', activebackground = 'green', 
                          activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.cdb.pack(side = LEFT)
        self.stob = Button(self.frb, text = 'Run Color', command = self.colrun, 
                           bg = 'yellow', fg = 'black', activebackground = 'green', 
                           activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.stob.pack(side = LEFT)
        self.recb = Button(self.frb, text = 'Record Set Date', command = self.recdat, 
                         bg = 'yellow', fg = 'black', activebackground = 'green', 
                         activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.recb.pack(side = LEFT)
        self.hcbb = Button(self.frb, text = 'Highlight', command = self.colorh, 
                           bg = 'yellow', fg = 'black', activebackground = 'green', 
                           activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.hcbb.pack(side = LEFT)
        self.clbcb = Button(self.frb, text = 'Cal Bg Color', command = self.calbg, 
                            bg = 'yellow', fg = 'black', activebackground = 'green', 
                            activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.clbcb.pack(side = LEFT)
        self.setb = Button(self.frb, text = 'Saving Colors', command = self.savs, 
                           bg = 'yellow', fg = 'black', activebackground = 'green', 
                           activeforeground = 'white', highlightthickness = 0, bd = 0)
        self.setb.pack(side = LEFT)
        self.but = Button(self.frb, text = 'Close', command = root.destroy, 
                         bg = 'blue', fg = 'white', activebackground = 'black', 
                         activeforeground = 'white',highlightthickness = 0, bd = 0)
        self.but.pack(side = LEFT)
        
    def ccal(self, event = None):
        #Creating Calendar according to the scales of the years, months and days.
        
        self.label.config(font = 'times 20 bold')
        cc = ChoCal(self.sc1.get(), self.sc2.get(), self.sc3.get())
        self.sc3.config(to = cc.monrang(self.sc1.get(), self.sc2.get()))
        self.text.config(state = 'normal')
        self.text.delete('1.0', END)
        self.text.insert(END, cc.createcal(), 'bd')
        self.tdcol()
        sch1 = self.text.search(str(self.sc3.get()),'3.0',END)
        while True:        
            if int(sch1[sch1.index('.')+1:]) > 6: 
                if len(str(self.sc3.get())) > 1:
                    sch2 = f"{sch1[:sch1.index('.')]}.{str(eval(sch1[sch1.index('.')+1:])+2)}"
                    break
                else:
                    sch2 = f"{sch1[:sch1.index('.')]}.{str(eval(sch1[sch1.index('.')+1:])+1)}"
                    break
            adn = f"{sch1[:sch1.index('.')]}.{str(eval(sch1[sch1.index('.')+1:])+1)}"
            sch1 = self.text.search(str(self.sc3.get()),adn,END)
        gt = self.text.get(sch1,sch2)
        self.text.delete(sch1, sch2)
        self.text.insert(sch1,gt, ('hg'))
        self.text.config(state = 'disabled')
        if self.cald():
            self.lvar.set(self.cald())
        else:
            self.tn()

    def tdcol(self):
        #Highlight Color of today's date.
        
        if self.sc2.get() == dt.date.today().month and self.sc1.get() == dt.date.today().year:
            sch1 = self.text.search(str(dt.datetime.today().day),'3.0',END)
            while True:        
                if int(sch1[sch1.index('.')+1:]) > 6: 
                    if len(str(dt.datetime.today().day)) > 1:
                        sch2 = f"{sch1[:sch1.index('.')]}.{str(eval(sch1[sch1.index('.')+1:])+2)}"
                        break
                    else:
                        sch2 = f"{sch1[:sch1.index('.')]}.{str(eval(sch1[sch1.index('.')+1:])+1)}"
                        break
                adn = f"{sch1[:sch1.index('.')]}.{str(eval(sch1[sch1.index('.')+1:])+1)}"
                sch1 = self.text.search(str(dt.datetime.today().day),adn,END)
            gt = self.text.get(sch1,sch2)
            self.text.delete(sch1, sch2)
            self.text.insert(sch1,gt, ('thg'))
    
    def cald(self):
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
        
        if CalGui.RUN:
            self.stob.configure(text = 'Run Color')
            CalGui.RUN = False
        else:
            self.stob.configure(text = 'Stop Color')
            CalGui.RUN = True

    def scald(self, event = None):
        #Setting year, month and day as default on set date check button.
         
        self.label.config(font = 'times 20 bold')
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

    def sdat(self):
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
        if 'Caldata' == dirc[dirc.rfind("/")+1:]:
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
        
        import os
        dirc = os.getcwd()
        if 'Caldata' == dirc[dirc.rfind("/")+1:]:
            fi = ''
            files = [i for i in os.listdir() if '.' in i]
            if files:
                for fil in range(len(files)):
                    fi += ''.join(f'{fil+1}: {files[fil]}\n')
                file = simpledialog.askinteger('CalGui', f'Choose File:\n{fi}')
                if file  and file <= len(files):
                    o=''
                    with open(f'{files[file-1]}', 'r') as rd:
                        lg = rd.readlines()
                        for i,j in enumerate(lg):
                            o+=''.join(f'\n{i+1}:{eval(j[:-1])[1]}')
                    chdat = simpledialog.askinteger('CalGui', f'There are {o}\nrecords, choose:')
                    if chdat:
                        if chdat <= len(lg):
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
                            messagebox.showinfo(f'{files[file-1][:-4]}: {dt.date(y,m,d)}',
                                                f'{eval(lg[chdat-1][:-1])[1]}')
                        else:
                            messagebox.showwarning('CalGui', 'No such Record!!!')
                    else:
                        chdat = simpledialog.askinteger('CalGui', f'Delete, {o}\nrecords, choose:')
                        if chdat:
                            del lg[chdat-1]
                            with open(f'{files[file-1]}', 'w') as wr:
                                wr.writelines(lg)
                        else:
                            ask = messagebox.askyesno('CalGui', 'Remove Records?')
                            if ask:
                                os.remove(f'{files[file-1]}')
                else:
                    messagebox.showwarning('CalGui', 'Please choose a file!!!')    
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
            tm = dt.datetime.timestamp(dt.datetime.today().replace(microsecond=0))
            if tm >= self.rdr[1]:
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
            self.label.config(font = 'times 15 bold')
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
                self.label.config(font = 'times 20 bold')
                messagebox.showinfo('CalGui', 'No days left!')
            
        else:
            CalGui.SELF = True
            self.label.config(font = 'times 20 bold')
            self.lvar.set(self.cald())
            

    def colorh(self, event = None):
        #Changing color on the highlight and the foreground.
        
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
                tl.destroy()
            
            tl = Toplevel()
            tl.overrideredirect(True)
            spb = Spinbox(tl, command= high, values=lc, 
                          font=Font(family='Helvetica', size=20, weight='bold'))
            spb.pack(side = LEFT, padx = 5)
            spb.bind("<q>",chc)
            rt1 = BooleanVar()
            rbt1 = ttk.Radiobutton(tl, text = 'H', variable = rt1, value = False)
            rbt2 = ttk.Radiobutton(tl, text = 'F', variable = rt1, value = True)
            rbt1.pack(pady = 15, padx = 5)
            rbt2.pack(pady = 10, padx = 5)
            CalGui.TOP = tl
            spb.focus_force()
        else:
            CalGui.TOP.lift()
 
    def calbg(self, event = None):
        #Changing colors for the Calendar background and foreground(the text).
        
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
                tl.destroy()
            
            tl = Toplevel()
            tl.overrideredirect(True)
            spb2 = Spinbox(tl, values = lc, command= clc, font=Font(family='Helvetica', 
                           size=20, weight='bold'))
            spb2.pack(side = LEFT, padx = 5)
            spb2.bind("<q>",chc)
            rt2 = BooleanVar()
            cbr1 = ttk.Radiobutton(tl, text = 'B', variable = rt2, value = False)
            cbr2 = ttk.Radiobutton(tl, text = 'F', variable = rt2, value = True)
            cbr1.pack(pady = 15, padx = 5)
            cbr2.pack(pady = 10, padx = 5)
            CalGui.TOP = tl
            spb2.focus_force()
        else:
            CalGui.TOP.lift()

    def savs(self, event = None):
        #Saving the color theme that has been set.
        
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
                ask = messagebox.askyesno('CalGui', 'Overwrite existing setting?')
                if ask:
                    std = {}
                    with open('stc.txt', 'w') as sett:
                        std = {'Highlight': self.text.tag_cget("hg","background"),
                               'Foreground': self.text.tag_cget("hg","foreground"),
                               'Label': str(self.label.cget('foreground')),
                               'CB': str(self.text.cget('background')),
                               'CF': str(self.text.cget('foreground'))
                               }
                        sett.write(f'{std}')
                else:
                    messagebox.showinfo('CalGui', 'Saving setting aborted!')
            else:
                std = {}
                with open('stc.txt', 'w') as sett:
                    std = {'Highlight': self.text.tag_cget("hg","background"),
                           'Foreground': self.text.tag_cget("hg","foreground"),
                           'Label': str(self.label.cget('foreground')),
                           'CB': str(self.text.cget('background')),
                           'CF': str(self.text.cget('foreground'))
                           }
                    sett.write(f'{std}')
        else:
            if 'stc.txt' in os.listdir():
                ask = messagebox.askyesno('CalGui', '"Yes" set color, and "No" to delete setting!')
                if ask:
                    std = dict()
                    with open('stc.txt') as sett:
                        rd = sett.read()
                        std = eval(rd)
                    
                    self.text.tag_config('hg', background = std['Highlight'], 
                                         foreground= std['Foreground'])
                    self.text.config(background = std['CB'], foreground= std['CF'])
                    self.label.config(foreground = std['Label'])
                    
                else:
                    os.remove('stc.txt')
            else:
                messagebox.showinfo('CalGui', 'No colors saved yet!')
        os.chdir(dirc)
        messagebox.showinfo('Info setting Now', 
        f'Highlight: {self.text.tag_cget("hg","background")}\nForground: {self.text.tag_cget("hg","foreground")}\nLabel Color: {self.label.cget("foreground")}\nCalBackground: {self.text.cget("background")}\nCalForeground: {self.text.cget("foreground")}')
        
def main():
    import os
    if 'Caldata' in os.listdir():
        os.chdir('Caldata')
    else:
        os.mkdir('Caldata')
        os.chdir('Caldata')
    root =  Tk()
    start = CalGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()