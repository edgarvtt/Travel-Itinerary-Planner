# app.py
# app.py
import json
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Classes de Modelo (POO) ---
class User:
    def __init__(self, id, name, email, password):
        self.id, self.name, self.email, self.password = id, name, email, password
    def to_dict(self): return {"id": self.id, "name": self.name, "email": self.email}

class Trip:
    def __init__(self, id, user_id, destination, name, start_date, end_date, is_suggestion=False, budget=0.0):
        self.id, self.user_id, self.destination, self.name, self.start_date, self.end_date, self.is_suggestion = id, user_id, destination, name, start_date, end_date, is_suggestion
        self.budget = budget
    def to_dict(self): 
        return {
            "id": self.id, "user_id": self.user_id, "destination": self.destination, 
            "name": self.name, "start_date": self.start_date, "end_date": self.end_date,
            "is_suggestion": self.is_suggestion, "budget": self.budget
        }

class Flight:
    def __init__(self, id, trip_id, company, code, departure, arrival, is_done=False):
        self.id, self.trip_id, self.company, self.code, self.departure, self.arrival, self.is_done = id, trip_id, company, code, departure, arrival, is_done
    def to_dict(self): return {"id": self.id, "trip_id": self.trip_id, "company": self.company, "code": self.code, "departure": self.departure, "arrival": self.arrival, "is_done": self.is_done}

class Hotel:
    def __init__(self, id, trip_id, name, checkin, checkout, is_done=False):
        self.id, self.trip_id, self.name, self.checkin, self.checkout, self.is_done = id, trip_id, name, checkin, checkout, is_done
    def to_dict(self): return {"id": self.id, "trip_id": self.trip_id, "name": self.name, "checkin": self.checkin, "checkout": self.checkout, "is_done": self.is_done}

class Activity:
    def __init__(self, id, trip_id, description, date, is_done=False):
        self.id, self.trip_id, self.description, self.date, self.is_done = id, trip_id, description, date, is_done
    def to_dict(self): return {"id": self.id, "trip_id": self.trip_id, "description": self.description, "date": self.date, "is_done": self.is_done}

class Expense:
    def __init__(self, id, trip_id, description, amount, currency, date, category):
        self.id, self.trip_id, self.description, self.amount, self.currency, self.date, self.category = id, trip_id, description, amount, currency, date, category
    def to_dict(self): return self.__dict__

