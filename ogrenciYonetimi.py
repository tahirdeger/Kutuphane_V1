import json
import os
import datetime
import locale

class Ogrenci:
    def __init__(self, ogrenci_adi, ogrenci_soyadi, numarasi):
        self.ogrenci_adi = ogrenci_adi
        self.ogrenci_soyadi = ogrenci_soyadi
        self.numarasi = numarasi
        self.okunan = []
        

class Yonet:
    def __init__(self):
        self.ogrenciler = []
        #Eski kullanici verilerini json dosyasından alalım
        self.ogrenci_yukle()

#Öğrencileri JSON dosyasından yükleme  
    def ogrenci_yukle(self):
        #dosyanın olup olmadığını anlamak için os modülü kullanalım
        if os.path.exists("ogrenciler.json"):
            with open("ogrenciler.json","r",encoding="utf-8") as dosya:
                kullanicilar = json.load(dosya)                                    #Buradan gelen veri JSON string'ler içeren bir liste
                for x in kullanicilar:
                    kullanici = json.loads(x)                                    #Burada her bir elemanı sözlük yapısına çevirdik
                    #print(kullanici)
                    kullanici_obje = Ogrenci(kullanici["ogrenci_adi"] , kullanici["ogrenci_soyadi"] , kullanici["numarasi"])      #sözlük yapısını obje yapısına çeviriyoruz
                    kullanici_obje.okunan = kullanici["okunan"]                    
                    self.ogrenciler.append(kullanici_obje)                                             #obje yapısını kullanıcılar class'ına ekliyoruz
            #print(self.ogrenciler)
###################################################################################################################    

#Yeni öğrenci kaydetme
    def kayit_ol(self, ogrenci : Ogrenci):
        self.ogrenciler.append(ogrenci)
        self.kaydet()
        print("Kullanıcı oluşturuldu! ")

    def kaydet(self):
        #class'lar JSON içine kaydedilemezler. Bknz: https://www.w3schools.com/python/python_json.asp
        #Bu sebeple burda class yapısını liste ve ardından sözlük yapısına çevirmeliyiz ki JSON'a gönderebilelim:
        liste = []
    
        for u in self.ogrenciler:
            liste.append(json.dumps(u.__dict__))    #kullanıcı objesindeki __dict__ methodu ile kullanıcı bilgileri JSON stringine döbdürülüp, listeye kaydedilecek
        
        with open("ogrenciler.json","w",encoding="utf-8") as dosya:
            json.dump(liste, dosya)
        
        self.yeniden_yukle()

###################################################################################################################    
#Öğrenciye yeni kitap aldırma işlemi:    
    def kitap_al(self, ogrenci_no, kitap_adi , yazari , no):
        locale.setlocale(locale.LC_ALL, '')
        for i in self.ogrenciler:
            if i.numarasi == ogrenci_no:
                alis_tarihi = datetime.datetime.now()
                x = ["Kitap no:" , no , "Kitap adı:", kitap_adi , "Yazarı:",yazari ,"Alış tarihi:" , str(datetime.datetime.strftime(alis_tarihi, "%d %B %A %Y"))]
                i.okunan.append(x)
                
        self.kaydet()
###################################################################################################################    

#Öğrenciye kitap teslim ettirme işlemi
    def kitap_sil(self, numara, kitap_adi , yazari , no):
        locale.setlocale(locale.LC_ALL, '')
        for i in self.ogrenciler:
            if i.numarasi == numara:
                for x in i.okunan:
                    if x[1] == no:
                        veris_tarihi = datetime.datetime.now()
                        x.append(str(datetime.datetime.strftime(veris_tarihi, "%d %B %A %Y")))
                        self.kaydet()
                        
        self.kaydet()

###################################################################################################################    

    def sorgula(self, numara):
        liste_ogrenci = []
        liste_kitaplar = []
        for i in self.ogrenciler:            
            if i.numarasi == numara:
                liste_ogrenci.append(i.numarasi)              
                if len(i.okunan) == 0:
                    print("Öğrenci hiç kitap okumamış !")
                    return "kitap yok"
                else:
                    print("Öğrenci kitap okumuş, liste gönderildi")
                    for i in i.okunan:
                        liste_kitaplar.append(i)
                    return liste_kitaplar

        if not numara in liste_ogrenci:
            print("Öğrenci kaydı bulunamadı !")
            return "kayıt yok"
    
###################################################################################################################    

    def ogrenci_listele(self):
        if len(self.ogrenciler) == 0:
            print("Kayıtlı öğrenci yok !")
            return False
        else:
            liste=[]
            for x in self.ogrenciler:

                liste.append(x.numarasi)
            liste.sort()
            for x in self.ogrenciler:

                for i in range(len(liste)):
                    if x.numarasi == liste[i]:
                        liste[i] = x
            return liste
            # for x in liste: 
            #     if len(x.okunan) == 0:
            #         if (f"Öğrenci no: {x.numarasi}    Öğrenci adı soyadı: {x.ogrenci_adi.ljust(10)} {x.ogrenci_soyadi.ljust(10)}")
            #     else:
            #         print(f"Öğrenci no: {x.numarasi}    Öğrenci adı soyadı: {x.ogrenci_adi.ljust(10)} {x.ogrenci_soyadi.ljust(10)}      Son okuduğu/okuyor olduğu kitap: {x.okunan[-1][3].ljust(30)}   Kitap kodu:{x.okunan[-1][1]}")

###################################################################################################################    


    def ogrenciSil(self, ogrenci_no):
        liste_ogrenci =[]
        print(f"{ogrenci_no} silinecek")
        for ogrenci in self.ogrenciler:
            liste_ogrenci.append(ogrenci.numarasi)
            if ogrenci.numarasi == ogrenci_no:
                if len(ogrenci.okunan) == 0: 
                    self.ogrenciler.remove(ogrenci)
                    self.kaydet()
                else:
                    return "kitap okuyor"
        if not ogrenci_no in liste_ogrenci:
            print("Ogrenci kaydı bulunamadı!")
            return "yok"
###################################################################################################################    

    def yeniden_yukle(self):
        self.ogrenciler.clear()
        #dosyanın olup olmadığını anlamak için os modülü kullanalım
        self.ogrenci_yukle()