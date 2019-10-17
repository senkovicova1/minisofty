from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk

#nebude lepsie mat class miesto global premennych?
#ako yariadi5, abz sa otvoril az po kliknuti na subor?
#v buttonoch je place miesto grid ok?

rules = {}
a = Image.open("chocolada.png")
b = Image.open("donut.png")
c = Image.open("zmrzlina.png")
sipka = Image.open("sipka.png")
rulesImg = {}
pravidla = None
slovo = [False, False, False, False, False]

def vyberSubor():
    file_path = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes =(("Text File", "*.txt"),("All Files","*.*")),)
    loadRules(file_path[file_path.rindex("/")+1:])

def zobrazPostup():
    #bude zobrazovať postup
    return

def noveSlovo(slovo):
    #zruší celý postup a koncové slovo - dorobiť
    #zruší počiatočné slovo
    i = 0
    while i < 5:
        if(slovo[i] == False):
            i = i + 1
            break
        else:
            slovo[i].after(0, slovo[i].destroy)
            i = i + 1
    slovo = [False, False, False, False, False]

def StartMove(img, event):
    img.x = event.x
    img.y = event.y

def StopMove(img, event, x, y, render):
    info = img.place_info()
    dx = int(info.get('x'))
    dy = int(info.get('y'))
    print(a, b)
    #mimo prestoru na počiatocne slovo
    if not (5 < dx < 175) & (285 < dy < 335):
        img.place(x=x,y=y)
    else:
        #prvý štvorec
        if 5 < dx < 39:
            #ak uz tam je obraz, vymaze ho
            if slovo[0] != False:
                slovo[0].after(0, slovo[0].destroy)
            slovo[0] = img
            img.place(x=5, y=300)
        #druhy stvorec
        elif 39 < dx < 73:
            #nedovoli polozit obraz, pokial nie je polozeny obraz vo stvorci predtym
            if not slovo[0]:
                img.place(x=x, y=y)
            else:
                # ak uz tam je obraz, vymaze ho
                if slovo[1] != False:
                    slovo[1].after(0, slovo[1].destroy)
                slovo[1] = img
                img.place(x=39, y=300)
        #treti stvorec
        elif 73 < dx < 107:
            #nedovoli polozit obraz, pokial nie je polozeny obraz vo stvorci predtym
            if not slovo[1]:
                img.place(x=x, y=y)
            else:
                # ak uz tam je obraz, vymaze ho
                if slovo[2] != False:
                    slovo[2].after(0, slovo[2].destroy)
                slovo[2] = img
                img.place(x=73, y=300)
        #stvrty stvorec
        elif 107 < dx < 141:
            #nedovoli polozit obraz, pokial nie je polozeny obraz vo stvorci predtym
            if not slovo[2]:
                img.place(x=x, y=y)
            else:
                # ak uz tam je obraz, vymaze ho
                if slovo[3] != False:
                    slovo[3].after(0, slovo[3].destroy)
                slovo[3] = img
                img.place(x=107, y=300)
        #piaty stvorec
        elif 141 < dx < 175:
            #nedovoli polozit obraz, pokial nie je polozeny obraz vo stvorci predtym
            if not slovo[3]:
                img.place(x=x, y=y)
            else:
                # ak uz tam je obraz, vymaze ho
                if slovo[4] != False:
                    slovo[4].after(0, slovo[4].destroy)
                slovo[4] = img
                img.place(x=141, y=300)
        #vytvori novy obrazok
        n = Label(image=render)
        n.bind("<ButtonPress-1>", lambda event: StartMove(n, event))
        n.bind("<ButtonRelease-1>", lambda event: StopMove(n, event, x, y, render))
        n.bind("<B1-Motion>", lambda event: OnMotion(n, event))
        n.place(x=x,y=y)

def OnMotion(img, event):
    deltax = event.x - img.x
    deltay = event.y - img.y
    x = img.winfo_x() + deltax
    y = img.winfo_y() + deltay
    img.place(x=x, y=y)

def loadRules(file):
    global rules
    with open(file,'r') as t:
        riadok = t.readline().strip()
        while riadok != '':
            arr = riadok.split(" ")
            rules[arr[0]] = arr[1]
            riadok = t.readline().strip()
    drawRules()

