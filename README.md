# 🧭 Travel Itinerary Planner

Hi👋🏽 This is my project in "Projeto de Software", below are the conceptual classes of the project 👇🏽

👤 User

*Description*: Represents a user registered on the platform.

. **id** (string): Unique user identifier. <br/>
. **name** (string): Username. <br/>
. **email** (string): User's email address. <br/>
. **password** (string): User password. <br/>
. **preferences** (array de strings): Travel preferences (e.g.,"adventure," "relax," "historic"). <br/>

🗺️ Itinerary

*Description*: The central object, representing the complete travel plan.

. **id** (string): Unique route identifier. <br/>
. **title** (string): Travel plan title. <br/>
. **startDate** (date): Trip start date. <br/>
. **endDate** (date): Trip end date. <br/>
. **status** (string) :Planning status (e.g., "draft", "planned", "active") <br/>
