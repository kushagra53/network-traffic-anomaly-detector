FROM python:3.12.4-slim

WORKDIR /network-traffic-anomaly-detector

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py app.py
COPY ids_model.pkl ids_model.pkl
COPY label_encoder.pkl label_encoder.pkl
COPY feature_names.pkl feature_names.pkl


EXPOSE 5000 

CMD ["python", "app.py"]   
