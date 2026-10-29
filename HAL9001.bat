@echo off
chcp 65001 >nul
title HAL9001 - Cryo-Monitor Launcher

:menu
cls
echo.
echo  ================================================
echo  ^> HAL-9000 Cryo-Monitor Launcher ^<
echo  ================================================
echo.
echo  [1] Avviare Dashboard Streamlit
echo  [2] Avviare con browser predefinito
echo  [3] Generare dati missione CSV
echo  [4] Aprire cartella progetto
echo  [5] Pulire cache Streamlit
echo  [6] Test dipendenze Python
echo  [0] Esci
echo.
echo ================================================
set /p scelta="Seleziona opzione: "

if "%scelta%"=="1" goto avvia
if "%scelta%"=="2" goto avvia_browser
if "%scelta%"=="3" goto genera_csv
if "%scelta%"=="4" goto apri_cartella
if "%scelta%"=="5" goto pulisci_cache
if "%scelta%"=="6" goto test_deps
if "%scelta%"=="0" goto esci

echo.
echo [!] Opzione non valida!
timeout /t 2 >nul
goto menu

:avvia
echo.
echo [*] Avvio dashboard...
python -m streamlit run HAL9001.py
goto fine

:avvia_browser
echo.
echo [*] Avvio dashboard con browser predefinito...
start http://localhost:8501
streamlit run HAL9001.py
goto fine

:genera_csv
echo.
echo [*] Generazione dati missione (50 anni)...
python -c "
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

crew = ['D. Bowman', 'F. Poole', 'E. Halvorsen', 'S. Williams', 'V. Kaminsky']
days = 18250
start_date = datetime(2030, 1, 1)

hr_mean, hr_std = 4.2, 0.1
temp_mean, temp_std = -267.5, 0.03
brain_min, brain_max = 0.1, 0.2
dist_per_day_ly = 0.00027

date_range = [start_date + timedelta(days=d) for d in range(days)]
days_array = np.arange(days)
dist_ly = days_array * dist_per_day_ly
n_records = days * len(crew)

hr_values = np.random.normal(hr_mean, hr_std, n_records)
temp_values = np.random.normal(temp_mean, temp_std, n_records)
brain_values = np.random.uniform(brain_min, brain_max, n_records)

crew_ids = np.repeat(crew, days)
day_ids = np.tile(days_array, len(crew))
dates = np.repeat([d.strftime('%Y-%m-%d') for d in date_range], len(crew))
distances = np.tile(dist_ly, len(crew))

data = {
    'Mission_Day': day_ids,
    'Date': dates,
    'PatientID': crew_ids,
    'HeartRate_bpm': np.round(hr_values, 2),
    'BodyTemp_C': np.round(temp_values, 2),
    'BrainActivity_Hz': np.round(brain_values, 3),
    'Distance_LY': np.round(distances, 5)
}
df = pd.DataFrame(data)
df.to_csv('HAL9001_Mission_Data.csv', index=False)
print(f'[*] Generati {len(df)} record salvati in HAL9001_Mission_Data.csv')
"
echo.
pause
goto menu

:apri_cartella
explorer .
goto menu

:pulisci_cache
echo.
echo [*] Pulizia cache Streamlit...
streamlit cache clear
echo [*] Cache pulita!
echo.
pause
goto menu

:test_deps
echo.
echo [*] Test dipendenze...
python -c "import streamlit; print('[OK] streamlit')" || echo "[ERR] streamlit mancante"
python -c "import pandas; print('[OK] pandas')" || echo "[ERR] pandas mancante"
python -c "import numpy; print('[OK] numpy')" || echo "[ERR] numpy mancante"
python -c "import plotly; print('[OK] plotly')" || echo "[ERR] plotly mancante"
echo.
pause
goto menu

:esci
cls
echo.
echo  ================================================
echo  ^> HAL-9000 Monitor Offline ^<
echo  ================================================
timeout /t 2 >nul
exit

:fine
