# app.py
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Classes ---
class User:
    def __init__(self, id, name, email, password):
        self.id, self.name, self.email, self.password = id, name, email, password
    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

class Trip:
    def __init__(self, id, user_id, destination, name, start_date, end_date):
        self.id, self.user_id, self.destination, self.name, self.start_date, self.end_date = id, user_id, destination, name, start_date, end_date
    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "destination": self.destination, "name": self.name, "start_date": self.start_date, "end_date": self.end_date}

class Flight:
    def __init__(self, id, trip_id, company, code, departure, arrival):
        self.id, self.trip_id, self.company, self.code, self.departure, self.arrival = id, trip_id, company, code, departure, arrival
    def to_dict(self):
        return {"id": self.id, "trip_id": self.trip_id, "company": self.company, "code": self.code, "departure": self.departure, "arrival": self.arrival}

class Hotel:
    def __init__(self, id, trip_id, name, checkin, checkout):
        self.id, self.trip_id, self.name, self.checkin, self.checkout = id, trip_id, name, checkin, checkout
    def to_dict(self):
        return {"id": self.id, "trip_id": self.trip_id, "name": self.name, "checkin": self.checkin, "checkout": self.checkout}

class Activity:
    def __init__(self, id, trip_id, description, date):
        self.id, self.trip_id, self.description, self.date = id, trip_id, description, date
    def to_dict(self):
        return {"id": self.id, "trip_id": self.trip_id, "description": self.description, "date": self.date}

# --- Classe de Armazenamento com Persistência em JSON --- mantém os dados salvos como um banco de dados
class DataStore:
    def __init__(self, filename='database.json'):
        self._filename = filename
        self._data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self._filename):
            return {"users": [], "trips": [], "flights": [], "hotels": [], "activities": []}
        with open(self._filename, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError: # Lida com arquivo JSON vazio ou corrompido
                return {"users": [], "trips": [], "flights": [], "hotels": [], "activities": []}

    def _save_data(self):
        with open(self._filename, 'w') as f:
            json.dump(self._data, f, indent=4)

    def _get_next_id(self, collection_name):
        if not self._data[collection_name]: return 1
        return max(item['id'] for item in self._data[collection_name]) + 1

    def add_user(self, name, email, password):
        user = User(self._get_next_id('users'), name, email, password)
        self._data['users'].append(user.__dict__); self._save_data(); return user

    def find_user_by_email(self, email):
        user_data = next((u for u in self._data['users'] if u['email'] == email), None)
        return User(**user_data) if user_data else None

    def find_user_by_id(self, user_id):
        user_data = next((u for u in self._data['users'] if u['id'] == user_id), None)
        return User(**user_data) if user_data else None

    def add_trip(self, user_id, dest, name, start, end):
        trip = Trip(self._get_next_id('trips'), user_id, dest, name, start, end)
        self._data['trips'].append(trip.__dict__); self._save_data(); return trip

    def find_trip_by_id(self, trip_id):
        trip_data = next((t for t in self._data['trips'] if t['id'] == trip_id), None)
        return Trip(**trip_data) if trip_data else None
        
    def get_all_trips(self):
        return [Trip(**t) for t in self._data['trips']]

    def add_flight(self, trip_id, company, code, departure, arrival):
        flight = Flight(self._get_next_id('flights'), trip_id, company, code, departure, arrival)
        self._data['flights'].append(flight.__dict__); self._save_data(); return flight

    def add_hotel(self, trip_id, name, checkin, checkout):
        hotel = Hotel(self._get_next_id('hotels'), trip_id, name, checkin, checkout)
        self._data['hotels'].append(hotel.__dict__); self._save_data(); return hotel

    def add_activity(self, trip_id, description, date):
        activity = Activity(self._get_next_id('activities'), trip_id, description, date)
        self._data['activities'].append(activity.__dict__); self._save_data(); return activity

    def get_details_for_trip(self, trip_id):
        return {
            "flights": [f for f in self._data['flights'] if f['trip_id'] == trip_id],
            "hotels": [h for h in self._data['hotels'] if h['trip_id'] == trip_id],
            "activities": [a for a in self._data['activities'] if a['trip_id'] == trip_id]
        }

# --- Configuração da Aplicação ---
app = Flask(__name__)
CORS(app)
db = DataStore()

# --- Rotas da API ---
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json();
    if db.find_user_by_email(data['email']): return jsonify({'message': 'Email já existe.'}), 409
    user = db.add_user(data['name'], data['email'], data['password']); return jsonify({'user': user.to_dict()}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(); user = db.find_user_by_email(data['email'])
    if user and user.password == data['password']: return jsonify({'user': user.to_dict()}), 200
    return jsonify({'message': 'Credenciais inválidas.'}), 401

@app.route('/api/trips', methods=['GET', 'POST'])
def handle_trips():
    if request.method == 'GET':
        all_trips = db.get_all_trips()
        return jsonify({"trips": [t.to_dict() for t in all_trips]}), 200
    
    if request.method == 'POST':
        data = request.get_json()
        if not db.find_user_by_id(data.get('user_id')): return jsonify({'message': 'Usuário não encontrado.'}), 404
        trip = db.add_trip(data['user_id'], data['destination'], data['name'], data['start_date'], data['end_date'])
        return jsonify({'trip': trip.to_dict()}), 201

@app.route('/api/trips/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    trip = db.find_trip_by_id(trip_id)
    if trip: return jsonify({'trip': trip.to_dict()}), 200
    return jsonify({'message': 'Viagem não encontrada.'}), 404

@app.route('/api/trips/<int:trip_id>/details', methods=['GET'])
def get_trip_details(trip_id):
    trip = db.find_trip_by_id(trip_id)
    if not trip: return jsonify({'message': 'Viagem não encontrada.'}), 404
    details = db.get_details_for_trip(trip_id)
    details['suggestions'] = [
        {"type": "Restaurante", "name": f"Comida Típica de {trip.destination}"},
        {"type": "Ponto Turístico", "name": f"Monumento Principal de {trip.destination}"}
    ]
    return jsonify(details), 200

@app.route('/api/trips/<int:trip_id>/flights', methods=['POST'])
def add_flight_to_trip(trip_id):
    if not db.find_trip_by_id(trip_id): return jsonify({'message': 'Viagem não encontrada.'}), 404
    data = request.get_json()
    flight = db.add_flight(trip_id, data['company'], data['code'], data['departure'], data['arrival'])
    return jsonify({'flight': flight.to_dict()}), 201

@app.route('/api/trips/<int:trip_id>/hotels', methods=['POST'])
def add_hotel_to_trip(trip_id):
    if not db.find_trip_by_id(trip_id): return jsonify({'message': 'Viagem não encontrada.'}), 404
    data = request.get_json()
    hotel = db.add_hotel(trip_id, data['name'], data['checkin'], data['checkout'])
    return jsonify({'hotel': hotel.to_dict()}), 201

@app.route('/api/trips/<int:trip_id>/activities', methods=['POST'])
def add_activity_to_trip(trip_id):
    if not db.find_trip_by_id(trip_id): return jsonify({'message': 'Viagem não encontrada.'}), 404
    data = request.get_json()
    activity = db.add_activity(trip_id, data['description'], data['date'])
    return jsonify({'activity': activity.to_dict()}), 201

if __name__ == '__main__':
    app.run(debug=True)
