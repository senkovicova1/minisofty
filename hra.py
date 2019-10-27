from tkinter import *
from tkinter import filedialog
import random
from functools import partial

from PIL import Image, ImageTk


rules = {} #pravidla nacitane zo suboru - index je ynacka obrazku a value je na co sa zmeni
rulesImg = {} #pravidla ale uz s obrazkami 
pics = {} #tri obrazky reprezentujuce slova
sipka = Image.open("sipka.png")
win = Image.open("win.jpg")

winRef = None

slovo = [False, False, False, False, False] #pociatocne slovo v obrazkoch
startWord = [None, None, None, None, None] #pociatocne slovo v znakoch
endWord = [] #koncove slovo, v znakoch nie obrazkoch
endWordImg = [] #koncove slovo v obrazkoch
dis_img = [False, False, False]

difficulty = 1 #difficulty je koeficient ktory sa po kazdom kole zvysuje az po 5; udava kolko pravidiel sa uplatni na pociatocne slovo
steps = [] #steps je tuple (slovo v stringu, pravidlo ktore nanho bolo aplikovane - a,b,c)
stepsImg = [] #to iste ako hore ale s img, kvoli referenciam na zmazanie
helpArr = [] #pomocne pole, nemali by sme ho potrebovat, but here we are

showSteps = True

gameWon = False

def vyberSubor():
    file_path = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes =(("Text File", "*.txt"),("All Files","*.*")),)
    loadRules(file_path[file_path.rindex("/")+1:])

def zobrazPostup():
    global showSteps, steps
    showSteps = not showSteps
    #zmeni check/uncheck pri zobrazovaní postupu v menu
    if not showSteps:
        check_button.set(0)
    if len(steps) > 0 and not gameWon:
        drawPostup()

def noveSlovo(slovo):
    global startWord, endWord, endWordImg, gameWon, winRef, steps, stepsImg, difficulty, dis_img
    #zruší celý postup a koncové slovo - dorobiť
    #odblokuje používanie obrázkov
    if (len(endWord) == 0):
        
        return
    
    if dis_img[0] != False:
        for n in range(3):
            dis_img[n].after(0, dis_img[n].destroy)
            dis_img[n] = False
    #zruší počiatočné slovo
    i = 0
    while i < 5:
        if(slovo[i] == False):
            i = i + 1
            break
        else:
            slovo[i].after(0, slovo[i].destroy)
            slovo[i] = False
            i = i + 1
            
    startWord = [None, None, None, None, None]
    if (gameWon):
        difficulty += 1
        if difficulty >= 6:
            difficulty = 6
        winRef.after(0, winRef.destroy)
        winRef = None
    gameWon = False
    for p in stepsImg:
        a,b = p
        a.after(0, a.destroy)
        if b is not None:
            b.after(0, b.destroy)
    steps = []
    endWord = []
    for a in endWordImg:
        a.after(0, a.destroy)
    endWordImg = []
    
    #zobrazi sipku
    vytvorSipku()

def StartMove(img, event):
    img.x = event.x
    img.y = event.y

def StopMove(index, img, event, x, y, render):
    global startWord
    info = img.place_info()
    dx = int(info.get('x'))
    dy = int(info.get('y'))
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
            startWord[0] = index
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
                startWord[1] = index
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
                startWord[2] = index
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
                startWord[3] = index
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
                startWord[4] = index
                img.place(x=141, y=300)
        #vytvori novy obrazok
                
        n = Label(image=render)
        n.bind("<ButtonPress-1>", lambda event: StartMove(n, event))
        n.bind("<ButtonRelease-1>", lambda event: StopMove(index, n, event, x, y, render))
        n.bind("<B1-Motion>", lambda event: OnMotion(n, event))
        n.place(x=x,y=y)



def OnMotion(img, event):
    deltax = event.x - img.x
    deltay = event.y - img.y
    x = img.winfo_x() + deltax
    y = img.winfo_y() + deltay
    img.place(x=x, y=y)

def loadRules(file):
    global rules, pics
    with open(file,'r') as t:
        cesta = t.readline().strip()
        riadok = t.readline().strip()
        i = 0
        while riadok != '' or i <= 2:
            arr = riadok.split(" ")
            rules[arr[0]] = arr[2]
            pics[arr[0]] = Image.open(cesta + "/" + arr[0] + ".png")
            helpArr.append(arr[0])
            riadok = t.readline().strip()
            i += 1
    drawRules()

