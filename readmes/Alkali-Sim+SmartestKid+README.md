# SmartestKid AI Assistant

A Windows desktop AI assistant built in Python. Assistant (without tools) is ~1000 lines of python code, with super simple chat UI inspired by the original AI, SmarterChild. Uses Windows COM automation to interface with Microsoft Office (Word, Excel), Images, and your file system. Perfect for Windows users looking to explore AI-powered desktop automation.

## Demo
https://github.com/user-attachments/assets/a7b0ae86-53d6-4407-b2dd-ea6f4abb59e4

## Features

- Toggle between voice and text input modes
- Interface with Word, Excel, Images, and your file system (Windows only)
- Cute draggable interface elements

## Requirements

- Windows OS
- Python 3.7+
- OPENAI_API_API key for AI responses
- Microsoft Office (for Word/Excel features)
- Virtual environment (recommended)

## Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix/MacOS:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install tkinter pillow pyaudio httpx python-dotenv
   ```
4. Create a `.env` file in the root directory with your API keys:
   ```env
   # API Keys
   OPENAI_API_KEY=your_openai_api_key_here

   # Paths
   DATALAKE_DIRECTORY=path/to/your/datalake
   ```
5. Run the application:
   ```bash
   python smartest_kid.py
   ```

## Usage

- Click the microphone icon to toggle voice input
- Click the message icon to toggle the chat interface
- Drag the robot or chat window to reposition them
- Press ESC to exit the application

## Project Structure

- `smartest_kid.py`: Main application and robot animation logic
- `chat_interface.py`: Chat UI implementation
- `ai_assistant.py`: AI integration with Claude API
- `assets/`: Contains UI icons and robot character images
- `tools/`: Contains tools for the assistant to use
- `datalake/`: Contains data for the assistant to use
- `.env`: Configuration and API keys

## License

MIT License

## Contributing

Want to contribute? Here are some areas we'd love help with:
1. Office Integration - Expand Excel/Word functionality and add new Office app support
2. Assistant Personality - Add Clippy-style emotions and contextual reactions (pls someone find these gifs)
3. New Tools - Integrate with more applications (PowerPoint, PDF readers, browsers, etc.)

Feel free to open an issue or submit a pull request!

## Authors

Victor Von Miller & Emmett Goodman
