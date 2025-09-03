# --- Importações ---
import json
import os
import random
import string
from flask import Flask, request, jsonify #converter dict python para database.json
from flask_cors import CORS #FUNCIONAMENTO DA API

#Classes 

class ItineraryItem:
    def __init__(self, id, trip_id, is_done=False):
        self.id = id
        self.trip_id = trip_id
        self.is_done = is_done

    def to_dict(self):
        return self.__dict__

#  classes Flight, Hotel, Activity e Expense HERDAM ItineraryItem.
class Flight(ItineraryItem):
    def __init__(self, id, trip_id, company, code, departure, arrival, is_done=False):
        super().__init__(id, trip_id, is_done)
        self.company = company
        self.code = code
        self.departure = departure
        self.arrival = arrival

class Hotel(ItineraryItem):
    def __init__(self, id, trip_id, name, checkin, checkout, is_done=False):
        super().__init__(id, trip_id, is_done)
        self.name = name
        self.checkin = checkin
        self.checkout = checkout

class Activity(ItineraryItem):
    def __init__(self, id, trip_id, description, date, is_done=False):
        super().__init__(id, trip_id, is_done)
        self.description = description
        self.date = date
        
class Expense(ItineraryItem):
    def __init__(self, id, trip_id, description, amount, currency, date, category, is_done=False):
        # A despesa também herda, mas o 'is_done' não é tão relevante aqui,
        super().__init__(id, trip_id, is_done)
        self.description = description
        self.amount = amount
        self.currency = currency
        self.date = date
        self.category = category


class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password #seria diferente ao migrar para um banco de dados

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

class Trip:
    def __init__(self, id, user_id, destination, name, start_date, end_date, is_suggestion=False, budget=0.0, share_code=None, collaborators=None):
        self.id = id
        self.user_id = user_id
        self.destination = destination
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.is_suggestion = is_suggestion
        self.budget = budget
        self.share_code = share_code
        self.collaborators = collaborators if collaborators is not None else []

    def to_dict(self):
        return self.__dict__


# Classe de Armazenamento com json
class DataStore:
    def __init__(self, filename='database.json'):
        self._filename = filename
        self._data = self._load_data()

    def _load_data(self):
        if not os.path.exists(self._filename):
            default_data = { "users": [], "trips": [], "flights": [], "hotels": [], "activities": [], "expenses": [] }
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
        collection = self._data.get(collection_name, [])
        if not collection: return 1
        return max(item.get('id', 0) for item in collection) + 1
    
    def _generate_share_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def add_user(self, name, email, password):
        user = User(self._get_next_id('users'), name, email, password)
        self._data['users'].append(user.__dict__)
        self._save_data()
        return user
    
    def find_user_by_email(self, email):
        user_data = next((u for u in self._data['users'] if u.get('email') == email), None)
        return User(**user_data) if user_data else None
    
    def find_user_by_id(self, user_id):
        user_data = next((u for u in self._data['users'] if u.get('id') == user_id), None)
        return User(**user_data) if user_data else None

    def add_trip(self, user_id, dest, name, start, end, share_code):
        if share_code and self.find_trip_by_share_code(share_code):
            return None 

        if not share_code:
            share_code = self._generate_share_code()
            while self.find_trip_by_share_code(share_code):
                share_code = self._generate_share_code()

        trip = Trip(self._get_next_id('trips'), user_id, dest, name, start, end, share_code=share_code, collaborators=[])
        self._data['trips'].append(trip.to_dict())
        self._save_data()
        return trip

    def find_trip_by_share_code(self, code):
        trip_data = next((t for t in self._data['trips'] if t.get('share_code') == code), None)
        return Trip(**trip_data) if trip_data else None

    def add_collaborator_to_trip(self, trip_id, user_id):
        for trip in self._data['trips']:
            if trip.get('id') == trip_id:
                if 'collaborators' not in trip or trip['collaborators'] is None:
                    trip['collaborators'] = []
                if user_id not in trip['collaborators'] and trip.get('user_id') != user_id:
                    trip['collaborators'].append(user_id)
                    self._save_data()
                return Trip(**trip)
        return None

    def get_user_trips(self, user_id):
        user_trips = []
        for t_data in self._data.get('trips', []):
            is_owner = t_data.get('user_id') == user_id
            is_collaborator = user_id in t_data.get('collaborators', [])
            if (is_owner or is_collaborator) and not t_data.get('is_suggestion', False):
                user_trips.append(Trip(**t_data))
        return user_trips

    def find_trip_by_id(self, trip_id):
        trip_data = next((t for t in self._data['trips'] if t.get('id') == trip_id), None)
        return Trip(**trip_data) if trip_data else None
    def get_suggestion_trips(self):
        return [Trip(**t_data) for t_data in self._data.get('trips', []) if t_data.get('is_suggestion', False)]
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

    def _add_item(self, collection_name, item_class, trip_id, **kwargs):
        # Este método agora pode adicionar qualquer 'ItineraryItem'
        item = item_class(self._get_next_id(collection_name), trip_id, **kwargs)
        self._data[collection_name].append(item.to_dict())
        self._save_data()
        return item
    
    def add_flight(self, trip_id, **kwargs): return self._add_item('flights', Flight, trip_id, **kwargs)
    def add_hotel(self, trip_id, **kwargs): return self._add_item('hotels', Hotel, trip_id, **kwargs)
    def add_activity(self, trip_id, **kwargs): return self._add_item('activities', Activity, trip_id, **kwargs)
    def add_expense(self, trip_id, **kwargs): return self._add_item('expenses', Expense, trip_id, **kwargs)

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


