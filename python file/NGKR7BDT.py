# child_mortality_pipeline.py

import pandas as pd

# ---------------------------
# STEP 1: Load the DHS dataset
# ---------------------------
file_path = "C:\\Users\\PIFFMAN\\Desktop\\synthetic_child_mortality\\NGKR7BDT\\NGKR7BFL.DTA"  # Update with your file path
 
print("📂 Loading DHS Children’s Recode dataset...")
df = pd.read_stata(file_path, convert_categoricals=False)
print("✅ File loaded successfully. Shape:", df.shape)

# ---------------------------
# STEP 2: Extract key variables
# ---------------------------
columns_needed = {
    "caseid": "household_id",    # Household identifier
    "b5": "child_alive",         # Survival status (1 = alive, 0 = dead)
    "b7": "age_at_death",        # Age at death in months (if dead)
    "b19": "age_at_survey",      # Age at survey in months (if alive)
    "v025": "residence",         # Residence type (1 = urban, 2 = rural)
    "v190": "wealth_index",      # Wealth quintile (1 = poorest ... 5 = richest)
    "v106": "mother_education",  # Education level (0 = none, 1 = primary, 2 = secondary, 3 = higher)
    "v012": "mother_age",        # Mother’s age
    "v024": "region"             # Region / geopolitical zone
}

df = df[list(columns_needed.keys())].rename(columns=columns_needed)

# ---------------------------
# STEP 3: Recode variables
# ---------------------------
# Event variable: 1 = child died, 0 = alive
df["event"] = df["child_alive"].apply(lambda x: 0 if x == 1 else 1)

# Time variable: if dead → age at death, if alive → age at survey
df["time"] = df.apply(
    lambda row: row["age_at_death"] if row["event"] == 1 else row["age_at_survey"],
    axis=1
)


# Residence mapping
df["area"] = df["residence"].map({1: "Urban", 2: "Rural"})

# Wealth mapping
wealth_map = {1: "Poorest", 2: "Poorer", 3: "Middle", 4: "Richer", 5: "Richest"}
df["wealth"] = df["wealth_index"].map(wealth_map)

# Education mapping
edu_map = {0: "None", 1: "Primary", 2: "Secondary", 3: "Higher"}
df["education"] = df["mother_education"].map(edu_map)

# ---------------------------
# STEP 4: Save cleaned dataset
# ---------------------------
df_clean = df[[
    "household_id", "time", "event", "area", "wealth", 
    "education", "mother_age", "region"
]]

df_clean.to_csv("child_mortality_f.csv", index=False)
print("✅ Clean dataset saved as child_mortality_f.csv")

# ---------------------------
# STEP 5: Summary Statistics
# ---------------------------
print("\n📊 Summary Statistics:")
print("Sample size N:", len(df_clean))
print("Event counts:\n", df['event'].value_counts())
print("Total deaths recorded:", df_clean['event'].sum())
print("Overall death rate (%):", round(df_clean['event'].mean() * 100, 2))
print("\nNeonatal deaths (time=0 & event=1):", ((df['event']==1) & (df['time']==0)).sum())
print("\nTime summary:\n", df['time'].describe())
print("\nUrban/Rural distribution:\n", df['area'].value_counts())
print("\nDeaths by Urban/Rural:\n", df.groupby('area')['event'].mean())
print("\nDeaths by Wealth quintile:\n", df.groupby('wealth')['event'].mean())
print("\nDeaths by Area:")
print(df_clean.groupby("area")["event"].sum())
print("\nDeaths by Wealth Quintile:")
print(df_clean.groupby("wealth")["event"].sum())
print("\nDeaths by Mother’s Education:")
print(df_clean.groupby("education")["event"].sum())
print("\nDeaths by Region:")
print(df_clean.groupby("region")["event"].sum())
