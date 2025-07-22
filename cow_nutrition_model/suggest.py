import pandas as pd
from .utils import categorize_age
from .nutrition_rules import nutrition_map

# Load CSV once
df = pd.read_csv("cow_nutrition_model/nutrition_dataset.csv")

def get_nutrition_advice(breed, age, stage):
    age_group = categorize_age(age)

    # Try dataset first
    match = df[
        (df["breed"].str.lower() == breed.lower()) &
        (df["age_group"].str.lower() == age_group.lower()) &
        (df["stage"].str.lower() == stage.lower())
    ]

    if not match.empty:
        row = match.iloc[0]
        return {
            "nutrition": row["nutrition"],
            "food": row["food"],
            "supplements": row["supplements"],
            "remedies": row["remedies"],
            "follow_up": row["follow_up"]
        }

    # Fallback to rule-based
    rules = nutrition_map.get(stage) or nutrition_map.get(age_group)
    return rules if rules else {"nutrition": "No data found."}
