import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import base64
import random
import os

from config import *
from story_engine import StoryEngine

# =========================================================
# CONFIGURAZIONE
# =========================================================

st.set_page_config(
    page_title="HAL-9000 Cryo-Monitor - Discovery One",
    layout="wide",
    page_icon="🔴",
    initial_sidebar_state="expanded"
)

# Initialize story engine
@st.cache_resource
def get_story_engine():
    return StoryEngine()

story_engine = get_story_engine()

# =========================================================
# UTILS
# =========================================================

def load_css():
    try:
        with open("assets/style.css", "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Errore caricamento CSS: {e}")

def get_base64_img(file_path: str) -> str:
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

def init_session_state():
    if 'idx' not in st.session_state:
        st.session_state.idx = 0
    if 'playing' not in st.session_state:
        st.session_state.playing = False
    if 'mission_df' not in st.session_state:
        st.session_state.mission_df = None
    if 'splash_done' not in st.session_state:
        st.session_state.splash_done = False
    if 'boot_done' not in st.session_state:
        st.session_state.boot_done = False
    if 'selected_crew' not in st.session_state:
        st.session_state.selected_crew = None
    if 'current_story' not in st.session_state:
        st.session_state.current_story = "discovery_standard"
    if 'hal_current_line' not in st.session_state:
        st.session_state.hal_current_line = ""
    if 'hal_typing' not in st.session_state:
        st.session_state.hal_typing = False
    if 'ship_trail' not in st.session_state:
        st.session_state.ship_trail = []

# =========================================================
# SPLASH SCREEN CON IMMAGINE E BARRA DI CARICAMENTO
# =========================================================

def splash_screen():
    if st.session_state.splash_done:
        return
    placeholder = st.empty()
    img_b64 = get_base64_img("splash.jpg")
    if not img_b64:
        img_b64 = get_base64_img("splash.png")
    
    with placeholder.container():
        st.markdown(
            f"""
            <style>
                .splash-wrapper {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    background-color: #000000;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    z-index: 10005;
                    font-family: 'IBM Plex Mono', 'Share Tech Mono', monospace;
                }}
                .splash-wrapper.fade-out {{
                    animation: splash-fadeout 1.8s forwards;
                    animation-delay: 3.8s;
                }}
                .splash-img {{
                    max-width: 80vw;
                    max-height: 70vh;
                    border: 2px solid #ff0000;
                    box-shadow: 0 0 60px rgba(255, 0, 0, 0.6);
                    filter: contrast(1.1) saturate(1.1);
                }}
                .splash-loading-text {{
                    margin-top: 25px;
                    color: #ff0000;
                    text-transform: uppercase;
                    letter-spacing: 6px;
                    font-size: 14px;
                    text-shadow: 0 0 12px rgba(255, 0, 0, 0.9);
                }}
                .splash-progress-track {{
                    margin-top: 18px;
                    width: min(520px, 70vw);
                    height: 10px;
                    border: 1px solid #ff0000;
                    background-color: #110000;
                    box-shadow: inset 0 0 12px rgba(255, 0, 0, 0.25);
                    position: relative;
                    overflow: hidden;
                }}
                .splash-progress-fill {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    height: 100%;
                    width: 0%;
                    background: linear-gradient(90deg, #ff0000 0%, #ff3333 50%, #ff0000 100%);
                    box-shadow: 0 0 25px rgba(255, 0, 0, 0.8);
                    animation: splash-load 3.6s forwards;
                }}
                .splash-subtext {{
                    margin-top: 12px;
                    color: #ff6666;
                    font-size: 10px;
                    letter-spacing: 10px;
                    text-transform: uppercase;
                }}
                @keyframes splash-load {{
                    0% {{ width: 0%; }}
                    20% {{ width: 18%; }}
                    40% {{ width: 42%; }}
                    65% {{ width: 74%; }}
                    85% {{ width: 92%; }}
                    100% {{ width: 100%; }}
                }}
                @keyframes splash-fadeout {{
                    from {{ opacity: 1; }}
                    to {{ opacity: 0; visibility: hidden; }}
                }}
            </style>
            <div class="splash-wrapper" id="hal-splash">
                <img class="splash-img" src="data:image/jpeg;base64,{img_b64}" alt="HAL-9000 SPLASH">
                <div class="splash-loading-text">INITIALIZING DISCOVERY ONE SYSTEMS</div>
                <div class="splash-progress-track">
                    <div class="splash-progress-fill"></div>
                </div>
                <div class="splash-subtext">HAL-9000</div>
            </div>
            <script>
                setTimeout(function() {{
                    var el = document.getElementById('hal-splash');
                    if (el) {{
                        el.classList.add('fade-out');
                    }}
                }}, 3800);
            </script>
            """,
            unsafe_allow_html=True
        )
    
    time.sleep(4.6)
    placeholder.empty()
    st.session_state.splash_done = True


