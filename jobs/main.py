import os
import time
import uuid

from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import datetime, timedelta
import random

# Coordinates of Milano and Torino
TORINO_COORDINATES = {
    "latitude": 45.116177,
    "longitude": 7.742615,
}
MILANO_COORDINATES = {
    "latitude": 45.464664,
    "longitude": 9.188540,
}

# Calculate the movement increments
LATITUDE_INCREMENT = (MILANO_COORDINATES['latitude'] - MILANO_COORDINATES['latitude']) / 100
LONGITUDE_INCREMENT = (MILANO_COORDINATES['longitude'] - MILANO_COORDINATES['longitude']) / 100

# Environment variables for configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_data')

random.seed(42)
start_time = datetime.now()
start_location = TORINO_COORDINATES.copy()

def get_next_time():
    global start_time
    # update frequency
    start_time += timedelta(seconds=random.randint(30, 60))
    return start_time

def generate_gps_data(device_id, timestamp, vehicle_type='private'):
    return {
        'id': uuid.uuid4(),
        'deviceID': device_id,
        'timestamp': timestamp,
        'speed': random.uniform(0, 100), # km/h
        'direction': 'North-East',
        'vehicleType': vehicle_type
    }

def generate_traffic_camera_data(device_id, timestamp, location, camera_id):
    return {
        'id': uuid.uuid4(),
        'deviceID': device_id,
        'camera_id': camera_id,
        'timestamp': timestamp,
        'location': location,
        'snapshot': 'Base64Encoded',
    }

def generate_weather_data(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'deviceID': device_id,
        'timestamp': timestamp,
        'location': location,
        'temperature': random.uniform(-10, 45),
        'weatherCondition': random.choice(['sunny', 'cloudy', 'rainy', 'snowy']),
        'precipitation': random.uniform(0, 25),
        'windSpeed': random.uniform(0, 50),
        'humidity': random.uniform(0, 100),
        'airQualityIndex': random.uniform(0, 500),
    }

def generate_emergency_incident_data(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'deviceID': device_id,
        'timestamp': timestamp,
        'location': location,
        'incidentId': uuid.uuid4(),
        'type': random.choice(['Accident', 'Fire', 'Medical', 'None']),
        'status': random.choice(['Active', 'Resolved']),
        'description': 'Description of the incident'
    }

def simulate_vehicle_movement():
    global start_location
    # Moves towards Milano
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT
    # Add some randomness to simulate an actual travel
    start_location['latitude'] += random.uniform(-0.0005, 0.0005)
    start_location['longitude'] += random.uniform(-0.0005, 0.0005)
    # return the movement update
    return start_location

def generate_vehicle_data(device_id):
    location = simulate_vehicle_movement()
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': get_next_time().isoformat(),
        'location': (location['latitude'], location['longitude']),
        'speed': random.uniform(10, 100),
        'direction': 'North-East',
        'make': 'VW',
        'model': 'Taigo',
        'year': '2024',
        'fuelType':'Hybrid',
    }

def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object pf type {obj.__class__.__name__} is not JSON serializer')

def delivery_report (err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivery to {msg.topic()} [{msg.partition()}]')

def produce_data_to_kafka(producer, topic, data):
    producer.produce(
        topic,
        key = str(data['id']),
        value = json.dumps(data, default= json_serializer).encode('utf-8'),
        on_delivery= delivery_report
    )
    producer.flush()

def simulate_journey(producer, device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        gps_data = generate_gps_data(device_id, vehicle_data['timestamp'])
        traffic_camera_data = generate_traffic_camera_data(device_id, vehicle_data['timestamp'], vehicle_data['location'], camera_id='camera123')
        weather_data = generate_weather_data(device_id, vehicle_data['timestamp'], vehicle_data['location'])
        emergency_incident_data = generate_emergency_incident_data(device_id, vehicle_data['timestamp'], vehicle_data['location'])

        if (vehicle_data['location'][0] >= MILANO_COORDINATES['latitude']
                and vehicle_data['location'][1] <= MILANO_COORDINATES['longitude']):
            print('Vehicle has reached Milano')
            break
        produce_data_to_kafka(producer, VEHICLE_TOPIC, vehicle_data)
        produce_data_to_kafka(producer, GPS_TOPIC, gps_data)
        produce_data_to_kafka(producer, TRAFFIC_TOPIC, traffic_camera_data)
        produce_data_to_kafka(producer, WEATHER_TOPIC, weather_data)
        produce_data_to_kafka(producer, EMERGENCY_TOPIC, emergency_incident_data)
        time.sleep(3)


if __name__ == "__main__":
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'kafka error: {err}'),
    }
    producer = SerializingProducer(producer_config)
    try:
        simulate_journey(producer, 'Vehicle-123')
    except KeyboardInterrupt:
        print('Simulation ended by the user')
    except Exception as e:
        print(f'Unexpected Error occurred: {e}')

