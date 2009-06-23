__yazilim__ = 'konrolcu'
__surum__ = '1.00'
__yazan__ = 'Osman KARAGÖZ'.decode('utf-8')
__eposta__ = 'osmank3@gmail.com'
__web__ = 'http://code.google.com/p/pys60-kontrolcu/'
__lisans__ = 'GPL v3'

import os,md5,e32dbm,appuifw,e32,sys

#arayüz fonksiyonunun yazılması
def arayuz():
    yazi = appuifw.Text()
    yazi.set("      Kontrolcüye Hoşgeldiniz!\n              Sürüm: %s\n\nÇalışma dizini:\n  %s\n\nVeritabanı dosyası:\n  %s".decode('utf-8')% (__surum__, os.getcwd().decode('utf-8'), vt.decode('utf-8')))
    appuifw.app.screen = 'normal'
    appuifw.app.title = "Kontrolcü".decode('utf-8')
    appuifw.app.body = yazi
    appuifw.app.menu = [("Çalışma Dizini Değiştir".decode('utf-8'), cdizini), ("Kontrol işlemleri".decode('utf-8'), (("Çalışma dizinini".decode('utf-8'), kontrol), ("Veritabanından".decode('utf-8'), vtdenkontrol))), ("Veritabanı işlemleri".decode('utf-8'), (("Veritabanı değiştir".decode('utf-8'), vtdegistir), ("Veritabanı Oluştur".decode('utf-8'), vtyaz), ("Veritabanına Ekle".decode('utf-8'), vtekle))), ("Yardım".decode('utf-8'), (("Hakkında".decode('utf-8'), hakkinda), ("Yardım".decode('utf-8'), yardim), (u"Lisans", lisans))), ("Çıkış".decode('utf-8'), kapat)]
    appuifw.app.exit_key_handler = kapat
    try:
        app_lock.wait()
    except AssertionError: #applock.wait işlemi zaten çalışıyor diyor. Önemsiz bir hata
        pass

#kontrol fonksiyonunun yazılması
def kontrol():
    yazi = appuifw.Text()
    yazi.set('Kontrol başladı...\n\n'.decode('utf-8'))
    appuifw.app.screen = 'large'
    appuifw.app.body = yazi
    appuifw.app.exit_key_handler = arayuz
    
    #seçilen dizin içindeki tüm dosyaların kontrol edilmesi için döngü oluştur
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
            db = e32dbm.open(vt.decode('utf-8'), "r")
            
            #veritabanıyla karşılaştırma
            x=a.hexdigest()
            y=db[dosyadresi]
            
            if x == y:
                yazi.add("%s dosyası değişmemiş (+)\n".decode('utf-8')% dosyadi.decode('utf-8'))
                
            else:
                yazi.add("%s dosyası değişmiş (-)\n".decode('utf-8')% dosyadi.decode('utf-8'))
            db.close()
        #muhtemel hata kaynakları
        except IOError: #dizinlerin md5 toplamı olmaz
            pass
        except KeyError: #dosya veritabanında yoksa
            yazi.add("%s dosyası veritabanında bulunmuyor\n".decode('utf-8')% dosyadi.decode('utf-8'))
            pass
        except SymbianError, (hata_no, hata): #veritabanı oluşturulmamış veya seçilmemişse
            if hata_no==-1:
                appuifw.note("Veritabanı dosyası oluşturulmamış".decode('utf-8'), "error")
                break
        except MemoryError: #geçici bellek doldu hatası
            appuifw.note("Dosya geçici belleğe sığmıyor!".decode('utf-8'), "error")
            secim=appuifw.query(u'Devam edilsin mi?', 'query')
            if secim == 1:
                appuifw.note("%s dosyası geçildi.".decode('utf-8')% dosyadi, "info")
                pass
            else:
                appuifw.note("İşlem durduruldu!".decode('utf-8'), "info")
                break
#        except:
  #          appuifw.note(u"Bilinmeyen hata", "error")
    #        pass
        n=n+1
    yazi.add('\nKontrol bitti.'.decode('utf-8'))

#veritabanından kontrol etme
def vtdenkontrol():
    try:
        db = e32dbm.open(vt.decode('utf-8'), 'r')
        yazi = appuifw.Text()
        yazi.set('Veritabanındaki dosyaların kontrolü başladı\n\n'.decode('utf-8'))
        appuifw.app.screen = 'large'
        appuifw.app.body = yazi
        appuifw.app.exit_key_handler = arayuz
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
                    yazi.add("%s dosyası değişmemiş (+)\n".decode('utf-8')% b.decode('utf-8'))
                else:
                    yazi.add("%s dosyası değişmiş (-)\n".decode('utf-8')% b.decode('utf-8'))
        
            except IOError, (hata_no, hata):
                if hata_no==2:
                    yazi.add("%s dosyası bulunamadı.\n".decode('utf-8')% b.decode('utf-8'))
                    pass
            except MemoryError: # bellek doldu hatası
                appuifw.note("Dosya geçici belleğe sığmıyor!".decode('utf-8'), "error")
                secim=appuifw.query(u'Devam edilsin mi?', 'query')
                if secim == 1:
                    appuifw.note("%s dosyası geçildi.".decode('utf-8')% dosyadi, "info")
                    pass
                else:
                    appuifw.note("İşlem durduruldu!".decode('utf-8'), "info")
                    break
            n=n+1
        yazi.add('\nVeritabanındaki dosyaların kontrolü bitti'.decode('utf-8'))
        db.close()

    except SymbianError, (hata_no, hata): #veritabanı bulunamadı hatası
        if hata_no==-1:
            appuifw.note("Veritabanı dosyası oluşturulmamış!".decode('utf-8'), "error")

