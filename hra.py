from tkinter import *
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

def vyberSubor():  
    file_path = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes =(("Text File", "*.txt"),("All Files","*.*")),)
    loadRules(file_path[file_path.rindex("/")+1:])

def zobrazPostup():
    #bude zobrazovať postup
    return

def noveSlovo():
    #zruší celý postup, zruší počiatočné a koncové slovo
    return

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
menubar.add_cascade(label ="Nové slovo", command=noveSlovo())

#tlačidlá s pravidlami - dá sa ešte upraviť písmo a namiesto text bude image s odkazom
##pravidla = LabelFrame (root, bg='#D9A5F9', text="Tlačidlá s pravidlami")
##pravidlo1 = Button(pravidla, text="pravidlo 1")
##pravidlo1.grid(column=0, row=0)
##pravidlo2 = Button(pravidla, text="pravidlo 2")
##pravidlo2.grid(column=0, row=1)
##pravidlo3 = Button(pravidla, text="pravidlo 3")
##pravidlo3.grid(column=0, row=2)
##pravidla.place(x=5, y=5, height=100, width=150)

#písmená - ešte zistím ako spraviť infinity image
pismena = LabelFrame (root, bg='#ffd6dc')
render1 = ImageTk.PhotoImage(Image.open("chocolada.png").resize((50, 50), Image.ANTIALIAS))
img1 = Label(pismena, image=render1)
img1.place(x=5, y=5)
render2 = ImageTk.PhotoImage(Image.open("donut.png").resize((50, 50), Image.ANTIALIAS))
img2 = Label(pismena, image=render2)
img2.place(x=5, y=65)
render3 = ImageTk.PhotoImage(Image.open("zmrzlina.png").resize((50, 50), Image.ANTIALIAS))
img3 = Label(pismena, image=render3)
img3.place(x=5, y=125)

pismena.place(x=5, y=155, height=190, width=170)

#vstupné slovo - bude nejake pole
pociatocne_slovo = LabelFrame(root, text="Počiatočné slovo")
pociatocne_slovo.place(x=5, y=350, height=50, width=170)

#koncové slovo - bude nejake pole
koncove_slovo = LabelFrame(root, text="Koncové slovo")
koncove_slovo.place(x=5, y=405, height=50, width=170)

#postup
postup = LabelFrame(root, text='Postup', bg='#deeff5')
postup.place(x=180, y=5, height=450, width=400)



root.config(menu=menubar, bg='#ADD8E6')
root.mainloop()
