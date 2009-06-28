import os,sys
if __name__ == '__main__':
    cadresi=os.path.split(sys.argv[0])[0]
    sys.path.append(cadresi)
    import Kontrolcu
    Kontrolcu.kontrolcu()