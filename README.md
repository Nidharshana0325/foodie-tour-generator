🍽️ AI-Powered Foodie Tour Guide
https://img.shields.io/badge/python-3.8%252B-blue
https://img.shields.io/badge/flask-2.0%252B-red
https://img.shields.io/badge/Julep_AI-integrated-green
https://img.shields.io/badge/license-MIT-orange

🌟 Overview
The Foodie Tour Guide is an intelligent culinary assistant that creates personalized one-day food experiences for any city, considering weather conditions, seasonal dishes, transportation options, and budget constraints. Powered by Julep AI's advanced language model, this application combines practical travel planning with engaging storytelling about local cuisine.

🛠️ Tech Stack
Core Components
Backend Framework: Flask (Python)

AI Engine: Julep AI (grok-3-beta model)

Weather API: wttr.in

Frontend: HTML/CSS/JavaScript (served via Flask)

Persistence: Local file storage for agent ID

Key Dependencies
plaintext
flask==2.0.1
requests==2.26.0
julep==0.1.0  # Julep AI client library
python-dotenv==0.19.0
✨ Key Features
🍜 Intelligent Food Itineraries
Three-meal planning (breakfast, lunch, dinner)

Seasonal dish recommendations based on current month

Budget-aware suggestions (all within specified INR limit)

Restaurant pairing with each recommended dish

🚍 Integrated Travel Planning
Transportation recommendations between locations

Cost-efficiency analysis for transit options

Weather-adaptive suggestions (indoor/outdoor dining)

📖 Cultural Storytelling
Origin stories and fun facts for each dish

Local culinary traditions and history

Engaging narrative format

⚙️ Technical Features
Persistent agent management (via local storage)

Real-time weather integration

Multi-city processing in single request

Error handling and logging

🚀 Getting Started
Prerequisites
Python 3.8+

Julep API key

Basic understanding of Flask applications

Installation
Clone the repository:

bash
git clone https://github.com/yourusername/foodie-tour-guide.git
cd foodie-tour-guide
Install dependencies:

bash
pip install -r requirements.txt
Set up environment:

bash
echo "JULEP_API_KEY=your_api_key_here" > .env
Running the Application
bash
python app.py
The application will be available at http://localhost:5000

📚 API Documentation
Endpoints
POST /api/generate-tour
Generates food tour itineraries for one or more cities.

Request Body:

json
{
  "cities": ["Mumbai", "Delhi"],
  "budget": 1500
}
Successful Response:

json
[
  {
    "city": "Mumbai",
    "weather": "Sunny",
    "season": "Monsoon",
    "itinerary": "Your detailed food tour plan...",
    "budget": 1500
  }
]
Error Response:

json
{
  "error": "Error message description"
}
🏗️ Project Structure
plaintext
foodie-tour-guide/
├── app.py                # Main application logic
├── agent_id.txt          # Persistent agent storage
├── requirements.txt      # Python dependencies
├── static/               # Frontend assets
│   ├── index.html        # Main interface
│   ├── styles.css        # Optional styling
│   └── script.js         # Optional JavaScript
└── README.md             # This documentation
🌍 Deployment Options
1. Render (Recommended)
Create new Web Service

Set environment variables:

JULEP_API_KEY

PORT (default: 5000)

Set build command: pip install -r requirements.txt

Set start command: python app.py

2. Docker Deployment
dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
3. Traditional VPS
Set up Nginx reverse proxy

Use Gunicorn as WSGI server:

bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements.
