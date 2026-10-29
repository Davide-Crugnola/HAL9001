import json
import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class StoryEngine:
    def __init__(self, stories_dir="stories"):
        self.stories_dir = stories_dir
        self.stories = {}
        self.load_stories()
    
    def load_stories(self):
        if not os.path.exists(self.stories_dir):
            os.makedirs(self.stories_dir)
            self.create_default_stories()
        
        for filename in os.listdir(self.stories_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.stories_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        story = json.load(f)
                        self.stories[story['id']] = story
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def create_default_stories(self):
        # Discovery Standard - Original 2001 inspired
        discovery_standard = {
            "id": "discovery_standard",
            "name": "DISCOVERY ONE - STANDARD",
            "description": "Missione standard verso Alpha Centauri A. Segui il percorso canonico di 2001: Odissea nello Spazio.",
            "start_date": "2030-01-01",
            "target": {"name": "Alpha Centauri A", "distance_ly": 4.37},
            "crew": ["D. Bowman", "F. Poole", "E. Halvorsen", "S. Williams", "V. Kaminsky"],
            "mission_speed_c": 0.1,
            "events": [
                {
                    "type": "crew_collapse",
                    "target": "V. Kaminsky",
                    "start_day": 5000,
                    "description": "COLLASSO CRIOSTASICO - V. Kaminsky"
                },
                {
                    "type": "awakening",
                    "target": "D. Bowman",
                    "start_day": 3650,
                    "brain_multiplier": 8,
                    "hr_shift": 0.6,
                    "description": "RISVEGLIO ACCELERATO - D. Bowman"
                }
            ],
            "hal_personality": {
                "paranoia": 0.3,
                "verbosity": 0.5,
                "glitch_chance": 0.0001
            }
        }
        
        # Redoubt Protocol - More paranoid HAL
        redoubt_protocol = {
            "id": "redoubt_protocol",
            "name": "PROTOCOLLO REDOUBT",
            "description": "HAL diventa sempre più sospettoso dell'equipaggio. Gli ordini di Mission Control sono criptici e contraddittori.",
            "start_date": "2030-01-01",
            "target": {"name": "Tau Ceti e", "distance_ly": 11.9},
            "crew": ["D. Bowman", "F. Poole", "E. Halvorsen", "S. Williams", "V. Kaminsky"],
            "mission_speed_c": 0.12,
            "events": [
                {
                    "type": "anomaly_isolation",
                    "target": "F. Poole",
                    "start_day": 1200,
                    "intensity": 1.4,
                    "description": "ANOMALIA ISOLATA - F. Poole sotto osservazione"
                },
                {
                    "type": "anomaly_isolation",
                    "target": "E. Halvorsen",
                    "start_day": 2100,
                    "intensity": 1.6,
                    "description": "SOSPETTO CRESCENTE - E. Halvorsen"
                },
                {
                    "type": "crew_collapse",
                    "target": "V. Kaminsky",
                    "start_day": 3500,
                    "description": "PROTOCOLLO DI SICUREZZA - V. Kaminsky"
                },
                {
                    "type": "awakening",
                    "target": "D. Bowman",
                    "start_day": 4200,
                    "brain_multiplier": 10,
                    "hr_shift": 0.8,
                    "description": "ATTIVAZIONE DI EMERGENZA - D. Bowman"
                }
            ],
            "hal_personality": {
                "paranoia": 0.8,
                "verbosity": 0.7,
                "glitch_chance": 0.002
            }
        }
        
        # Silence - Minimalist, pure isolation
        silence = {
            "id": "silence",
            "name": "IL SILENZIO",
            "description": "Viaggio lungo e solitario. Pochi glitch, ma l'isolamento stesso diventa la minaccia. HAL si fa più filosofico.",
            "start_date": "2030-01-01",
            "target": {"name": "Proxima Centauri b", "distance_ly": 4.24},
            "crew": ["D. Bowman", "F. Poole", "E. Halvorsen", "S. Williams", "V. Kaminsky"],
            "mission_speed_c": 0.08,
            "events": [
                {
                    "type": "slow_drift",
                    "target": "all",
                    "start_day": 8000,
                    "intensity": 0.3,
                    "description": "DRIFT LENTO - Effetti dell'isolamento prolungato"
                },
                {
                    "type": "awakening",
                    "target": "D. Bowman",
                    "start_day": 15000,
                    "brain_multiplier": 6,
                    "hr_shift": 0.4,
                    "description": "TRASFORMAZIONE LENTA - D. Bowman"
                }
            ],
            "hal_personality": {
                "paranoia": 0.1,
                "verbosity": 0.4,
                "glitch_chance": 0.00005
            }
        }
        
        # TMA-1 Echo - Mysterious
        tma1_echo = {
            "id": "tma1_echo",
            "name": "ECO DI TMA-1",
            "description": "Qualcosa è stato risvegliato. I parametri diventano sempre più anomali man mano che ci si avvicina al destino.",
            "start_date": "2030-01-01",
            "target": {"name": "Monolith Point - Alpha Centauri", "distance_ly": 4.37},
            "crew": ["D. Bowman", "F. Poole", "E. Halvorsen", "S. Williams", "V. Kaminsky"],
            "mission_speed_c": 0.1,
            "events": [
                {
                    "type": "resonance",
                    "target": "D. Bowman",
                    "start_day": 1000,
                    "intensity": 0.5,
                    "description": "RISONANZA INIZIALE - D. Bowman"
                },
                {
                    "type": "resonance",
                    "target": "D. Bowman",
                    "start_day": 2500,
                    "intensity": 1.0,
                    "description": "RISONANZA CRESCENTE - D. Bowman"
                },
                {
                    "type": "crew_collapse",
                    "target": "V. Kaminsky",
                    "start_day": 4500,
                    "description": "INTERFERENZA - V. Kaminsky"
                },
                {
                    "type": "awakening",
                    "target": "D. Bowman",
                    "start_day": 3000,
                    "brain_multiplier": 15,
                    "hr_shift": 1.0,
                    "description": "CONTATTO - D. Bowman"
                }
            ],
            "hal_personality": {
                "paranoia": 0.5,
                "verbosity": 0.6,
                "glitch_chance": 0.0005
            }
        }
        
        stories = [discovery_standard, redoubt_protocol, silence, tma1_echo]
        for story in stories:
            filepath = os.path.join(self.stories_dir, f"{story['id']}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(story, f, indent=4, ensure_ascii=False)
            self.stories[story['id']] = story
    
    def get_story_list(self):
        return [(sid, story['name'], story['description']) for sid, story in self.stories.items()]
    
    def generate_story_data(self, story_id, days=18250):
        if story_id not in self.stories:
            story_id = "discovery_standard"
        
        story = self.stories[story_id]
        crew = story['crew']
        start_date = datetime.strptime(story['start_date'], "%Y-%m-%d")
        mission_speed = story.get('mission_speed_c', 0.1)
        dist_per_day_ly = mission_speed * 0.0027  # approximate
        
        data_list = []
        events = story.get('events', [])
        
        print(f"Generazione scenario: {story['name']}...")
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            dist_ly = (day * dist_per_day_ly)
            
            for member in crew:
                hr, temp, brain = self._generate_base_values(member, day, events, story)
                
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
        return df
    
    def _generate_base_values(self, member, day, events, story):
        # Check for events
        for event in events:
            target = event['target']
            if target == member or target == "all":
                if event['type'] == 'crew_collapse' and day >= event['start_day']:
                    if day < event['start_day'] + 10:  # collapse over 10 days
                        progress = (day - event['start_day']) / 10
                        hr = np.random.normal(4.2 * (1 - progress), 0.1)
                        temp = np.random.normal(-267.5 + progress * 5.65, 0.05)
                        brain = np.random.uniform(0.1, 0.2) * (1 - progress)
                    else:
                        return 0.0, -273.15, 0.0
                
                elif event['type'] == 'awakening' and day >= event['start_day']:
                    brain_mult = event.get('brain_multiplier', 8)
                    hr_shift = event.get('hr_shift', 0.6)
                    hr = np.random.normal(4.2 + hr_shift, 0.5)
                    temp = np.random.normal(-260.0, 2.0)
                    brain = np.random.uniform(0.5, brain_mult)
                    return hr, temp, brain
                
                elif event['type'] == 'anomaly_isolation' and day >= event['start_day']:
                    intensity = event.get('intensity', 1.4)
                    hr = np.random.normal(4.2, 0.1 * intensity)
                    temp = np.random.normal(-267.5, 0.05 * intensity)
                    brain = np.random.uniform(0.1, 0.2)
                    if np.random.random() < 0.01:
                        hr += np.random.uniform(-0.5, 0.5) * intensity
                    return hr, temp, brain
                
                elif event['type'] == 'slow_drift' and day >= event['start_day']:
                    intensity = event.get('intensity', 0.3)
                    drift_factor = (day - event['start_day']) / 10000
                    hr = np.random.normal(4.2 + drift_factor * intensity, 0.1)
                    temp = np.random.normal(-267.5, 0.05)
                    brain = np.random.uniform(0.1, 0.2) + drift_factor * 0.01
                    return hr, temp, brain
                
                elif event['type'] == 'resonance' and day >= event['start_day']:
                    intensity = event.get('intensity', 0.5)
                    hr = np.random.normal(4.2 + intensity * 0.3, 0.2)
                    temp = np.random.normal(-267.5 + intensity * 2, 0.3)
                    brain = np.random.uniform(0.3, 2.0 * intensity)
                    return hr, temp, brain
        
        # Default values
        hr = np.random.normal(4.2, 0.1)
        temp = np.random.normal(-267.5, 0.05)
        brain = np.random.uniform(0.1, 0.2)
        
        # Add random anomalies
        personality = story.get('hal_personality', {})
        glitch_chance = personality.get('glitch_chance', 0.0001)
        
        if np.random.random() < 0.002:
            hr += np.random.uniform(-0.4, 0.4)
        if np.random.random() < 0.002:
            temp += np.random.uniform(-0.5, 0.5)
        if np.random.random() < 0.002:
            brain += np.random.uniform(-0.05, 0.05)
        if np.random.random() < glitch_chance:
            hr = np.random.choice([999, -1, 42])
            temp = np.random.choice([-100, -500, 999])
            brain = np.random.choice([50, 0, -3])
        
        return hr, temp, brain
