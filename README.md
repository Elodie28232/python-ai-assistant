# Voice Virtual Assistant with ElevenLabs

A Python-based voice assistant that uses ElevenLabs for conversational AI and text-to-speech. It can greet you, answer questions, and provide weather updates via the OpenWeatherMap API — all in your voice.

---

## Features
- Talk to the assistant using your voice  
- Set up a personalized schedule  
- Get real-time weather updates  
- Easy to add more commands  

---

## Setup

### Requirements
- Python 3.8 or higher  
- ElevenLabs API key and Agent ID ([get them here](https://elevenlabs.io/))  
- OpenWeatherMap API key ([get it here](https://openweathermap.org/api))  (TODO)

### Installation
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project directory with the following content:
   ```env
   ELEVEN_API_KEY=your_elevenlabs_api_key
   ELEVEN_AGENT_ID=your_elevenlabs_agent_id
   OPENWEATHER_API_KEY=your_openweathermap_api_key
   ```
3. Run the assistant:
   ```sh
   python voice-assist.py
   ```

## Usage
- The assistant will greet you and wait for your input.
- You can ask about the weather (e.g., "What's the weather in London?").
- To stop the assistant, press `Ctrl+C`.

## Credits
This project is inspired by and adapted from the [Codedex Voice Virtual Assistant with ElevenLabs project](https://www.codedex.io/projects/create-a-voice-virtual-assistant-with-elevenlabs). Special thanks to Codedex for their educational resources and project inspiration.

## License
This project is for educational purposes. See the original Codedex project for further licensing details.
