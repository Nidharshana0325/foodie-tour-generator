import time
import requests
from julep import Julep
import datetime
import os
from flask import Flask, request, jsonify, send_file
import traceback

# Initialize Flask app
app = Flask(__name__, static_folder='.', template_folder='.')

# Initialize Julep client with your API key
client = Julep(api_key="eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTQyMTA1OTksImlhdCI6MTc0OTAyNjU5OSwic3ViIjoiNTViZGRjMjMtMjliMS01NGRlLThhYTEtN2I0NDFkYzI0MGZkIn0.xXF8Rf1Ikss1i2ZaBea5V6ZnRinG-kAh4YCbsS4NE8U-N6ZveXm9wNiMv-qrJ9LuTSuEeR_rcj8avDzQmPg-Dw")

AGENT_ID_FILE = "agent_id.txt"

def create_agent():
    agent = client.agents.create(
        name="Foodie Tour Guide with Transport and Budget",
        model="grok-3-beta",  # Updated to a likely model name; confirm with Julep API docs
        about="A creative culinary assistant that builds one-day foodie experiences considering weather, iconic dishes, local stories, transport, and budget."
    )
    with open(AGENT_ID_FILE, "w") as f:
        f.write(agent.id)
    print(f"Agent created with ID: {agent.id}")
    return agent

def load_agent():
    if os.path.exists(AGENT_ID_FILE):
        with open(AGENT_ID_FILE, "r") as f:
            agent_id = f.read().strip()
        try:
            agent = client.agents.get(agent_id)
            print(f"Loaded existing agent with ID: {agent_id}")
            return agent
        except Exception as e:
            print(f"Failed to load agent {agent_id}: {e}")
            print("Creating new agent...")
            return create_agent()
    else:
        print("Agent ID file not found. Creating new agent...")
        return create_agent()

def fetch_weather(city):
    try:
        res = requests.get(f"https://wttr.in/{city}?format=%C", timeout=5)
        res.raise_for_status()
        return res.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching weather for {city}: {e}")
        return "Unknown"

def get_season():
    month = datetime.datetime.now().month
    if month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8]:
        return "Monsoon"
    else:
        return "Winter"

def get_next_day_date():
    # Get the current date and add one day
    current_date = datetime.datetime.now()
    next_day = current_date + datetime.timedelta(days=1)
    return next_day.strftime("%B %d, %Y")  # e.g., "June 09, 2025"

def generate_foodie_tour(agent, city, weather, season, budget_inr):
    next_day_date = get_next_day_date()
    prompt_user_content = f"""City: {city}
Weather: {weather}
Season: {season}
Date: {next_day_date}
Daily Food Budget (INR): ₹{budget_inr}
Requirements:
- Suggest breakfast, lunch, and dinner dishes (famous & seasonal)
- Include one origin story or fun fact for each dish
- Recommend one restaurant per dish, keeping total day's food cost within ₹{budget_inr}
- Choose indoor or outdoor dining based on weather
- Suggest the best transport method between meal locations (e.g., walking, taxi, public transport), considering cost efficiency
- Craft a storytelling-style one-day foodie itinerary for {next_day_date} including transport and budget details
- Ensure all monetary values are formatted with the ₹ symbol (e.g., ₹500)
"""

    task_definition = {
        "name": f"Foodie Tour with Budget & Transport: {city}",
        "description": "Generates a culinary story for one-day in a city including transport and budget considerations.",
        "main": [{
            "prompt": [
                {
                    "role": "system",
                    "content": "You are a foodie tour guide who crafts immersive food journeys. Include weather insights, iconic & seasonal dishes, local stories, vivid narration, transport suggestions, and budget-conscious restaurant options. Format all monetary values with the ₹ symbol."
                },
                {
                    "role": "user",
                    "content": prompt_user_content
                }
            ]
        }]
    }

    try:
        print(f"Creating task for city: {city}")
        task = client.tasks.create(agent_id=agent.id, **task_definition)
        print(f"Task created with ID: {task.id}")
        execution = client.executions.create(task_id=task.id, input={})
        print(f"Execution started with ID: {execution.id}")

        while True:
            result = client.executions.get(execution.id)
            if result.status == 'succeeded':
                # Assuming the Julep API returns a structure similar to the provided response
                output = result.output
                # Check if the output is a dict with 'choices' (like the provided response)
                if isinstance(output, dict) and 'choices' in output and len(output['choices']) > 0:
                    itinerary_text = output['choices'][0].get('message', {}).get('content', str(output))
                else:
                    itinerary_text = str(output)  # Fallback to string conversion
                print(f"Task succeeded for {city}. Output: {itinerary_text}")
                return itinerary_text
            elif result.status == 'failed':
                error_msg = f"Task failed for {city}: {result.error}"
                print(error_msg)
                return error_msg
            else:
                print(f"⏳ Generating foodie tour for {city}...")
                time.sleep(2)
    except Exception as e:
        error_msg = f"Error during Julep task execution for {city}: {str(e)}"
        print(error_msg)
        return error_msg

# Flask route to serve the index.html file
@app.route('/')
def serve_index():
    return send_file('index.html')

# Flask API endpoint to generate foodie tour
@app.route('/api/generate-tour', methods=['POST'])
def api_generate_tour():
    try:
        data = request.get_json()
        cities = data.get('cities', [])
        budget_inr = data.get('budget', 1000)

        if not cities:
            return jsonify({"error": "No cities provided"}), 400

        agent = load_agent()
        season = get_season()
        results = []

        for city in cities:
            weather = fetch_weather(city)
            itinerary = generate_foodie_tour(agent, city, weather, season, budget_inr)
            if itinerary and not itinerary.startswith("Task failed") and not itinerary.startswith("Error during"):
                results.append({
                    "city": city,
                    "budget": budget_inr,
                    "weather": weather,
                    "season": season,
                    "itinerary": itinerary
                })
            else:
                results.append({
                    "city": city,
                    "budget": budget_inr,
                    "weather": weather,
                    "season": season,
                    "itinerary": itinerary if itinerary else f"Could not generate foodie tour for {city}."
                })

        return jsonify(results), 200

    except Exception as e:
        print(f"Error in API: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)