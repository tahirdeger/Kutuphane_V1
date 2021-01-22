import os
import json
import ogrenciYonetimi
import datetime
import locale

ogrenci_yonetim = ogrenciYonetimi.Yonet()


class Kitap:
    def __init__(self, kitap_adi , yazari , no , sayfa_sayisi):
        self.kitap_adi = kitap_adi
        self.yazari = yazari
        self.no = no
        self.sayfa_sayisi = sayfa_sayisi
        self.ogrenci = []
        self.okuyanlar = []


class Yonet:
    def __init__(self):
        self.kitaplar = []
        self.ogrenci_kitaplar = []
        #Eski kullanici verilerini json dosyasından alalım
        self.kutuphane_kitap_yukle()
        self.ogrenci_kitap_yukle()

#BAŞLANGIÇ YAPILANDIRMASI
#################################################################################################################################################
#Kütüphanede yer alan kitapların listesini JSON'dan alalım:
    def kutuphane_kitap_yukle(self):
        #dosyanın olup olmadığını anlamak için os modülü kullanalım
        if os.path.exists("kitaplar.json"):
            with open("kitaplar.json","r",encoding="utf-8") as dosya:
                kitaplar = json.load(dosya)                                    #Buradan gelen veri JSON string'ler içeren bir liste
                for x in kitaplar:
                    kitap = json.loads(x)                                    #Burada her bir elemanı sözlük yapısına çevirdik
                    #print(kitap)
                    kitap_obje = Kitap( kitap["kitap_adi"] , kitap["yazari"] , kitap["no"] , kitap["sayfa_sayisi"])      #sözlük yapısını obje yapısına çeviriyoruz
                    kitap_obje.okuyanlar = kitap["okuyanlar"]
                    
                    self.kitaplar.append(kitap_obje)                                             #obje yapısını kullanıcılar class'ına ekliyoruz
            #print(self.kitaplar)
##################################################################################################################################################
#Öğrencilerde bulunan kitapların listesini JSON'dan alalım: 
    def ogrenci_kitap_yukle(self):
        #dosyanın olup olmadığını anlamak için os modülü kullanalım
        if os.path.exists("alinankitaplar.json"):
            with open("alinankitaplar.json","r",encoding="utf-8") as dosya:
                ogrenci_kitaplar = json.load(dosya)                                    #Buradan gelen veri JSON string'ler içeren bir liste
                for x in ogrenci_kitaplar:
                    kitap = json.loads(x)                                    #Burada her bir elemanı sözlük yapısına çevirdik
                    #print(kitap)
                    kitap_obje = Kitap( kitap["kitap_adi"] , kitap["yazari"] , kitap["no"] , kitap["sayfa_sayisi"])      #sözlük yapısını obje yapısına çeviriyoruz
                    kitap_obje.ogrenci = kitap["ogrenci"]
                    kitap_obje.okuyanlar = kitap["okuyanlar"]
                    
                    self.ogrenci_kitaplar.append(kitap_obje)                                             #obje yapısını kullanıcılar class'ına ekliyoruz
            #print(self.ogrenci_kitaplar)

#KOMUTLAR- METHOTLAR
#################################################################################################################################################
#Kütüphaneye kitap ekleyelim:
    def kutuphane_kitap_ekle(self, kitap : Kitap):
        self.kitaplar.append(kitap)
        self.kutuphane_kaydet()
        print("Kitap ekleme işlemi tamamlandı ")

    def kutuphane_kaydet(self):
        #class'lar JSON içine kaydedilemezler. Bknz: https://www.w3schools.com/python/python_json.asp
        #Bu sebeple burda class yapısını liste ve ardından sözlük yapısına çevirmeliyiz ki JSON'a gönderebilelim:
        liste = []
    
        for u in self.kitaplar:
            liste.append(json.dumps(u.__dict__))    #kullanıcı objesindeki __dict__ methodu ile kullanıcı bilgileri JSON stringine döbdürülüp, listeye kaydedilecek
        
        with open("kitaplar.json","w",encoding="utf-8") as dosya:
            json.dump(liste, dosya)
#################################################################################################################################################    
#Ogrencilere kitap ekleyelim:
    def ogrenci_kitap_ekle(self, kitap : Kitap):
        self.ogrenci_kitaplar.append(kitap)
        self.ogrenci_kaydet()
        print("Kitap ekleme işlemi tamamlandı ")

    def ogrenci_kaydet(self):
        #class'lar JSON içine kaydedilemezler. Bknz: https://www.w3schools.com/python/python_json.asp
        #Bu sebeple burda class yapısını liste ve ardından sözlük yapısına çevirmeliyiz ki JSON'a gönderebilelim:
        liste2 = []
    
        for u in self.ogrenci_kitaplar:
            liste2.append(json.dumps(u.__dict__))    #kullanıcı objesindeki __dict__ methodu ile kullanıcı bilgileri JSON stringine döbdürülüp, listeye kaydedilecek
        
        with open("alinankitaplar.json","w",encoding="utf-8") as dosya:
            json.dump(liste2, dosya)