def drawRules():
    global rulesImg, pics, rules, root, pravidla, render1, render2, render3, helpArr
    r = sorted(list(rules.keys()))
        
    for i in range(len(rules)):
        index = r[i]
        seq = rules[index]
        
        length = 30 + 30 + 30*len(seq)
        rule = Image.new('RGBA', (length, 30), (255,255,255,0))
        
        rule.paste(pics[index].resize((30, 30)), (0, 0))
        rule.paste(sipka.resize((30, 30)), (30, 0))
        
        for s in range(len(seq)):
            rule.paste(pics[seq[s]].resize((30,30)), (60+30*s, 0))

        rulesImg[index] = ImageTk.PhotoImage(rule)

        if i == 0:
            action_with_arg = partial(addStep, helpArr[0])
            pravidlo1 = Button(pravidla, image=rulesImg[index], bg="#deeff5", command=action_with_arg)
            pravidlo1.place(x=5, y=5)
            
            render1 = ImageTk.PhotoImage(pics[index].resize((30, 30), Image.ANTIALIAS))
            img1 = Label(image=render1)
            img1.bind("<ButtonPress-1>", lambda event: StartMove(img1, event))
            img1.bind("<ButtonRelease-1>", lambda event: StopMove(helpArr[0], img1, event, 10, 160, render1))
            img1.bind("<B1-Motion>", lambda event: OnMotion(img1, event))
            img1.place(x=10, y=160)
            
        elif i == 1:
            action_with_arg = partial(addStep, helpArr[1])
            pravidlo2 = Button(pravidla, image=rulesImg[index], bg="#deeff5", command=action_with_arg)
            pravidlo2.place(x=5, y=45)

            render2 = ImageTk.PhotoImage(pics[index].resize((30, 30), Image.ANTIALIAS))
            img2 = Label(image=render2)
            img2.bind("<ButtonPress-1>", lambda event: StartMove(img2, event))
            img2.bind("<ButtonRelease-1>", lambda event: StopMove(helpArr[1], img2, event, 10, 200, render2))
            img2.bind("<B1-Motion>", lambda event: OnMotion(img2, event))
            img2.place(x=10, y=200)
            
        elif i == 2:
            action_with_arg = partial(addStep, helpArr[2])
            pravidlo3 = Button(pravidla, image=rulesImg[index], bg="#deeff5", command=action_with_arg)
            pravidlo3.place(x=5, y=85)

            render3 = ImageTk.PhotoImage(pics[index].resize((30, 30), Image.ANTIALIAS))
            img3 = Label(image=render3)
            img3.bind("<ButtonPress-1>", lambda event: StartMove(img3, event))
            img3.bind("<ButtonRelease-1>", lambda event: StopMove(helpArr[2], img3, event, 10, 240, render3))
            img3.bind("<B1-Motion>", lambda event: OnMotion(img3, event))
            img3.place(x=10, y=240)

def vytvorSipku():
    global arrow
    arrow = Canvas(root, height=50, width=80, bg='#deeff5', bd=-2)
    arrow.create_polygon(0, 15, 50, 15, 50, 0, 80, 25, 50, 50, 50, 35, 0, 35, fill='green')
    arrow.bind("<ButtonPress-1>", getColor)
    arrow.place(x=190, y=285)

def getColor(event):
    global arrow
    dx = event.x
    dy = event.y
    ids = arrow.find_overlapping(dx, dy, dx, dy)
    if ids:
        index = ids[-1]
        color = arrow.itemcget(index, "fill")
        if color == 'green':
            if slovo[0] != False:
                #vytvori nepohyblive obrazky cez uz existujuce, cim ich zablokuje
                img_b1 = Label(image=render1)
                img_b1.place(x=10, y=160)
                img_b2 = Label(image=render2)
                img_b2.place(x=10, y=200)
                img_b3 = Label(image=render3)
                img_b3.place(x=10, y=240)
                global dis_img
                dis_img = [img_b1, img_b2, img_b3]
                #nedovoli pohnut pismenami v slove
                i = 0
                while i < 5:
                    if (slovo[i] == False):
                        i = i + 1
                        break
                    else:
                        slovo[i].unbind("<ButtonPress-1>")
                        slovo[i].unbind("<ButtonRelease-1>")
                        slovo[i].unbind("<B1-Motion>")
                        i = i + 1
                #sipka zmizne
                generateEndWord()
                arrow.destroy()

