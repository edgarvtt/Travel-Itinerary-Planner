# 🧭 Travel Itinerary Planner

Hi👋🏽 This is my project in "Projeto de Software", below are the conceptual classes of the project 👇🏽

## for use: 

salve o programa em um diretório no seu computador <br/>
execute ele através do terminal "python nome_do_arquivo.py" <br/>
após isso, abra index.html para começar <br/>
**(pode ser necessário instalar o FLASK, se sua máquina não tiver ele instalado)** </br>


## notes:

o programa é essencialmente python, mas outras tecnologias foram usadas para compor a parte visual,
a questão de simular um servidor, simular um banco de dados e a parte lógica do back-end está em python com o JSON, enquanto visualmente foram usados frameworks CSS Tailwand , HTML e JS.
<br/>

decidi fazer com tecnologias web por ter uma maior familiriade (sempre tive afinidade com UX/UI e  tecnologias front-end) e por ter a certeza que ficaria algo mais bonito, já que
a curva de aprendizado para aprender uma biblioteca python que entregasse a parte da interface gráfica de com uma experiência de úsuario seria bastante alta (para mim que começaria do zero)
então estou usando habilidades que adqueri anteriormente, como pode ser visto em outros projetos meus neste github. </br>

Salientando também que o meu calcanhar de aquiles foi o JSON, sendo que ele deve ser retirado posteriomente, que por vez é desnecessário no contexto da disciplina. Estou usando por ele está simulando um banco de dados convertendo as informações do atributo de classes em dicionários em JSON. </br>

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