# --- Classe de Armazenamento com Persistência em JSON ---
class DataStore:
    def __init__(self, filename='database.json'):
        self._filename = filename
        self._data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self._filename):
            default_data = {
                "users": [], 
                "trips": [
                    {"id": 1, "user_id": 0, "destination": "Costa Rica", "name": "Aventura na Selva", "start_date": "2025-07-10", "end_date": "2025-07-20", "is_suggestion": True, "budget": 5000.0},
                    {"id": 2, "user_id": 0, "destination": "Kyoto, Japão", "name": "Templos e Tradições", "start_date": "2025-04-05", "end_date": "2025-04-15", "is_suggestion": True, "budget": 7500.0}
                ], 
                "flights": [], "hotels": [], "activities": [], "expenses": []
            }
            with open(self._filename, 'w') as f: json.dump(default_data, f, indent=4)
            return default_data
        
        with open(self._filename, 'r') as f:
            try:
                data = json.load(f)
                for key in ["users", "trips", "flights", "hotels", "activities", "expenses"]: data.setdefault(key, [])
                return data
            except (json.JSONDecodeError, TypeError): 
                return {"users": [], "trips": [], "flights": [], "hotels": [], "activities": [], "expenses": []}

    def _save_data(self):
        with open(self._filename, 'w') as f: json.dump(self._data, f, indent=4)

    def _get_next_id(self, collection_name):
        if not self._data.get(collection_name): return 1
        return max(item.get('id', 0) for item in self._data[collection_name]) + 1

    def add_user(self, name, email, password):
        user = User(self._get_next_id('users'), name, email, password)
        self._data['users'].append(user.__dict__)
        self._save_data()
        return user
    
    def find_user_by_email(self, email):
        user_data = next((u for u in self._data['users'] if u.get('email') == email), None)
        if user_data:
            return User(id=user_data.get('id'), name=user_data.get('name'), email=user_data.get('email'), password=user_data.get('password'))
        return None
    
    def find_user_by_id(self, user_id):
        user_data = next((u for u in self._data['users'] if u.get('id') == user_id), None)
        if user_data:
            return User(id=user_data.get('id'), name=user_data.get('name'), email=user_data.get('email'), password=user_data.get('password'))
        return None

    def add_trip(self, user_id, dest, name, start, end):
        trip = Trip(self._get_next_id('trips'), user_id, dest, name, start, end, is_suggestion=False)
        self._data['trips'].append(trip.__dict__)
        self._save_data()
        return trip

    def find_trip_by_id(self, trip_id):
        trip_data = next((t for t in self._data['trips'] if t.get('id') == trip_id), None)
        if trip_data:
            return Trip(**trip_data)
        return None
        
    def get_user_trips(self, user_id):
        results = []
        for t_data in self._data.get('trips', []):
            if t_data.get('user_id') == user_id and not t_data.get('is_suggestion', False):
                results.append(Trip(**t_data))
        return results

    def get_suggestion_trips(self):
        results = []
        for t_data in self._data.get('trips', []):
            if t_data.get('is_suggestion', False):
                results.append(Trip(**t_data))
        return results
    
    def update_trip_budget(self, trip_id, budget):
        for trip in self._data['trips']:
            if trip.get('id') == trip_id:
                trip['budget'] = budget
                self._save_data()
                return Trip(**trip)
        return None

    def _update_item_status(self, collection_name, item_id, is_done):
        for item in self._data.get(collection_name, []):
            if item.get('id') == item_id:
                item['is_done'] = is_done
                self._save_data()
                return item
        return None

    def add_flight(self, trip_id, company, code, departure, arrival):
        flight = Flight(self._get_next_id('flights'), trip_id, company, code, departure, arrival)
        self._data['flights'].append(flight.__dict__)
        self._save_data()
        return flight

    def add_hotel(self, trip_id, name, checkin, checkout):
        hotel = Hotel(self._get_next_id('hotels'), trip_id, name, checkin, checkout)
        self._data['hotels'].append(hotel.__dict__)
        self._save_data()
        return hotel

    def add_activity(self, trip_id, description, date):
        activity = Activity(self._get_next_id('activities'), trip_id, description, date)
        self._data['activities'].append(activity.__dict__)
        self._save_data()
        return activity
    
    def add_expense(self, trip_id, description, amount, currency, date, category):
        expense = Expense(self._get_next_id('expenses'), trip_id, description, amount, currency, date, category)
        self._data['expenses'].append(expense.__dict__)
        self._save_data()
        return expense
        
    def get_expenses_for_trip(self, trip_id):
        return [Expense(**e) for e in self._data.get('expenses', []) if e.get('trip_id') == trip_id]

    def remove_expense(self, expense_id):
        initial_len = len(self._data['expenses'])
        self._data['expenses'] = [e for e in self._data['expenses'] if e.get('id') != expense_id]
        if len(self._data['expenses']) < initial_len:
            self._save_data()
            return True
        return False

    def get_details_for_trip(self, trip_id):
        return {
            "flights": [f for f in self._data.get('flights', []) if f.get('trip_id') == trip_id],
            "hotels": [h for h in self._data.get('hotels', []) if h.get('trip_id') == trip_id],
            "activities": [a for a in self._data.get('activities', []) if a.get('trip_id') == trip_id]
        }

# --- Configuração da Aplicação ---
app = Flask(__name__)
CORS(app)
db = DataStore()