def generateEndWord():
    global difficulty, endWord, startWord, rules, gameWon, steps
    word = [w for w in startWord if w is not None]    
    
    for i in range(difficulty):
        r = set(word)
        r.discard(None)
        rule = random.choice(list(r))
        word = applyRule(word, rule)
    endWord = word
    drawEndWord(endWord)

    steps.append(("".join([w for w in endWord if w is not None]), None))    
    addStep(None, "".join([w for w in startWord if w is not None]), )
    

def applyRule(word, rule):    
    seq = rules[rule]
    string = "".join(word)
    newWord = string[:string.index(rule)] + seq + string[string.index(rule)+1:]
##   print(word, " + (", rule, " => ", seq, ") = ", newWord)
    return [char for char in newWord]

def drawEndWord(word):
    global endWordImg, pics
    for i in range(len(word)):
        im = Image.open("obrazky/" + word[i] + ".png")
        render = ImageTk.PhotoImage(im.resize((30, 30), Image.ANTIALIAS))
        img = Label(image=render)
        img.image = render
        img.place(x=10+31*(i%5), y=360+(30*(i//5)))
        endWordImg.append(img)

def addStep(rule, word = None):
    global steps, endWord, gameWon    
    if (gameWon):
        return
    if rule is not None and len(endWord) > 0 and rule in steps[-2][0]:
        theLast = steps.pop()
        a, b = steps.pop() 
        steps.append((a, rule))
        w = applyRule(a, rule)
        steps.append((w, None))
        steps.append(theLast)
    elif word is not None:        
        theLast = steps.pop()
        steps.append((word, None))
        steps.append(theLast)
    drawPostup()

def check():
    global endWord, steps
    return "".join(endWord) == "".join(steps[-2][0])

def drawPostup():
    global steps, stepsImg, rulesImg, pics, showSteps, gameWon
    i = len(stepsImg) - 1    
    while i >= 0:
        stepsImg[i][0].after(0, stepsImg[i][0].destroy)
        if (stepsImg[i][1] is not None):
            stepsImg[i][1].after(0, stepsImg[i][1].destroy)
        stepsImg.pop()
        i -= 1

    if showSteps:        
        for i in range(len(steps)):                 
            a, b = steps[i]            
               
            p = Image.new('RGBA', (40*len(a), 40), (255,255,255,0))
                    
            for s in range(len(a)):
                p.paste(pics[a[s]].resize((40,40)), (40*s, 0))

            y = 30 + 50*i
            if i == len(steps)-1:
                 y = 440
      
            pic = ImageTk.PhotoImage(p)
            img = Label(image=pic)
            img.image = pic
            img.place(x=190, y=y)

            img2 = None
            if b is not None and showSteps:
                img2 = Label(image=rulesImg[b])
                img2.image = rulesImg[b]
                img2.place(x=660+31*5, y=30 + 50*i)
        
            stepsImg.append((img, img2))
    else:
        a, b = steps[0]
        p = Image.new('RGBA', (40*len(a), 40), (222,239,245,0))
                    
        for s in range(len(a)):
            p.paste(pics[a[s]].resize((40,40)), (40*s, 0))
      
        pic = ImageTk.PhotoImage(p)
        img = Label(image=pic)
        img.image = pic
        img.place(x=190, y=30)

        img2 = None
        if b is not None and showSteps:
            img2 = Label(image=rulesImg[b])
            img2.image = rulesImg[b]
            img2.place(x=660+31*5, y=30)
        
        stepsImg.append((img, img2))

        c, d = steps[-1]
        p = Image.new('RGBA', (40*len(c), 40), (222,239,245,0))
                        
        for s in range(len(c)):
            p.paste(pics[c[s]].resize((40,40)), (40*s, 0))
          
        pic = ImageTk.PhotoImage(p)
        img = Label(image=pic)
        img.image = pic
        img.place(x=190, y=440)

        img2 = None
            
        stepsImg.append((img, img2))

        if (len(steps) > 2):
            e, f = steps[-2]
            p = Image.new('RGBA', (40*len(e), 40), (255,255,255,0))
                        
            for s in range(len(e)):
                p.paste(pics[e[s]].resize((40,40)), (40*s, 0))
          
            pic = ImageTk.PhotoImage(p)
            img = Label(image=pic)
            img.image = pic
            img.place(x=190, y=30 + 50)

            img2 = None
            if f is not None and showSteps:
                img2 = Label(image=rulesImg[f])
                img2.image = rulesImg[f]
                img2.place(x=660+31*5, y=30 + 50)

            stepsImg.insert(1, (img, img2))   
    
    if check():
        gameWon = True
        disableGame()
        drawWin()

def disableGame():
    #zariadi aby sa uz nedalo klikat na buttony 
    return

def drawWin():
    global win, winRef
    pic = ImageTk.PhotoImage(win.resize((300, 300), Image.ANTIALIAS))
    img = Label(image=pic, bd=-2)
    img.image = pic
    img.place(x=350, y=100)
    winRef = img
    

def deleteSteps():
    global steps, stepsImg, gameWon, winRef
    if (len(steps) > 2) and not gameWon:
        steps = steps[:1] + steps[-1:]
        first = steps[0][0]
        last = steps[1][0]
        steps = [(first, None), (last, None)]
        drawPostup()
        
    if (len(steps) > 2) and gameWon:
        steps = steps[:1] + steps[-1:]
        first = steps[0][0]
        last = steps[1][0]
        steps = [(first, None), (last, None)]
        winRef.after(0, winRef.destroy)
        winRef = None
        gameWon = False
        drawPostup()
    
root = Tk()
root.title("Gramatik")
root.geometry("1000x500")
#menu
menubar = Menu(root)
menubar.add_cascade(label="Súbor", command=lambda: vyberSubor())
nastavenia = Menu(menubar, tearoff=0)
check_button = Variable()
check_button.set(1)
nastavenia.add_checkbutton(label="Zobrazovať postup", variable=check_button, command=zobrazPostup)
menubar.add_cascade(label ="Nastavenia", menu=nastavenia)
menubar.add_command(label ="Nové slovo", command= lambda slovo=slovo: noveSlovo(slovo))
menubar.add_command(label ="Riešiť odznova", command=deleteSteps)

#frame pre pravidlá
pravidla = LabelFrame (root, bg='#D9A5F9', text="Tlačidlá s pravidlami")
pravidla.place(x=5, y=5, height=145, width=170)

#pociatocne slovo
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
koncove_slovo.place(x=5, y=340, height=150, width=170)

#postup
postup = LabelFrame(root, text='Postup', bg='#deeff5')
postup.place(x=180, y=5, height=485, width=800)

#sipka na potvrdenie pociatocneho slova
arrow = Canvas(root)
vytvorSipku()

#písmená
pismena = LabelFrame (root, bg='#ffd6dc')
render1 = None
render2 = None
render3 = None
##render1 = ImageTk.PhotoImage(Image.open("chocolada.png").resize((30, 30), Image.ANTIALIAS))
##    img1 = Label(image=render1)
##    img1.bind("<ButtonPress-1>", lambda event: StartMove(img1, event))
##    img1.bind("<ButtonRelease-1>", lambda event: StopMove(img1, event, 10, 160, render1))
##    img1.bind("<B1-Motion>", lambda event: OnMotion(img1, event))
##    img1.place(x=10, y=160)
##    render2 = ImageTk.PhotoImage(Image.open("donut.png").resize((30, 30), Image.ANTIALIAS))
##    img2 = Label(image=render2)
##    img2.bind("<ButtonPress-1>", lambda event: StartMove(img2, event))
##    img2.bind("<ButtonRelease-1>", lambda event: StopMove(img2, event, 10, 200, render2))
##    img2.bind("<B1-Motion>", lambda event: OnMotion(img2, event))
##    img2.place(x=10, y=200)
##    render3 = ImageTk.PhotoImage(Image.open("zmrzlina.png").resize((30, 30), Image.ANTIALIAS))
##    img3 = Label(image=render3)
##    img3.bind("<ButtonPress-1>", lambda event: StartMove(img3, event))
##    img3.bind("<ButtonRelease-1>", lambda event: StopMove(img3, event, 10, 240, render3))
##    img3.bind("<B1-Motion>", lambda event: OnMotion(img3, event))
##    img3.place(x=10, y=240)
pismena.place(x=5, y=155, height=125, width=170)

root.config(menu=menubar, bg='#ADD8E6')
root.mainloop()
