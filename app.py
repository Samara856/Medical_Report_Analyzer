from flask import Flask, render_template, request, flash, redirect, url_for
import re
from ocr_utils import extract_text_from_image

app = Flask(__name__)
app.secret_key = "dev"

reference_ranges = {
    'haemoglobin_g_dl': (12, 16),
    'glucose_mg_dl': (70, 140),
    'hba1c_pct': (4, 5.6),
    'urea_mg_dl': (7, 20),
    'creatinine_mg_dl': (0.6, 1.3),
    'total_cholesterol_mg_dl': (125, 200),
    'hdl_mg_dl': (40, 60),
    'ldl_mg_dl': (0, 100),
    'triglyceride_mg_dl': (0, 150),
    'hemoglobin_g_dl': (12, 16),
    'rbc_million_ul': (4.2, 6.1),
    'wbc_10e3_ul': (4.5, 11),
    'platelet_10e3_ul': (150, 450),
    'esr_mm_hr': (0, 20),
    'crp_mg_l': (0, 5),
    'sodium_meq_l': (135, 145),
    'potassium_meq_l': (3.5, 5.1),
    'chloride_meq_l': (98, 107),
    'calcium_mg_dl': (8.5, 10.5),
    'bilirubin_total_mg_dl': (0.1, 1.2),
    'S.ALT(SGPT)': (7, 56),
    'ast_u_l': (10, 40),
    'alp_u_l': (44, 147),
    'ggt_u_l': (9, 48),
    'iron_ug_dl': (60, 170),
    'ferritin_ng_ml': (12, 300),
    'vitamin_d_ng_ml': (20, 50),
    'tsh_uiu_ml': (0.4, 4.0),
    'ft4_ng_dl': (0.7, 1.9),
    'b12_pg_ml': (200, 900),
    'uric_acid_mg_dl': (3.5, 7.2),
    'neutrophils_pct': (40, 60),        
    'lymphocytes_pct': (20, 40),     
    'monocytes_pct': (2, 8),            
    'eosinophils_pct': (1, 4),           
    'basophils_pct': (0, 1),
    'platelet_count_10e3_ul': (150, 450), 
    'mpv_fl': (7.5, 11.5),  
    'pcv_pct': (36, 50),
}

patterns = {
    'haemoglobin_g_dl': r'\b(?:haemoglobin|hb|hgb)\b[:\-]?\s*(\d{1,2}(?:\.\d+)?)',
    'glucose_mg_dl': r'glucose[:\s]*([\d.]+)',
    'hba1c_pct': r'hba1c[:\s]*([\d.]+)',
    'urea_mg_dl': r'urea[:\s]*([\d.]+)',
    'creatinine_mg_dl': r'creatinine[:\s]*([\d.]+)',
    'total_cholesterol_mg_dl': r'total cholesterol[:\s]*([\d.]+)',
    'hdl_mg_dl': r'hdl[:\s]*([\d.]+)',
    'ldl_mg_dl': r'ldl[:\s]*([\d.]+)',
    'triglyceride_mg_dl': r'triglyceride[:\s]*([\d.]+)',
    'hemoglobin_g_dl': r'hemoglobin[:\s]*([\d.]+)',
    'rbc_million_ul': r'rbc[:\s]*([\d.]+)',
    'wbc_10e3_ul': r'wbc[:\s]*([\d.]+)',
    'platelet_10e3_ul': r'platelet[:\s]*([\d.]+)',
    'esr_mm_hr': r'esr[:\s]*([\d.]+)',
    'crp_mg_l': r'crp[:\s]*([\d.]+)',
    'sodium_meq_l': r'sodium[:\s]*([\d.]+)',
    'potassium_meq_l': r'potassium[:\s]*([\d.]+)',
    'chloride_meq_l': r'chloride[:\s]*([\d.]+)',
    'calcium_mg_dl': r'calcium[:\s]*([\d.]+)',
    'bilirubin_total_mg_dl': r'bilirubin[:\s]*([\d.]+)',
    'S.ALT(SGPT)': r'S\.?ALT\s*\(?\s*SGPT\s*\)?\s*[:\-]?\s*(\d+(?:\.\d+)?)',
    'ast_u_l': r'ast[:\s]*([\d.]+)',
    'alp_u_l': r'alp[:\s]*([\d.]+)',
    'ggt_u_l': r'ggt[:\s]*([\d.]+)',
    'iron_ug_dl': r'iron[:\s]*([\d.]+)',
    'ferritin_ng_ml': r'ferritin[:\s]*([\d.]+)',
    'vitamin_d_ng_ml': r'vitamin d[:\s]*([\d.]+)',
    'tsh_uiu_ml': r'tsh[:\s]*([\d.]+)',
    'ft4_ng_dl': r'ft4[:\s]*([\d.]+)',
    'b12_pg_ml': r'b12[:\s]*([\d.]+)',
    'uric_acid_mg_dl': r'uric acid[:\s]*([\d.]+)',
    'neutrophils_pct': r'neutrophils?\s*[:\-]?\s*(\d{1,2}(?:\.\d+)?)\s*%?', 
    'lymphocytes_pct': r'lymphocytes?\s*[:\-]?\s*(\d{1,2}(?:\.\d+)?)\s*%?',
    'monocytes_pct': r'monocytes?\s*[:\-]?\s*(\d{1,2}(?:\.\d+)?)\s*%?',
    'eosinophils_pct': r'eosinophils?\s*[:\-]?\s*(\d{1,2}(?:\.\d+)?)\s*%?',
    'basophils_pct': r'basophils?\s*[:\-]?\s*(\d{1,2}(?:\.\d+)?)\s*%?',
    'platelet_count_10e3_ul': r'(?:platelet count|total platelet count)\s*[:\-]?\s*(\d{2,4}(?:\.\d+)?)',
    'mpv_fl': r'(?:mpv|mean platelet volume)\s*[:\-]?\s*(\d{1,2}(?:\.\d+)?)',
    'pcv_pct': r'(?:pcv|hct|hematocrit)\s*[:\-]?\s*(\d{1,2}(?:\.\d+)?)\s*%?',
}