#################################################################################################################################################
#Kütüphaneden Öğrenciye kitap ver:
    def kitap_al(self , ogrenci_numara , kitap_numara):
        liste3=[]
        for i in self.kitaplar:
            if kitap_numara == i.no:
                liste3.append(i.no)
                ogrenci_yonetim.kitap_al(ogrenci_numara,i.kitap_adi,i.yazari,i.no)
                locale.setlocale(locale.LC_ALL, '')
                alinma = datetime.datetime.now()
                for x in ogrenci_yonetim.ogrenciler:
                    if x.numarasi == ogrenci_numara:
                        ogrenci_bilgi = [ogrenci_numara , x.ogrenci_adi , x.ogrenci_soyadi, str(datetime.datetime.strftime(alinma, "%d %B %A %Y"))]
                        break
                i.okuyanlar.append(ogrenci_bilgi)
                i.ogrenci.append(ogrenci_numara)
                self.ogrenci_kitap_ekle(i)
                self.kitaplar.remove(i)
                self.kutuphane_kaydet()
                #print(self.kitaplar)
                break
        if not kitap_numara in liste3:
            print("Kitap kaydı bulunamadı !")
            return False
        else:
            print("Başarılı")
            return True
#################################################################################################################################################  
#Öğrenciden kütüphaneye kitap teslim et    
    def kitap_teslim(self, ogrenci_numara ,kitap_numara):
        liste=[]
        for i in self.ogrenci_kitaplar:
            if kitap_numara == i.no:
                liste.append(i.no)
                
                if i.ogrenci[0] == ogrenci_numara:                   
                    ogrenci_yonetim.kitap_sil(ogrenci_numara,i.kitap_adi,i.yazari,i.no)
                    i.ogrenci = []
                    locale.setlocale(locale.LC_ALL, '')
                    verilme = datetime.datetime.now()
                    for x in i.okuyanlar:
                        if ogrenci_numara == x[0]:
                            x.append(str(datetime.datetime.strftime(verilme, "%d %B %A %Y")))
                    self.kutuphane_kitap_ekle(i)
                    self.ogrenci_kitaplar.remove(i)
                    self.ogrenci_kaydet()
                    #print(self.kitaplar)
                    break
                else:
                    print("Belirtilen kitap bu öğrencide değil !")
                    return "yanlis"
        if not kitap_numara in liste:
            print("Kitap kaydı bulunamadı !")
            return False
        else:
            return True
#################################################################################################################################################
#Kütüphanede bulunan kitapların listesi
    def kutuphane_listesi(self):
        if len(self.kitaplar)==0:
            print ("Kütüphanede kitap yok !")
            return False
        else:
            liste4=[]
            for x in self.kitaplar:
                liste4.append(x.no)
            liste4.sort()
            for x in self.kitaplar:
                for i in range(len(liste4)):
                    if x.no == liste4[i]:
                        liste4[i] = x
            return liste4
            # for x in liste4:
            #     print(f"Kayıt no: {x.no}    Kitabın adı: {x.kitap_adi.ljust(50)}      Yazarı: {x.yazari}")

#################################################################################################################################################
#Öğrencilerde bulunan kitapların listesi
    def ogrenci_kitap_listesi(self):
        if len(self.ogrenci_kitaplar) == 0:
            print ("Kitap alan öğrenci yok !")
            return False
        else:
            liste=[]
            for x in self.ogrenci_kitaplar:

                liste.append(x.no)
            liste.sort()
            for x in self.ogrenci_kitaplar:

                for i in range(len(liste)):
                    if x.no == liste[i]:
                        liste[i] = x
            return liste
            # for x in liste:
            #     print(f"Kayıt no: {x.no}    Kitabın adı: {x.kitap_adi.ljust(40)}      Yazarı: {x.yazari}")

#Kitap silme işlemi
    def kitapSil(self, kitap_no):
        liste_kitap =[]
        print(f"{kitap_no} silinecek")
        for kitap in self.kitaplar:
            liste_kitap.append(kitap.no)
            if kitap.no == kitap_no:
                self.kitaplar.remove(kitap)
                self.kutuphane_kaydet()
        for kitap in self.ogrenci_kitaplar:
            liste_kitap.append(kitap.no)
            if kitap.no == kitap_no:
                print("Kitap şuan öğrencide olduğu için silinemiyor.\nLütfen kitap sorgulama yaparak kontrol edin !")
                return "ogrencide"
        if not kitap_no in liste_kitap:
            print("Kitap kaydı bulunamadı!")
            return "yok"