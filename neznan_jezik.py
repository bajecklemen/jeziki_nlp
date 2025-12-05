from jezik_nlp import *

VHOD = 'besedilo_v_neznanem_jeziku.txt'
IME_IZHODNE_DATOTEKE = "frekvenca_bigramov_neznanega.csv"

koncni_df = preberi_in_obdelaj_datoteko(VHOD, BIGRAMI, STOLPCI_DF)

# Izhod v CSV datoteko
koncni_df.to_csv(IME_IZHODNE_DATOTEKE, index=False, sep=';', encoding='utf-8')

print(f"Podatki uspešno izvoženi v datoteko: {IME_IZHODNE_DATOTEKE}")



    
