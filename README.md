# 🩺 Smart Medical Report Analyzer  

![Screenshot](https://github.com/Samara856/Medical_Report_Analyzer/blob/master/Medical%20Report%20Analyzer%20.png)
<p align="center">
  <img src="https://github.com/Samara856/Medical_Report_Analyzer/blob/master/Medical%20Report%20Analyzer%20.png" alt="Logo" width="200" style="border-radius:15px;"/>
</p>




[![Flask](https://img.shields.io/badge/Flask-2.0+-blue.svg)](https://flask.palletsprojects.com/)  
[![Python](https://img.shields.io/badge/Python-3.9+-yellow.svg)](https://www.python.org/)  
[![OCR](https://img.shields.io/badge/OCR-Tesseract-green.svg)](https://github.com/tesseract-ocr/tesseract)  
[![Render](https://img.shields.io/badge/Deployed%20on-Render-purple.svg)](https://render.com/)  

👉 **Live Demo:** [Smart Medical Report Analyzer](https://medical-report-analyzer-2-20m7.onrender.com)  

---

## 📖 About the Project  

**Smart Medical Report Analyzer** is a modern web application designed to help patients and healthcare professionals quickly interpret medical lab reports.  
Manually reading lab results can be confusing and time-consuming. This app leverages **OCR (Optical Character Recognition)** to extract data from scanned reports or images and provides instant insights about test results.  

Key benefits:  
- Automatically identifies whether lab values are **Normal, High, or Low**  
- Reduces human error in interpreting reports  
- Provides a user-friendly interface for both patients and medical staff  
- Saves time and helps users make informed health decisions  

By combining OCR with intelligent analysis, this tool makes understanding medical reports faster, simpler, and more accurate.


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

**Backend:**  
- Python 3.9+  
- Flask (Web Framework)  

**OCR Engine:**  
- Tesseract OCR (Text extraction from images/PDFs)  

**Frontend:**  
- HTML5, CSS3  
- JavaScript  
- Jinja2 Templates (for dynamic content rendering)  

**Database (Optional/Future):**  
- SQLite / PostgreSQL  

**Deployment:**  
- Render.com (Cloud Hosting)  

**Development Tools:**  
- Git & GitHub  
- Visual Studio Code / PyCharm  
- Postman (for API testing, optional)  
 

---

## 🚀 Getting Started  

Follow these steps to run the project locally:  

### 1️⃣ Clone the Repository  

git clone :[ https://github.com/Samara856/[smart-medical-report-analyzer](https://github.com/Samara856/Medical_Report_Analyzer)](https://github.com/Samara856/Medical_Report_Analyzer.git)


### 2️⃣ Create Virtual Environment & Install Dependencies

bash
python -m venv venv

#### On Linux/Mac
source venv/bin/activate

#### On Windows
venv\Scripts\activate

pip install -r requirements.txt

### 3️⃣ Run the App

bash
python app.py

##🔮 Future Improvements

🤖 Machine Learning model for predictive medical analysis
☁️ Cloud storage for past medical records
📱 Dedicated mobile app for patients
