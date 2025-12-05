# Kako podobni so si jeziki
Osnovno gradivo je v 479 jezikov prevedena Deklaracija o človekovih pravicah. V mapi udhr. Zanima nas če se da s teh besedil odkriti, kateri jeziki so si bližje.
Ta projekt je bil narejen kot zabaven poskus, ki preverja, ali lahko računalnik prepozna, v katerem jeziku je besedilo, in hkrati ugotovi, kateri jeziki so si med seboj najbolj sorodni.

## Priprava besedil

Da pisava ne bi vplivala sem najprej transliteriral vsa besedila v male ascii znake, odstranil vsa ločila in dugo navlako tako da je vse zapisano z [a-z] in presledkom. Uporabil sem pythonova modula [unidecode](https://pypi.org/project/Unidecode/) in unidecodedata. 

## Frekvence bigramov

Za vsako transliterirano besedilo sem sestavil vektor relativnih frekvenc bigramov aa, ab, ac, ...
koda je v `glavni.py`, funkcije so v `jezik_nlp.py`, rezultat je datoteka `frekvence_bigramov.csv`.
Datoteke `test.py`, `bigram_frekvence_TEST.csv` so namenjene le testiranju funkcij v modulu.

## Gručenje

V delotoku `jeziki.ows` je gručenje jezikov, očitno podobne jezike da skupaj v gruče. Vsi slovanskiso skupaj.

## Prikaz na zemljevidu

Gruče jezikov sem hotel prikazati tudi na svetovnem zemljevidu, To sem naredil tako, da sem pripravil seznam držav, za vse te države sem izbral glavni jezik približno število govorcev. Potem sem pa države pobarval v barvah gruč.
Vse podatke o državah `globalni_dominantni_jeziki_z_govorci.csv` sem pripravil s skripto `globalni_dominantni_jeziki.py`, skripto pa je napisalo UI.

## Prepoznavanje jezika

Ko že imamo za vsak jezik bigramski vektor, me je zanimalo, če bi lahko model napovedal v katerem jeziku je besedilo.
Delotok tega poskusa je v delotoku `identifikacija_jezika.ows`. Vsebuje en kup napovednih modelov in analizo, kateri je boljši.
Če imamo besedilo in ne vemo v katerme jeziku je, ga damo v datoteko `besedilo_v_neznanem_jeziku.txt`, pošenemo skripto `neznan_jezik.py` ki shrani bigramsski vektor jezika v datoteko `frekvenca_bigramov_neznanega.csv`. To datoteko priklopimo v delotoku `identifikacija_jezika.ows`. Ponovno naložimo podatke in določimo jezik kot ciljno spremenljivko. Za zaneslivost napovedi je fino, če je vsaj kakih sto besed besedila.





