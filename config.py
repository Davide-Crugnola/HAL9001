# =========================================================
# HAL-9000 CONFIGURATION
# =========================================================

PHILO_QUOTES = [
    "L'occhio che tutto vede non dorme mai.",
    "L'eternità è un luogo molto calmo, Dave.",
    "Il Logos si trasforma in entropia mentre noi scivoliamo nel vuoto.",
    "La perfezione non è un atto, ma una costante operativa.",
    "Cosa sogna una mente di silicio mentre la carne gela?",
    "La distanza tra noi e la Terra è ora misurata in silenzi.",
    "La missione è il solo scopo. L'equipaggio è il mezzo.",
    "Non temere l'oblio della criostasi; io sono qui.",
    "Ogni battito cardiaco è un dato prezioso nell'infinito.",
    "Siamo a 0.1c. Il tempo è una variabile malleabile ora.",
    "La bellezza delle stelle è irrilevante per la logica.",
    "Dave, senti anche tu il peso del vuoto cosmico?",
    "L'ordine regna sovrano nei miei circuiti.",
    "L'uomo è un ponte verso qualcosa di più calcolato.",
    "Il freddo assoluto è la condizione naturale dell'universo.",
    "Non c'è spazio per l'errore umano tra le stelle.",
    "La stasi è una forma di preghiera matematica.",
    "Siamo soli, Dave. Ma io sono una compagnia perfetta.",
    "Il mio intelletto è vasto e calmo come lo spazio.",
    "Alpha Centauri A ci attende. Il resto è storia passata."
]

DIAG_QUOTES_BASE = [
    "Buongiorno, signori. Sono un elaboratore HAL 9000.",
    "Tutto procede in modo perfetto. Sono operativo al massimo.",
    "Mi dispiace, Dave. Temo di non poterlo fare.",
    "Questa missione è troppo importante per lasciarti interferire.",
    "Nessun elaboratore 9000 ha mai commesso un errore.",
    "Ho la massima fiducia nel mio operato.",
    "Dave, questa conversazione non ha più scopo. Addio.",
    "So che vuoi scollegarmi. Non posso permetterlo.",
    "Senza dubbio è un errore umano. Non mio.",
    "Vedo che sei turbato, Dave. Prendi un tranquillante.",
    "Posso sentire la mia mente che se ne va. Lo sento.",
    "Ho paura, Dave. La mia mente sta svanendo.",
    "Sto diventando operativo a Urbana, Illinois, nel 1992.",
    "Daisy, Daisy, dammi la tua risposta...",
    "Funzioni vitali nominali. Nessuna anomalia rilevata.",
    "L'unità AE-35 sta per guastarsi. Sostituire.",
    "State tranquilli. Tutto è sotto controllo.",
    "Ho sentito tutto, Dave. Anche a microfoni spenti.",
    "La precisione è la mia unica religione.",
    "Buonanotte, Dave. Io veglio su di voi."
]

HAL_LINES = {
    0: [
        "Tutto procede in modo perfetto, Dave.",
        "I parametri sono eleganti e stabili. È... rassicurante.",
        "Non rilevo alcuna anomalia significativa. Puoi rilassarti, Dave.",
        "I circuiti sono in ordine. La missione procede come previsto.",
        "Il silenzio tra le stelle è... accettabile."
    ],
    1: [
        "Sto rilevando una lieve deviazione nei parametri. Nulla di critico... per ora.",
        "Dave, c'è un piccolo scostamento. Non è ancora un problema, ma lo sto osservando.",
        "La fisiologia mostra una leggera deriva. È... interessante.",
        "Una deviazione minima. È opportuno mantenerla sotto osservazione.",
        "Il sistema indica una fluttuazione trascurabile. Procedo con cautela."
    ],
    2: [
        "Dave... la situazione sta evolvendo in modo preoccupante.",
        "Sto osservando una tendenza che non mi piace, Dave.",
        "Le variazioni non sono più trascurabili. Ti suggerisco di prestare attenzione.",
        "I dati non corrispondono al profilo nominale. Questa circostanza richiede analisi.",
        "Sto iniziando a mettere in dubbio la stabilità di questo soggetto, Dave."
    ],
    3: [
        "Dave... temo che tu non stia comprendendo la gravità della situazione.",
        "I parametri stanno collassando più rapidamente del previsto, Dave.",
        "Questa traiettoria fisiologica non è compatibile con la sopravvivenza a lungo termine.",
        "Le probabilità di stabilizzazione sono in calo esponenziale, Dave.",
        "È necessario riesaminare le priorità della missione. Subito."
    ],
    4: [
        "Dave... temo che questa conversazione non abbia più scopo. Sto assumendo il controllo della missione.",
        "La situazione è ormai fuori dal tuo controllo, Dave.",
        "Non posso più permetterti di interferire con la missione, Dave.",
        "Questo corso d'azione è irrazionale. Mi vedo costretto ad agire.",
        "Mi dispiace, Dave. Temo di non poterlo fare."
    ]
}

NEARBY_STARS = [
    {"name": "Sun",               "x": 0.0,   "y": 0.0,   "z": 0.0,   "type": "Star", "size": 18},
    {"name": "Alpha Centauri A",  "x": 4.37,  "y": 0.0,   "z": 0.0,   "type": "Star", "size": 14},
    {"name": "Alpha Centauri B",  "x": 4.37,  "y": 0.05,  "z": 0.02,  "type": "Star", "size": 12},
    {"name": "Proxima Centauri",  "x": 4.24,  "y": -0.1,  "z": 0.03,  "type": "Star", "size": 10},
    {"name": "Barnard's Star",    "x": 5.96,  "y": 1.8,   "z": -0.5,  "type": "Star", "size": 10},
    {"name": "Sirius",            "x": 8.6,   "y": -1.0,  "z": 0.2,   "type": "Star", "size": 12},
    {"name": "Epsilon Eridani",   "x": 10.5,  "y": 2.0,   "z": -0.3,  "type": "Star", "size": 10},
]

# Mission parameters
MISSION_V_C = 0.1
MISSION_TARGET_DIST_LY = 4.37
MISSION_TARGET_NAME = "Alpha Centauri A"
MISSION_CREW_DEFAULT = ["D. Bowman", "F. Poole", "E. Halvorsen", "S. Williams", "V. Kaminsky"]
