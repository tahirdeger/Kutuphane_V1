import sys, os
import kutuphane
import ogrenciYonetimi


from PyQt5 import QtWidgets , QtGui
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox

from MainKutuphaneGiris import Ui_MainWindow
from MainKitapKayit import Ui_MainKitapKayit
from MainOgrenciKayit import Ui_MainOgernciKayit


ogrenci_yonetimi = ogrenciYonetimi.Yonet()
kitap_yonetimi = kutuphane.Yonet()



############################################################
def sayiDenetle(giris):   
    try:
        giris = int(giris)
        if giris <= 0:
            return False
        else:
            return giris
    except:
        return False


class KitapKayit(QtWidgets.QMainWindow):
    def __init__(self):
        super(KitapKayit,self).__init__()

        self.ui_kitap = Ui_MainKitapKayit()
        self.ui_kitap.setupUi(self)
        self.ui_kitap.btn_iptal.clicked.connect(self.kitapCikis)
        self.ui_kitap.btn_tamam.clicked.connect(self.kaydet)
    
    def kitapCikis(self):        
        self.hide()

    def kaydet(self):
        kayit_no = self.ui_kitap.txt_kayit.text()
        kitap_adi = self.ui_kitap.txt_kitap.text()
        kitap_yazari = self.ui_kitap.txt_yazar.text()
        kitap_sayfa = self.ui_kitap.txt_sayfa.text()
        
        if kayit_no and kitap_adi and kitap_yazari and kitap_sayfa is not None:
            denetle = sayiDenetle(kayit_no)
            denetle2 = sayiDenetle(kitap_sayfa)
            if denetle == False or denetle2 == False:
                QMessageBox.warning(self,"Hatalı giriş" , "Lütfen doğru giriş yaptığınıza emin olun !\n'Kayıt numarası' ve 'Sayfa sayısı' için 0'dan büyük bir sayı girmelisiniz.", QMessageBox.Ok , QMessageBox.Cancel)              
            else:
                kayit_no = int(kayit_no)
                kitap_sayfa = int(kitap_sayfa)
                if len(kitap_yonetimi.kitaplar)== 0:
                    kitap = kutuphane.Kitap(kitap_adi,kitap_yazari,kayit_no,kitap_sayfa)
                    kitap_yonetimi.kutuphane_kitap_ekle(kitap)
                    QMessageBox.information (self,"Başarılı" , "Kitap kaydı başarıyla tamamlandı ! ", QMessageBox.Ok , QMessageBox.Cancel)
                    self.hide()
                else:
                    liste=[]
                    for i in kitap_yonetimi.kitaplar:
                        liste.append(i.no)
                    for i in kitap_yonetimi.ogrenci_kitaplar:
                        liste.append(i.no)
                    if kayit_no in liste:
                        QMessageBox.warning(self,"Uyarı" , "Kitap zaten kayıtlı,\nya da kayıt numarası kullanılıyor ! ", QMessageBox.Ok , QMessageBox.Cancel)       
                    else:
                        kitap = kutuphane.Kitap(kitap_adi,kitap_yazari,kayit_no,kitap_sayfa)
                        kitap_yonetimi.kutuphane_kitap_ekle(kitap)                            
                        QMessageBox.information (self,"Başarılı" , "Kitap kaydı başarıyla tamamlandı ! ", QMessageBox.Ok , QMessageBox.Cancel)
                        self.hide()
                            

