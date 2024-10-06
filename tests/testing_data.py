# Pytest tests
def test_data_years():
    df = pd.read_csv("../data/traffic_accidents.csv")
    df["date"] = pd.to_datetime(df["date"])
    min_year = df["date"].min().year
    max_year = df["date"].max().year
    assert (max_year - min_year) > 11, "Data does not span more than 11 years"


def test_data_rows():
    df = pd.read_csv("../data/traffic_accidents.csv")
    assert len(df) > 240000, "Data does not have more than 240,000 rows"
