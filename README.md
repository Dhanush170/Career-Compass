# 🧭 Career Compass

**Career Compass** is a full-stack AI application that bridges the gap between human potential and algorithmic gatekeepers. It doesn't just grade resumes; it provides a comprehensive career intelligence analysis, including ATS scoring, role fit prediction, and personalized upskilling paths.

## 🚀 Key Features

  * **Hybrid Scoring Engine:** Combines KEYBERT (Math) & Gemini 2.5 (Cognitive) for accurate scoring.
  * **Gap Analysis:** Identifies missing hard skills vs. "noise"
  * **Automated Upskilling:** Generates tailored learning paths and resume bullet point boosters.
  * **Mega-Prompt Architecture:** Optimized backend for single-pass analysis (No rate limits).

## 🛠️ Tech Stack

  * **Frontend:** React.js, Tailwind CSS, Lucide Icons
  * **Backend:** FastAPI, Python, Uvicorn
  * **AI Models:** Google Gemini 2.5 Flash, SBERT, KeyBERT, LLMWhisperer

-----

## ⚡ Quick Start Guide

Follow these steps to set up the project locally.

### 1\. Prerequisites

  * Python 3.9+
  * Node.js & npm
  * API Keys for **Google Gemini** and **Unstract LLMWhisperer**.

### 2\. Clone the Repository

```bash
git clone https://github.com/Dhanush170/career-compass.git
cd career-compass
```

### 3\. Backend Setup

Open a terminal and navigate to the backend folder:

```bash
cd backend
```

**Create and Activate Virtual Environment:**

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**Install Dependencies:**

```bash
pip install -r requirements.txt
```

**Configure Secrets:**
Create a `.env` file inside the `backend/` folder and add your keys:

```ini
GOOGLE_API_KEY="your_google_api_key_here"
LLMWHISPERER_API_KEY="your_llmwhisperer_key_here"
```

**Start the Server:**

```bash
uvicorn app.main:app --reload
# Server runs on http://127.0.0.1:8000
```

### 4\. Frontend Setup

Open a **new terminal** and navigate to the frontend folder:

```bash
cd frontend
```

**Install Dependencies:**

```bash
npm install
```

**Start the React App:**

```bash
npm run dev
# App runs on http://localhost:5173
```

-----

## 🏃‍♂️ Usage

1.  Open `http://localhost:5173` in your browser.
2.  Paste a **Job Description (JD)** in the left box.
3.  Upload your **Resume (PDF)** in the right box.
4.  Click **"Analyze My Fit"**.

