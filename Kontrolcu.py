_surum = "2.0"
_web = 'http://code.google.com/p/pys60-kontrolcu/'
_yazan = 'Osman KARAGÖZ'.decode('utf-8')
_eposta = 'osmank3@gmail.com'
_lisans = 'GPL v3'

import appuifw, e32, e32dbm, md5, os, sys

from key_codes import \
     EKeyLeftArrow, EKeyRightArrow, EKeyUpArrow, EKeyDownArrow, EKeyDevice3, \
     EKey0, EKey2, EKey5, EKey8, EKeyBackspace

def tr(yazilan):
    return yazilan.decode('utf-8')


class kontrolcu:
    def __init__(self):
        self.kilit = e32.Ao_lock()
        self.cadresi=os.path.split(sys.argv[0])[0]
        self.vt=self.cadresi + "\\veritabani"
        self.kok()
    
    #kök dizini için fonksiyon
    def kok(self):
        self.dlist=[]
        self.dlist=e32.drive_list()
        self.dgost()

    #liste gösterme fonksiyonu
    def dgost(self, seciliolan=0):
        self.liskut = appuifw.Listbox(self.dlist, self.komut)
        self.liskut.set_list(self.dlist, seciliolan)
        appuifw.app.body = self.liskut
        appuifw.app.screen = 'normal'
        appuifw.app.title = tr("Kontrolcü")
        appuifw.app.exit_key_handler = self.kapat
        self.liskut.bind(EKeyLeftArrow, lambda: self.komut('ustd'))
        self.liskut.bind(EKeyRightArrow, lambda: self.komut('altd'))
        self.liskut.bind(EKey0, lambda: self.komut('kokd'))
        self.liskut.bind(EKey2, lambda: self.komut('enust'))
        self.liskut.bind(EKey5, lambda: self.komut('orta'))
        self.liskut.bind(EKey8, lambda: self.komut('enalt'))
        self.liskut.bind(EKeyBackspace, lambda: self.komut('sil'))
        appuifw.app.menu = [(tr("Yenile"), self.dyenile), (tr("Veritabanı işlemleri"), ((tr("VT'den kontrol"), self.VtdenKont), (tr("Veritabanı sıfırla"), self.Vt0),(tr("Veritabanı yedekle"), self.VtYed))), (tr("Yardım"), ((tr("Hakkında"), self.hakkinda), (tr("Yardım"), self.yardim), (u"Lisans", self.lisans))), (tr("Çıkış"), self.kapat)]
        try:
            self.kilit.wait()
        except AssertionError:
            pass

    #Arayüz için komut fonsiyonu
    def komut(self, secenek=None):
        if secenek == None:
            self.secim = self.dlist[self.liskut.current()].encode('utf-8')
            MenuList= [tr("Aç"), tr("Gir"), tr("İçeriği VT'ye ekle"), tr("VT yedeğini geri yükle"), tr("Kontrol et"), tr("Veritabanına ekle"), tr("Sil")]
            if os.path.isdir(self.secim) == 1:
                MenuList.pop(3)
                MenuList.pop(2)
                MenuList.pop(0)
                menuSecim = appuifw.popup_menu(MenuList)
                if menuSecim == 0:
                    os.chdir(self.secim)
                    self.dlist=[]
                    if len(os.listdir(os.getcwd())) == 0:
                        self.dlist.append(tr('-Dizin Boş-'))
                        self.dgost()
                    else:
                        self.dyenile()
                elif menuSecim == 1:
                    os.chdir(self.secim)
                    self.Kont()
                elif menuSecim == 2:
                    os.chdir(self.secim)
                    self.VtEkle()
                elif menuSecim == 3:
                    onay = appuifw.query(tr('Dizin silinsin mi?'), 'query')
                    try:
                        if onay == 1:
                            os.rmdir(self.secim)
                            self.dyenile()
                    except OSError, (hata_no, hata):
                        if hata_no == 17:
                            appuifw.note(tr('Dizin boş değil'), 'error')
            elif self.secim.count(".e32dbm") == 0:
                MenuList.pop(3)
                MenuList.pop(2)
                MenuList.pop(1)
                menuSecim = appuifw.popup_menu(MenuList)
                if self.secim == '-Dizin Boş-':
                    pass
                elif menuSecim == 0:
                    try:
                        appuifw.Content_handler().open_standalone(tr(os.getcwd() + self.secim))
                    except TypeError:
                        appuifw.note(tr("Dosya biçimi desteklenmiyor."), "error")
                    except SymbianError, (hata_no, hata):
                        if hata_no == -12010:
                            pass
                elif menuSecim == 1:
                    self.dKont()
                elif menuSecim == 2:
                    self.dVtEkle()
                elif menuSecim == 3:
                    onay = appuifw.query(tr('Dosya silinsin mi?'), 'query')
                    try:
                        if onay == 1:
                            os.remove(self.secim)
                            self.dyenile()
                    except OSError, (hata_no, hata):
                        if hata_no == 13:
                            appuifw.note(tr('Dosya kullanımda'), 'error')
            else:
                MenuList.pop(1)
                MenuList.pop(0)
                menuSecim = appuifw.popup_menu(MenuList)
                if menuSecim == 0:
                    self.VtGeriYuk('c')
                elif menuSecim == 1:
                    self.VtGeriYuk('n')
                elif menuSecim == 2:
                    self.dKont()
                elif menuSecim == 3:
                    self.dVtEkle()
                elif menuSecim == 4:
                    onay = appuifw.query(tr('Dosya silinsin mi?'), 'query')
                    try:
                        if onay == 1:
                            os.remove(self.secim)
                            self.dyenile()
                    except OSError, (hata_no, hata):
                        if hata_no == 13:
                            appuifw.note(tr('Dosya kullanımda'), 'error')
        elif secenek == "ustd":
            if os.getcwd() == 'C:\\' or os.getcwd() == 'D:\\' or os.getcwd() == 'E:\\' or os.getcwd() == 'Z:\\':
                self.kok()
            elif self.dlist == e32.drive_list():
                pass
            else:
                os.chdir('..')
                self.dyenile()
        elif secenek == "altd": 
            self.secim = self.dlist[self.liskut.current()].encode('utf-8')
            if os.path.isdir(self.secim) == 1:
                os.chdir(self.secim)
                self.dlist=[]
                if len(os.listdir(os.getcwd())) == 0:
                    self.dlist.append(tr('-Dizin Boş-'))
                    self.dgost()
                else:
                    self.dyenile()
            else:
                pass
        elif secenek == "sil":
            self.secim = self.dlist[self.liskut.current()].encode('utf-8')
            try:
                if os.path.isfile(self.secim):
                    onay = appuifw.query(tr('Dosya silinsin mi?'), 'query')
                    if onay == 1:
                        os.remove(self.secim)
                        self.dyenile()
                if os.path.isdir(self.secim):
                    onay = appuifw.query(tr('Dizin silinsin mi?'), 'query')
                    if onay == 1:
                        os.rmdir(self.secim)
                        self.dyenile()
            except OSError, (hata_no, hata):
                if hata_no == 17:
                    appuifw.note(tr('Dizin boş değil'), 'error')
                if hata_no == 13:
                    appuifw.note(tr('Dosya kullanımda'), 'error')
        elif secenek == "kokd":
            self.kok()
        elif secenek == "enust":
            self.dgost(0)
        elif secenek == "enalt":
            self.dgost(len(self.dlist)-1)
        elif secenek == "orta":
            self.dgost(len(self.dlist)/2)

    #arayüz yenileme için fonksiyon
    def dyenile(self):
        if self.dlist == e32.drive_list():
            self.dgost()
        if len(os.listdir(os.getcwd())) == 0:
            self.dlist=[]
            self.dlist.append(tr('-Dizin Boş-'))
            self.dgost()
        else:
            self.dlist=[]
            doslist=[]
            for i in os.listdir(os.getcwd()):
                if os.path.isdir(i):
                    self.dlist.append(tr(i))
                else:
                    doslist.append(tr(i))
            self.dlist += doslist
            self.dgost()

    #Bir dizin içeriği için kontrol fonksiyonu
    def Kont(self):
        self.yazi = appuifw.Text()
        self.yazi.set(tr('Kontrol başladı...\n\n'))
        appuifw.app.screen = 'large'
        appuifw.app.body = self.yazi
        appuifw.app.exit_key_handler = self.dyenile
        n=0
        while n < len(os.listdir("")):
            try:
                #kontrol edilecek dosyanın okunması
                dosyadi=os.listdir("")[n]
                dosyadresi=os.getcwd() + dosyadi
                dosyakont=file(dosyadi).read() 
                
                #md5 toplamını oluşturma
                a=md5.new()
                a.update(dosyakont)
                
                #geçici belleği boşaltma
                del dosyakont
                
                #veritabanını okumak üzere açma
                db = e32dbm.open(self.vt, "r")
                
                #veritabanıyla karşılaştırma
                x=a.hexdigest()
                y=db[dosyadresi]
                
                if x == y:
                    self.yazi.add(tr("%s dosyası değişmemiş (+)\n")% tr(dosyadi))
                    
                else:
                    self.yazi.add(tr("%s dosyası değişmiş (-)\n")% tr(dosyadi))
                db.close()
            #muhtemel hata kaynakları
            except IOError: #dizinlerin md5 toplamı olmaz
                pass
            except KeyError: #dosya veritabanında yoksa
                self.yazi.add(tr("%s dosyası veritabanında bulunmuyor\n")% tr(dosyadi))
                pass
            except SymbianError, (hata_no, hata): #veritabanı oluşturulmamış veya seçilmemişse
                if hata_no==-1:
                    appuifw.note(tr("Veritabanı dosyası oluşturulmamış"), "error")
                    break
            except MemoryError: #geçici bellek doldu hatası
                appuifw.note(tr("Dosya geçici belleğe sığmıyor!"), "error")
                secim=appuifw.query(u'Devam edilsin mi?', 'query')
                if secim == 1:
                    appuifw.note(tr("%s dosyası geçildi.")% dosyadi, "info")
                    pass
                else:
                    appuifw.note(tr("İşlem durduruldu!"), "info")
                    break
            n=n+1
        self.yazi.add(tr('\nKontrol bitti.'))
        os.chdir("..")

    #Tek dosyanın kontrolü için fonksiyon
    def dKont(self):
        try:
            #kontrol edilecek dosyanın okunması
            dosyadi=self.secim
            dosyadresi=os.getcwd() + dosyadi
            dosyakont=file(dosyadi).read()
            
            #md5 toplamını oluşturma
            a=md5.new()
            a.update(dosyakont)
            
            #geçici belleği boşaltma
            del dosyakont
            
            #veritabanını okumak üzere açma
            db = e32dbm.open(self.vt, "r")
            
            #veritabanıyla karşılaştırma
            x=a.hexdigest()
            y=db[dosyadresi]
            
            if x == y:
                appuifw.note(tr("%s dosyası değişmemiş (+)\n")% tr(dosyadi), "info")
                
            else:
                appuifw.note(tr("%s dosyası değişmiş (-)\n")% tr(dosyadi), "info")
            db.close()
        #muhtemel hata kaynakları
        except KeyError: #dosya veritabanında yoksa
            appuifw.note(tr("%s dosyası veritabanında bulunmuyor\n")% tr(dosyadi), "error")
        except SymbianError, (hata_no, hata): #veritabanı oluşturulmamış veya seçilmemişse
            if hata_no==-1:
                appuifw.note(tr("Veritabanı dosyası oluşturulmamış"), "error")
        except MemoryError: #geçici bellek doldu hatası
            appuifw.note(tr("Dosya geçici belleğe sığmıyor!"), "error")

    #Dizin içeriğini veritabanına ekleme
    def VtEkle(self):
        db = e32dbm.open(self.vt, "c")
        
        self.yazi = appuifw.Text()
        self.yazi.set(tr('Veritabanına ekleme başladı...\n\n'))
        appuifw.app.screen = 'large'
        appuifw.app.body = self.yazi
        appuifw.app.exit_key_handler = self.dyenile

        #seçilen dizindeki tüm dosyaların veritabanına eklenmesi için döngü oluşturulacak
        n=0
        while n < len(os.listdir("")):
            try: #veritabanına eklenecek dosyaların okunması
                dosyadi=os.listdir("")[n]
                dosyakont=file(dosyadi).read()
                
                #md5 toplamını oluşturma
                a=md5.new()
                a.update(dosyakont)
                
                #geçici belleği boşaltma
                del dosyakont
                
                #veritabanına öğe ekleme
                kontop=a.hexdigest()
                dosyadresi = os.getcwd() + dosyadi
                db[dosyadresi] = kontop
                self.yazi.add(tr("%s veri tabanına eklendi.\n")% tr(dosyadi))
            #Muhtemel hata kaynakları
            except IOError: #dizinlerin md5 toplamı olmaz
                pass
            except MemoryError: #bellek doldu hatası
                appuifw.note(tr("Dosya geçici belleğe sığmıyor!"), "error")
                secim=appuifw.query(u'Devam edilsin mi?', 'query')
                if secim == 1:
                    appuifw.note(tr("%s dosyası geçildi.")% dosyadi, "info")
                    pass
                else:
                    appuifw.note(tr("İşlem durduruldu!"), "info")
                    break
            n=n+1
        self.yazi.add(tr("\nVeritabanına ekleme bitti."))
        db.close()
        os.chdir("..")

    #Tek dosya için veritabanına ekleme fonsiyonu
    def dVtEkle(self):
        db = e32dbm.open(self.vt, "c")
        
        try:
            dosyadi=self.secim
            dosyadresi = os.getcwd() + dosyadi
            dosyakont=file(dosyadi).read()
            
            #md5 toplamını oluşturma
            a=md5.new()
            a.update(dosyakont)
            
            #geçici belleği boşaltma
            del dosyakont
            
            #veritabanına öğe ekleme
            kontop=a.hexdigest()
            db[dosyadresi] = kontop
            appuifw.note(tr("%s veri tabanına eklendi.\n")% tr(dosyadi), "conf")
        #Muhtemel hata kaynakları
        except MemoryError: #bellek doldu hatası
            appuifw.note(tr("Dosya geçici belleğe sığmıyor!"), "error")
        db.close()

    #Veritabanı içeriğindeki dosyaların kontrolü
    def VtdenKont(self):
        try:
            db = e32dbm.open(self.vt, 'r')
            self.yazi = appuifw.Text()
            self.yazi.set(tr('Veritabanındaki dosyaların kontrolü başladı\n\n'))
            appuifw.app.screen = 'large'
            appuifw.app.body = self.yazi
            appuifw.app.exit_key_handler = self.dyenile
            n=0
            while n<len(db.keys()):
                a=md5.new()
                b=db.keys()[n]
                try:
                    dosya=file(b).read()
                    a.update(dosya)
                    
                    #geçici belleği boşaltma
                    del dosya
                    
                    x=a.hexdigest()
                    y=db[b]
                    if x==y:
                        self.yazi.add(tr("%s dosyası değişmemiş (+)\n")% tr(b))
                    else:
                        self.yazi.add(tr("%s dosyası değişmiş (-)\n")% tr(b))
                
                except IOError, (hata_no, hata):
                    if hata_no==2:
                        self.yazi.add(tr("%s dosyası bulunamadı.\n")% tr(b))
                        pass
                except MemoryError: # bellek doldu hatası
                    appuifw.note(tr("Dosya geçici belleğe sığmıyor!"), "error")
                    secim=appuifw.query(u'Devam edilsin mi?', 'query')
                    if secim == 1:
                        appuifw.note(tr("%s dosyası geçildi.")% dosyadi, "info")
                        pass
                    else:
                        appuifw.note(tr("İşlem durduruldu!"), "info")
                        break
                n=n+1
            self.yazi.add(tr('\nVeritabanındaki dosyaların kontrolü bitti'))
            db.close()

        except SymbianError, (hata_no, hata): #veritabanı bulunamadı hatası
            if hata_no==-1:
                appuifw.note(tr("Veritabanı dosyası oluşturulmamış!"), "error")

    #Veritabanı içeriğini sıfırlamak için fonksiyon
    def Vt0(self):
        db = e32dbm.open(self.vt, "n")
        db.clear()
        db.close()
        appuifw.note(tr("Veritabanı sıfırlandı!"), "conf")

    #Veritabanı yedeği almak için fonksiyon
    def VtYed(self):
        dbvt = e32dbm.open(self.vt, 'r')
        try:
            vtyed = appuifw.query(tr("Yedeği kaydetme yeri:"), "text", tr("C:\\yedek"))
            dbyed = e32dbm.open(vtyed, 'n')
            for i in dbvt.keys():
                dbyed[i]=dbvt[i]
            dbyed.sync()
            dbyed.close()
            dbvt.close()
            appuifw.note(tr('Yedek oluşturuldu.'), 'conf')
        except:
            appuifw.note(tr('Yedek oluşturulamadı'), 'error')

    #Veritabanı yedeği geri yükleme ve veritabanı içerik birleştirme
    def VtGeriYuk(self, yontem):
        dbvt = e32dbm.open(self.vt, yontem)
        vtyed = os.getcwd() + self.secim
        dbyed = e32dbm.open(vtyed, 'r')
        for i in dbyed.keys():
            dbvt[i]=dbyed[i]
        dbvt.sync()
        dbvt.close()
        dbyed.close()
        if yontem == 'n':
            appuifw.note(tr('Yedek geri yüklendi.'), 'conf')
        else:
            appuifw.note(tr('Dosya içeriği veritabanına eklendi.'), 'conf')

    #hakkında bölümünün yazılması
    def hakkinda(self):
        self.yazi = appuifw.Text()
        self.yazi.set(tr("\n\n          Kontrolcü Hakkında\n\nSürüm: %s\n\nWeb: %s\n\nYazan: %s\ne-posta: %s\n\n%s ile lisanslanmıştır.")% (_surum, _web, _yazan, _eposta, _lisans))
        appuifw.app.screen = 'full'
        appuifw.app.body = self.yazi
        appuifw.app.exit_key_handler = self.kok

    #yardım kısmının yazılması
    def yardim(self):
        yardimdos = file(self.cadresi+"\\"+"Yardım").read()
        self.yazi = appuifw.Text()
        self.yazi.set(yardimdos.decode('utf-8'))
        appuifw.app.screen = 'full'
        appuifw.app.body = self.yazi
        appuifw.app.exit_key_handler = self.kok

    #lisans kısmının yazılması
    def lisans(self):
        lisansdos = file(self.cadresi+"\\"+"Lisans").read()
        self.yazi = appuifw.Text()
        self.yazi.set(lisansdos.decode('utf-8'))
        appuifw.app.screen = 'full'
        appuifw.app.body = self.yazi
        appuifw.app.exit_key_handler = self.kok

    #kapatma fonksiyonu
    def kapat(self):
        self.kilit.signal()
#        sys.exit()

if __name__ == '__main__':
    #kontrolcu()
    pass