class OgrenciKayit(QtWidgets.QMainWindow):
    def __init__(self):
        super(OgrenciKayit,self).__init__()

        self.ui_ogrenci = Ui_MainOgernciKayit()
        self.ui_ogrenci.setupUi(self)
        self.ui_ogrenci.btn_iptal.clicked.connect(self.ogrenciCikis)
        self.ui_ogrenci.btn_tamam.clicked.connect(self.ogrenciKaydet)
    
    def ogrenciCikis(self):        
        self.hide()
    
    def ogrenciKaydet(self):
        ogrenci_no = self.ui_ogrenci.txt_no.text()
        ogrenci_adi = self.ui_ogrenci.txt_ogrenciadi.text()
        ogrenci_soyadi = self.ui_ogrenci.txt_ogrencisoyadi.text()
           
        if ogrenci_no and ogrenci_adi and ogrenci_soyadi is not None:
            denetle = sayiDenetle(ogrenci_no)
            if denetle == False:
                QMessageBox.warning(self,"Hatalı giriş" , "Lütfen doğru giriş yaptığınıza emin olun !\n'Öğrenci numarası' için 0'dan büyük bir sayı girmelisiniz.", QMessageBox.Ok , QMessageBox.Cancel)              
            else:
                ogrenci_no = int(ogrenci_no)
                if len(ogrenci_yonetimi.ogrenciler)==0:
                    ogrenci = ogrenciYonetimi.Ogrenci(ogrenci_adi,ogrenci_soyadi,ogrenci_no)
                    ogrenci_yonetimi.kayit_ol(ogrenci)
                    QMessageBox.information (self,"Başarılı" , "Öğrenci kaydı başarıyla tamamlandı ! ", QMessageBox.Ok , QMessageBox.Cancel)
                    self.hide()
                else:
                    liste=[]
                    for i in ogrenci_yonetimi.ogrenciler:                    
                        liste.append(i.numarasi)
                    if ogrenci_no in liste:
                        QMessageBox.warning(self,"Uyarı" , "Öğrenci zaten kayıtlı,\nya da numarası kullanılıyor ! ", QMessageBox.Ok , QMessageBox.Cancel)
                    else:
                        ogrenci = ogrenciYonetimi.Ogrenci(ogrenci_adi,ogrenci_soyadi,ogrenci_no)
                        ogrenci_yonetimi.kayit_ol(ogrenci)
                        QMessageBox.information (self,"Başarılı" , "Öğrenci kaydı başarıyla tamamlandı ! ", QMessageBox.Ok , QMessageBox.Cancel)
                        self.hide()


