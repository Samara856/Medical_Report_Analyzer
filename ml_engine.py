REFERENCE_RANGES = {
    'glucose': (70, 140),
    'cholesterol': (125, 200),
    'hemoglobin': (13.5, 17.5),
}

def parse_medical_text(text):
    values = {}
    lines = text.lower().split("\n")
    for line in lines:
        if "glucose" in line:
            values['glucose'] = extract_value(line)
        elif "cholesterol" in line:
            values['cholesterol'] = extract_value(line)
        elif "hemoglobin" in line:
            values['hemoglobin'] = extract_value(line)
    return values

def extract_value(text):
    for part in text.split():
        try:
            return float(part)
        except:
            continue
    return 0

def detect_anomalies(values):
    alerts = {}
    for key, value in values.items():
        low, high = REFERENCE_RANGES.get(key, (0, 999))
        if value < low:
            alerts[key] = 'Low'
        elif value > high:
            alerts[key] = 'High'
        else:
            alerts[key] = 'Normal'
    return alerts
