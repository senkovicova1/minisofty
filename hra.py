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

def StartMove(img, event):
    img.x = event.x
    img.y = event.y

def StopMove(img, event, x, y, render):
    info = img.place_info()
    a = int(info.get('x'))
    b = int(info.get('y'))
    print(a, b)
    if not (5 < a < 205) & (315 < b < 395):
        img.place(x=x,y=y)
    else:
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
pravidla.place(x=5, y=5, height=100, width=200)

#vstupné slovo - bude nejake pole
pociatocne_slovo = LabelFrame(root, text="Počiatočné slovo")
pociatocne_slovo.place(x=5, y=315, height=80, width=200)

#koncové slovo - bude nejake pole
koncove_slovo = LabelFrame(root, text="Koncové slovo")
koncove_slovo.place(x=5, y=400, height=80, width=200)

#postup
postup = LabelFrame(root, text='Postup', bg='#deeff5')
postup.place(x=160, y=5, height=450, width=400)

#písmená
pismena = LabelFrame (root, bg='#ffd6dc')
render1 = ImageTk.PhotoImage(Image.open("chocolada.png").resize((50, 50), Image.ANTIALIAS))
img1 = Label(image=render1)
img1.bind("<ButtonPress-1>", lambda event: StartMove(img1, event))
img1.bind("<ButtonRelease-1>", lambda event: StopMove(img1, event, 10, 115, render1))
img1.bind("<B1-Motion>", lambda event: OnMotion(img1, event))
img1.place(x=10, y=115)
render2 = ImageTk.PhotoImage(Image.open("donut.png").resize((50, 50), Image.ANTIALIAS))
img2 = Label(image=render2)
img2.bind("<ButtonPress-1>", lambda event: StartMove(img2, event))
img2.bind("<ButtonRelease-1>", lambda event: StopMove(img2, event, 10, 175, render2))
img2.bind("<B1-Motion>", lambda event: OnMotion(img2, event))
img2.place(x=10, y=175)
render3 = ImageTk.PhotoImage(Image.open("zmrzlina.png").resize((50, 50), Image.ANTIALIAS))
img3 = Label(image=render3)
img3.bind("<ButtonPress-1>", lambda event: StartMove(img3, event))
img3.bind("<ButtonRelease-1>", lambda event: StopMove(img3, event, 10, 235, render3))
img3.bind("<B1-Motion>", lambda event: OnMotion(img3, event))
img3.place(x=10, y=235)
pismena.place(x=5, y=110, height=200, width=200)

root.config(menu=menubar, bg='#ADD8E6')
root.mainloop()
