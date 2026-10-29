import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_emergency_log():
    crew = ["D. Bowman", "F. Poole", "E. Halvorsen", "S. Williams", "V. Kaminsky"]
    days = 18250 # 50 anni
    start_date = datetime(2030, 1, 1)
    data_list = []
    
    print("Inizio generazione log di emergenza...")

    for day in range(days):
        current_date = start_date + timedelta(days=day)
        dist_ly = (day * 0.00027)
        
        for member in crew:

            # ============================================================
            # ATTO III — COLLASSO DI KAMINSKY
            # ============================================================
            if member == "V. Kaminsky" and day > 5000:
                hr, temp, brain = 0.0, -273.15, 0.0
            
            # ============================================================
            # ATTO III — ASCESA DI BOWMAN
            # ============================================================
            elif member == "D. Bowman" and day > 3650:
                hr = np.random.normal(4.8, 0.5)
                temp = np.random.normal(-260.0, 2.0)
                brain = np.random.uniform(0.5, 4.0)

            # ============================================================
            # ATTO I-II-IV-V — RESTO DELLA CREW
            # ============================================================
            else:
                hr = np.random.normal(4.2, 0.1)
                temp = np.random.normal(-267.5, 0.05)
                brain = np.random.uniform(0.1, 0.2)

                # ========================================================
                # A) MICRO‑ANOMALIE CASUALI
                # ========================================================
                if np.random.random() < 0.002:
                    hr += np.random.uniform(-0.4, 0.4)
                if np.random.random() < 0.002:
                    temp += np.random.uniform(-0.5, 0.5)
                if np.random.random() < 0.002:
                    brain += np.random.uniform(-0.05, 0.05)

                # ========================================================
                # B) GLITCH RARI
                # ========================================================
                if np.random.random() < 0.0001:
                    hr = np.random.choice([999, -1, 42])
                    temp = np.random.choice([-100, -500, 999])
                    brain = np.random.choice([50, 0, -3])

                # ========================================================
                # DINAMICHE PSICOLOGICHE (10 punti)
                # ========================================================

                # 1) correlazioni inesistenti
                if np.random.random() < 0.001:
                    brain += (hr - 4.2) * np.random.uniform(0.1, 0.3)

                # 2) valori troppo perfetti
                if np.random.random() < 0.001:
                    hr = 4.200

                # 3) anomalie sincronizzate
                if member in ["F. Poole", "E. Halvorsen"] and day % 777 == 0:
                    hr += 0.3

                # 4) micro-shift periodici
                if day % 500 == 0:
                    temp += np.random.uniform(-0.2, 0.2)

                # 5) glitch psicologico
                if np.random.random() < 0.0001:
                    hr = np.random.choice([999, -1, 42])

                # 6) drift lentissimo
                if day > 2000 and np.random.random() < 0.0005:
                    brain += (day / 18250) * 0.01

                # 7) oscillazioni contraddittorie
                if np.random.random() < 0.0008:
                    hr += np.random.choice([-0.3, +0.3])

                # 8) pattern ritmici
                if day % 1234 == 0:
                    brain += 0.07

                # 9) anomalie isolate
                if member == "S. Williams" and day % 999 == 0:
                    temp += 1.0

                # 10) valori impossibili ma non troppo
                if np.random.random() < 0.0002:
                    brain = round(brain * np.random.uniform(5, 10), 3)

            # ============================================================
            # SALVATAGGIO RIGA
            # ============================================================
            data_list.append({
                "Mission_Day": day,
                "Date": current_date.strftime("%Y-%m-%d"),
                "PatientID": member,
                "HeartRate_bpm": round(hr, 2),
                "BodyTemp_C": round(temp, 2),
                "BrainActivity_Hz": round(brain, 3),
                "Distance_LY": round(dist_ly, 5)
            })

    df = pd.DataFrame(data_list)
    df.to_csv("mission_log_emergency.csv", index=False)
    print("File 'mission_log_emergency.csv' generato con successo.")

if __name__ == "__main__":
    generate_emergency_log()
