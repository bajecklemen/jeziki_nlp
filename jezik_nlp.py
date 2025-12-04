import unidecode
import re
import unicodedata
from collections import defaultdict
import pandas as pd
import os
import io

def ustvari_nabor_bigramov(abeceda):
    """
    Ustvari seznam vseh možnih bigramov iz ročno definiranega niza znakov.
    znaki - Niz vseh dovoljenih znakov (npr. 'a-z in presledek').    
    vrne - list vseh bigramov.
    """
    vsi_bigrami = [c1 + c2 for c1 in abeceda for c2 in abeceda]
    return vsi_bigrami

BIGRAMI = ustvari_nabor_bigramov('abcdefghijklmnopqrstuvwxyz ')
STOLPCI_DF = ['Jezik'] + BIGRAMI

def transliteriraj(besedilo):
    # Vse pretvorimo v male črke (velika pisava ne vpliva na glasoslovje)
    besedilo = besedilo.lower()  

    # To pretvori cirilico, devanagari, itd. v LATINIČNI ekvivalent.
    # Npr. ruski 'привет' postane 'privet', kitajski znak postane pinyin.
    besedilo_translit = unidecode.unidecode(besedilo)
    
    # Odstrani morebitne preostale diakritike (npr. 'é' -> 'e', 'ü' -> 'u')
    # Čeprav 'unidecode' to večinoma stori,
    normalizirano = ''.join(
        c for c in unicodedata.normalize('NFD', besedilo_translit)
        if unicodedata.category(c) != 'Mn' # Odstrani znake za diakritike
    )
    
    # Ohranimo samo [a-z] in presledke
    # Sedaj, ko so vse pisave v ASCII (ali blizu), lahko varno odstranimo vse,
    # kar ni del abecede: šumnike, številke, eksotične simbole.
    koncno_besedilo = re.sub(r'[^a-z\s]', '', normalizirano)
    
    # čiščenje presledkov
    koncno_besedilo = re.sub(r'\s+', ' ', koncno_besedilo).strip()

    return koncno_besedilo


def generiraj_frekvencni_vektor_bigramov(besedilo_translitirano, vsi_bigrami):
    """
    Izračuna relativne frekvence vseh bigramov v danem besedilu.
    Uporablja defaultdict za učinkovito štetje.
    besedilo_translitirano (str): Očiščeno in transliterirano besedilo.
    vsi_bigrami (list): Seznam vseh možnih bigramov.
        
    vrne list relativnih frekvenc vseh bigramov.
    """
    
    if len(besedilo_translitirano) < 2:
        # Če je besedilo prekratko, vrnemo 0.0 frekvence za vse bigrame
        return [0.0] * len(vsi_bigrami)
        
    # Uporaba defaultdict(int) za enostavno štetje brez preverjanja obstoja ključa
    bigram_counts = defaultdict(int)
    skupno_stevilo_bigramov = len(besedilo_translitirano) - 1
    
    # 1. Štetje pojavitev z defaultdict
    for i in range(skupno_stevilo_bigramov):
        bigram = besedilo_translitirano[i:i+2]
        if bigram in vsi_bigrami:
             bigram_counts[bigram] += 1
        
    frekvencni_vektor = []
    #Iteriramo strogo po vrstnem redu
    for bigram in vsi_bigrami:
        count = bigram_counts[bigram]
        frekvenca = count / skupno_stevilo_bigramov
        frekvencni_vektor.append(frekvenca)
    
    return frekvencni_vektor

def sestavi_dataframe_iz_nabora(testni_nabor, bigram_atributi):
    """
    Obdela testni nabor, izračuna frekvence in sestavi Pandas DataFrame.
    """
    
    podatki_za_df = [] # Seznam vrstic za DataFrame
    
    for primer in testni_nabor:
        ime_jezika = primer['jezik']
        besedilo = primer['besedilo']
        
        # 1. Transliteracija in čiščenje
        tt = transliteriraj(besedilo)
        
        # 2. Generiranje frekvenčnega vektorja (lista številk)
        frekvence = generiraj_frekvencni_vektor_bigramov(tt, bigram_atributi)
        
        # 3. Sestavljanje vrstice: Ime jezika + Frekvence
        # Vrsta mora imeti na začetku metapodaček (ime jezika), sledi pa 729 frekvenc.
        vrstica = [ime_jezika] + frekvence
        
        podatki_za_df.append(vrstica)


    # 4. Kreiranje DataFrame
    df = pd.DataFrame(podatki_za_df, columns=STOLPCI_DF)
    return df

def preberi_in_obdelaj_vse_datoteke(mapa_pot, bigram_atributi, stolpci_df):
    """
    Prebere vse .txt datoteke v mapi, jih obdela in vrne DataFrame.
    """
    podatki_za_df = [] 
    
    # za vse datoteke v mapi
    for ime_datoteke in os.listdir(mapa_pot):
        if ime_datoteke.endswith('.txt'):
            # Ime datoteke brez končnice ".txt"
            ime_jezika = os.path.splitext(ime_datoteke)[0]
            polna_pot = os.path.join(mapa_pot, ime_datoteke)
            
            try:
                # Branje vsebine datoteke
                with io.open(polna_pot, 'r', encoding='utf-8') as f:
                    vsebina_besedila = f.read()
                
                # Obdelava NLP funkcijami iz modula
                tt = transliteriraj(vsebina_besedila)
                frekvence = generiraj_frekvencni_vektor_bigramov(tt, bigram_atributi)
                
                # Sestavljanje vrstice
                vrstica = [ime_jezika] + frekvence
                podatki_za_df.append(vrstica)
                
            except Exception as e:
                print(f"Napaka pri obdelavi datoteke {ime_datoteke}: {e}")
                continue # Preskoči na naslednjo datoteko

    # Kreiranje DataFrame
    df = pd.DataFrame(podatki_za_df, columns=stolpci_df)
    
    return df



