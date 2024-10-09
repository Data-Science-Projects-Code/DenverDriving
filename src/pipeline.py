import pandas as pd

# List of values to replace directly in the code for simplicity
VALUES_TO_REPLACE = [
    "0",
    "00",
    " 00",
    "  00",
    "01",
    "02",
    "03",
    "05",
    " 06",
    "07",
    "17",
    "18",
    "021",
    "91",
    "Na",
    "na",
    "/",
    " ",
    "--",
    "-",
]


def load_data():
    """Attempts to load data from various sources with a fallback to an empty DataFrame."""
    file_paths = [
        "../data/traffic_accidents.csv",
        # "../data/traffic_accidents.parquet",
        # "/kaggle/input/denver-traffic-accidents/denver_accidents.parquet",
        # "/kaggle/input/denver-traffic-accidents/traffic_accidents.csv",
    ]

    for path in file_paths:
        try:
            if path.endswith(".parquet"):
                return pd.read_parquet(path), f"Parquet file loaded from {path}"
            elif path.endswith(".csv"):
                return pd.read_csv(
                    path, low_memory=False
                ), f"CSV file loaded from {path}"
        except FileNotFoundError:
            continue

    return pd.DataFrame(), "File not found. Returning empty DataFrame."


def format_column_names(df):
    """Converts column names to Title_Snake_Case format."""
    df.columns = [
        "_".join(word.capitalize() for word in col.split("_")) for col in df.columns
    ]
    return df


def drop_unused_columns(df):
    """Drops columns that are not useful for analysis."""
    unused_columns = [
        "Object_Id",
        "Last_Occurrence_Date",
        "Geo_X",
        "Geo_Y",
        "Point_X",
        "Point_Y",
        "X",
        "Y",
    ]
    return df.drop(unused_columns, axis=1, errors="ignore")


def convert_to_datetime(df):
    """Converts columns containing 'Date' in their name to datetime format."""
    date_cols = [col for col in df.columns if "Date" in col]
    for col in date_cols:
        df[col] = pd.to_datetime(
            df[col], format="%m/%d/%Y %I:%M:%S %p", errors="coerce"
        )
    return df


def clean_data(df):
    """Performs data cleaning operations on specific columns."""
    df.dropna(subset=["Geo_Lon", "Geo_Lat"], axis=0, inplace=True)
    df["Top_Traffic_Accident_Offense"] = (
        df["Top_Traffic_Accident_Offense"].str.rstrip().replace("TRAF - ", "")
    )
    return df


def fix_missing_data(df, number_cols, text_cols):
    """Handles missing values and incorrect entries in the data."""
    # Fill missing values in numerical columns
    df[number_cols] = df[number_cols].fillna(-1)

    # Fill missing values and handle special cases in text columns
    df[text_cols] = (
        df[text_cols]
        .fillna("Data Misentered")
        .replace(r"^\s*$", "Data Misentered", regex=True)
    )
    df[text_cols] = df[text_cols].replace(VALUES_TO_REPLACE, "Data Misentered")
    return df


def column_contents_to_title_case(df, columns):
    """Converts the contents of specified columns to title case."""
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title()
    return df


def convert_columns_to_category(df, category_cols):
    """Converts specified columns to categorical data type."""
    df[category_cols] = df[category_cols].astype("category")
    return df


def main():
    df, load_message = load_data()
    print(load_message)

    df = (
        df.pipe(format_column_names)
        .pipe(drop_unused_columns)
        .pipe(convert_to_datetime)
        .pipe(clean_data)
    )

    number_cols = df.select_dtypes(include=["int", "float"]).columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()

    df = fix_missing_data(df, number_cols, text_cols)

    title_case_cols = [col for col in text_cols if "Id" not in col]
    df = column_contents_to_title_case(df, title_case_cols)

    additional_cols = [
        "Offense_Code",
        "Offense_Code_Extension",
        "Precinct_Id",
        "Bicycle_Ind",
        "Pedestrian_Ind",
        "Seriously_Injured",
        "Fatalities",
    ]

    to_categorical = [
        col for col in text_cols if col not in text_cols[1:2]
    ] + additional_cols
    df = convert_columns_to_category(df, to_categorical)

    # Convert specified columns to float32 for optimized storage
    df = df.astype(
        {"Incident_Id": "float32", "Geo_Lon": "float32", "Geo_Lat": "float32"}
    )

    # Save the processed DataFrame to a parquet file
    df.to_parquet("../data/denver_accidents.parquet")


if __name__ == "__main__":
    main()
