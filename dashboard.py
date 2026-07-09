import panel as pn
import requests

pn.extension(design='bootstrap')

title = pn.pane.Markdown("#AeroActive - Sistem de Evaluare și Alertă", styles={'font-family': 'Arial'})
subtitle = pn.pane.Markdown("Modificați valorile de mai jos pentru a simula citirile live transmise de senzorii urbani.")

co_slider = pn.widgets.IntSlider(name='CO AQI Value', start=0, end=200, value=1)
ozone_slider = pn.widgets.IntSlider(name='Ozone AQI Value', start=0, end=200, value=36)
no2_slider = pn.widgets.IntSlider(name='NO2 AQI Value', start=0, end=200, value=0)
pm25_slider = pn.widgets.IntSlider(name='PM2.5 AQI Value', start=0, end=200, value=51)

predict_button = pn.widgets.Button(name='Evaluează Calitatea Aerului', button_type='primary', sizing_mode='stretch_width')

result_pane = pn.pane.Markdown("###Status: Așteptare date de la senzori...", styles={'font-size': '16px'})


def evalueaza_aer(event):
    payload = {
        "CO AQI Value": co_slider.value,
        "Ozone AQI Value": ozone_slider.value,
        "NO2 AQI Value": no2_slider.value,
        "PM2.5 AQI Value": pm25_slider.value
    }
    
    result_pane.object = "Se calculează indicele de risc..."
    
    try:
        response = requests.post("http://127.0.0.1:5001/api/v1/predict", json=payload, timeout=5)
        
        if response.status_code == 200:
            res_json = response.json()
            categorie_aer = res_json['data']['prediction_label']
            
            color_map = {
                "Good": "#2ecc71",      
                "Moderate": "#f1c40f",   
                "Unhealthy": "#e74c3c",  
                "Very Unhealthy": "#9b59b6",
                "Hazardous": "#7f8c8d"
            }
            culoare = color_map.get(categorie_aer, "#000000")
            
            result_pane.object = f"""
            <div style="padding: 20px; border-radius: 10px; background-color: {culoare}20; border: 2px solid {culoare}; text-align: center;">
                <h3 style="margin: 0; color: #333;">Stare Aer Identificată:</h3>
                <h1 style="margin: 10px 0 0 0; color: {culoare}; text-transform: uppercase; font-family: Arial;">{categorie_aer}</h1>
            </div>
            """
        else:
            result_pane.object = f"Eroare API Backend: {response.json().get('message', 'Eroare necunoscută')}"
            
    except requests.exceptions.ConnectionError:
        result_pane.object = "**Eroare de conexiune:** Asigurați-vă că serverul backend (`app.py`) este pornit pe portul 5001!"
    except Exception as e:
        result_pane.object = f"Eroare neprevăzută: {str(e)}"


predict_button.on_click(evalueaza_aer)


sidebar = pn.Column(
    "## 🛠️ Telemetrie Senzori",
    co_slider,
    ozone_slider,
    no2_slider,
    pm25_slider,
    pn.Spacer(height=15),
    predict_button,
    styles={'background': '#f8f9fa', 'padding': '20px', 'border-radius': '10px'}
)

main_content = pn.Column(
    title,
    subtitle,
    pn.Spacer(height=30),
    result_pane,
    sizing_mode='stretch_width'
)

layout = pn.Row(
    sidebar,
    pn.Spacer(width=40),
    main_content,
    sizing_mode='stretch_width',
    margin=(40, 40, 40, 40)
)

layout.servable()