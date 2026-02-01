# Sant_Tukaram_Maharaj_PS4
# PrepPro - AI Interview Coach 🎓

PrepPro is a cutting-edge AI-powered interview coaching platform designed to help job seekers improve their interview skills. It combines **Computer Vision**, **Speech Analysis**, and **Large Language Models** to provide comprehensive feedback on performance.

## 🚀 Features

- **Real-time Video Analysis**: Tracks eye contact and emotion detection using MediaPipe and OpenCV.
- **Speech Analytics**: Measures speaking speed (Words Per Minute), filler word count, and speech clarity.
- **Interactive AI Coaching**: Leverages Google Gemini AI to evaluate answer quality and provide personalized feedback.
- **Detailed Performance Reports**: Provides a weighted scorecard (Content 50%, Vision 30%, Speech 20%) with specific improvement tips.
- **Interview History**: Track your progress over multiple sessions.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend Logic**: Python
- **Computer Vision**: OpenCV, MediaPipe
- **Natural Language Processing**: Google Generative AI (Gemini)
- **Database**: SQLite (SQLAlchemy)
- **Audio Processing**: PyAudio, SpeechRecognition

## 📋 Prerequisites

- Python 3.8+
- A Google Gemini API Key

## ⚙️ Setup & Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd prep-pro
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**:
    Create a `.env` file in the root directory and add your Google Gemini API key:
    ```env
    GEMINI_API_KEY="your_api_key_here"
    ```

4.  **Run Database Migrations**:
    ```bash
    python migrate_db.py
    ```

5.  **Start the Application**:
    ```bash
    streamlit run app.py
    ```
    *(Or `python -m streamlit run app.py` if the command is not in your PATH)*

## 📂 Project Structure

- `app.py`: Main entry point for the Streamlit application.
- `src/`: Core logic and components.
  - `vision/`: Video processing and facial analysis.
  - `speech/`: Audio recording and transcription.
  - `nlp/`: Answer evaluation and feedback generation.
  - `ui/`: Custom Streamlit components and styling.
  - `utils/`: Authentication, database, and helper functions.
- `data/`: Storage for database and session files.
- `migrate_db.py`: Database schema management script.

## 📜 License

This project is licensed under the MIT License.
