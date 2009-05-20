# GPL v3 ile lisanslanmıştır

import os,md5,e32dbm,appuifw

vt = "c:\\nokia\\vt.db"

def kontrol():
    n=0
    while n < len(os.listdir("")):
        try:
            dosyadi=os.listdir("")[n]
            dosyakont=file(dosyadi).read()
            a=md5.new()
            a.update(dosyakont)
            db = e32dbm.open(vt, "r")
            x=a.hexdigest()
            y=db[dosyadi]
            if x == y:
                print dosyadi.decode('utf-8'), "dosyası değişmemiş (+)".decode('utf-8')
            else:
                appuifw.note("%s dosyası değişmiş (-)".decode('utf-8')% dosyadi.decode('utf-8'), "info")
            db.close()
        except IOError:
            pass
        except KeyError:
            appuifw.note("%s veritabanında bulunmuyor".decode('utf-8')% dosyadi.decode('utf-8'), "info")
            pass
        except SymbianError:
            appuifw.note("veritabanı bulunamıyor".decode('utf-8'), "error")
            break
        except:
            appuifw.note(u"Bilinmeyen hata", "error")
            pass
        n=n+1

def vtyaz():
    db = e32dbm.open(vt, "c")
    n=0
    while n < len(os.listdir("")):
        try:
            dosyadi=os.listdir("")[n]
            dosyakont=file(dosyadi).read()
            a=md5.new()
            a.update(dosyakont)
            kontop=a.hexdigest()
            db[dosyadi] = kontop
            print "%s veri tabanına eklendi.".decode('utf-8')% dosyadi.decode('utf-8')
        except IOError:
            pass
        except:
            appuifw.note(u"Bilinmeyen hata", "error")
            pass
        n=n+1
    db.close()

def vtsil():
    vts = vt + ".e32dbm"
    try:
        os.remove(vts)
        appuifw.note("%s veritabanı silindi".decode('utf-8')% vts, "info")
    except OSError:
        appuifw.note("Veritabanı bulunamadı".decode('utf-8'), "error")
        pass
    except:
        appuifw.note(u"Bilinmeyen hata", "error")
        pass

def cdizini():
    surucu=[u"C:",u"E:","Özel".decode('utf-8')]
    dizin=appuifw.popup_menu(surucu, "Çalışma dizinini seçin:".decode('utf-8'))
    if dizin == 0:
        os.chdir("c:")
    if dizin == 1:
        os.chdir("e:")
    try:
        if dizin == 2:
            ozel=appuifw.query('Çalışma dizinini yazın:'.decode('utf-8'),"text")
            os.chdir(ozel)
    except TypeError:
        appuifw.note('Çalışma dizini şeçmemişseniz ana menüden tekrar seçin'.decode('utf-8'),"info")
        pass
    appuifw.note('Çalışma dizini:\n'.decode('utf-8')+os.getcwd().decode('utf-8'),"conf")

#fonksiyolar burada bitti simdi arayuzu yazalim

appuifw.app.title = "Kontrolcü".decode('utf-8')
cdizini()
appmenu=''
while appmenu != 4:
    menu=["Çalışma Dizini Değiştir".decode('utf-8'), u"Kontrol et", "Veritabanına Ekle".decode('utf-8'), "Veritabanını Sil".decode('utf-8'), "Çıkış".decode('utf-8')]
    appmenu=appuifw.selection_list(choices=menu, search_field=1)
    if appmenu == 0:
        cdizini()
    if appmenu == 1:
        kontrol()
    if appmenu == 2:
        vtyaz()
    if appmenu == 3:
        vtsil()
    if appmenu == 4:
        appuifw.note("Hoşçakalın".decode('utf-8'))

print "çıkıldı".decode('utf-8')