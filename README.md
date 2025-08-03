# 🧭 Travel Itinerary Planner

Hi👋🏽 This is my project in "Projeto de Software", below are the conceptual classes of the project 👇🏽

👤 User

*Description*: Represents a user registered on the platform.

. **id** (string): Unique user identifier.
. **name** (string): Username.
. **email** (string): User's email address.
. **password** (string): User password.
. **preferences** (array de strings): Travel preferences (e.g.,"adventure," "relax," "historic").

🗺️ Itinerary

*Description*: The central object, representing the complete travel plan.

. **id** (string): Unique route identifier..
. **title** (string): Travel plan title..
. **startDate** (date): Trip start date.
. **endDate** (date): Trip end date.
. **status** (strings) :Planning status (e.g., "draft", "planned", "active")
