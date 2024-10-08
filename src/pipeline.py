import pandas as pd
from datetime import time

df = pd.read_csv("../data/traffic_accidents.csv", low_memory=False)

df.columns = [
    "_".join(word.capitalize() for word in col.split("_")) for col in df.columns
]

df.drop(
    ["Last_Occurrence_Date", "Point_X", "Point_Y", "Geo_X", "Geo_Y", "X", "Y"],
    axis=1,
    inplace=True,
)

date_cols = [col for col in df.columns if "Date" in col]

int_cols = [col for col in df.select_dtypes(include="int64").columns]

cat_cols = [
    "Offense_Code",
    "Offense_Code_Extension",
    "Top_Traffic_Accident_Offense",
    "District_Id",
    "Precinct_Id",
    "Bicycle_Ind",
    "Pedestrian_Ind",
    "Harmful_Event_Seq_1",
    "Harmful_Event_Seq_2",
    "Harmful_Event_Seq_3",
    "Road_Location",
    "Road_Description",
    "Road_Contour",
    "Road_Condition",
    "Light_Condition",
    "Tu1_Vehicle_Type",
    "Tu1_Travel_Direction",
    "Tu1_Vehicle_Movement",
    "Tu1_Driver_Action",
    "Tu1_Driver_Humancontribfactor",
    "Tu1_Pedestrian_Action",
    "Tu2_Vehicle_Type",
    "Tu2_Travel_Direction",
    "Tu2_Vehicle_Movement",
    "Tu2_Driver_Action",
    "Tu2_Driver_Humancontribfactor",
    "Tu2_Pedestrian_Action",
    "Seriously_Injured",
    "Fatality_Mode_1",
    "Fatality_Mode_2",
    "Seriously_Injured_Mode_1",
    "Seriously_Injured_Mode_2",
]

for col in date_cols:
    df[col] = pd.to_datetime(df[col], format="%m/%d/%Y %I:%M:%S %p")

for col in int_cols:
    df[col] = df[col].astype("int32")

for col in cat_cols:
    df[col] = df[col].astype("category")

df["Fatalities"] = pd.to_numeric(df["Fatalities"], errors="coerce")

# Overwrite NaNs
field_not_entered_cols = [
    "Seriously_Injured_Mode_1",
    "Seriously_Injured_Mode_2",
    "Tu1_Pedestrian_Action",
    "Tu2_Vehicle_Type",
    "Tu2_Travel_Direction",
    "Tu2_Vehicle_Movement",
    "Tu2_Driver_Action",
    "Tu2_Driver_Humancontribfactor",
    "Tu2_Pedestrian_Action",
]
pending_investigation_cols = [
    "Fatality_Mode_1",
    "Fatality_Mode_2",
    "Tu1_Vehicle_Movement",
    "Incident_Address",
    "Road_Location",
    "Road_Condition",
]
minus_one_cols = ["Bicycle_Ind", "Pedestrian_Ind"]

df[field_not_entered_cols] = df[field_not_entered_cols].fillna("Field Not Entered")

# df[pending_investigation_cols] = df[pending_investigation_cols].fillna(
#     "Pending Investigation and/or Court Hearing"
# )
# df[minus_one_cols] = df[minus_one_cols].fillna(-1).astype("int32")

# df.to_parquet("../data/denver_accidents.parquet")
