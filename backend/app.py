from flask import Flask, request, jsonify
import joblib
import numpy as np
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

try:
    model = joblib.load('model_aer.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    print("Modelul și Label Encoder-ul au fost încărcate cu succes!")
except Exception as e:
    print(f"Eroare critică la încărcarea fișierelor ML: {e}")

@app.route('/api/v1/predict', methods=['POST'])
def predict_air_quality():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Lipsesc datele JSON.'}), 400
        
    required_fields = ['CO AQI Value', 'Ozone AQI Value', 'NO2 AQI Value', 'PM2.5 AQI Value']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({'status': 'error', 'message': f'Lipsesc câmpuri: {missing_fields}'}), 400

    try:
        input_data = {
            'CO AQI Value': [float(data['CO AQI Value'])],
            'Ozone AQI Value': [float(data['Ozone AQI Value'])],
            'NO2 AQI Value': [float(data['NO2 AQI Value'])],
            'PM2.5 AQI Value': [float(data['PM2.5 AQI Value'])]
        }
        
        input_df = pd.DataFrame(input_data)
        
        prediction_numeric = model.predict(input_df)[0]
        prediction_text = label_encoder.inverse_transform([prediction_numeric])[0]
        
        return jsonify({
            'status': 'success',
            'data': {
                'prediction_code': int(prediction_numeric),
                'prediction_label': prediction_text
            }
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    print(f"The WSGI Container for Tornado is initializing on port {port}...")
    
    container = WSGIContainer(app)
    http_server = HTTPServer(container)
    http_server.listen(port)
    
    print(f"Production Tornado server is running...")
    IOLoop.current().start()