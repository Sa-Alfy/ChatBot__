## Modern Assistant Interface

A feature-rich desktop application built with Python and Tkinter that combines multiple useful tools in a modern, gradient-styled interface.

![Assistant Interface Preview](screenshots/preview.png)

## Features

### Text-to-Voice Converter
- Convert any text to speech
- Clean and intuitive interface
- Real-time conversion

### Weather Information
- Get detailed weather data for any city
- Visual weather indicators with icons
- Display temperature, humidity, wind, and more
- Day/night cycle indicators
- Dynamic background based on weather conditions

### YouTube Downloader
- Download videos or extract audio
- Progress tracking with speed indicator
- Supports high-quality video downloads
- Automatic format conversion
- Organized downloads folder structure

## Technical Details

### Built With
- Python 3.8+
- Tkinter for GUI
- Custom styling and modern UI elements
- Gradient backgrounds
- Responsive design

### Core Libraries
- `pyttsx3` for text-to-speech
- `yt-dlp` for YouTube downloads
- `Pillow` for image handling
- `requests` for API communication

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/ChatBot__-main.git
cd ChatBot__-main
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Install FFmpeg (required for YouTube downloads)
- Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

4. Run the application
```bash
python -m ChatBot.gui.gui
```

## Usage

### Text-to-Voice
1. Click the "Text-to-Voice" button
2. Enter your text in the input field
3. Click "Convert to Voice" to hear the audio

### Weather Information
1. Click the "Weather Info" button
2. Enter a city name
3. View detailed weather information with visual indicators

### YouTube Downloader
1. Click the "YouTube Downloader" button
2. Paste a YouTube URL
3. Select video or audio format
4. Click download and monitor progress
5. Find downloaded files in the downloads folder

## Project Structure
```
ChatBot__-main/
├── ChatBot/
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── gui.py
│   │   └── custom_widgets.py
│   ├── bot/
│   │   ├── __init__.py
│   │   └── bot.py
│   └── gui_images/
│       ├── wave.png
│       ├── cloud.png
│       ├── gmail_logo.png
│       ├── youtube_logo.png
│       └── weather_icons/
├── downloads/
│   ├── videos/
│   └── audio/
├── requirements.txt
└── README.md
```

## Configuration

### Weather API
The application uses OpenWeatherMap API. To use your own API key:
1. Get an API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Replace the API key in `bot.py`

### Download Locations
- Videos are saved to: `/downloads/videos/`
- Audio is saved to: `/downloads/audio/`

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits
- Weather data provided by OpenWeatherMap
- YouTube downloading powered by yt-dlp
- Icons and visual elements designed for modern UI

## Credits
- Weather data provided by OpenWeatherMap
- YouTube downloading powered by yt-dlp
- Icons and visual elements designed for modern UI
- GUI development assistance from Microsoft Copilot
- Additional GUI improvements and feature implementations by GitHub Copilot

## Author
Shariar Ahamed  
Email: www.saaulfy@gmail.com

## Acknowledgments
- Thanks to the Python community for the amazing libraries
- Special thanks to Microsoft Copilot for initial GUI development assistance
- Thanks to GitHub Copilot for improved UI design, code organization, and feature implementation

## Development History
- Initial GUI implementation with Microsoft Copilot
- Enhanced features and modern UI design with GitHub Copilot:
  - Gradient backgrounds and modern styling
  - Weather display improvements
  - YouTube download progress tracking
  - Improved file organization
  - Better error handling
  - Download directory management

Data Persistence: Implement features to save user inputs and settings between sessions.


If you want to help me learn about this project it will be a huge help, Thank You.