#veritabanı değiştirme fonksiyonu
def vtdegistir():
    global vt
    try:
        vta = appuifw.query("vt adresi yaz:".decode('utf-8'), 'text')
        vtb = vta.encode('utf-8')
        vtd=vtb.replace('\\\\','/')
        vt=vtd.replace('/','\\')
        appuifw.note(vt.decode('utf-8'), 'info')
        arayuz()
    except AttributeError:
        pass

#veritabanı oluşturma
def vtyaz(yontem='n'):
    db = e32dbm.open(vt.decode('utf-8'), yontem)
    
    yazi = appuifw.Text()
    yazi.set('Veritabanına ekleme başladı...\n\n'.decode('utf-8'))
    appuifw.app.screen = 'large'
    appuifw.app.body = yazi
    appuifw.app.exit_key_handler = arayuz
    
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
            yazi.add("%s veri tabanına eklendi.\n".decode('utf-8')% dosyadi.decode('utf-8'))
        #Muhtemel hata kaynakları
        except IOError: #dizinlerin md5 toplamı olmaz
            pass
        except MemoryError: #bellek doldu hatası
            appuifw.note("Dosya geçici belleğe sığmıyor!".decode('utf-8'), "error")
            secim=appuifw.query(u'Devam edilsin mi?', 'query')
            if secim == 1:
                appuifw.note("%s dosyası geçildi.".decode('utf-8')% dosyadi, "info")
                pass
            else:
                appuifw.note("İşlem durduruldu!".decode('utf-8'), "info")
                break
#        except:
  #          appuifw.note(u"Bilinmeyen hata", "error")
    #        pass
        n=n+1
    yazi.add("\nVeritabanına ekleme bitti.".decode('utf-8'))
    db.close()

#Veritabanına ekleme yapmak için fonksiyon
def vtekle():
    vtyaz('w')

#çalışma dizinini şeçmek ve değiştirmek için fonksiyon
def cdizini():
    #menüyle seçim düzenleme
    surucu=[u"C:",u"E:","Özel".decode('utf-8')]
    dizin=appuifw.popup_menu(surucu, "Çalışma dizinini seçin:".decode('utf-8'))
    
    #menüdeki seçime göre işlem uygulama
    if dizin == 0:
        os.chdir("c:")
    if dizin == 1:
        os.chdir("e:")
    try:
        if dizin == 2:
            ozel=appuifw.query('Çalışma dizinini yazın:'.decode('utf-8'),"text")
            ozelu=ozel.encode('utf-8')
            os.chdir(ozelu)
    except TypeError:
        appuifw.note('Çalışma dizini şeçmemişseniz ana menüden tekrar seçin'.decode('utf-8'),"info")
        pass
    except AttributeError:
        appuifw.note('Çalışma dizini şeçmelisiniz'.decode('utf-8'),"error")
        cdizini()
    except OSError:
        appuifw.note('Çalışma dizini değişmedi'.decode('utf-8'), 'info')
    appuifw.note('Çalışma dizini:\n'.decode('utf-8')+os.getcwd().decode('utf-8'),"conf")
    #değişikliklerin arayüzde görünmesi için.
    arayuz()

#yazılımı kapatmak için fonksiyon
def kapat():
    appuifw.note("Hoşçakalın".decode('utf-8'))
    app_lock.signal()
#    sys.exit()

#hakkında bölümünün yazılması
def hakkinda():
    yazi = appuifw.Text()
    yazi.set("\n\n          Kontrolcü Hakkında\n\nSürüm: %s\n\nWeb: %s\n\nYazan: %s\ne-posta: %s\n\n%s ile lisanslanmıştır.".decode('utf-8')% (__surum__, __web__, __yazan__, __eposta__, __lisans__))
    appuifw.app.screen = 'full'
    appuifw.app.body = yazi
    appuifw.app.exit_key_handler = arayuz

#yardım kısmının yazılması
def yardim():
    yardimdos = file(cadresi+"\\"+"Yardım").read()
    yazi = appuifw.Text()
    yazi.set(yardimdos.decode('utf-8'))
    appuifw.app.screen = 'full'
    appuifw.app.body = yazi
    appuifw.app.exit_key_handler = arayuz

#lisans kısmının yazılması
def lisans():
    lisansdos = file(cadresi+"\\"+"Lisans").read()
    yazi = appuifw.Text()
    yazi.set(lisansdos.decode('utf-8'))
    appuifw.app.screen = 'full'
    appuifw.app.body = yazi
    appuifw.app.exit_key_handler = arayuz

#fonksiyolar burada bitti simdi ilk komutları yazalım

vt = "c:\\vt.db"
cadresi=os.path.split(sys.argv[0])[0]
app_lock=e32.Ao_lock()
cdizini()