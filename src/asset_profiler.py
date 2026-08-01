import pandas as pd 

def profile_asset(df, asset):
    series = df[asset]
    unique_count = series.nunique()

    if unique_count <= 5:
        category = "Digital"
    else : 
        category = "Analog"


    if category == "Analog":
        profile = analog_profiler(series)
    else:
        profile = digital_profiler(series)

    profile["asset"] = asset

    return profile

def analog_profiler(series):
    return {
        "category": "Analog",
        "min": series.min(),
        "max": series.max(),
        "mean": series.mean(),
        "median": series.median(),
        "std": series.std(),
        "unique_count": series.nunique(),
    } 

def digital_profiler(series):
    return {
        "category": "Digital",
        "unique_count": series.nunique(),
        "state_counts": series.value_counts().to_dict()
    }