def extract_values(text):
    values = {}
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.I)
        if match:
            values[test] = float(match.group(1))
    return values

def interpret_value(test_name, value):
    low, high = reference_ranges.get(test_name, (None, None))
    if low is None or high is None:
        return "Unknown"
    if value < low:
        return "Low"
    elif value > high:
        return "High"
    else:
        return "Normal"

def interpret_all(values):
    return {test: interpret_value(test, val) for test, val in values.items()}

def generate_summary(labels):
    messages = []

    if labels.get('glucose_mg_dl') == 'High' or labels.get('hba1c_pct') == 'High':
        messages.append("Possible diabetes risk detected.")
    elif labels.get('glucose_mg_dl') == 'Low':
        messages.append("Blood sugar is too low (hypoglycemia risk).")

    if labels.get('hemoglobin_g_dl') == 'Low':
        messages.append("Possible anemia detected (low hemoglobin).")
    elif labels.get('hemoglobin_g_dl') == 'High':
        messages.append("High hemoglobin — possible dehydration or lung issue.")

    if labels.get('total_cholesterol_mg_dl') == 'High':
        messages.append("High total cholesterol — increased heart disease risk.")
    elif labels.get('total_cholesterol_mg_dl') == 'Low':
        messages.append("Low total cholesterol — may indicate malnutrition or hyperthyroidism.")

    if labels.get('hdl_mg_dl') == 'Low':
        messages.append("Low HDL cholesterol — bad for heart health (less protective).")
    elif labels.get('hdl_mg_dl') == 'High':
        messages.append("High HDL cholesterol — protective effect for heart.")

    if labels.get('ldl_mg_dl') == 'High':
        messages.append("High LDL cholesterol — bad cholesterol, may clog arteries.")

    if labels.get('triglyceride_mg_dl') == 'High':
        messages.append("High triglycerides — risk factor for heart disease.")

    if labels.get('creatinine_mg_dl') == 'High':
        messages.append("Possible kidney dysfunction (high creatinine).")
    elif labels.get('creatinine_mg_dl') == 'Low':
        messages.append("Low creatinine — may indicate low muscle mass or liver issues.")

    if labels.get('urea_mg_dl') == 'High':
        messages.append("High urea — possible kidney issues or dehydration.")
    elif labels.get('urea_mg_dl') == 'Low':
        messages.append("Low urea — could suggest liver problems or malnutrition.")

    if labels.get('rbc_million_ul') == 'Low':
        messages.append("Low RBC count — may suggest anemia.")
    elif labels.get('rbc_million_ul') == 'High':
        messages.append("High RBC count — possible dehydration or heart/lung condition.")

    if labels.get('wbc_10e3_ul') == 'High':
        messages.append("High WBC count — possible infection or inflammation.")
    elif labels.get('wbc_10e3_ul') == 'Low':
        messages.append("Low WBC count — may indicate immune suppression or bone marrow disorder.")

    if labels.get('platelet_10e3_ul') == 'High':
        messages.append("High platelet count — risk of clotting.")
    elif labels.get('platelet_10e3_ul') == 'Low':
        messages.append("Low platelet count — bleeding risk.")

    if labels.get('esr_mm_hr') == 'High':
        messages.append("High ESR — indicates inflammation or chronic disease.")

    if labels.get('crp_mg_l') == 'High':
        messages.append("High CRP — acute inflammation or infection suspected.")

    if labels.get('bilirubin_total_mg_dl') == 'High':
        messages.append("High bilirubin — possible liver or bile duct issues (jaundice).")

    if labels.get('S.ALT(SGPT)') == 'High' or labels.get('ast_u_l') == 'High':
        messages.append("Elevated liver enzymes — possible liver inflammation or damage.")

    if labels.get('alp_u_l') == 'High':
        messages.append("High ALP — possible liver or bone disorder.")

    if labels.get('ggt_u_l') == 'High':
        messages.append("High GGT — could indicate liver or bile duct problems.")

    if labels.get('iron_ug_dl') == 'Low':
        messages.append("Low iron — may suggest iron-deficiency anemia.")
    elif labels.get('iron_ug_dl') == 'High':
        messages.append("High iron — possible iron overload or hemochromatosis.")

    if labels.get('ferritin_ng_ml') == 'Low':
        messages.append("Low ferritin — suggests depleted iron stores.")
    elif labels.get('ferritin_ng_ml') == 'High':
        messages.append("High ferritin — may indicate inflammation or iron overload.")

    if labels.get('vitamin_d_ng_ml') == 'Low':
        messages.append("Low Vitamin D — risk of bone weakness and immune issues.")

    if labels.get('tsh_uiu_ml') == 'High':
        messages.append("High TSH — potential hypothyroidism.")
    elif labels.get('tsh_uiu_ml') == 'Low':
        messages.append("Low TSH — possible hyperthyroidism.")

    if labels.get('ft4_ng_dl') == 'High':
        messages.append("High FT4 — hyperthyroidism may be present.")
    elif labels.get('ft4_ng_dl') == 'Low':
        messages.append("Low FT4 — suggests hypothyroidism.")

    if labels.get('b12_pg_ml') == 'Low':
        messages.append("Low B12 — possible deficiency causing fatigue or nerve issues.")

    if labels.get('uric_acid_mg_dl') == 'High':
        messages.append("High uric acid — gout or kidney stone risk.")
    elif labels.get('uric_acid_mg_dl') == 'Low':
        messages.append("Low uric acid — uncommon but could indicate liver or kidney issues.")

    if not messages:
        messages.append("All lab values are within normal ranges.")

    return messages

