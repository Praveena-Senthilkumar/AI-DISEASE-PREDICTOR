def categorize_age(age):
    try:
        age = int(age)
        if age < 1:
            return "Calf"
        elif age <= 3:
            return "Growing"
        elif 3 < age <= 8:
            return "Adult"
        else:
            return "Senior"
    except:
        return "Unknown"
