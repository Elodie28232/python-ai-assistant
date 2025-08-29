
# Import standard libraries
import sys  # Provides access to system-specific parameters and functions
import time  # Used for time-related functions (e.g., sleep)
import os  # Used for interacting with the operating system (e.g., environment variables)
from dotenv import load_dotenv  # Loads environment variables from a .env file

# Import third-party library for making HTTP requests
import requests  # Used to send HTTP requests (e.g., to APIs)

# --- Helper Function: Get Weather ---
def get_weather(city):
    """
    Fetches the current weather for a given city using the OpenWeatherMap API.
    - city: Name of the city (string)
    - Returns: Weather description string or error message
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Get API key from environment variable (set in .env)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"  # API endpoint
    try:
        response = requests.get(url).json()  # Send GET request and parse JSON response
        if "main" in response:  # Check if response contains weather data
            temp = response["main"]["temp"]  # Extract temperature
            description = response["weather"][0]["description"]  # Extract weather description
            return f"The weather in {city} is {temp}°C with {description}."
        return "Could not get weather info."
    except Exception as e:
        # If any error occurs (e.g., network issue), return error message
        return "Error fetching weather."


# --- Load Environment Variables ---
load_dotenv()  # Loads variables from .env file into environment
API_KEY = os.getenv("ELEVEN_API_KEY")  # ElevenLabs API key
AGENT_ID = os.getenv("ELEVEN_AGENT_ID")  # ElevenLabs Agent ID

# --- Import ElevenLabs SDK and Types ---
from elevenlabs import ElevenLabs  # Main ElevenLabs client
from elevenlabs.conversational_ai.conversation import Conversation  # Conversation class for managing chat
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface  # Handles audio input/output
from elevenlabs.types import ConversationConfig  # Configuration for conversation

# --- User Info ---
user_name = "Elodie"
schedule = "Internship Planning for February at 10:00; Reply to messages 12:00"  # Example schedule

# --- Conversation Prompt ---
# This prompt guides the assistant's behavior and tone
prompt = f"""
You are a professional virtual assistant.
The user has the following schedule: {schedule}.
Speak concisely and clearly, like a helpful assistant.
Always prioritize actionable information.
Do not use unnecessary small talk.
"""
first_message = f"Hello {user_name}, how can I help you today?"  # Initial greeting

# --- Conversation Override (optional, not used here) ---
conversation_override = {
    "agent": {
       # "prompt": {"prompt": f"Hello {user_name}, your schedule is: {schedule}."}
    }
}

# --- Conversation Configuration ---
config = ConversationConfig(
    user_id="elodie_1234",  # Unique string for your session
    conversation_config_override={},  # Optional overrides
    extra_body={},           # Required for SDK (can be empty)
    dynamic_variables={}     # Required for SDK (can be empty)
)



# --- Initialize ElevenLabs Client ---
client = ElevenLabs(api_key=API_KEY)  # Create ElevenLabs client with your API key

# --- Select Voice ---
all_voices = client.voices.get_all()  # Get all available voices (returns list of (voice_id, [Voice]) tuples) = debugging step
voice_id_to_use = "QxpsWUTZAxznFqyH1goJ"  # The ID of the voice you want to use

# Find the desired voice object by its ID
voice = None  # Will hold the selected voice object
for vid, voices_list in all_voices:
    for v in voices_list:  # voices_list is a list of Voice objects
        if v.voice_id == voice_id_to_use:
            voice = v  # Found the desired voice
            break
    if voice:
        break

if voice:
    print(f"Using voice: {voice.name} (ID: {voice.voice_id})")  # Confirm selected voice
else:
    print("Voice not found. Available voices:")
    for vid, voices_list in all_voices:
        for v in voices_list:
            print(f"ID: {v.voice_id}, Name: {v.name}")  # List available voices

# --- Callback Functions (for debugging, not used in main loop) ---
def print_agent_response(response):
    print("Agent says:", response)  # Print agent's response

def print_interrupted_response(original, corrected):
    print("Agent interrupted:", corrected)  # Print interrupted response

def print_user_transcript(transcript):
    print("You said:", transcript)  # Print what user said

# --- Initialize Conversation ---
conversation = Conversation(
    client,  # ElevenLabs client
    AGENT_ID,  # Agent ID
    config=config,  # Conversation configuration
    requires_auth=True,  # Require authentication
    audio_interface=DefaultAudioInterface()  # Use default audio input/output
)

# TODO: Optionally, start conversation only with a specific keyword

# --- Start Session ---
conversation.start_session()
print("Assistant started. Press Ctrl+C to stop.")

# Wait briefly to ensure WebSocket is connected before sending messages
time.sleep(1)  # Small delay, adjust if needed

# --- Send Prompt and Greeting as First Messages ---
conversation.send_user_message(prompt)  # Send assistant prompt
conversation.send_user_message(first_message)  # Send initial greeting


# --- Main Loop: Keep Assistant Running ---
# This loop keeps the assistant running until you press Ctrl+C
try:
    while True:
        time.sleep(0.1)  # Sleep briefly to keep CPU usage low
except KeyboardInterrupt:
    print("\nStopping assistant...")  # Print message when stopping

    # Send goodbye message to conversation so it speaks it before exiting
    conversation.send_user_message("Goodbye, have a great day!")

    # Wait a bit to let the AI finish speaking
    time.sleep(0.1)

    sys.exit(0)  # Exit the program

# --- TODO: Check this Main Listening Loop ---
# The following code (commented out) shows how you could process user voice input in real time.
# It demonstrates how to fetch transcripts, handle 'goodbye', and answer weather queries.
#
# try:
#     while True:
#         # Fetch the latest user transcript from the audio interface
#         transcript = conversation.audio_interface.get_last_transcript()  # Get last recognized speech
#         if transcript:
#             print("You said:", transcript)
#
#             # Exit if user says goodbye
#             if "goodbye" in transcript.lower():
#                 conversation.send_user_message("Goodbye! Have a great day!")
#                 conversation.stop_session()
#                 break
#
#             # Example: weather query
#             if "weather in" in transcript.lower():
#                 city = transcript.lower().split("weather in")[-1].strip()  # Extract city name
#                 weather_info = get_weather(city)  # Get weather info
#                 conversation.send_user_message(weather_info)  # Respond with weather
#
#         # Small sleep to prevent CPU overuse
#         time.sleep(0.1)
#
# except KeyboardInterrupt:
#     print("\nStopping assistant...")
#     conversation.stop_session()
#     sys.exit(0)
