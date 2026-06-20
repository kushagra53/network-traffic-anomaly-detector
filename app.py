from flask import Flask ,request, jsonify
import joblib
import pandas as pd 
import numpy as np

app = Flask(__name__)
# you're creating a Flask application object.
# app
# ├── route()
# ├── run()
# ├── config
# ├── error handling
# └── request processing

model= joblib.load('ids_model.pkl')
label_encoder= joblib.load('label_encoder.pkl')
feature_names = joblib.load('feature_names.pkl')

ATTACK_MAPPING = {
    0: 'back', 1: 'buffer_overflow', 2: 'ftp_write', 3: 'guess_passwd',
    4: 'imap', 5: 'normal', 6: 'ipsweep', 7: 'land', 8: 'loadmodule',
    9: 'multihop', 10: 'neptune', 11: 'nmap', 12: 'portsweep',
    13: 'rootkit', 14: 'satan', 15: 'smurf', 16: 'spy', 17: 'teardrop',
    18: 'warezclient', 19: 'warezmaster'
}

@app.route('/predict', methods=['POST'])
def predict_attack():
    try:
        data = request.json
        
        # Ensure all features present (fill missing with 0)
        connection_data = {name: data.get(name, 0) for name in feature_names}
        df = pd.DataFrame([connection_data])
        
        # Predict
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df).max()
        
        attack_name = ATTACK_MAPPING.get(prediction, f'class_{prediction}')
        
        return jsonify({
            'prediction': int(prediction),
            'attack_type': attack_name,
            'confidence': float(probability),
            'status': 'ALERT' if probability > 0.9 else 'MONITOR'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model': 'NSL-KDD IDS v1.0'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