############################################################
class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp,self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        ################################################### BAĞLANTILAR
        
        self.ui.btn_cikis.clicked.connect(self.cikis)
        self.ui.btn_kutuphanelistele.clicked.connect(self.kutuphaneKitaplar)
        self.ui.btn_verilenlistele.clicked.connect(self.verilenKitaplar)
        self.ui.btn_ogrencilistele.clicked.connect(self.ogrenciListesi)
        self.ui.btn_ogrencisorgula.clicked.connect(self.ogrenciSorgula)
        self.ui.btn_kitapal.clicked.connect(self.kitapAl)
        self.ui.btn_kitapteslim.clicked.connect(self.kitapTeslim)
        self.ui.btn_kitapekle.clicked.connect(self.kitapEkle)
        self.ui.btn_ogrenciekle.clicked.connect(self.ogrenciEkle)
        self.ui.btn_kitapsorgula.clicked.connect(self.kitapSorgula)
        self.ui.lbl_resim.setPixmap(QtGui.QPixmap("logo.jpg"))
        self.ui.btn_kitap_sil.clicked.connect(self.kitapSil)
        self.ui.btn_ogrencisil.clicked.connect(self.ogrenciSil)
        self.ui.btn_yazdir.clicked.connect(self.yazdir)

        ################################################### FOKSİYONLAR
    
    
    def cikis(self):
        quit()


    def yazdir(self):
        with open("yazdiriliyor.txt", 'w',encoding="utf-8") as dosya:
            baslik = self.ui.lbl_bilgi.text()
            dosya.write(baslik)
            dosya.write("\n"+ 100*"_" +"\n")

            for satir in range(self.ui.table_bilgi.rowCount()):
                eklenen = ""
                for kolon in range(self.ui.table_bilgi.columnCount()):
                    item = self.ui.table_bilgi.item(satir, kolon)                   
                    if item is not None:
                        eklenen = item.text()
                    else:
                        eklenen = ' '
                    if kolon == 0:
                        dosya.write(eklenen.ljust(3))
                    else:
                        dosya.write(eklenen.ljust(30))

                dosya.write("\n"+ 100*"_" +"\n")
        
        secim = QMessageBox.warning(self,"Yazdırılıyor" , "Açılan dosyada CTRL + P basarak yazdırma işlemi yapabilirsiniz ! ", QMessageBox.Ok , QMessageBox.Cancel)    
        if secim == QMessageBox.Ok:
            os.startfile("yazdiriliyor.txt")
        else:
            os.startfile("yazdiriliyor.txt")


    def ogrenciSil(self):
        self.ui.lbl_resim.hide()
        ogrenci , ok = QInputDialog.getText(self , "Öğrenci silme işlemi" , "Lütfen silmek istediğiniz öğrencinin numarasını girin..." , QLineEdit.Normal)
        if ogrenci and ok is not None:
            numara = sayiDenetle(ogrenci)            
            if numara == False:
                QMessageBox.warning(self,"Hatalı giriş" , "Lütfen doğru giriş yaptığınıza emin olun !\nOgrenci numarası için 0'dan büyük bir sayı girmelisiniz.", QMessageBox.Ok , QMessageBox.Cancel)
            else:
                sonuc = ogrenci_yonetimi.ogrenciSil(numara)
                if sonuc == "yok":
                    QMessageBox.warning(self,"Silinemiyor" , "Öğrenci kaydı bulunamadı !\nÖğrenci kaydedilmemiş veya daha önce silinmiş olabilir.", QMessageBox.Ok , QMessageBox.Cancel)   
                elif sonuc == "kitap okuyor":
                    QMessageBox.warning(self,"Silinemiyor" , "Öğrencinin okumakta olduğu kitap var, öğrenci silinemez !\nLütfen sorgulama yapınız.", QMessageBox.Ok , QMessageBox.Cancel)   
                else:
                    QMessageBox.information(self,"Silme tamamlandı" , f"{numara} numaralı öğrenciyi silme işlemi başarıyla gerçekleşti.", QMessageBox.Ok , QMessageBox.Cancel)   


    def kitapSil(self):
        self.ui.lbl_resim.hide()
        kitap , ok = QInputDialog.getText(self , "Kitap silme işlemi" , "Lütfen silmek istediğiniz kitabın kayıt numarasını girin..." , QLineEdit.Normal)
        if kitap and ok is not None:
            numara = sayiDenetle(kitap)            
            if numara == False:
                QMessageBox.warning(self,"Hatalı giriş" , "Lütfen doğru giriş yaptığınıza emin olun !\nKitap kayıt numarası için 0'dan büyük bir sayı girmelisiniz.", QMessageBox.Ok , QMessageBox.Cancel)
            else:
                sonuc = kitap_yonetimi.kitapSil(numara)
                if sonuc == "ogrencide":
                    QMessageBox.warning(self,"Hata" , "Kitap şuan öğrencide olduğu için silinemiyor.\nLütfen kitap sorgulama yaparak kontrol edin !", QMessageBox.Ok , QMessageBox.Cancel)   
                elif sonuc == "yok":
                    QMessageBox.warning(self,"Hata" , "Kitap kaydı bulunamadı !\nKitap kaydedilmemiş veya daha önce silinmiş olabilir.", QMessageBox.Ok , QMessageBox.Cancel)   
                else:
                    QMessageBox.information(self,"Silme tamamlandı" , f"{numara} numaralı kitabı silme işlemi başarıyla gerçekleşti.", QMessageBox.Ok , QMessageBox.Cancel)   


    def kitapSorgula(self):
        self.ui.lbl_resim.hide()
        if len(kitap_yonetimi.kitaplar) == 0:
            QMessageBox.warning(self,"Uyarı" , "Sistemde kayıtlı kitap yok ! ", QMessageBox.Ok , QMessageBox.Cancel)   
        else: 
            kitap , ok = QInputDialog.getText(self , "Kitap arama" , "Lütfen sorgulamak istediğiniz kitabın kayıt numarasını girin..." , QLineEdit.Normal)
            if kitap and ok is not None:
                numara = sayiDenetle(kitap)                
                if numara == False:
                    QMessageBox.warning(self,"Hatalı giriş" , "Lütfen doğru giriş yaptığınıza emin olun !\nKitap kayıt numarası için 0'dan büyük bir sayı girmelisiniz.", QMessageBox.Ok , QMessageBox.Cancel)
                else:
                    self.ui.table_bilgi.clear()
                    kitap = int(kitap)
                    liste_kutuphane = []
                    
                    for x in kitap_yonetimi.kitaplar:                        
                        liste_kutuphane.append(x.no)
                        if x.no == kitap:
                            self.ui.lbl_bilgi.setText(f"{x.kitap_adi} isimli kitabı okuyanların listesi")
                            tekrar = len(x.okuyanlar)
                            self.ui.table_bilgi.setRowCount(tekrar)
                            self.ui.table_bilgi.setColumnCount(4)
                            self.ui.table_bilgi.setHorizontalHeaderLabels(("Öğrenci no" , "Öğrenci adı ve soyadı" , "Alış tarihi" , "Veriş tarihi"))
                            self.ui.table_bilgi.setColumnWidth(0,75)
                            self.ui.table_bilgi.setColumnWidth(1,200)
                            self.ui.table_bilgi.setColumnWidth(2,200)
                            self.ui.table_bilgi.setColumnWidth(3,200)
                        
                            for satir in range(tekrar): 
                                
                                self.ui.table_bilgi.setItem(satir,0,QTableWidgetItem(str(x.okuyanlar[satir][0])))
                                self.ui.table_bilgi.setItem(satir,1,QTableWidgetItem(x.okuyanlar[satir][1] + " " +x.okuyanlar[satir][2]))
                                self.ui.table_bilgi.setItem(satir,2,QTableWidgetItem(x.okuyanlar[satir][3]))   
                                self.ui.table_bilgi.setItem(satir,3,QTableWidgetItem(x.okuyanlar[satir][4]))
                        
                    if kitap in liste_kutuphane:
                        print("Kitap kütüphanede")
                        QMessageBox.information(self,"Kitap bilgisi" , "Sorguladığınız kitap şuan kütüphanededir.", QMessageBox.Ok , QMessageBox.Cancel)
                                                
                    else:
                        for i in kitap_yonetimi.ogrenci_kitaplar:
                            liste_kutuphane.append(i.no)
                            if kitap == i.no:
                                self.ui.lbl_bilgi.setText(f"{i.kitap_adi} isimli kitabı okuyanların listesi")
                                print(i.ogrenci)
                                for y in ogrenci_yonetimi.ogrenciler:
                                    if y.numarasi == i.ogrenci[0]:
                                        print(y.numarasi, y.ogrenci_adi , y.ogrenci_soyadi)
                                        QMessageBox.information(self,"Kitap bilgisi" , f"Sorguladığınız kitap {y.numarasi} numaralı \n{y.ogrenci_adi} {y.ogrenci_soyadi} isimli öğrencidedir.", QMessageBox.Ok , QMessageBox.Cancel)
                                                       
                                
                                #Okuyanları listeleyecek
                                
                                tekrar = len(i.okuyanlar)
                                self.ui.table_bilgi.setRowCount(tekrar)
                                self.ui.table_bilgi.setColumnCount(4)
                                self.ui.table_bilgi.setHorizontalHeaderLabels(("Öğrenci no" , "Öğrenci adı ve soyadı" , "Alış tarihi" , "Veriş tarihi"))
                                self.ui.table_bilgi.setColumnWidth(0,75)
                                self.ui.table_bilgi.setColumnWidth(1,200)
                                self.ui.table_bilgi.setColumnWidth(2,200)
                                self.ui.table_bilgi.setColumnWidth(3,200)

                                satir = 0
                                for x in range(tekrar): 
                                    if len(i.okuyanlar[satir]) == 5:
                                        self.ui.table_bilgi.setItem(satir,0,QTableWidgetItem(str(i.okuyanlar[satir][0])))
                                        self.ui.table_bilgi.setItem(satir,1,QTableWidgetItem(i.okuyanlar[satir][1] + " " +i.okuyanlar[satir][2]))
                                        self.ui.table_bilgi.setItem(satir,2,QTableWidgetItem(i.okuyanlar[satir][3]))   
                                        self.ui.table_bilgi.setItem(satir,3,QTableWidgetItem(i.okuyanlar[satir][4]))
                                    else:
                                        self.ui.table_bilgi.setItem(satir,0,QTableWidgetItem(str(i.okuyanlar[satir][0])))
                                        self.ui.table_bilgi.setItem(satir,1,QTableWidgetItem(i.okuyanlar[satir][1] + " " +i.okuyanlar[satir][2]))
                                        self.ui.table_bilgi.setItem(satir,2,QTableWidgetItem(i.okuyanlar[satir][3]))
                                    satir += 1
                    if not kitap in liste_kutuphane:
                        QMessageBox.information(self,"Kitap bilgisi" , f"Sorguladığınız kayıt numarasına sahip bir kitap yoktur.\nLütfen kayıt yapınız.", QMessageBox.Ok , QMessageBox.Cancel)
                                        

    def kitapEkle(self):
        self.ui.lbl_resim.hide()
        self.w = KitapKayit()
        self.w.show()


    def ogrenciEkle(self):
        self.ui.lbl_resim.hide()
        self.o = OgrenciKayit()
        self.o.show()
        
        
    def kitapAl(self):
        self.ui.lbl_resim.hide()
        if len(kitap_yonetimi.kitaplar) == 0:
            QMessageBox.warning(self,"Uyarı" , "Sistemde kayıtlı kitap yok ! ", QMessageBox.Ok , QMessageBox.Cancel)   
        elif len(ogrenci_yonetimi.ogrenciler)== 0:
            QMessageBox.warning(self,"Uyarı" , "Sistemde kayıtlı öğrenci yok ! ", QMessageBox.Ok , QMessageBox.Cancel)   
        else: 
            ogrenci , ok = QInputDialog.getText(self , "Öğrenci bilgisi" , "Öğrenci numarasını girin..." , QLineEdit.Normal)
            if ogrenci and ok is not None:
                numara = sayiDenetle(ogrenci)                
                if numara == False:
                    secim = QMessageBox.warning(self,"Hatalı giriş" , "Lütfen doğru giriş yaptığınıza emin olun !\nÖğrenci numarası için 0'dan büyük bir sayı girmelisiniz.", QMessageBox.Ok , QMessageBox.Cancel)
                    if secim == QMessageBox.Ok:
                        print("Yeniden giriş")
                        self.kitapAl()
                else:
                    sonuc = ogrenci_yonetimi.sorgula(int(ogrenci))
                    if sonuc == "kayıt yok":
                        secim = QMessageBox.warning(self,"Uyarı" , "Öğrenci bilgisi bulunamadı ! ", QMessageBox.Ok , QMessageBox.Cancel)
                        if secim == QMessageBox.Ok:
                            print("Yeniden giriş")
                            self.kitapAl()                    
                    else:
                        kitap , ok = QInputDialog.getText(self , "Kitap bilgisi" , "Kitap kayıt numarasını girin..." , QLineEdit.Normal)
                        if kitap and ok is not None:
                            numara = sayiDenetle(kitap)
                            if numara == False:
                                secim = QMessageBox.warning(self,"Hatalı giriş" , "Lütfen doğru giriş yaptığınıza emin olun !\nÖğrenci numarası için 0'dan büyük bir sayı girmelisiniz.", QMessageBox.Ok , QMessageBox.Cancel)
                                if secim == QMessageBox.Ok:
                                    print("Yeniden giriş")
                                    self.kitapAl()
                    
                            else:
                                print(ogrenci,kitap)
                                sonuc = kitap_yonetimi.kitap_al(int(ogrenci) , int(kitap))
                                ogrenci_yonetimi.yeniden_yukle()
                                if sonuc == False:
                                    QMessageBox.warning(self,"İşlem başarısız" , "Belirtilen kitap bulunamadı ! ", QMessageBox.Ok , QMessageBox.Cancel)
                                else:
                                    QMessageBox.warning(self,"Başarılı" , "Kitap alma işlemi tamamlandı ! ", QMessageBox.Ok , QMessageBox.Cancel)  


    def kitapTeslim(self):
        self.ui.lbl_resim.hide()
        if len(kitap_yonetimi.ogrenci_kitaplar) == 0:
            QMessageBox.warning(self,"Uyarı" , "Sistemde kayıtlı kitap yok ! ", QMessageBox.Ok , QMessageBox.Cancel)   
        elif len(ogrenci_yonetimi.ogrenciler)== 0:
            QMessageBox.warning(self,"Uyarı" , "Sistemde kayıtlı öğrenci yok ! ", QMessageBox.Ok , QMessageBox.Cancel)   
        else: 
            ogrenci , ok = QInputDialog.getText(self , "Öğrenci bilgisi" , "Öğrenci numarasını girin..." , QLineEdit.Normal)
            if ogrenci and ok is not None:
                numara = sayiDenetle(ogrenci)
                if numara == False:
                    secim = QMessageBox.warning(self,"Hatalı giriş" , "Lütfen doğru giriş yaptığınıza emin olun !\nÖğrenci numarası için 0'dan büyük bir sayı girmelisiniz.", QMessageBox.Ok , QMessageBox.Cancel)
                    if secim == QMessageBox.Ok:
                        print("Yeniden giriş")
                        self.kitapTeslim()
                else:
                    sonuc = ogrenci_yonetimi.sorgula(int(ogrenci))
                    if sonuc == "kayıt yok":
                        secim = QMessageBox.warning(self,"Uyarı" , "Öğrenci bilgisi bulunamadı ! ", QMessageBox.Ok , QMessageBox.Cancel)
                        if secim == QMessageBox.Ok:
                            print("Yeniden giriş")
                            self.kitapTeslim()                    
                    else:
                        kitap , ok = QInputDialog.getText(self , "Kitap bilgisi" , "Teslim edilecek kitabın kayıt numarasını girin..." , QLineEdit.Normal)
                        if kitap and ok is not None:
                            numara = sayiDenetle(kitap)
                            if numara == False:
                                secim = QMessageBox.warning(self,"Hatalı giriş" , "Lütfen doğru giriş yaptığınıza emin olun !\nÖğrenci numarası için 0'dan büyük bir sayı girmelisiniz.", QMessageBox.Ok , QMessageBox.Cancel)
                                if secim == QMessageBox.Ok:
                                    print("Yeniden giriş")
                                    self.kitapTeslim()
                            else:
                                print(ogrenci,kitap)
                                sonuc = kitap_yonetimi.kitap_teslim(int(ogrenci) , int(kitap))
                                ogrenci_yonetimi.yeniden_yukle()
                                if sonuc == "yanlis":
                                    QMessageBox.warning(self,"İşlem başarısız" , "Belirtilen kitap bu öğrencide değil ! ", QMessageBox.Ok , QMessageBox.Cancel)
                                elif sonuc == False:
                                    QMessageBox.warning(self,"İşlem başarısız" , "Belirtilen kitap kaydı bulunamadu ! ", QMessageBox.Ok , QMessageBox.Cancel)
                                else:
                                    QMessageBox.warning(self,"Başarılı" , "Kitap teslim etme işlemi tamamlandı ! ", QMessageBox.Ok , QMessageBox.Cancel)   


    def ogrenciSorgula(self):
        self.ui.lbl_resim.hide()
        if len(ogrenci_yonetimi.ogrenciler) == 0:
            QMessageBox.warning(self,"Uyarı" , "Sistemde kayıtlı öğrenci yok ! ", QMessageBox.Ok , QMessageBox.Cancel)
        else:
            item = ""
            text , ok = QInputDialog.getText(self , "Öğrenci sorgulama" , "Öğrenci numarasını girin..." , QLineEdit.Normal ,item)
            if text and ok is not None:
                numara = sayiDenetle(text)
                if numara == False:
                    secim = QMessageBox.warning(self,"Hatalı giriş" , "Lütfen doğru giriş yaptığınıza emin olun !\n0'dan büyük bir sayı girmelisiniz.", QMessageBox.Ok , QMessageBox.Cancel)
                    if secim == QMessageBox.Ok:
                        print("Yeniden giriş")
                        self.ogrenciSorgula()
                else:
                    sonuc = ogrenci_yonetimi.sorgula(int(text))
                    if sonuc == "kayıt yok":
                        secim = QMessageBox.warning(self,"Uyarı" , "Öğrenci bilgisi bulunamadı ! ", QMessageBox.Ok , QMessageBox.Cancel)
                        if secim == QMessageBox.Ok:
                            print("Yeniden giriş")
                            self.ogrenciSorgula()
                    elif sonuc == "kitap yok":
                        QMessageBox.warning(self,"Uyarı" , "Öğrenciye ait kayıtlı kitap bilgisi bulunamadı ! ", QMessageBox.Ok , QMessageBox.Cancel)

                    else:
                        liste = ogrenci_yonetimi.ogrenci_listele()
                        for x in liste:
                            if x.numarasi == numara:
                                self.ui.lbl_bilgi.setText(f"{x.ogrenci_adi} {x.ogrenci_soyadi} isimli öğrencinin okuduğu kitaplar:")
                                break
                        self.ui.table_bilgi.clear()
                        self.ui.table_bilgi.setRowCount(len(sonuc))
                        self.ui.table_bilgi.setColumnCount(5)
                        self.ui.table_bilgi.setHorizontalHeaderLabels(("Kitap no" , "Kitap adı", "Yazarı", "Alış tarihi" , "Veriş tarihi"))
                        self.ui.table_bilgi.setColumnWidth(0,75)
                        self.ui.table_bilgi.setColumnWidth(1,160)
                        self.ui.table_bilgi.setColumnWidth(2,160)
                        self.ui.table_bilgi.setColumnWidth(3,160)
                        self.ui.table_bilgi.setColumnWidth(4,160)          
                        satir = 0
                        for x in sonuc: 
                            self.ui.table_bilgi.setItem(satir,0,QTableWidgetItem(str(x[1])))
                            self.ui.table_bilgi.setItem(satir,1,QTableWidgetItem(x[3]))
                            self.ui.table_bilgi.setItem(satir,2,QTableWidgetItem(x[5]))
                            self.ui.table_bilgi.setItem(satir,3,QTableWidgetItem(x[7]))
                            if x[7] != x[-1]:
                                self.ui.table_bilgi.setItem(satir,4,QTableWidgetItem(x[-1]))
                            satir += 1
        

    def ogrenciListesi(self):
        self.ui.lbl_resim.hide()

        self.ui.lbl_bilgi.setText("Sistemde kayıtlı öğrencilerin listesi:")
        self.ui.table_bilgi.clear()
        if ogrenci_yonetimi.ogrenci_listele() == False:
            QMessageBox.warning(self,"Uyarı" , "Sistemde kayıtlı öğrenci yok ! ", QMessageBox.Ok , QMessageBox.Cancel)

        else:
            liste = ogrenci_yonetimi.ogrenci_listele()
            self.ui.table_bilgi.setRowCount(len(liste))
            self.ui.table_bilgi.setColumnCount(4)
            self.ui.table_bilgi.setHorizontalHeaderLabels(("Numara" , "Adı soyadı", "Şuan okuduğu kitap", "Kitap kodu"))
            self.ui.table_bilgi.setColumnWidth(0,75)
            self.ui.table_bilgi.setColumnWidth(1,300)
            self.ui.table_bilgi.setColumnWidth(2,300)
            self.ui.table_bilgi.setColumnWidth(3,75)           
            satir = 0
            for x in liste: 
                if len(x.okunan) == 0:
                    self.ui.table_bilgi.setItem(satir,0,QTableWidgetItem(str(x.numarasi)))
                    self.ui.table_bilgi.setItem(satir,1,QTableWidgetItem(x.ogrenci_adi +" "+ x.ogrenci_soyadi))
                else:
                    self.ui.table_bilgi.setItem(satir,0,QTableWidgetItem(str(x.numarasi)))
                    self.ui.table_bilgi.setItem(satir,1,QTableWidgetItem(x.ogrenci_adi +" "+ x.ogrenci_soyadi))
                    if x.okunan[-1][7] == x.okunan[-1][-1]:
                        self.ui.table_bilgi.setItem(satir,2,QTableWidgetItem(x.okunan[-1][3]))
                        self.ui.table_bilgi.setItem(satir,3,QTableWidgetItem(str(x.okunan[-1][1])))
                satir += 1


    def kutuphaneKitaplar(self):
        self.ui.lbl_resim.hide()
        self.ui.lbl_bilgi.setText("Kütüphanede bulunan kitapların listesi:")
        if kitap_yonetimi.kutuphane_listesi() == False:
            QMessageBox.warning(self,"Uyarı" , "Sistemde kayıtlı kitap yok ! ", QMessageBox.Ok , QMessageBox.Cancel)

        else:
            liste = kitap_yonetimi.kutuphane_listesi()
            self.ui.table_bilgi.setRowCount(len(liste))
            self.ui.table_bilgi.setColumnCount(4)
            self.ui.table_bilgi.setHorizontalHeaderLabels(("Kayıt no" , "Kitabın adı", "Yazarı", "Sayfa sayısı"))
            self.ui.table_bilgi.setColumnWidth(0,75)
            self.ui.table_bilgi.setColumnWidth(1,220)
            self.ui.table_bilgi.setColumnWidth(2,220)
            self.ui.table_bilgi.setColumnWidth(3,220)

           
            satir = 0
            for x in liste: 
                self.ui.table_bilgi.setItem(satir,0,QTableWidgetItem(str(x.no)))
                self.ui.table_bilgi.setItem(satir,1,QTableWidgetItem(x.kitap_adi))
                self.ui.table_bilgi.setItem(satir,2,QTableWidgetItem(x.yazari))
                self.ui.table_bilgi.setItem(satir,3,QTableWidgetItem(str(x.sayfa_sayisi)))
                satir += 1  


    def verilenKitaplar(self):
        self.ui.lbl_resim.hide()
        self.ui.lbl_bilgi.setText("Öğrencilere verilmiş olan kitapların listesi:")
        if kitap_yonetimi.ogrenci_kitap_listesi() == False:
            QMessageBox.warning(self,"Uyarı" , "Sistemde kayıtlı kitap yok ! ", QMessageBox.Ok , QMessageBox.Cancel)

        else:
            liste = kitap_yonetimi.ogrenci_kitap_listesi()
            self.ui.table_bilgi.setRowCount(len(liste))
            self.ui.table_bilgi.setColumnCount(3)
            self.ui.table_bilgi.setHorizontalHeaderLabels(("Kayıt no" , "Kitabın adı", "Yazarı"))
            self.ui.table_bilgi.setColumnWidth(0,75)
            self.ui.table_bilgi.setColumnWidth(1,300)
            self.ui.table_bilgi.setColumnWidth(2,300)
           
            satir = 0
            for x in liste: 
                self.ui.table_bilgi.setItem(satir,0,QTableWidgetItem(str(x.no)))
                self.ui.table_bilgi.setItem(satir,1,QTableWidgetItem(x.kitap_adi))
                self.ui.table_bilgi.setItem(satir,2,QTableWidgetItem(x.yazari))
                satir += 1  

        ###################################################


def app():
    app = QtWidgets.QApplication(sys.argv)
    win = MyApp()
    win.show()
    sys.exit(app.exec_())
app()