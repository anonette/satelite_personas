# 🚀 Installation Guide - Dynamic Citizen Personas

## Quick Setup

### 1. Clone & Navigate
```bash
git clone [your-repo-url]
cd Satelite
```

### 2. Create Virtual Environment
```bash
python -m venv vnv
```

### 3. Activate Virtual Environment
**Windows (PowerShell):**
```bash
vnv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
vnv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source vnv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Setup
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here  # Optional for voice
```

### 6. Run the Application
```bash
streamlit run main.py
```

### 7. Open in Browser
Navigate to: `http://localhost:8501`

## 🎭 First Time Usage

1. **Load Satellite Data**: Use the sidebar to load TIFF files or ZIP archives
2. **Activate Personas**: Click "🔊 Activate" on different spectral bands
3. **Watch Conflicts**: New personas automatically challenge existing ones
4. **Generate More Conflicts**: Click "⚔️ Generate Conflict" when 2+ personas are active
5. **Chat**: Ask questions and watch personas argue with each other!

## 🔧 Optional Features

### Voice Synthesis (Recommended)
```bash
# Uncomment in requirements.txt:
# elevenlabs>=0.2.0

pip install elevenlabs
```
Add your ElevenLabs API key to `.env` file.

### Advanced Spectral Analysis
```bash
# Uncomment in requirements.txt:
# spectral>=0.23.1
# sentinelsat>=1.2.0

pip install spectral sentinelsat
```

## 📁 Sample Data

The `images/TIFF/` directory contains sample Prague satellite data to get started immediately.

## 🐛 Troubleshooting

### Common Issues:
- **Import errors**: Ensure all requirements are installed
- **API errors**: Check your OpenAI API key in `.env`
- **No conflicts**: Make sure multiple personas are activated
- **Voice not working**: ElevenLabs API key required for audio

### System Requirements:
- Python 3.8+
- 4GB+ RAM
- Internet connection for AI APIs
- Modern web browser

## 🎪 Ready to Create Environmental Drama!

Your conflict-driven spectral theater is ready. Load some satellite data and watch Prague's environmental activists argue about the city's future!