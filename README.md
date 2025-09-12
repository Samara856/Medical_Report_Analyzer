# 🩺 Smart Medical Report Analyzer  

[![Flask](https://img.shields.io/badge/Flask-2.0+-blue.svg)](https://flask.palletsprojects.com/)  
[![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)  
[![OCR](https://img.shields.io/badge/OCR-Tesseract-green.svg)](https://github.com/tesseract-ocr/tesseract)  
[![Render](https://img.shields.io/badge/Deployed%20on-Render-purple.svg)](https://render.com/)  

👉 **Live Demo:** [Smart Medical Report Analyzer](https://medical-report-analyzer-2-20m7.onrender.com)  

---

## 📖 About the Project  
**Smart Medical Report Analyzer** is a lightweight and intelligent web application designed to make medical reports easy to understand.  
Many patients find it difficult to interpret lab values in their reports — this tool automatically extracts results using **OCR (Optical Character Recognition)** and compares them with reference ranges to provide clear insights.  

✨ With just a simple upload, users can instantly know whether their test results are **Normal, High, or Low**.  
It saves time, reduces confusion, and empowers patients to take better care of their health.  

---

## ✨ Features  
- 📂 Upload scanned medical reports (images or PDFs)  
- 🔍 Extract text and lab values using **Tesseract OCR**  
- ⚖️ Compare values with standard medical ranges  
- 📊 Instant health insights (Normal / High / Low)  
- 💻 Clean, lightweight, and responsive web interface  
- 🌐 Fully deployed and accessible online  

---

## 🛠️ Tech Stack  
- **Backend**: Python (Flask)  
- **OCR Engine**: Tesseract OCR  
- **Frontend**: HTML, CSS, JavaScript (Jinja2 templates)  
- **Deployment**: Render  

---

## 🚀 Getting Started  

Follow these steps to run the project locally:  

### 1️⃣ Clone the Repository  

bash
git clone https://github.com/Samara856/[smart-medical-report-analyzer](https://github.com/Samara856/Medical_Report_Analyzer)
cd smart-medical-report-analyzer

2️⃣ Create Virtual Environment & Install Dependencies

bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate

pip install -r requirements.txt

3️⃣ Run the App

bash
python app.py

🔮 Future Improvements

🤖 Machine Learning model for predictive medical analysis
☁️ Cloud storage for past medical records
📱 Dedicated mobile app for patients