#  Configuração da Aplicação Flask ---
app = Flask(__name__)
CORS(app)
db = DataStore()


# Helpers ---
def user_has_permission(trip_id, user_id):
    trip = db.find_trip_by_id(trip_id)
    if not trip:
        return False, (jsonify({'message': 'Viagem não encontrada.'}), 404)
    collaborators = trip.collaborators if trip.collaborators is not None else []
    if trip.user_id == user_id or user_id in collaborators:
        return True, None
    return False, (jsonify({'message': 'Permissão negada.'}), 403)


#  Rotas da API ---
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if db.find_user_by_email(data['email']): 
        return jsonify({'message': 'Este email já está em uso.'}), 409
    user = db.add_user(data['name'], data['email'], data['password'])
    return jsonify({'user': user.to_dict()}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db.find_user_by_email(data['email'])
    if user and user.password == data['password']: 
        return jsonify({'user': user.to_dict()}), 200
    return jsonify({'message': 'Credenciais inválidas.'}), 401

@app.route('/api/trips', methods=['POST'])
def create_trip():
    data = request.get_json()
    share_code = data.get('share_code', '').strip()
    trip = db.add_trip(data['user_id'], data['destination'], data['name'], data['start_date'], data['end_date'], share_code)
    
    if not trip:
        return jsonify({'message': 'Este código de partilha já está em uso. Por favor, escolha outro.'}), 409

    return jsonify({'trip': trip.to_dict()}), 201

@app.route('/api/trips/join', methods=['POST'])
def join_trip():
    data = request.get_json()
    share_code = data.get('share_code')
    user_id = data.get('user_id')
    trip = db.find_trip_by_share_code(share_code)
    if not trip:
        return jsonify({'message': 'Código de partilha inválido.'}), 404
    
    updated_trip = db.add_collaborator_to_trip(trip.id, user_id)
    return jsonify({'trip': updated_trip.to_dict()}), 200

@app.route('/api/my-trips', methods=['GET'])
def get_my_trips():
    user_id = int(request.args.get('user_id'))
    user_trips = db.get_user_trips(user_id)
    return jsonify({"trips": [t.to_dict() for t in user_trips]}), 200

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    suggestion_trips = db.get_suggestion_trips()
    return jsonify({"trips": [t.to_dict() for t in suggestion_trips]}), 200

@app.route('/api/trips/<int:trip_id>', methods=['GET'])
def get_trip(trip_id):
    trip = db.find_trip_by_id(trip_id)
    return jsonify({'trip': trip.to_dict()}) if trip else (jsonify({'message': 'Viagem não encontrada.'}), 404)

@app.route('/api/trips/<int:trip_id>/budget', methods=['PATCH'])
def update_budget(trip_id):
    data = request.get_json()
    user_id = data.get('user_id')
    has_perm, error_resp = user_has_permission(trip_id, user_id)
    if not has_perm: return error_resp
    updated_trip = db.update_trip_budget(trip_id, float(data['budget']))
    return jsonify({'trip': updated_trip.to_dict()}) if updated_trip else (jsonify({'message': 'Viagem não encontrada.'}), 404)

@app.route('/api/trips/<int:trip_id>/details', methods=['GET'])
def get_trip_details(trip_id):
    details = db.get_details_for_trip(trip_id)
    return jsonify(details), 200

def add_item_to_trip(trip_id, item_type):
    data = request.get_json()
    user_id = data.pop('user_id', None)
    has_perm, error_resp = user_has_permission(trip_id, user_id)
    if not has_perm: return error_resp

    add_method = getattr(db, f"add_{item_type}")
    item = add_method(trip_id, **data)
    return jsonify({item_type: item.to_dict()}), 201

@app.route('/api/trips/<int:trip_id>/flights', methods=['POST'])
def add_flight_to_trip(trip_id): return add_item_to_trip(trip_id, 'flight')
@app.route('/api/trips/<int:trip_id>/hotels', methods=['POST'])
def add_hotel_to_trip(trip_id): return add_item_to_trip(trip_id, 'hotel')
@app.route('/api/trips/<int:trip_id>/activities', methods=['POST'])
def add_activity_to_trip(trip_id): return add_item_to_trip(trip_id, 'activity')

@app.route('/api/trips/<int:trip_id>/expenses', methods=['GET', 'POST'])
def handle_expenses(trip_id):
    if request.method == 'GET':
        expenses = db.get_expenses_for_trip(trip_id)
        return jsonify({"expenses": [e.to_dict() for e in expenses]}), 200
    if request.method == 'POST':
        return add_item_to_trip(trip_id, 'expense')

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    if db.remove_expense(expense_id):
        return jsonify({'message': 'Despesa removida com sucesso.'}), 200
    return jsonify({'message': 'Despesa não encontrada.'}), 404

def update_item_status(item_type, item_id):
    data = request.get_json()
    collection_name = 'activities' if item_type == 'activity' else f'{item_type}s'
    updated_item = db._update_item_status(collection_name, item_id, data['is_done'])
    return jsonify(updated_item) if updated_item else (jsonify({'message': f'{item_type.capitalize()} not found'}), 404)

@app.route('/api/flights/<int:item_id>/status', methods=['PATCH'])
def update_flight_status(item_id): return update_item_status('flight', item_id)
@app.route('/api/hotels/<int:item_id>/status', methods=['PATCH'])
def update_hotel_status(item_id): return update_item_status('hotel', item_id)
@app.route('/api/activities/<int:item_id>/status', methods=['PATCH'])
def update_activity_status(item_id): return update_item_status('activity', item_id)


#  Execução da Aplicação 
if __name__ == '__main__':
    app.run(debug=True)

