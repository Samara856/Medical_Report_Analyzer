def get_lifestyle_tips(alerts):
    tips = []
    if alerts.get('glucose') == 'High':
        tips.append("🩺 Reduce sugar intake and include 30 minutes of walking.")
    if alerts.get('cholesterol') == 'High':
        tips.append("🩺 Avoid oily food; eat oats and do daily cardio.")
    if alerts.get('hemoglobin') == 'Low':
        tips.append("🩺 Eat spinach, red meat, and citrus fruits.")
    return tips
