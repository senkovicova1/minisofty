from tkinter import *
from PIL import Image, ImageTk

def vyberSubor():
    #zobrazi prehliadač súborov
    return

def zobrazPostup():
    #bude zobrazovať postup
    return

def noveSlovo():
    #zruší celý postup, zruší počiatočné a koncové slovo
    return

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

#tlačidlá s pravidlami - dá sa ešte upraviť písmo a namiesto test bude image s odkazom
pravidla = LabelFrame (root, bg='#D9A5F9', text="Tlačidlá s pravidlami")
pravidlo1 = Button(pravidla, text="pravidlo 1")
pravidlo1.grid(column=0, row=0)
pravidlo2 = Button(pravidla, text="pravidlo 2")
pravidlo2.grid(column=0, row=1)
pravidlo3 = Button(pravidla, text="pravidlo 3")
pravidlo3.grid(column=0, row=2)
pravidla.place(x=5, y=5, height=100, width=150)

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

pismena.place(x=5, y=110, height=200, width=150)

#vstupné slovo - bude nejake pole
pociatocne_slovo = LabelFrame(root, text="Počiatočné slovo")
pociatocne_slovo.place(x=5, y=315, height=50, width=150)

#koncové slovo - bude nejake pole
koncove_slovo = LabelFrame(root, text="Koncové slovo")
koncove_slovo.place(x=5, y=370, height=50, width=150)

#postup
postup = LabelFrame(root, text='Postup', bg='#deeff5')
postup.place(x=160, y=5, height=450, width=400)

root.config(menu=menubar, bg='#ADD8E6')
root.mainloop()
