# import streamlit as st
from flask import Flask, request, jsonify
from agent import initialize_ai_model, create_ai_crew, generate_itinerary
from tools import load_api_key

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the AI Travel Planner API!"

@app.route('/generate_itinerary', methods=['POST'])
def generate_travel_itinerary():
    # Get input data from the request body (JSON)
    data = request.get_json()

    origin = data.get('origin')
    cities = data.get('cities')
    date_range = data.get('date_range')
    interests = data.get('interests')

    # Input validation
    if not origin or not cities or not date_range or not interests:
        return jsonify({"error": "Please provide all required fields: origin, cities, date_range, and interests."}), 400

    # Load API key from environment
    api_key = load_api_key()
    if not api_key:
        return jsonify({"error": "API key not found. Please set your API key in the environment."}), 500

    api_key = load_api_key()
    if not api_key:
        return jsonify({"error": "API key not found."}), 500
    
    openaigpt4 = initialize_ai_model(api_key)
    cities_list = [city.strip() for city in cities.split(',')]
    data_to_process = {
        "origin": origin,
        "cities": cities_list,
        "date_range": date_range,
        "interests": interests
    }

    ai_crew = create_ai_crew(openaigpt4)
    itinerary = generate_itinerary(data_to_process, ai_crew)

    
    # Return the generated itinerary as a JSON response
    return jsonify({"itinerary": itinerary})

if __name__ == '__main__':
    app.run(debug=True)


# def main():
#     st.title("AI Travel Planner")

#     # Mengajukan pertanyaan kepada pengguna
#     origin = st.text_input("From where will you be traveling from?")
#     cities = st.text_input("What are the cities options you are interested in visiting? (separate by commas)")
#     date_range = st.text_input("What is the date range you are interested in traveling?")
#     interests = st.text_input("What are some of your high level interests and hobbies?")

#     if st.button("Generate Itinerary"):
#         #Load API key from environtment
#         api_key = load_api_key()
#         if not api_key:
#             st.error("API key not found. Please set your API")
#             return
#         #Initialize AI model 
#         openaigpt4 = initialize_ai_model(api_key)

#         # Data yang akan diproses oleh AI Crew
#         data = {
#             "origin": origin,
#             "cities": cities,
#             "date_range": date_range,
#             "interests": interests
#         }


#         # Create AI Crew
#         ai_crew = create_ai_crew(openaigpt4)

#         #Generate Itinerary
#         itinerary = generate_itinerary(data, ai_crew)

#         #Display Itinerary
#         st.markdown(itinerary)
        
# if __name__ == "__main__":
#     main()
