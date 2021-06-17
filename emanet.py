import db
import kutuphaneKitapligi
import kitap_emanet_teslim
from tkinter import *
from tkinter.ttk import Treeview
from tkinter import ttk
from tkinter import messagebox
from datetime import date, datetime, timedelta


today = date.today()
nexttime = datetime.now() + timedelta(days=14)

def stok(kitap_ISBN):
    db.mycursor.execute('SELECT kitap_sayisi FROM kutuphane_otomasyonu.kitaplar WHERE ISBN_no_kitap = %s',(kitap_ISBN,))
    result = db.mycursor.fetchall()
    return result[0][0]

def stokGuncelle(kitap_ISBN):
    result = stok(kitap_ISBN)
    db.mycursor.execute('UPDATE kutuphane_otomasyonu.kitaplar SET kitap_sayisi = %s WHERE ISBN_no_kitap = %s',(result-1, kitap_ISBN))
    db.mydb.commit()

def kitabiAl(uyeID, kitap_ISBN, kutuphane_id):
    db.mycursor.execute("INSERT INTO kutuphane_otomasyonu.emanet (`uye_ID`, `kitap_ISBN`, `kutuphane_ID`, `alım_tarihi`, `teslim_tarihi`, `emanet_durumu`) VALUES (%s, %s, %s, %s, %s, %s)",
    (uyeID, kitap_ISBN, kutuphane_id, today.strftime("%Y-%m-%d"), nexttime, 0))

    db.mydb.commit()
    stokGuncelle(kitap_ISBN)

def emanetAl(uyeID, kitap_ISBN, kutuphane_id, pencere, secim):
    if (stok(kitap_ISBN) > 0):
        kitabiAl(uyeID, kitap_ISBN, kutuphane_id)
        pencere.destroy()
        kutuphaneKitapligi.kitapDoldur(secim, uyeID)
    else:
        messagebox.showerror("Kitap Yok", "Alacak olduğunuz kitap şuan stokta bulunmamaktadır.")

def emanetTeslim(uyeID):

    def getrow(event):
        rowid = kitapListeleTree.identify_row(event.y)
        item = kitapListeleTree.item(kitapListeleTree.focus())
        s2.set(item['values'][0])

    yeniPencere = Toplevel()
    yeniPencere.title("İşlemlerim")
    yeniPencere.geometry("820x700")
    yeniPencere['background'] = '#1C2833'

    pgen = 820
    pyuks = 700

    ekrangen = yeniPencere.winfo_screenwidth()
    ekranyuks = yeniPencere.winfo_screenheight()

    x = (ekrangen - pgen) / 2
    y = (ekranyuks - pyuks) / 2

    yeniPencere.geometry("%dx%d+%d+%d"%(pgen, pyuks, x, y))

    Label(yeniPencere, text="Kitaplar",
        bg="#009999", fg="white", font="Times 14 italic").pack()
    wrapper2 = LabelFrame(yeniPencere,height=120,bg="#1C2833",fg="#009999",
                        highlightbackground="#009999", highlightcolor="#009999", highlightthickness=1, bd=2)
    wrapper2.pack(fill="both",expand="yes",padx=20,pady=8)

    style = ttk.Style()
    style.map('Treeview', background=[('selected', '#cc3300')])
    #-------------------------------
    kitapListeleTree = Treeview(wrapper2,column=("1","2","3","4","5"),
                            show='headings',height="4",
                            selectmode="extended")
    kitapListeleTree.pack(side="left")
    kitapListeleTree.place(x=0,y=0)

    s1 = StringVar()
    s2 = StringVar()

    yscroolbar = Scrollbar(wrapper2, orient="vertical",
                        command=kitapListeleTree.yview)
    yscroolbar.pack(side='right', fill=Y)


    kitapListeleTree.config(yscrollcommand=yscroolbar.set)

    kitapListeleTree.column("#1", anchor=CENTER, width=150, minwidth=60)
    kitapListeleTree.heading("#1", text="ISBN")

    kitapListeleTree.column("#2", anchor=CENTER, width=190, minwidth=100)
    kitapListeleTree.heading("#2", text="Kitap")

    kitapListeleTree.column("#3", anchor=CENTER, width=180, minwidth=60)
    kitapListeleTree.heading("#3", text="Kütüphane")

    kitapListeleTree.column("#4", anchor=CENTER, width=125, minwidth=100)
    kitapListeleTree.heading("#4", text="Alım Tarihi")

    kitapListeleTree.column("#5", anchor=CENTER, width=125, minwidth=80)
    kitapListeleTree.heading("#5", text="Teslim Tarihi")

    kitaplar = kitap_emanet_teslim.emaneAlinanKitaplar(uyeID)
    s1.set(len(kitaplar))

    #s1 = StringVar(wrapper1,kitap_emanet_teslim.emaneAlinanKitaplarSayısı(uyeID)) seklinde yaprsan çalışır set ve get kullanmana gerek yok
    
    for i in range(len(kitaplar)):
        kitapListeleTree.insert('', 'end', values=kitaplar[i])

    kitapListeleTree.bind('<Double 1>',getrow)

    entry_1= Entry(yeniPencere,textvariable=s2,state='disabled')

    emanet_btn = Button(yeniPencere, text="Teslim Et",width=17, height = 3, 
                    command = lambda : kitap_emanet_teslim.teslimEt(entry_1.get()),
                    bg="#009999",fg="white",font="Times 12 bold",highlightcolor="#009999",highlightbackground="#009999",
                    highlightthickness=4,borderwidth=2)
    emanet_btn.pack(side="right")
