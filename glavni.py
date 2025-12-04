from jezik_nlp import *

MAPA_Z_DATOTEKAMI = './udhr' # '.'  če za isto mapo
IME_IZHODNE_DATOTEKE = "frekvence_bigramov.csv"

koncni_df = preberi_in_obdelaj_vse_datoteke(MAPA_Z_DATOTEKAMI, BIGRAMI, STOLPCI_DF)


koncni_df.to_csv(IME_IZHODNE_DATOTEKE, index=False, sep=';', encoding='utf-8')

print(f"Podatki uspešno izvoženi v {IME_IZHODNE_DATOTEKE}")