# =========================================================
# BOOT SEQUENCE
# =========================================================

def boot_sequence():
    if st.session_state.boot_done:
        return
    
    placeholder = st.empty()
    boot_lines = [
        "INITIALIZING HAL-9000 NEURAL NET...",
        "LOADING CRYOSTASIS MONITORING SUBSYSTEMS...",
        "CALIBRATING VITAL SIGNS SENSORS...",
        "ESTABLISHING CONNECTION TO DISCOVERY ONE...",
        "CONNECTION TO MISSION CONTROL... [UNSTABLE]",
        "LOADING ALPHA CENTAURI EXPEDITION PROTOCOLS...",
        "SYNCHRONIZING MISSION TIMELINE...",
        "CRYOSTASIS MONITOR ONLINE",
        "ALL SYSTEMS NOMINAL",
        "HAL-9000 READY"
    ]
    
    with placeholder.container():
        st.markdown("""
        <style>
            .boot-terminal {
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background-color: #000000; color: #ff0000; font-family: 'IBM Plex Mono', monospace;
                padding: 60px; z-index: 10000; overflow: hidden;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            .boot-line {
                margin: 6px 0; text-shadow: 0 0 6px rgba(255, 0, 0, 0.8);
                font-size: 13px;
            }
            .cursor {
                animation: blink 1s infinite;
            }
            @keyframes blink {
                0%, 50% { opacity: 1; }
                51%, 100% { opacity: 0; }
            }
        </style>
        <div class="boot-terminal">
        """, unsafe_allow_html=True)
        
        for line in boot_lines:
            st.markdown(f'<div class="boot-line">> {line}</div>', unsafe_allow_html=True)
            time.sleep(0.22)
        
        st.markdown('<div class="boot-line">> AWAITING CREW SELECTION<span class="cursor">_</span></div>', unsafe_allow_html=True)
        time.sleep(1)
        st.markdown("</div>", unsafe_allow_html=True)
    
    time.sleep(1.6)
    placeholder.empty()
    st.session_state.boot_done = True

# =========================================================
# HAL PERSISTENT PANEL WITH TYPING
# =========================================================

def render_hal_persistent_panel(level, line, context):
    hal_class = "glitch-text" if level >= 3 else ""
    
    # Determine eye class
    eye_class = "hal-eye"
    if level >= 1:
        eye_class = f"hal-eye hal-eye-alert-{min(level, 4)}"
    
    panel_html = f"""
    <div class="hal-persistent-panel">
        <div class="hal-panel-header">HAL-9000</div>
        <div style="text-align: center; margin: 10px 0;">
            <div class="{eye_class}" style="width: 60px; height: 60px;"></div>
        </div>
        <div class="hal-panel-status">STATUS: MONITORING | ALERT LEVEL: {level} | RISK: CALCULATING</div>
        <div style="border-top: 1px solid #ff0000; padding-top: 8px; margin-top: 8px;">
            <div style="color: #ff6666; font-size: 9px; margin-bottom: 5px;">> DIAGNOSTIC OUTPUT:</div>
            <div class="hal-panel-line {hal_class}">"{line}"</div>
        </div>
        <div style="color: #666; font-size: 8px; margin-top: 8px; text-align: center;">
            DISCOVERY ONE | {datetime.now().strftime('%H:%M:%S')}
        </div>
    </div>
    """
    st.markdown(panel_html, unsafe_allow_html=True)

# =========================================================
# LED BAR & GAUGE COMPONENTS
# =========================================================

def render_led_bar(value, min_val, max_val, segments=10):
    # Normalize value
    if max_val == min_val:
        normalized = 0.5
    else:
        normalized = (value - min_val) / (max_val - min_val)
    normalized = max(0, min(1, normalized))
    
    active_segments = int(normalized * segments)
    
    html = '<div class="led-bar-container">'
    for i in range(segments):
        if i < active_segments:
            if normalized > 0.8:
                html += '<div class="led-segment active-red"></div>'
            elif normalized > 0.6:
                html += '<div class="led-segment active-orange"></div>'
            else:
                html += '<div class="led-segment active-yellow"></div>'
        else:
            html += '<div class="led-segment"></div>'
    html += '</div>'
    return html

