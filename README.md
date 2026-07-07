🤖 AI Career Advisor

An AI-powered Career Advisor built with Python, Flask, and the Groq API that helps users discover the most suitable careers in the computer science and technology field. The chatbot asks users about their interests, skills, education, and experience, then provides personalized career recommendations with compatibility percentages, required skills, learning paths, and expected salary ranges.

✨ Features
💬 Interactive AI conversation
🎯 Personalized career recommendations
📊 Career match percentage
💻 Focused on Computer Science & IT careers
📚 Suggests skills and technologies to learn
💰 Provides estimated salary ranges
⚡ Powered by the Groq Llama 3.3 model
🌐 Simple Flask web interface
🔒 Secure API key management using .env
🛠️ Tech Stack
Python
Flask
Flask-CORS
Groq API
python-dotenv
HTML, CSS & JavaScript
🚀 How It Works
The AI asks users about their interests, skills, education, and experience.
It analyzes the responses using the Groq LLM.
It recommends 2–3 computer-related career paths with:
Career match percentage
Job description
Skills to learn
Estimated salary range
Users receive concise and personalized career guidance.
📦 Installation
git clone https://github.com/yourusername/ai-career-advisor.git
cd ai-career-advisor

pip install -r requirements.txt

# Create a .env file
GROQ_API_KEY=your_api_key_here

python app.py
