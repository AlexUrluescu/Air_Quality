import panel as pn
import requests

pn.extension(sizing_mode="stretch_width")

# ------------------------------------------------------------------
# CSS custom — look futurist, light, glassmorphism, responsive
# ------------------------------------------------------------------
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

:root {
    --accent: #06b6d4;
    --accent-2: #6366f1;
    --bg-soft: #f4f7fb;
}

html, body {
    font-family: 'Inter', system-ui, sans-serif !important;
    background: radial-gradient(circle at 10% 0%, #eef4ff 0%, #f7fafc 40%, #f4f7fb 100%) !important;
}

/* Header */
#header {
    background: rgba(255, 255, 255, 0.65) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(6, 182, 212, 0.15) !important;
    box-shadow: 0 2px 20px rgba(15, 23, 42, 0.04) !important;
}

#header .title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    background: linear-gradient(90deg, #0f172a, var(--accent-2), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Sidebar */
#sidebar {
    background: rgba(255, 255, 255, 0.55) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-right: 1px solid rgba(15, 23, 42, 0.06) !important;
}

.bk-panel-models-markup .markdown h3 {
    font-family: 'Space Grotesk', sans-serif;
    color: #0f172a;
    font-weight: 600;
    letter-spacing: 0.3px;
}

/* Sensor cards wrapping sliders */
.sensor-card {
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(6, 182, 212, 0.15);
    border-radius: 16px;
    padding: 14px 16px 6px 16px;
    margin-bottom: 14px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
    transition: all 0.25s ease;
}
.sensor-card:hover {
    border-color: rgba(6, 182, 212, 0.4);
    box-shadow: 0 6px 20px rgba(6, 182, 212, 0.12);
    transform: translateY(-1px);
}

/* Slider text/labels */
.bk-slider-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    color: #1e293b !important;
    font-size: 13.5px !important;
}

/* Buton principal - gradient futurist */
.bk-btn-primary {
    background: linear-gradient(135deg, var(--accent-2), var(--accent)) !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.4px;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35) !important;
    transition: all 0.2s ease !important;
}
.bk-btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(6, 182, 212, 0.4) !important;
}

/* Card rezultat container */
.result-wrapper {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 6px;
    box-shadow: 0 10px 40px rgba(15, 23, 42, 0.06);
}

/* ------------------------------------------------------------------
   Responsive: forțăm explicit stivuirea layout-ului pe ecrane mici,
   nu ne bazăm doar pe breakpoint-ul intern al FastListTemplate
   ------------------------------------------------------------------ */
@media (max-width: 800px) {

    #header .title { font-size: 16px !important; }

    /* Sidebar-ul trece deasupra, pe toată lățimea, nu mai e coloană laterală */
    #sidebar {
        position: relative !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        height: auto !important;
        border-right: none !important;
        border-bottom: 1px solid rgba(15, 23, 42, 0.08) !important;
        padding-bottom: 12px !important;
    }

    /* Main-ul ocupă tot ce rămâne, fără margine rezervată pentru sidebar */
    #main {
        margin-left: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        padding: 12px !important;
    }

    /* Containerul general devine coloană (sidebar sus, conținut jos) */
    .fast-list-template,
    #body-design-provider,
    #body {
        flex-direction: column !important;
    }

    .sensor-card { padding: 10px 12px 4px 12px; }
    .result-wrapper { border-radius: 18px; }

    /* butonul rămâne lizibil și pe ecrane foarte mici */
    .bk-btn-primary { font-size: 14px !important; }
}