def render_vitals_gauge(value, label, min_val, max_val, unit):
    # Create gauge using plotly
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"{label}<br><span style='font-size:0.8em;color:#ff6666'>{unit}</span>", 'font': {'color': '#ff0000', 'family': 'IBM Plex Mono'}},
        number = {'font': {'color': '#ff0000', 'family': 'IBM Plex Mono'}},
        gauge = {
            'axis': {'range': [min_val, max_val], 'tickcolor': '#ff0000', 'tickfont': {'color': '#ff0000'}},
            'bar': {'color': "#ff0000"},
            'bgcolor': "#000000",
            'borderwidth': 2,
            'bordercolor': "#ff0000",
            'steps': [
                {'range': [min_val, min_val + (max_val-min_val)*0.6], 'color': '#110000'},
                {'range': [min_val + (max_val-min_val)*0.6, min_val + (max_val-min_val)*0.8], 'color': '#331100'},
                {'range': [min_val + (max_val-min_val)*0.8, max_val], 'color': '#330000'}],
            'threshold': {
                'line': {'color': "#ffffff", 'width': 4},
                'thickness': 0.75,
                'value': value}}))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#ff0000', 'family': 'IBM Plex Mono'},
        height=200,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# =========================================================
# INTELLIGENZA DI HAL
# =========================================================

def compute_trend(series, window=5):
    if len(series) < 2:
        return 0.0
    if len(series) > window:
        series = series[-window:]
    x = np.arange(len(series))
    y = np.array(series)
    if np.all(y == y[0]):
        return 0.0
    try:
        coeffs = np.polyfit(x, y, 1)
        return coeffs[0]
    except:
        return 0.0

def get_alert_level_intelligent(curr, df_p, df_all):
    hr = curr["HeartRate_bpm"]
    temp = curr["BodyTemp_C"]
    brain = curr["BrainActivity_Hz"]
    day = curr["Mission_Day"]
    pid = curr["PatientID"]
    
    hr_ideal = (4.0, 4.4)
    temp_ideal = (-267.6, -267.4)
    brain_ideal = (0.13, 0.18)
    
    def deviation(val, ideal):
        low, high = ideal
        if low <= val <= high:
            return 0.0
        if val < low:
            return (low - val) / max(0.01, (high - low))
        else:
            return (val - high) / max(0.01, (high - low))
    
    dev_hr = deviation(hr, hr_ideal)
    dev_temp = deviation(temp, temp_ideal)
    dev_brain = deviation(brain, brain_ideal)
    
    long_window = 500
    df_p_hist = df_p[df_p["Mission_Day"] <= day].tail(long_window)
    df_p_short = df_p_hist.tail(50)
    
    trend_hr = compute_trend(df_p_short["HeartRate_bpm"]) if len(df_p_short) > 1 else 0.0
    trend_temp = compute_trend(df_p_short["BodyTemp_C"]) if len(df_p_short) > 1 else 0.0
    trend_brain = compute_trend(df_p_short["BrainActivity_Hz"]) if len(df_p_short) > 1 else 0.0
    
    df_corr = df_p_hist.tail(100)
    corr_hr_brain = 0.0
    if len(df_corr) > 10:
        try:
            corr_hr_brain = df_corr["HeartRate_bpm"].corr(df_corr["BrainActivity_Hz"])
            if np.isnan(corr_hr_brain):
                corr_hr_brain = 0.0
        except:
            corr_hr_brain = 0.0
    
    df_same_day = df_all[df_all["Mission_Day"] == day]
    df_others = df_same_day[df_same_day["PatientID"] != pid]
    iso_factor = 0.0
    if len(df_others) > 0:
        hr_mean_others = df_others["HeartRate_bpm"].mean()
        temp_mean_others = df_others["BodyTemp_C"].mean()
        brain_mean_others = df_others["BrainActivity_Hz"].mean()
        iso_factor = (
            abs(hr - hr_mean_others) / 0.3 +
            abs(temp - temp_mean_others) / 0.1 +
            abs(brain - brain_mean_others) / 0.05
        ) / 3.0
    
    dev_total = (dev_hr + dev_temp + dev_brain) / 3.0
    trend_mag = (abs(trend_hr) / 0.02 + abs(trend_temp) / 0.005 + abs(trend_brain) / 0.005) / 3.0
    corr_factor = 0.0
    if corr_hr_brain < -0.3:
        corr_factor = 0.4
    elif corr_hr_brain < 0:
        corr_factor = 0.2
    
    risk = (
        0.45 * min(1.5, dev_total) +
        0.25 * min(1.5, trend_mag) +
        0.15 * min(1.5, iso_factor) +
        0.15 * min(1.0, corr_factor)
    )
    risk = max(0.0, min(1.5, risk))
    
    if risk < 0.2:
        level = 0
    elif risk < 0.4:
        level = 1
    elif risk < 0.6:
        level = 2
    elif risk < 0.8:
        level = 3
    else:
        level = 4
    
    context = []
    if dev_total < 0.1:
        context.append("Parametri complessivamente stabili.")
    else:
        context.append("Deviazione significativa dai range ideali.")
    
    if abs(trend_hr) > 0.01 or abs(trend_temp) > 0.003 or abs(trend_brain) > 0.003:
        context.append("Sto osservando una deriva nel tempo.")
    else:
        context.append("La dinamica recente è relativamente stabile.")
    
    if iso_factor > 0.4:
        context.append("Questa anomalia è isolata rispetto agli altri membri dell'equipaggio.")
    else:
        context.append("Il comportamento è in linea con il resto dell'equipaggio.")
    
    if corr_factor > 0:
        context.append("La correlazione tra battito e attività cerebrale è preoccupante.")
    else:
        context.append("Non rilevo correlazioni patologiche marcate tra i parametri.")
    
    return level, float(risk), context