def generate_recommendations(labels):
    tips = []

    if labels.get('glucose_mg_dl') == 'High' or labels.get('hba1c_pct') == 'High':
        tips.append("Reduce intake of sugar, white bread, and processed carbs.")
        tips.append("Walk or exercise at least 30 minutes daily.")
        tips.append("Monitor blood sugar regularly.")
    elif labels.get('glucose_mg_dl') == 'Low':
        tips.append("Eat small, frequent meals with complex carbs.")
        tips.append("Avoid skipping meals and excessive insulin doses.")

    if labels.get('hemoglobin_g_dl') == 'Low' or labels.get('rbc_million_ul') == 'Low':
        tips.append("Eat iron-rich foods: spinach, red meat, lentils.")
        tips.append("Pair iron with Vitamin C for better absorption.")
        tips.append("Consult your doctor for iron supplements if needed.")

    if labels.get('total_cholesterol_mg_dl') == 'High' or labels.get('ldl_mg_dl') == 'High':
        tips.append("Limit fried food, red meat, and full-fat dairy.")
        tips.append("Exercise regularly to boost heart health.")
        tips.append("Include more fiber (vegetables, oats, fruits).")

    if labels.get('hdl_mg_dl') == 'Low':
        tips.append("Eat healthy fats: olive oil, nuts, avocados.")
        tips.append("Quit smoking and increase physical activity.")

    if labels.get('triglyceride_mg_dl') == 'High':
        tips.append("Cut down on sugary drinks and alcohol.")
        tips.append("Increase aerobic exercise and fiber intake.")

    if labels.get('creatinine_mg_dl') == 'High' or labels.get('urea_mg_dl') == 'High':
        tips.append("Stay hydrated with plenty of water.")
        tips.append("Limit high-protein diet if advised by doctor.")
        tips.append("Consult a nephrologist if levels persist.")

    if labels.get('wbc_10e3_ul') == 'High':
        tips.append("Get adequate rest and monitor for signs of infection.")
    elif labels.get('wbc_10e3_ul') == 'Low':
        tips.append("Maintain hygiene to avoid infections.")
        tips.append("Consult a doctor for immune evaluation.")

    if labels.get('platelet_10e3_ul') == 'Low':
        tips.append("Avoid injury-prone activities.")
        tips.append("Eat folate-rich foods (leafy greens).")
    elif labels.get('platelet_10e3_ul') == 'High':
        tips.append("Stay hydrated and avoid smoking.")

    if labels.get('esr_mm_hr') == 'High':
        tips.append("Track symptoms like joint pain, fever.")
        tips.append("Consult a physician for underlying inflammation.")

    if labels.get('crp_mg_l') == 'High':
        tips.append("Focus on an anti-inflammatory diet: berries, fish, leafy greens.")

    if labels.get('bilirubin_total_mg_dl') == 'High':
        tips.append("Avoid alcohol and fatty foods.")
        tips.append("Consult a doctor to evaluate liver function.")

    if labels.get('S.ALT(SGPT)') == 'High' or labels.get('ast_u_l') == 'High' or labels.get('alp_u_l') == 'High' or labels.get('ggt_u_l') == 'High':
        tips.append("Avoid alcohol and unnecessary medications.")
        tips.append("Maintain a liver-friendly diet (low-fat, high-fiber).")

    if labels.get('iron_ug_dl') == 'Low' or labels.get('ferritin_ng_ml') == 'Low':
        tips.append("Eat iron-rich foods and consider supplements.")
    elif labels.get('iron_ug_dl') == 'High' or labels.get('ferritin_ng_ml') == 'High':
        tips.append("Avoid excess red meat and iron supplements.")
        tips.append("Consult for iron overload screening.")

    if labels.get('vitamin_d_ng_ml') == 'Low':
        tips.append("Get 15–20 minutes of sunlight daily.")
        tips.append("Eat fatty fish, eggs, and fortified milk.")
        tips.append("Consider Vitamin D supplements as per doctor's advice.")

    if labels.get('tsh_uiu_ml') == 'High':
        tips.append("Consult an endocrinologist for hypothyroidism.")
        tips.append("Monitor symptoms like fatigue, weight gain.")
    elif labels.get('tsh_uiu_ml') == 'Low':
        tips.append("Screen for hyperthyroidism if symptoms appear.")

    if labels.get('ft4_ng_dl') == 'High':
        tips.append("Monitor symptoms like weight loss, tremors.")
        tips.append("Check for hyperthyroid conditions.")
    elif labels.get('ft4_ng_dl') == 'Low':
        tips.append("Consider thyroid hormone therapy (consult doctor).")

    if labels.get('b12_pg_ml') == 'Low':
        tips.append("Eat meat, eggs, and dairy.")
        tips.append("Vegetarians may need B12 supplements.")

    if labels.get('uric_acid_mg_dl') == 'High':
        tips.append("Limit red meat, seafood, and alcohol.")
        tips.append("Stay well hydrated to flush uric acid.")
    elif labels.get('uric_acid_mg_dl') == 'Low':
        tips.append("Evaluate for underlying causes with your doctor.")

    if labels.get('sodium_meq_l') == 'High':
        tips.append("Limit salty foods and processed snacks.")
        tips.append("Stay hydrated with plenty of water.")
        tips.append("Consult for kidney or adrenal issues.")
    elif labels.get('sodium_meq_l') == 'Low':
        tips.append("Increase safe salt intake (consult doctor).")
        tips.append("Consult for adrenal or kidney evaluation.")

    if labels.get('potassium_meq_l') == 'High':
        tips.append("Avoid potassium-rich foods (bananas, oranges).")
        tips.append("Consult for kidney function evaluation.")
    elif labels.get('potassium_meq_l') == 'Low':
        tips.append("Eat potassium-rich foods (avocado, spinach).")
        tips.append("Consult a doctor for supplementation.")

    if labels.get('chloride_meq_l') == 'High':
        tips.append("Stay hydrated and reduce salty foods.")
        tips.append("Consult for kidney or metabolic issues.")
    elif labels.get('chloride_meq_l') == 'Low':
        tips.append("Monitor for dehydration or vomiting.")
        tips.append("Consult for metabolic evaluation.")

    if labels.get('calcium_mg_dl') == 'High':
        tips.append("Limit calcium supplements and dairy if advised.")
        tips.append("Consult for parathyroid or bone issues.")
    elif labels.get('calcium_mg_dl') == 'Low':
        tips.append("Eat calcium-rich foods (dairy, greens).")
        tips.append("Consider Vitamin D to aid absorption.")

    if labels.get('neutrophils_pct') == 'High':
        tips.append("Monitor for infection or inflammation.")
        tips.append("Consult a doctor if symptoms persist.")
    elif labels.get('neutrophils_pct') == 'Low':
        tips.append("Avoid infections with good hygiene.")
        tips.append("Consult for immune system evaluation.")

    if labels.get('lymphocytes_pct') == 'High':
        tips.append("Monitor for viral infections or leukemia.")
        tips.append("Consult a doctor for further tests.")
    elif labels.get('lymphocytes_pct') == 'Low':
        tips.append("Boost immunity with a balanced diet.")
        tips.append("Consult for immune disorder evaluation.")

    if labels.get('monocytes_pct') == 'High':
        tips.append("Track for chronic infections or inflammation.")
        tips.append("Consult a doctor for evaluation.")
    elif labels.get('monocytes_pct') == 'Low':
        tips.append("Maintain hygiene to prevent infections.")
        tips.append("Consult for bone marrow issues.")

    if labels.get('eosinophils_pct') == 'High':
        tips.append("Check for allergies or parasitic infections.")
        tips.append("Consult a doctor for specific tests.")
    elif labels.get('eosinophils_pct') == 'Low':
        tips.append("Usually not concerning, consult if persistent.")

    if labels.get('basophils_pct') == 'High':
        tips.append("Monitor for allergic reactions or inflammation.")
        tips.append("Consult a doctor for further evaluation.")
    elif labels.get('basophils_pct') == 'Low':
        tips.append("Typically not significant, consult if other issues.")

    if labels.get('mpv_fl') == 'High':
        tips.append("Monitor for inflammation or bone marrow issues.")
        tips.append("Consult a doctor for further tests.")
    elif labels.get('mpv_fl') == 'Low':
        tips.append("Check for bone marrow suppression.")
        tips.append("Consult a doctor for evaluation.")

    if labels.get('pcv_pct') == 'High':
        tips.append("Stay hydrated to manage blood thickness.")
        tips.append("Consult for lung or heart conditions.")
    elif labels.get('pcv_pct') == 'Low':
        tips.append("Eat iron-rich foods (spinach, red meat).")
        tips.append("Consult for anemia evaluation.")

    if all(label == 'Normal' for label in labels.values()):
        tips.append("Great job! Maintain a balanced diet and healthy lifestyle.")
        tips.append("Regular exercise and hydration go a long way.")

    return tips

