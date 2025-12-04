from jezik_nlp import *

testni_nabor = [
    {
        "jezik": "Slovenščina",
        "pisava": "Latinica (slovenski diakritiki)",
        "besedilo": "Vsi ljudje se rodijo svobodni in enaki v dostojanstvu in pravicah. 1. člen.",
    },
    {
        "jezik": "Nemščina",
        "pisava": "Latinica (umlauti, eszett)",
        "besedilo": "Alle Menschen sind frei und gleich an Würde und Rechten geboren. §1.",
    },
    {
        "jezik": "Ruščina",
        "pisava": "Cirilica",
        "besedilo": "Все люди рождаются свободными и равными в своем достоинстве и правах.",
    },
    {
        "jezik": "Grščina",
        "pisava": "Grška abeceda",
        "besedilo": "Όλοι οι άνθρωποι γεννιούνται ελεύθεροι και ίσοι στην αξιοπρέπεια και τα δικαιώματά τους.",
    },
    {
        "jezik": "Arabščina",
        "pisava": "Arabska (zapis z desne na levo)",
        "besedilo": "يولد جميع الناس أحراراً ومتساوين في الكرامة والحقوق.",
    },
    {
        "jezik": "Japonščina",
        "pisava": "Kanji in Kana",
        "besedilo": "すべての人間は、生まれながらにして自由であり、かつ、尊厳と権利とについて平等である。",
    },
    {
        "jezik": "Hindi",
        "pisava": "Devanagari",
        "besedilo": "सभी मनुष्यों को गौरव और अधिकारों के विषय में जन्मजात स्वतंत्रता और समानता प्राप्त है।",
    },
    {
        "jezik": "Vietnamščina",
        "pisava": "Latinica (kompleksni diakritiki)",
        "besedilo": "Tất cả mọi người sinh ra đều được tự do và bình đẳng về phẩm giá và quyền lợi. Điều 1.",
    },
    {
        "jezik": "Islandščina",
        "pisava": "Latinica (staronordijski znaki)",
        "besedilo": "Allar menn eru fæddir frjálsir og jafnir að virðingu og réttindum.",
    },
    {
        "jezik": "Poljščina",
        "pisava": "Latinica (slovanski diakritiki)",
        "besedilo": "Wszyscy ludzie rodzą się wolni i równi pod względem swej godności i swych praw.",
    },
]





koncni_df = sestavi_dataframe_iz_nabora(testni_nabor, BIGRAMI)

# Izhod v CSV datoteko
ime_datoteke = "bigram_frekvence_TEST.csv"
koncni_df.to_csv(ime_datoteke, index=False, sep=';', encoding='utf-8')

print(f"Podatki uspešno izvoženi v datoteko: {ime_datoteke}")



    
