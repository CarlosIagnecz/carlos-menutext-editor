import tkinter as tk
from tkinter import filedialog
import sys

ui = tk.Tk()
ui.title("Carlos' menutext.bin Editor")

tbl = {}
tblinv = {} #I dont want to make a process intensive value 2 key algorithm

#menutext Field
menutext = None
mtlabel = None

#lvl_ord Field
lolabel = None
lvlord = []
lvllbls = []

#filename for hex
filename = "/"
filename1 = "/"
filename2 = "/"

def savemenutext():
    global tblinv
    global menutext
    global filename
    global filename1
    if filename=="/":
        print("Can't save menutext, no TBL file loaded.")
        return None
    if filename1=="/":
        print("Can't save menutext, no BIN file loaded.")
        return None
    hexstring = ""
    text = menutext.get("1.0",'end-1c')
    for i in text:
        try:
            hexstring += tblinv[i]
        except KeyError: #Prevent invalid characters
            pass
    hexdata = bytes.fromhex(hexstring)
    print("Output:")
    for i in range(1,len(hexstring)//48-1): #Output
        print(hexstring[(i-1)*48:i*48])

    with open(file=filename1,mode='wb') as file:
        file.write(hexdata)
    print(f"Saved successfully to {filename1}")

def savelspoint():
    global lvlord
    global filename2
    if filename2=="/":
        print("Can't save ls-point/lvl_ord, no BIN file loaded.")
        return None
    hexstring = ""
    for i in range(len(lvlord)):
        txt = lvlord[i].get("1.0",'end-1c')
        if txt != "SPECIAL":
            hx = str(hex(int(txt)))[2:]
            if len(hx)==1:
                hx = "0"+hx
            hexstring += hx
            
        else:
            hexstring += "80"
    print(hexstring)
    hexdata = bytes.fromhex(hexstring)
    with open(file=filename2,mode='wb') as file:
        file.write(hexdata)
    print(f"Saved successfully to {filename2}")

def loadmenutext():
    global filename
    global filename1
    global tbl
    global menutext
    global mtlabel
    global ui

    if len(tbl)==0:
        print("Can't load menutext, no TBL file loaded.")
        return None
    filename = filedialog.askopenfilename(initialdir = filename,title = "Select a File",filetypes = (("BIN files","*.bin*"),("All file types","*.*")))
    filename1 = filename
    with open(file=filename,mode='rb') as file:
        hexdata = str(file.read().hex())

    tbuff = [tbl[hexdata[i:i+2]] for i in range(0, len(hexdata), 2)]
    text = ""
    for i in range(len(tbuff)):
        if i%24==0 and i!=0:
            text += '\n'
        text += tbuff[i]
    if menutext:
        menutext.destroy()
    if mtlabel:
        mtlabel.destroy()
    menutext = tk.Text(ui,width=24,height=len(hexdata)//48)
    menutext.configure(font = ('Consolas')) 
    menutext.insert(tk.END, text) #inserts new value assigned by 2nd parameter

    mtlabel = tk.Label(ui, text="menutext.bin",font=('Consolas'),width=24,height=1)
    mtlabel.pack()
    menutext.pack()
    
def loadlspoint():
    global filename
    global filename2
    global lolabel
    global lvlord
    global lvllbls
    global ui

    filename = filedialog.askopenfilename(initialdir = filename,title = "Select a File",filetypes = (("BIN files","*.bin*"),("All file types","*.*")))
    filename2 = filename
    
    with open(file=filename,mode='rb') as file:
        hexdata = file.read().hex()
    tbuff = [int(hexdata[i:i+2],16) for i in range(0, len(hexdata), 2)]
    if lolabel:
        lolabel.destroy()
    if len(lvlord):
        for i in lvlord:
            i.destroy()
        lvlord = []
    if len(lvllbls):
        for i in lvllbls:
            i.destroy()
        lvllbls = []

    lolabel = tk.Label(ui, text="ls-point.bin/lvl_ord.bin",font=('Consolas'),width=24,height=1)
    lolabel.pack()
    
    for i in range(len(tbuff)//2):
        lvllbls.append(tk.Frame(ui))
        
        lvllbls.append(tk.Label(lvllbls[len(lvllbls)-1], text="ZONE",font=('Consolas'),width=5,height=1))
        lvllbls[len(lvllbls)-1].pack(side=tk.LEFT)
        
        lvlord.append(tk.Text(lvllbls[len(lvllbls)-2],width=7,height=1))
        lvlord[len(lvlord)-1].configure(font = ('Consolas'))
        if tbuff[i*2] == 128:
            lvlord[len(lvlord)-1].insert(tk.END, 'SPECIAL')
        else:
            lvlord[len(lvlord)-1].insert(tk.END, tbuff[i*2]) #inserts new value assigned by 2nd parameter
        lvlord[len(lvlord)-1].pack(side=tk.LEFT)

        lvllbls.append(tk.Label(lvllbls[len(lvllbls)-2], text="ACT",font=('Consolas'),width=4,height=1))
        lvllbls[len(lvllbls)-1].pack(side=tk.LEFT)
        
        lvlord.append(tk.Text(lvllbls[len(lvllbls)-3],width=8,height=1))
        lvlord[len(lvlord)-1].configure(font = ('Consolas')) 
        lvlord[len(lvlord)-1].insert(tk.END, tbuff[i*2+1]) #inserts new value assigned by 2nd parameter
        lvlord[len(lvlord)-1].pack(side=tk.LEFT)

        lvllbls[len(lvllbls)-3].pack()
            
    
def loadtbl():
    global tbl
    global tblinv
    global filename

    filename = filedialog.askopenfilename(initialdir = filename,title = "Select a File",filetypes = (("TBL files","*.tbl*"),("All file types","*.*")))
    with open(file=filename,mode='r') as file:
        split = file.read().split("\n")
    tbl = dict((i.split("=")[0].lower(),i.split("=")[1]) for i in split)
    tblinv = dict((i.split("=")[1],i.split("=")[0].lower()) for i in split)

def about():
    global menu
    top= tk.Toplevel(menu)
    top.title("About")
    tk.Label(top, text= "Carlos' menutext Editor is a program to help\n"+
             "edit the Level Select of Sonic 1 featuring:\n"+
             "- menutext editing by .tbl & .bin\n"+
             "-lvl_ord/lvl_ord.bin editing by .bin\n\n"+
             "Disassembly by Hivebrain assisted by drx,\n"+
             "Korama, Lightning, Magus, Nemesis, Stealth\n"+
             "Sonic The Hedgehog was developed SEGA",
             font=('Consolas'),height=10).pack()

def plshelp():
    global menu
    top= tk.Toplevel(menu)
    top.title("Help")
    tk.Label(top, text="To edit the menu, you must use the appended\n"+
             "menutext.tbl for character asignment, the menutext.bin\n"+
             "of your disasm that contains the data and ls-point.bin\n"+
             "of your disasm that contains the actual level its going to",
             font=('Consolas'),height=10).pack()

#Configure Menu Tab
menu = tk.Menu(ui)
ui.config(menu=menu)

#File Menu
filemenu = tk.Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Open .tbl', command=loadtbl)
filemenu.add_command(label='Open menutext.bin', command=loadmenutext)
filemenu.add_command(label='Save menutext.bin', command=savemenutext)
filemenu.add_separator()
filemenu.add_command(label='Open ls-point.bin/lvl_ord.bin', command=loadlspoint)
filemenu.add_command(label='Save ls-point.bin/lvl_ord.bin', command=savelspoint)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=ui.destroy)

#Help Menu
helpmenu = tk.Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=about)
helpmenu.add_command(label='HELP!', command=plshelp)

ui.mainloop()