@media (max-width: 420px) {
    #header .title { font-size: 14px !important; }
    .bk-slider-title { font-size: 12.5px !important; }
}
"""

pn.config.raw_css.append(CUSTOM_CSS)

# ------------------------------------------------------------------
# Widgets
# ------------------------------------------------------------------
slider_kwargs = dict(bar_color='#06b6d4', margin=(5, 10, 15, 10))

co_slider = pn.widgets.IntSlider(name='Monoxid de Carbon (CO)', start=0, end=200, value=1, **slider_kwargs)
ozone_slider = pn.widgets.IntSlider(name='Ozon (O3)', start=0, end=200, value=36, **slider_kwargs)
no2_slider = pn.widgets.IntSlider(name='Dioxid de Azot (NO2)', start=0, end=200, value=0, **slider_kwargs)
pm25_slider = pn.widgets.IntSlider(name='Particule Fine (PM2.5)', start=0, end=200, value=51, **slider_kwargs)

sensor_card = pn.Column(
    co_slider, ozone_slider, no2_slider, pm25_slider,
    css_classes=['sensor-card']
)

predict_button = pn.widgets.Button(
    name='⚡ Evaluează Calitatea Aerului',
    button_type='primary',
    sizing_mode='stretch_width',
    height=52
)

result_pane = pn.pane.HTML("""
    <div style="padding: 50px 24px; text-align: center; border-radius: 20px;
                background: linear-gradient(135deg, #f8fafc, #eef4ff);
                color: #64748b; border: 1.5px dashed #94a3b8;
                font-family: 'Inter', sans-serif;">
        <div style="font-size: 40px; margin-bottom: 10px;">📡</div>
        <h3 style="font-family: 'Space Grotesk', sans-serif; color:#334155; margin: 6px 0;">
            Așteptare date de la senzori...
        </h3>
        <p style="margin: 0; font-size: 14px;">
            Ajustați valorile din meniu și apăsați butonul de evaluare.
        </p>
    </div>
""", sizing_mode='stretch_width')

result_wrapper = pn.Column(result_pane, css_classes=['result-wrapper'], sizing_mode='stretch_width')


def evalueaza_aer(event):
    payload = {
        "CO AQI Value": co_slider.value,
        "Ozone AQI Value": ozone_slider.value,
        "NO2 AQI Value": no2_slider.value,
        "PM2.5 AQI Value": pm25_slider.value
    }

    predict_button.name = '⏳ Se calculează...'

    try:
        response = requests.post("http://127.0.0.1:5001/api/v1/predict", json=payload, timeout=5)

        if response.status_code == 200:
            res_json = response.json()
            categorie_aer = res_json['data']['prediction_label']

            color_map = {
                "Good": ("#10b981", "Calitate Excelentă", "Aerul este curat. Ideal pentru activități în aer liber!", "🌿"),
                "Moderate": ("#eab308", "Calitate Moderată", "Acceptabil, dar persoanele sensibile ar trebui să reducă efortul.", "🌤️"),
                "Unhealthy": ("#ef4444", "Aer Nesănătos", "Evitați efortul prelungit în aer liber! Purtați mască.", "⚠️"),
                "Very Unhealthy": ("#a855f7", "Foarte Periculos", "Risc major de sănătate. Rămâneți la interior!", "☣️"),
                "Hazardous": ("#475569", "Toxic", "Avertizare de urgență! Condiții toxice.", "☠️")
            }

            culoare, titlu, mesaj, icon = color_map.get(
                categorie_aer, ("#06b6d4", "Necunoscut", "Nu am putut evalua starea.", "❓")
            )

            result_pane.object = f"""
            <div style="padding: 40px 20px; border-radius: 20px;
                        background: linear-gradient(135deg, {culoare}12, {culoare}05);
                        border: 1.5px solid {culoare}55; text-align: center;
                        box-shadow: 0 8px 30px {culoare}22; font-family: 'Inter', sans-serif;">
                <div style="font-size: 34px; margin-bottom: 6px;">{icon}</div>
                <p style="margin: 0; color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px;">
                    Index de Risc Identificat
                </p>
                <h1 style="margin: 8px 0; color: {culoare}; font-size: 34px;
                           font-family: 'Space Grotesk', sans-serif; font-weight: 700;">
                    {titlu}
                </h1>
                <h3 style="margin: 0; color: #334155; font-weight: 500;">{categorie_aer}</h3>
                <hr style="border: 0; height: 1px; background: {culoare}40; margin: 22px auto; width: 60%;">
                <p style="font-size: 16px; color: #475569; margin: 0; max-width: 380px; margin: 0 auto;">
                    {mesaj}
                </p>
            </div>
            """
        else:
            result_pane.object = f"""
            <div style='padding: 24px; border-radius: 16px; background:#fef2f2;
                        border:1px solid #fca5a5; color:#b91c1c; font-family: Inter, sans-serif;'>
                Eroare: {response.json().get('message')}
            </div>"""

    except Exception:
        result_pane.object = """
        <div style='padding: 24px; border-radius: 16px; background:#fef2f2;
                    border:1px solid #fca5a5; color:#b91c1c; font-family: Inter, sans-serif;'>
            Nu s-a putut contacta serverul backend.
        </div>"""

    finally:
        predict_button.name = '⚡ Evaluează Calitatea Aerului'


predict_button.on_click(evalueaza_aer)

# ------------------------------------------------------------------
# Template - light, futurist
# ------------------------------------------------------------------
template = pn.template.FastListTemplate(
    title='AeroActive · Dashboard',
    header_background="#ffffff",
    accent_base_color="#06b6d4",
    theme_toggle=False,
    favicon=None,
    meta_viewport="width=device-width, initial-scale=1.0, maximum-scale=1.0",
    sidebar=[
        pn.pane.Markdown("### 🛰️ Parametri Senzor", margin=(10, 10, 0, 10)),
        pn.pane.Markdown(
            "Simulați datele transmise de hardware modificând valorile de mai jos:",
            margin=(0, 10, 10, 10),
            styles={'color': '#64748b', 'font-size': '13px'}
        ),
        sensor_card,
        pn.Spacer(height=6),
        predict_button
    ],
    main=[
        pn.Column(
            pn.pane.Markdown(
                "## Monitorizare în Timp Real",
                styles={'text-align': 'center', 'margin-top': '10px', 'color': '#0f172a'}
            ),
            pn.pane.Markdown(
                "Date live simulate de la rețeaua de senzori AeroActive",
                styles={'text-align': 'center', 'color': '#94a3b8', 'margin-top': '-10px'}
            ),
            pn.Spacer(height=10),
            result_wrapper,
            sizing_mode='stretch_width',
            max_width=800,
            align='center'
        )
    ]
)

template.servable()