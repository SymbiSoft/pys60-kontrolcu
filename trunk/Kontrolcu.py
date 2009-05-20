__yazilim__ = 'konrolcu'
__surum__ = '0.06'
__yazan__ = 'Osman KARAGÖZ'.decode('utf-8')
__eposta__ = 'osmank3@gmail.com'
__web__ = 'http://code.google.com/p/pys60-kontrolcu/'
__lisans__ = 'GPL v3'

import os,md5,e32dbm,appuifw,e32

#arayüz fonksiyonunun yazılması
def arayuz():
    yazi = appuifw.Text()
    yazi.set("      Kontrolcüye Hoşgeldiniz!\n              Sürüm: %s\n\nÇalışma dizini:\n  %s\n\nVeritabanı dosyası:\n  %s\n\n Seçenek tuşuna basın".decode('utf-8')% (__surum__, os.getcwd(), vt))
    appuifw.app.screen = 'normal'
    appuifw.app.title = "Kontrolcü".decode('utf-8')
    appuifw.app.body = yazi
    appuifw.app.menu = [("Çalışma Dizini Değiştir".decode('utf-8'), cdizini), (u"Kontrol et", kontrol), ("Veritabanı işlemleri".decode('utf-8'), (("Veritabanına Ekle".decode('utf-8'), vtyaz), ("Veritabanı Oluştur".decode('utf-8'), vtekle))), ("Hakkında".decode('utf-8'), hakkinda), ("Çıkış".decode('utf-8'), kapat)]
    appuifw.app.exit_key_handler = kapat
    try:
        app_lock.wait()
    except AssertionError: #applock.wait işlemi zaten çalışıyor diyor. Önemsiz bir hata
        pass

#kontrol fonksiyonunun yazılması
def kontrol():
    #seçilen dizin içindeki tüm dosyaların kontrol edilmesi için döngü oluştur
    n=0
    while n < len(os.listdir("")):
        try:
            #kontrol edilecek dosyanın okunması
            dosyadi=os.listdir("")[n]
            dosyakont=file(dosyadi).read() 
            
            #md5 toplamını oluşturma
            a=md5.new()
            a.update(dosyakont)
            
            #veritabanını okumak üzere açma
            db = e32dbm.open(vt, "r")
            
            #veritabanıyla karşılaştırma
            x=a.hexdigest()
            y=db[dosyadi]
            if x == y:
                print dosyadi.decode('utf-8'), "dosyası değişmemiş (+)".decode('utf-8')
            else:
                appuifw.note("%s dosyası değişmiş (-)".decode('utf-8')% dosyadi.decode('utf-8'), "info")
            db.close()
        #muhtemel hata kaynakları
        except IOError: #dizinlerin md5 toplamı olmaz
            pass
        except KeyError: #dosya veritabanında yoksa
            appuifw.note("%s veritabanında bulunmuyor".decode('utf-8')% dosyadi.decode('utf-8'), "info")
            pass
        except SymbianError: #veritabanı oluşturulmamış veya seçilmemişse
            appuifw.note("veritabanı bulunamıyor".decode('utf-8'), "error")
            break
        except:
            appuifw.note(u"Bilinmeyen hata", "error")
            pass
        n=n+1

#veritabanı oluşturma
def vtyaz(yontem='w'):
    db = e32dbm.open(vt, yontem)
    #seçilen dizindeki tüm dosyaların veritabanına eklenmesi için döngü oluşturulacak
    n=0
    while n < len(os.listdir("")):
        try: #veritabanına eklenecek dosyaların okunması
            dosyadi=os.listdir("")[n]
            dosyakont=file(dosyadi).read()
            
            #md5 toplamını oluşturma
            a=md5.new()
            a.update(dosyakont)
            
            #veritabanına öğe ekleme
            kontop=a.hexdigest()
            db[dosyadi] = kontop
            print "%s veri tabanına eklendi.".decode('utf-8')% dosyadi.decode('utf-8')
        
        #Muhtemel hata kaynakları
        except IOError: #dizinlerin md5 toplamı olmaz
            pass
        except:
            appuifw.note(u"Bilinmeyen hata", "error")
            pass
        n=n+1
    db.close()

#Veritabanına ekleme yapmak için fonksiyon
def vtekle():
    vtyaz('c')

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
    appuifw.note('Çalışma dizini:\n'.decode('utf-8')+os.getcwd().decode('utf-8'),"conf")
    #değişikliklerin geçerli olması için.
    arayuz()

#yazılımı kapatmak için fonksiyon
def kapat():
    appuifw.note("Hoşçakalın".decode('utf-8'))
    print "çıkıldı".decode('utf-8')
    app_lock.signal()

#hakkında bölümünün yazılması
def hakkinda():
   yazi = appuifw.Text()
   yazi.set("\n\n          Kontrolcü Hakkında\n\nSürüm: %s\n\nWeb: %s\n\nYazan: %s\ne-posta: %s\n\n%s ile lisanslanmıştır.".decode('utf-8')% (__surum__, __web__, __yazan__, __eposta__, __lisans__))
   appuifw.app.screen = 'full'
   appuifw.app.body = yazi
   appuifw.app.exit_key_handler = arayuz

#fonksiyolar burada bitti simdi ilk komutları yazalım

vt = "c:\\nokia\\vt.db"
app_lock=e32.Ao_lock()
cdizini()