@app.route('/')
def index():
    result = None
    return render_template('index.html', result=result)

@app.route('/', methods=['POST'])
def upload_report():
    file = request.files.get('report')
    if not file or file.filename == '':
        flash("Please upload a report file.")
        return redirect(url_for('index'))

    text = extract_text_from_image(file)
    if not text or len(text.strip()) == 0:
        flash("Could not extract text from the image. Try a clearer image.")
        return redirect(url_for('index'))

    values = extract_values(text)
    if not values:
        flash("Could not find any lab values in the report.")
        return redirect(url_for('index'))

    labels = interpret_all(values)
    summary = generate_summary(labels)
    recommendations = generate_recommendations(labels)

    result = {
        'values': values,
        'labels': labels,
        'summary': summary,
        'recommendations': recommendations,
    }
    
    return render_template('index.html', result=result)

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/trends')
def trends():
    return render_template('trends.html')

@app.route('/compare')
def compare():
    return render_template('compare.html')

@app.route('/patients')
def patients():
    return render_template('patients.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/reminders')
def reminders():
    return render_template('reminders.html')

@app.route('/treatment-plans')
def treatment_plans():
    return render_template('treatment-plans.html')

@app.route('/references')
def references():
    return render_template('references.html')

@app.route('/dictionary')
def dictionary():
    return render_template('dictionary.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/consult')
def consult():
    return render_template('consult.html')

@app.route('/export')
def export():
    return render_template('export.html')

@app.route('/telemedicine')
def telemedicine():
    return render_template('telemedicine.html')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port, debug=False)
