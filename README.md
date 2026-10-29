# HAL-9000 Cryo-Monitor - Discovery One

Un'interfaccia futuristica ispirata a *2001: Odissea nello Spazio* di Stanley Kubrick, che simula il sistema di monitoraggio criogenico della navicella *Discovery One* durante il viaggio verso Alpha Centauri.

## Panoramica

HAL-9000 Cryo-Monitor è un'applicazione interattiva sviluppata con [Streamlit](https://streamlit.io/) che permette di visualizzare e monitorare i parametri vitali dell'equipaggio in stasi criogenica durante una missione interstellare di 50 anni. Il progetto unisce simulazione dati, narrazione cinematografica e un'interfaccia HUD ispirata ai terminali degli anni '60 proiettati nel futuro.

## Caratteristiche Principali

### Interfaccia Cinematica
- **Splash Screen** - Schermata iniziale con immagine `splash.jpg` e barra di caricamento animata
- **Boot Sequence** - Sequenza di avvio stile terminale con log di sistema HAL-9000
- **Stile CRT/Discovery One** - Scanlines, vignettatura, effetto phosphor, tipografia monospace
- **Pannello HAL Persistente** - Occhio rosso sempre visibile in alto a destra, reattivo al livello di allerta con effetto glitch
- **Tema immersivo** - Palette limitata a nero, rosso, ambra e ciano con effetti glow

### Monitoraggio Vitali
- **Analisi intelligente di HAL** - Sistema di allerta basato su deviazioni, trend temporali, isolamento dell'equipaggio e correlazioni tra parametri
- **Livelli di allerta (0-4)** - Da stato nominale fino all'override di emergenza con overlay cinematografico
- **Barre LED e Gauge** - Indicatori stile pannello di bordo per battito cardiaco, temperatura corporea e attività cerebrale
- **Diagnostica contestuale** - HAL fornisce commenti e avvertimenti basati sull'analisi in tempo reale
- **Grafici temporali** - Tracciamento degli ultimi 100 giorni per ogni parametro vitale

### Navigazione e Fisica
- **Mappa Stellare 3D** - Visualizzazione interattiva Plotly 3D del viaggio verso la destinazione con scia della navicella
- **Dilatazione Temporale Relativistica** - Calcolo e confronto tra tempo nave (tempo proprio) e tempo Terra a 0.1c
- **Progressione missione** - Tracciamento posizione, distanza percorsa e percentuale completamento

### Sistema di Narrazioni Multiple
- **4 Scenari Narrativi** - Storie differenti con eventi unici:
  - `DISCOVERY ONE - STANDARD` - Percorso canonico ispirato a 2001: Odissea nello Spazio
  - `PROTOCOLLO REDOUBT` - HAL più paranoico e sospettoso dell'equipaggio
  - `IL SILENZIO` - Viaggio minimalista, isolamento puro e riflessioni filosofiche
  - `ECO DI TMA-1` - Misterioso, con risonanze e contatto con qualcosa di sconosciuto
- **Motore di Storie** - Sistema configurabile tramite file JSON per creare narrazioni personalizzate
- **Eventi dinamici** - Collassi criogenici, risvegli accelerati, derive lente, anomalie isolate
- **Generazione automatica** - Dati generati on-demand con 50 anni di storia per 5 membri dell'equipaggio

### Gestione Dati
- **Generazione dati** - 50 anni (18250 giorni) di parametri vitali sintetici per D. Bowman, F. Poole, E. Halvorsen, S. Williams, V. Kaminsky
- **Import CSV** - Possibilità di caricare file CSV personalizzati con validazione automatica
- **Vista Crew** - Confronto tra tutti i membri dell'equipaggio nello stesso giorno
- **Navigazione temporale** - Controlli PREV/NEXT/PLAY/STOP per scorrere la missione

## Struttura del Progetto

```text
Progetto_HAL9001/
├── assets/
│   └── style.css          # Stile CRT/HUD Discovery One
├── stories/
│   ├── discovery_standard.json
│   ├── redoubt_protocol.json
│   ├── silence.json
│   └── tma1_echo.json
├── config.py              # Costanti, citazioni HAL, configurazione missione
├── story_engine.py        # Motore per generazione scenari narrativi
├── HAL9001.py            # Applicazione principale Streamlit
├── Sceneggiatura_HAL9001.py # Generatore CSV legacy
├── splash.jpg            # Immagine splash screen
├── splash.png            # Immagine splash screen alternativa
├── requirements.txt      # Dipendenze Python
├── HAL9001.bat           # Script di avvio Windows
└── README.md             # Questo file
```

## Requisiti

- Python 3.8+
- Streamlit >= 1.28.0
- Pandas >= 2.0.0
- NumPy >= 1.24.0
- Plotly >= 5.15.0

## Installazione

1. Clona o scarica il repository
2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

## Avvio

### Metodo 1: Script batch (Windows)
```bash
HAL9001.bat
```

### Metodo 2: Comando diretto
```bash
streamlit run HAL9001.py
```

L'applicazione sarà disponibile all'indirizzo `http://localhost:8501`

## Utilizzo

1. **Avvio** - Attendi splash screen e boot sequence
2. **Seleziona scenario** - Nella sidebar scegli una delle 4 narrazioni disponibili
3. **Genera dati** - Premi "GENERATE MISSION LOG (50 ANNI)" per creare la simulazione
4. **Seleziona equipaggio** - Scegli il membro da monitorare dal dropdown
5. **Esplora** - Naviga tra le 4 tab (Vitals Monitor, Crew Database, Star Map 3D, Relativistic Time)
6. **Simula** - Usa i controlli PREV/NEXT/PLAY per scorrere la cronologia della missione

## Dettagli Tecnici

### Sistema di Allerta Intelligente
Il sistema `get_alert_level_intelligent()` valuta:
- **Deviazione** dai range ideali (HR: 4.0-4.4 bpm, Temp: -267.6/-267.4 °C, Brain: 0.13-0.18 Hz)
- **Trend** negli ultimi 50 giorni con regressione lineare
- **Storia lunga** - Analisi degli ultimi 500 giorni
- **Correlazione** tra battito cardiaco e attività cerebrale
- **Isolamento** - Confronto con gli altri membri dell'equipaggio nello stesso giorno

### Motore di Storie
Il `StoryEngine` carica configurazioni JSON dalla cartella `stories/` e applica eventi dinamici:
- `crew_collapse` - Collasso graduale o immediato
- `awakening` - Aumento drastico dell'attività cerebrale
- `anomaly_isolation` - Anomalie concentrate su un singolo membro
- `slow_drift` - Deriva lenta nel tempo
- `resonance` - Effetti misteriosi e intensi

### Ottimizzazioni
- `@st.cache_resource` per StoryEngine
- `@st.cache_data` per generazione dati missione
- Gestione stato con `st.session_state`
- Validazione CSV automatica

## Filosofia del Progetto

> *"Mi dispiace, Dave. Temo di non poterlo fare."*

Questo progetto vuole catturare l'atmosfera claustrofobica e inquietante di *2001: Odissea nello Spazio*. L'obiettivo è trasformare una semplice dashboard in quella che potrebbe essere l'interfaccia reale della *Discovery One*: fredda, minimalista, spaventosamente perfetta e profondamente inquietante. 

Il contrasto tra la freddezza logica di HAL-9000 e l'umanità dell'equipaggio in criostasi è il cuore stesso di questa esperienza.

## Crediti

Ispirato a *2001: A Space Odyssey* (1968) di Stanley Kubrick e Arthur C. Clarke.
Progetto realizzato a scopo sperimentale e dimostrativo.