# --- Rotas da API ---
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ['name', 'email', 'password']):
            return jsonify({'message': 'Dados incompletos.'}), 400
        if db.find_user_by_email(data['email']): 
            return jsonify({'message': 'Este email já está em uso.'}), 409
        user = db.add_user(data['name'], data['email'], data['password'])
        return jsonify({'user': user.to_dict()}), 201
    except Exception as e:
        print(f"ERRO em signup: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = db.find_user_by_email(data['email'])
        if user and user.password == data['password']: 
            return jsonify({'user': user.to_dict()}), 200
        return jsonify({'message': 'Credenciais inválidas.'}), 401
    except Exception as e:
        print(f"ERRO em login: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/trips', methods=['POST'])
def create_trip():
    try:
        data = request.get_json()
        if not db.find_user_by_id(data.get('user_id')): 
            return jsonify({'message': 'Usuário não encontrado.'}), 404
        trip = db.add_trip(data['user_id'], data['destination'], data['name'], data['start_date'], data['end_date'])
        return jsonify({'trip': trip.to_dict()}), 201
    except Exception as e:
        print(f"ERRO em create_trip: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/my-trips', methods=['GET'])
def get_my_trips():
    try:
        user_id_str = request.args.get('user_id')
        if not user_id_str: 
            return jsonify({'message': 'user_id é obrigatório.'}), 400
        user_trips = db.get_user_trips(int(user_id_str))
        return jsonify({"trips": [t.to_dict() for t in user_trips]}), 200
    except Exception as e:
        print(f"ERRO em get_my_trips: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    try:
        suggestion_trips = db.get_suggestion_trips()
        return jsonify({"trips": [t.to_dict() for t in suggestion_trips]}), 200
    except Exception as e:
        print(f"ERRO em get_suggestions: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/trips/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    try:
        trip = db.find_trip_by_id(trip_id)
        if trip: 
            return jsonify({'trip': trip.to_dict()}), 200
        return jsonify({'message': 'Viagem não encontrada.'}), 404
    except Exception as e:
        print(f"ERRO em get_trip: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/trips/<int:trip_id>/budget', methods=['PATCH'])
def update_budget(trip_id):
    try:
        data = request.get_json()
        if 'budget' not in data:
            return jsonify({'message': 'Orçamento em falta.'}), 400
        
        updated_trip = db.update_trip_budget(trip_id, float(data['budget']))
        if updated_trip:
            return jsonify({'trip': updated_trip.to_dict()}), 200
        return jsonify({'message': 'Viagem não encontrada.'}), 404
    except Exception as e:
        print(f"ERRO em update_budget: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/trips/<int:trip_id>/details', methods=['GET'])
def get_trip_details(trip_id):
    try:
        trip = db.find_trip_by_id(trip_id)
        if not trip: 
            return jsonify({'message': 'Viagem não encontrada.'}), 404
        details = db.get_details_for_trip(trip_id)
        details['suggestions'] = [
            {"type": "Restaurante", "name": f"Comida Típica de {trip.destination}"},
            {"type": "Ponto Turístico", "name": f"Monumento Principal de {trip.destination}"}
        ]
        return jsonify(details), 200
    except Exception as e:
        print(f"ERRO em get_trip_details: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/trips/<int:trip_id>/flights', methods=['POST'])
def add_flight_to_trip(trip_id):
    try:
        if not db.find_trip_by_id(trip_id): 
            return jsonify({'message': 'Viagem não encontrada.'}), 404
        data = request.get_json()
        flight = db.add_flight(trip_id, data['company'], data['code'], data['departure'], data['arrival'])
        return jsonify({'flight': flight.to_dict()}), 201
    except Exception as e:
        print(f"ERRO em add_flight_to_trip: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/trips/<int:trip_id>/hotels', methods=['POST'])
def add_hotel_to_trip(trip_id):
    try:
        if not db.find_trip_by_id(trip_id): 
            return jsonify({'message': 'Viagem não encontrada.'}), 404
        data = request.get_json()
        hotel = db.add_hotel(trip_id, data['name'], data['checkin'], data['checkout'])
        return jsonify({'hotel': hotel.to_dict()}), 201
    except Exception as e:
        print(f"ERRO em add_hotel_to_trip: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/trips/<int:trip_id>/activities', methods=['POST'])
def add_activity_to_trip(trip_id):
    try:
        if not db.find_trip_by_id(trip_id): 
            return jsonify({'message': 'Viagem não encontrada.'}), 404
        data = request.get_json()
        activity = db.add_activity(trip_id, data['description'], data['date'])
        return jsonify({'activity': activity.to_dict()}), 201
    except Exception as e:
        print(f"ERRO em add_activity_to_trip: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/trips/<int:trip_id>/expenses', methods=['GET', 'POST'])
def handle_expenses(trip_id):
    if not db.find_trip_by_id(trip_id):
        return jsonify({'message': 'Viagem não encontrada.'}), 404
    if request.method == 'GET':
        try:
            expenses = db.get_expenses_for_trip(trip_id)
            return jsonify({"expenses": [e.to_dict() for e in expenses]}), 200
        except Exception as e:
            print(f"ERRO em get_expenses: {e}")
            return jsonify({'message': 'Erro interno no servidor.'}), 500
    if request.method == 'POST':
        try:
            data = request.get_json()
            expense = db.add_expense(trip_id, data['description'], data['amount'], data['currency'], data['date'], data['category'])
            return jsonify({'expense': expense.to_dict()}), 201
        except Exception as e:
            print(f"ERRO em add_expense: {e}")
            return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        if db.remove_expense(expense_id):
            return jsonify({'message': 'Despesa removida com sucesso.'}), 200
        return jsonify({'message': 'Despesa não encontrada.'}), 404
    except Exception as e:
        print(f"ERRO em delete_expense: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

def update_item_status(item_type, item_id):
    try:
        data = request.get_json()
        if 'is_done' not in data: 
            return jsonify({'message': 'Missing is_done field'}), 400
        updated_item = db._update_item_status(f'{item_type}s', item_id, data['is_done'])
        if updated_item: 
            return jsonify(updated_item), 200
        return jsonify({'message': f'{item_type.capitalize()} not found'}), 404
    except Exception as e:
        print(f"ERRO em update_{item_type}_status: {e}")
        return jsonify({'message': 'Erro interno no servidor.'}), 500

@app.route('/api/flights/<int:item_id>/status', methods=['PATCH'])
def update_flight_status(item_id): return update_item_status('flight', item_id)
@app.route('/api/hotels/<int:item_id>/status', methods=['PATCH'])
def update_hotel_status(item_id): return update_item_status('hotel', item_id)
@app.route('/api/activities/<int:item_id>/status', methods=['PATCH'])
def update_activity_status(item_id): return update_item_status('activity', item_id)

if __name__ == '__main__':
    app.run(debug=True)
