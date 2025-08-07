# 🧭 Travel Itinerary Planner

Hi👋🏽 This is my project in "Projeto de Software", below are the conceptual classes of the project 👇🏽

## for use: 

salve o programa em um diretório no seu computador <br/>
execute ele através do terminal "python nome_do_arquivo.py" <br/>
será executado <br/>

## notes:

estou conhecendo bibliotecas melhores para o python, então a interface gráfica não foi das melhores e ando assistindo tutorial no youtube para melhorar isso. <br/>
O código está sendo enviado de uma vez já que eu perdi algum trecho da aula que falava que era para entregar o programa estruturado até 06-08, mas a partir de agora <br/>
vou realizando commit conforme for atualizando o projeto. <br/>

## Conceitual Class (what to expect conceptually from the program) 

### 👤 User

*Description*: Represents a user registered on the platform.

. **id** (string): Unique user identifier. <br/>
. **name** (string): Username. <br/>
. **email** (string): User's email address. <br/>
. **password** (string): User password. <br/>
. **preferences** (array de strings): Travel preferences (e.g.,"adventure," "relax," "historic"). <br/>

### 🗺️ Itinerary

*Description*: The central object, representing the complete travel plan.

. **id** (string): Unique route identifier. <br/>
. **title** (string): Travel plan title. <br/>
. **startDate** (date): Trip start date. <br/>
. **endDate** (date): Trip end date. <br/>
. **status** (string) :Planning status (e.g., "draft", "planned", "active") <br/>

### 🛧 Destination

*Description*: Represents a city, country or point of interest.

. **id** (string):Unique destination identifier. <br/>
. **name** (string): Destination name. <br/>
. **description** (date): Brief description of the location. <br/>
. **locationData** (object): Geolocation information (possible Google Maps) <br/>
. **reviews** (array Review): Collection of reviews(e.g., "draft", "planned", "active") <br/>
. **guides** (array Resource): Collection of travel guides and resources <br/>

### 🚅 TripDay 

*Description*: Represents a single day within the itinerary, organizing daily activities.

. **date** (date): The specific date of the day. <br/>

### 🏔️ Activity

*Description*: Represents a specific event or action in the itinerary (flight, hotel, tour, meal).

. **id** (string) :Unique activity identifier. <br/>
. **name** (string): Name of the activity (e.g. "Hotel Check-in", "Museum Visit"). <br/>
. **type** (string): Type of activity (e.g. "hotel", "flight", "tour", "meal") <br/>
. **startDate** (date): Start date and time. <br/>
. **endDate** (date): End date and time <br/>
. **description** (string): Activity details. <br/>
. **coast** (number): Estimated or actual cost. <br/>
. **type** (string): Reservation status (e.g. "reserved", "pending"). <br/>

### 🚕 Booking

*Description:* Stores information about a reservation.

. **id** (string): Unique reservation identifier. <br/>
. **bookingReference** (string): Reservation number. <br/>
. **provider** (string): Name of the booking provider (e.g. "Booking.com", "Decolar") simulation without APIs. <br/>
. **cost** (number): Final booking cost. <br/>
. **status** (string): Reservation status (e.g. "confirmed", "cancelled"). <br/>

### 💸 Expense

*Description:* Tracks the costs of a trip.

. **id** (string): Unique expense identifier. <br/>
. **description** (string): Expense description (e.g., "lunch", "ticket"). <br/>
. **amount** (number): Expense amount. <br/>
. **currency** (string): Currency used. <br/>
. **date** (date): Expense date. <br/>
. **category** (string): Expense category (e.g., "food", "transportation").<br/>
 
### ⭐ Review

*Description:* Contains user reviews and comments about destinations or activities.

. **id** (string): Unique review identifier. <br/>
. **text** (string): Comment text. <br/>
. **rating** (number): Score (e.g., 1 to 5 stars). <br/>
. **date** (date): Publication date. <br/>

### ⭐ Resource

*Description:* Represents travel guides, articles, or other useful resources.

. id (string): Unique identifier. <br/>
. title (string): Resource title. <br/>
. type (string): Resource type (e.g., "article," "video," "guide").<br/>
. url (string): Link to the resource. <br/>
. content (string): Resource content.