def drawRules():
    global rulesImg, a, b, c, rules, root, pravidla
    for index, seq in rules.items():
        length = 30 + 30 + 30*len(seq)
        rule = Image.new('RGBA', (length, 30), (255,255,255,0))
        if (index == "a"):
            rule.paste(a.resize((30, 30)), (0, 0))
        elif (index == "b"):
            rule.paste(b.resize((30, 30)), (0, 0))
        elif (index == "c"):
            rule.paste(c.resize((30, 30)), (0, 0))
        rule.paste(sipka.resize((30, 30)), (30, 0))
        for i in range(len(seq)):
            if (seq[i] == "a"):
                rule.paste(a.resize((30,30)), (60+30*i, 0))
            elif (seq[i] == "b"):
                rule.paste(b.resize((30,30)), (60+30*i, 0))
            elif (seq[i] == "c"):
                rule.paste(c.resize((30,30)), (60+30*i, 0))

        rulesImg[index] = ImageTk.PhotoImage(rule)

    pravidla = LabelFrame (root, bg='#D9A5F9', text="Tlačidlá s pravidlami")
    pravidlo1 = Button(pravidla, image=rulesImg["a"], bg="#deeff5")
    pravidlo1.place(x=5, y=5)
    pravidlo2 = Button(pravidla, image=rulesImg["b"], bg="#deeff5")
    pravidlo2.place(x=5, y=45)
    pravidlo3 = Button(pravidla, image=rulesImg["c"], bg="#deeff5")
    pravidlo3.place(x=5, y=85)
    pravidla.place(x=5, y=5, height=145, width=170)

root = Tk()
root.title("Gramatik")
root.geometry("600x500")
#menu
menubar = Menu(root)
menubar.add_cascade(label="Súbor", command=vyberSubor())
nastavenia = Menu(menubar, tearoff=0)
nastavenia.add_radiobutton(label="Zobrazovať postup", command=zobrazPostup())
menubar.add_cascade(label ="Nastavenia", menu=nastavenia)
menubar.add_command(label ="Nové slovo", command= lambda slovo=slovo: noveSlovo(slovo))

#vstupné slovo
pociatocne_slovo = LabelFrame(root, text="Počiatočné slovo")
ciary = Canvas(pociatocne_slovo, height=27, width=160)
ciary.create_line(34, 0, 34, 30)
ciary.create_line(68, 0, 68, 30)
ciary.create_line(102, 0, 102, 30)
ciary.create_line(136, 0, 136, 30)
ciary.place(x=0, y=0)

pociatocne_slovo.place(x=5, y=285, height=50, width=170)

#koncové slovo
koncove_slovo = LabelFrame(root, text="Koncové slovo")
koncove_slovo.place(x=5, y=340, height=50, width=170)

#postup
postup = LabelFrame(root, text='Postup', bg='#deeff5')
postup.place(x=180, y=5, height=450, width=400)

#písmená
pismena = LabelFrame (root, bg='#ffd6dc')
render1 = ImageTk.PhotoImage(Image.open("chocolada.png").resize((30, 30), Image.ANTIALIAS))
img1 = Label(image=render1)
img1.bind("<ButtonPress-1>", lambda event: StartMove(img1, event))
img1.bind("<ButtonRelease-1>", lambda event: StopMove(img1, event, 10, 160, render1))
img1.bind("<B1-Motion>", lambda event: OnMotion(img1, event))
img1.place(x=10, y=160)
render2 = ImageTk.PhotoImage(Image.open("donut.png").resize((30, 30), Image.ANTIALIAS))
img2 = Label(image=render2)
img2.bind("<ButtonPress-1>", lambda event: StartMove(img2, event))
img2.bind("<ButtonRelease-1>", lambda event: StopMove(img2, event, 10, 200, render2))
img2.bind("<B1-Motion>", lambda event: OnMotion(img2, event))
img2.place(x=10, y=200)
render3 = ImageTk.PhotoImage(Image.open("zmrzlina.png").resize((30, 30), Image.ANTIALIAS))
img3 = Label(image=render3)
img3.bind("<ButtonPress-1>", lambda event: StartMove(img3, event))
img3.bind("<ButtonRelease-1>", lambda event: StopMove(img3, event, 10, 240, render3))
img3.bind("<B1-Motion>", lambda event: OnMotion(img3, event))
img3.place(x=10, y=240)
pismena.place(x=5, y=155, height=125, width=170)

root.config(menu=menubar, bg='#ADD8E6')
root.mainloop()