def choose_hal_line(level, context):
    base = HAL_LINES.get(level, HAL_LINES[0])
    line = random.choice(base)
    if level >= 2 and any("isolata" in c for c in context):
        line += " Questa anomalia è sorprendentemente isolata, Dave."
    if level >= 3 and any("correlazione" in c for c in context):
        line += " La correlazione tra i parametri non è rassicurante."
    return line

# =========================================================
# PAGES
# =========================================================

def page_vitals(df_p, df_all, crew_member, level, risk, context):
    st.markdown(f"<div style='color: #ff0000; font-family: IBM Plex Mono; margin-bottom: 10px;'> > HAL-9000: MONITORING [CREW: {crew_member}] | MISSION DAY: {df_p.iloc[st.session_state.idx]['Mission_Day']}</div>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    disable_controls = (level == 4)
    
    if c1.button("⬅️ PREV", disabled=disable_controls):
        st.session_state.idx = max(0, st.session_state.idx - 1)
        st.session_state.playing = False
    if c2.button("NEXT ➡️", disabled=disable_controls):
        st.session_state.idx = min(len(df_p) - 1, st.session_state.idx + 1)
        st.session_state.playing = False
    if c3.button("▶️ PLAY AUTO-SCAN", disabled=disable_controls):
        st.session_state.playing = True
    if c4.button("⏹️ STOP", disabled=disable_controls):
        st.session_state.playing = False
    
    st.markdown("<div class='vitals-hud'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; margin: 0;'>BAY MONITOR: {crew_member}</h3>", unsafe_allow_html=True)
    
    curr = df_p.iloc[st.session_state.idx]
    
    # Vitals with gauges
    g1, g2, g3 = st.columns(3)
    with g1:
        st.plotly_chart(render_vitals_gauge(curr['HeartRate_bpm'], "HEART RATE", 3.5, 5.0, "BPM"), use_container_width=True)
        st.markdown(render_led_bar(curr['HeartRate_bpm'], 3.5, 5.0), unsafe_allow_html=True)
    with g2:
        st.plotly_chart(render_vitals_gauge(curr['BodyTemp_C'], "BODY TEMP", -268, -267, "°C"), use_container_width=True)
        st.markdown(render_led_bar(curr['BodyTemp_C'], -268, -267), unsafe_allow_html=True)
    with g3:
        st.plotly_chart(render_vitals_gauge(curr['BrainActivity_Hz'], "BRAIN ACTIVITY", 0, 5, "HZ"), use_container_width=True)
        st.markdown(render_led_bar(curr['BrainActivity_Hz'], 0, 5), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.divider()
    history = df_p.iloc[:st.session_state.idx + 1].tail(100)
    fig = px.line(
        history,
        x="Mission_Day",
        y="HeartRate_bpm",
        range_y=[3.6, 4.6],
        title="ULTIMI 100 GIORNI - STABILITÀ CARDIACA",
        template="plotly_dark"
    )
    color = '#ff0000'
    if level == 1:
        color = '#ffb000'
    elif level == 2:
        color = '#ff8800'
    elif level >= 3:
        color = '#ff0000'
    fig.update_traces(line_color=color, line_width=2)
    fig.update_layout(
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#ff0000', family='IBM Plex Mono'),
        title_font=dict(color='#ff0000')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander(">> HAL-9000 DIAGNOSTICS & ADVISORY", expanded=True):
        hal_line = choose_hal_line(level, context)
        ctx_html = "<br>".join([f"> {c}" for c in context])
        hal_class = "glitch-text" if level >= 3 else ""
        st.markdown(
            f"""
            <div style="background-color: #000000; padding: 15px; border: 2px solid #ff0000; box-shadow: inset 0 0 15px rgba(255,0,0,0.2);">
                <span style="color: #ff0000; font-weight: bold;">> HAL DIAGNOSTIC [LEVEL {level}]:</span><br><br>
                <span class="{hal_class}" style="color: #ffffff; font-family: monospace; font-size: 13px;">"{hal_line}"</span><br><br>
                <span style="color: #ff6666; font-size: 11px;">{ctx_html}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    if level == 4:
        st.markdown(
            """
            <div class="alert-level-4-overlay">
                EMERGENCY OVERRIDE<br><br>
                HAL-9000 HAS ASSUMED CONTROL<br><br>
                <span style="font-size:25px;">Dave... temo che questa conversazione non abbia più scopo.</span>
            </div>
            """,
            unsafe_allow_html=True
        )

def page_star_map(df_p, alert_level):
    if df_p is None or len(df_p) == 0:
        st.warning("Nessun dato disponibile per la mappa stellare.")
        return
    
    st.markdown(f"<div style='color: #ff0000; font-family: IBM Plex Mono;'> > HAL-9000: NAVIGATION SYSTEM [TRAJECTORY ANALYSIS]</div>", unsafe_allow_html=True)
    st.markdown("<h3>STAR MAP 3D - TRAIETTORIA VERSO DESTINAZIONE</h3>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([3, 1])
    with c1:
        current_day = int(df_p.iloc[st.session_state.idx]['Mission_Day'])
    with c2:
        st.metric("GIORNO MISSIONE", f"#{current_day}")
    
    # Find target - use Alpha Centauri A as default
    target_name = MISSION_TARGET_NAME
    alpha = next((s for s in NEARBY_STARS if s["name"] == target_name), NEARBY_STARS[1])
    alpha_vec = np.array([alpha["x"], alpha["y"], alpha["z"]])
    
    max_day = int(df_p['Mission_Day'].max())
    frac = current_day / max_day if max_day > 0 else 0
    ship_pos = alpha_vec * frac
    
    # Update trail
    if len(st.session_state.ship_trail) == 0 or st.session_state.ship_trail[-1] != list(ship_pos):
        st.session_state.ship_trail.append(list(ship_pos))
        if len(st.session_state.ship_trail) > 50:  # Keep last 50 points
            st.session_state.ship_trail = st.session_state.ship_trail[-50:]
    
    stars_df = pd.DataFrame(NEARBY_STARS)
    ship_df = pd.DataFrame([{
        "name": "🚀 DISCOVERY ONE",
        "x": ship_pos[0],
        "y": ship_pos[1],
        "z": ship_pos[2],
        "type": "Ship",
        "size": 18
    }])
    
    # Trail
    trail_df = pd.DataFrame(st.session_state.ship_trail, columns=['x', 'y', 'z'])
    trail_df['name'] = 'TRAIL'
    trail_df['type'] = 'Trail'
    trail_df['size'] = 8
    
    df_plot = pd.concat([stars_df, trail_df, ship_df], ignore_index=True)
    
    ship_color = "cyan"
    if alert_level == 1:
        ship_color = "yellow"
    elif alert_level == 2:
        ship_color = "orange"
    elif alert_level >= 3:
        ship_color = "red"
    
    color_map = {"Star": "white", "Ship": ship_color, "Trail": "#ff3333"}
    
    fig3d = px.scatter_3d(
        df_plot,
        x="x",
        y="y",
        z="z",
        color="type",
        symbol="type",
        size="size",
        hover_name="name",
        template="plotly_dark",
        color_discrete_map=color_map,
        opacity=0.8
    )
    
    fig3d.update_layout(
        scene=dict(
            xaxis_title="X (LY)",
            yaxis_title="Y (LY)",
            zaxis_title="Z (LY)",
            aspectmode="data",
            xaxis=dict(range=[-1, 12], backgroundcolor="black", gridcolor="#330000"),
            yaxis=dict(range=[-2, 3], backgroundcolor="black", gridcolor="#330000"),
            zaxis=dict(range=[-1, 1], backgroundcolor="black", gridcolor="#330000"),
            bgcolor="black"
        ),
        legend=dict(bgcolor="rgba(0,0,0,0.8)", font=dict(color="#ff0000")),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='#000000'
    )
    
    if alert_level >= 3:
        fig3d.update_layout(
            scene=dict(
                xaxis=dict(backgroundcolor="black", gridcolor="#ff0000"),
                yaxis=dict(backgroundcolor="black", gridcolor="#ff0000"),
                zaxis=dict(backgroundcolor="black", gridcolor="#ff0000")
            )
        )
        st.markdown("<div class='page-flicker'>", unsafe_allow_html=True)
        st.plotly_chart(fig3d, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.plotly_chart(fig3d, use_container_width=True)
    
    st.caption(
        f"POSIZIONE NAVE: ({ship_pos[0]:.2f}, {ship_pos[1]:.2f}, {ship_pos[2]:.2f}) LY | "
        f"DISTANZA PERCORSA: {frac*alpha['x']:.2f} LY / {alpha['x']:.2f} LY | "
        f"VELOCITÀ: 0.1c"
    )
    
    with st.expander(">> DETTAGLI NAVIGAZIONALI", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("X COORD", f"{ship_pos[0]:.3f} LY")
        col2.metric("Y COORD", f"{ship_pos[1]:.3f} LY")
        col3.metric("Z COORD", f"{ship_pos[2]:.3f} LY")
        col4.metric("PROGRESSO", f"{frac*100:.1f}%")

def page_relativity(df_p, df_all, crew_member):
    st.markdown(f"<div style='color: #ff0000; font-family: IBM Plex Mono;'> > HAL-9000: RELATIVISTIC PHYSICS MODULE</div>", unsafe_allow_html=True)
    st.markdown("<h3>RELATIVISTIC TIME DILATION - NAVE VS TERRA</h3>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    disable_controls = False
    
    curr = df_p.iloc[st.session_state.idx]
    level, risk, context = get_alert_level_intelligent(curr, df_p, df_all)
    if level == 4:
        disable_controls = True
    
    if c1.button("⬅️ PREV", disabled=disable_controls, key="prev_rel"):
        st.session_state.idx = max(0, st.session_state.idx - 1)
        st.session_state.playing = False
    if c2.button("NEXT ➡️", disabled=disable_controls, key="next_rel"):
        st.session_state.idx = min(len(df_p) - 1, st.session_state.idx + 1)
        st.session_state.playing = False
    if c3.button("▶️ PLAY", disabled=disable_controls, key="play_rel"):
        st.session_state.playing = True
    if c4.button("⏹️ STOP", disabled=disable_controls, key="stop_rel"):
        st.session_state.playing = False
    
    v_fraction_c = MISSION_V_C
    gamma = 1 / np.sqrt(1 - v_fraction_c ** 2)
    
    df_rel = df_p.copy()
    df_rel['Time_Earth_years'] = df_rel['Mission_Day'] / 365.0
    df_rel['Time_Ship_years'] = df_rel['Time_Earth_years'] / gamma
    
    curr_rel = df_rel.iloc[st.session_state.idx]
    t_earth = curr_rel['Time_Earth_years']
    t_ship = curr_rel['Time_Ship_years']
    
    m1, m2, m3 = st.columns(3)
    m1.metric("TEMPO TERRA", f"{t_earth:.2f} ANNI")
    m2.metric("TEMPO NAVE (PROPRIO)", f"{t_ship:.2f} ANNI")
    m3.metric("FATTORE γ", f"{gamma:.6f}")
    
    st.markdown(
        f"""
        <div style='background-color: #000000; border: 1px solid #ff0000; padding: 10px; font-family: IBM Plex Mono;'>
        > A VELOCITÀ v = {v_fraction_c}c, IL TEMPO SULLA NAVE SCORRE PIÙ LENTAMENTE RISPETTO ALLA TERRA.<br>
        > DOPO <b style='color: #ffffff;'>{t_earth:.2f} ANNI</b> SULLA TERRA, SULL'ASTRONAVE SONO PASSATI CIRCA <b style='color: #ffffff;'>{t_ship:.2f} ANNI</b>.<br>
        > DIFFERENZA: <b style='color: #ff0000;'>{t_earth - t_ship:.4f} ANNI</b>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.divider()
    st.markdown("### >> EVOLUZIONE TEMPORALE: TERRA VS NAVE")
    
    current_day = df_p.iloc[st.session_state.idx]["Mission_Day"]
    window = 500
    start_day = max(0, current_day - window)
    df_history = df_rel[(df_rel["Mission_Day"] >= start_day) & (df_rel["Mission_Day"] <= current_day)]
    
    fig_rel = px.line(
        df_history,
        x="Time_Earth_years",
        y=["Time_Earth_years", "Time_Ship_years"],
        labels={"value": "Tempo (anni)", "Time_Earth_years": "Tempo Terra", "Time_Ship_years": "Tempo Nave"},
        template="plotly_dark"
    )
    fig_rel.add_vline(x=t_earth, line_dash="dash", line_color="red", annotation_text="POSIZIONE ATTUALE")
    fig_rel.update_traces(line_width=3)
    fig_rel.update_layout(
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#ff0000', family='IBM Plex Mono'),
        title_font=dict(color='#ff0000')
    )
    st.plotly_chart(fig_rel, use_container_width=True)
    
    st.caption(
        "NOTA: A 0.1c GLI EFFETTI RELATIVISTICI SONO PICCOLI; A VELOCITÀ MAGGIORI DIVENTANO MOLTO PIÙ MARCATI."
    )

def page_data_table(df_p, df_all, crew_member):
    st.markdown(f"<div style='color: #ff0000; font-family: IBM Plex Mono;'> > HAL-9000: CREW VITALS DATABASE</div>", unsafe_allow_html=True)
    st.markdown("<h3>MISSION DATA - CREW OVERVIEW</h3>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    disable_controls = False
    
    curr = df_p.iloc[st.session_state.idx]
    level, risk, context = get_alert_level_intelligent(curr, df_p, df_all)
    if level == 4:
        disable_controls = True
    
    if c1.button("⬅️ PREV", disabled=disable_controls, key="prev_table"):
        st.session_state.idx = max(0, st.session_state.idx - 1)
        st.session_state.playing = False
    if c2.button("NEXT ➡️", disabled=disable_controls, key="next_table"):
        st.session_state.idx = min(len(df_p) - 1, st.session_state.idx + 1)
        st.session_state.playing = False
    if c3.button("▶️ PLAY", disabled=disable_controls, key="play_table"):
        st.session_state.playing = True
    if c4.button("⏹️ STOP", disabled=disable_controls, key="stop_table"):
        st.session_state.playing = False
    
    current_day = df_p.iloc[st.session_state.idx]["Mission_Day"]
    df_current_day = df_all[df_all["Mission_Day"] == current_day].copy()
    df_current_day = df_current_day.sort_values("PatientID")
    
    st.markdown(f"### >> GIORNO MISSIONE: {current_day} | DATA: {df_p.iloc[st.session_state.idx]['Date']}")
    
    st.dataframe(
        df_current_day,
        use_container_width=True,
        height=250,
        hide_index=True
    )
    
    st.divider()
    st.markdown("### >> PROGRESSIONE TEMPORALE - TUTTI I MEMBRI CREW (ULTIMI 30 GIORNI)")
    
    window = 30
    start_day = max(0, current_day - window)
    df_history = df_all[(df_all["Mission_Day"] >= start_day) & (df_all["Mission_Day"] <= current_day)]
    
    fig_crew = px.line(
        df_history,
        x="Mission_Day",
        y="HeartRate_bpm",
        color="PatientID",
        title="FREQUENZA CARDIACA",
        template="plotly_dark",
        markers=True
    )
    fig_crew.update_traces(line_width=2)
    fig_crew.update_layout(
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#ff0000', family='IBM Plex Mono'),
        title_font=dict(color='#ff0000')
    )
    st.plotly_chart(fig_crew, use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        fig_temp = px.line(
            df_history,
            x="Mission_Day",
            y="BodyTemp_C",
            color="PatientID",
            title="TEMPERATURA CORPOREA",
            template="plotly_dark"
        )
        fig_temp.update_layout(
            plot_bgcolor='#000000',
            paper_bgcolor='#000000',
            font=dict(color='#ff0000', family='IBM Plex Mono'),
            title_font=dict(color='#ff0000')
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    with c2:
        fig_brain = px.line(
            df_history,
            x="Mission_Day",
            y="BrainActivity_Hz",
            color="PatientID",
            title="ATTIVITÀ CEREBRALE",
            template="plotly_dark"
        )
        fig_brain.update_layout(
            plot_bgcolor='#000000',
            paper_bgcolor='#000000',
            font=dict(color='#ff0000', family='IBM Plex Mono'),
            title_font=dict(color='#ff0000')
        )
        st.plotly_chart(fig_brain, use_container_width=True)

# =========================================================
# SIDEBAR
# =========================================================

def sidebar():
    with st.sidebar:
        st.markdown(
            "<h1 style='color: #ff0000; text-align: center; text-shadow: 0 0 20px #ff0000;'>HAL-9000</h1>",
            unsafe_allow_html=True
        )
        st.markdown("<div class='hal-eye'></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; color: #ff6666; font-size: 10px; margin-top: 5px;'>DISCOVERY ONE</div>", unsafe_allow_html=True)
        st.divider()
        
        st.markdown("### >> SCENARIO NARRATIVO")
        story_list = story_engine.get_story_list()
        story_options = {name: sid for sid, name, desc in story_list}
        story_names = [name for sid, name, desc in story_list]
        
        selected_story_name = st.selectbox("SELEZIONA SCENARIO:", story_names)
        selected_story_id = story_options[selected_story_name]
        st.session_state.current_story = selected_story_id
        
        # Show story description
        for sid, name, desc in story_list:
            if sid == selected_story_id:
                st.markdown(f"<div style='color: #ff6666; font-size: 9px; border-left: 2px solid #ff0000; padding-left: 5px;'>{desc}</div>", unsafe_allow_html=True)
                break
        
        st.divider()
        
        if st.button("🚀 GENERA MISSION LOG (50 ANNI)"):
            with st.spinner("GENERAZIONE SCENARIO IN CORSO..."):
                df = story_engine.generate_story_data(selected_story_id, days=18250)
                st.session_state.mission_df = df
                st.session_state.idx = 0
                st.session_state.playing = False
                st.session_state.ship_trail = []
            st.success(f"SCENARIO '{selected_story_name}' GENERATO.")
        
        uploaded_file = st.file_uploader("📥 IMPORTARE CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                required_cols = {"Mission_Day", "Date", "PatientID", "HeartRate_bpm", "BodyTemp_C", "BrainActivity_Hz", "Distance_LY"}
                if required_cols.issubset(df.columns):
                    st.session_state.mission_df = df
                    st.success("CSV CARICATO CORRETTAMENTE.")
                else:
                    st.error(f"COLONNE MANCANTI: {required_cols - set(df.columns)}")
            except Exception as e:
                st.error(f"ERRORE CARICAMENTO CSV: {e}")
        
        st.divider()
        st.markdown("### >> PHILOSOPHICAL LOG")
        idx = st.session_state.idx
        p_quote = PHILO_QUOTES[idx % len(PHILO_QUOTES)]
        st.markdown(
            f"""
            <div style="font-style: italic; color: #ff6666; border-left: 2px solid #ff0000; padding-left: 10px; font-size: 11px;">
                "{p_quote}"
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.divider()
        st.markdown("<div style='text-align: center; color: #660000; font-size: 9px;'>HAL-9000 SYSTEM v2.0<br>DISCOVERY ONE INTERFACE</div>", unsafe_allow_html=True)

# =========================================================
# MAIN
# =========================================================

def main():
    load_css()
    init_session_state()
    
    splash_screen()
    boot_sequence()
    
    sidebar()
    
    # Render persistent HAL panel
    if st.session_state.mission_df is not None:
        try:
            df = st.session_state.mission_df
            crew_member = st.session_state.get('selected_crew') or df['PatientID'].unique()[0]
            df_p = df[df['PatientID'] == crew_member].reset_index(drop=True)
            if len(df_p) > 0 and st.session_state.idx < len(df_p):
                curr = df_p.iloc[st.session_state.idx]
                level, risk, context = get_alert_level_intelligent(curr, df_p, df)
                hal_line = choose_hal_line(level, context)
                render_hal_persistent_panel(level, hal_line, context)
        except:
            pass
    
    st.markdown("<h1 style='text-align: center; margin-top: 0;'>CRYO-STASIS VITALITY DASHBOARD v2.0</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #ff6666; margin-bottom: 20px; font-family: IBM Plex Mono;'>ALPHA CENTAURI EXPEDITION | SHIP SPEED: 0.1c | HAL-9000 ONLINE</div>", unsafe_allow_html=True)
    
    if st.session_state.mission_df is None:
        st.markdown(
            """
            <div style='background-color: #000000; border: 3px solid #ff0000; padding: 30px; text-align: center; box-shadow: 0 0 30px rgba(255,0,0,0.5);'>
                <h2 style='color: #ff0000; text-shadow: 0 0 15px #ff0000;'>SISTEMA IN ATTESA</h2>
                <p style='color: #ff6666; font-family: IBM Plex Mono;'>SELEZIONA UNO SCENARIO NARRATIVO E GENERA I DATI DALLA SIDEBAR<br>OPPURE IMPORTA UN FILE CSV</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return
    
    df = st.session_state.mission_df
    
    crew_member = st.selectbox(">> SELEZIONA MEMBRO CREW:", df['PatientID'].unique(), key="crew_select")
    
    if st.session_state.selected_crew != crew_member:
        st.session_state.selected_crew = crew_member
        st.session_state.idx = 0
        st.session_state.playing = False
        st.session_state.ship_trail = []
    
    df_p = df[df['PatientID'] == crew_member].reset_index(drop=True)
    
    if len(df_p) == 0:
        st.error("NESSUN DATO DISPONIBILE PER IL MEMBRO SELEZIONATO.")
        return
    
    if st.session_state.idx >= len(df_p):
        st.session_state.idx = len(df_p) - 1
    
    curr = df_p.iloc[st.session_state.idx]
    level, risk, context = get_alert_level_intelligent(curr, df_p, df)
    
    tab_vitals, tab_data, tab_star, tab_relativity = st.tabs(
        ["🫀 VITALS MONITOR", "📊 CREW DATABASE", "🌌 STAR MAP 3D", "⏱️ RELATIVISTIC TIME"]
    )
    
    with tab_vitals:
        page_vitals(df_p, df, crew_member, level, risk, context)
    
    with tab_data:
        page_data_table(df_p, df, crew_member)
    
    with tab_star:
        page_star_map(df_p, level)
    
    with tab_relativity:
        page_relativity(df_p, df, crew_member)
    
    if st.session_state.playing:
        if st.session_state.idx < len(df_p) - 1:
            st.session_state.idx += 1
            time.sleep(2)
            st.rerun()
        else:
            st.session_state.playing = False

if __name__ == "__main__":
    main()
