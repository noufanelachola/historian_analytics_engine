import re
import pandas as pd

asset_types = {
    "FIT": "Flow Indicator Transmitter",
    "LIT": "Level Indicator Transmitter",
    "AIT": "Analyzer Indicator Transmitter",
    "PIT": "Pressure Indicator Transmitter",
    "DPIT": "Differential Pressure Indicator Transmitter",
    "MV": "Motorized Valve",
    "P": "Pump",
    "UV": "UV Disinfection Unit"
}

def is_actuator(asset):
    info = classify_asset(asset)

    return info["asset_type"] in [
        "Pump",
        "Motorized Valve"
    ]

def classify_asset(asset):
    asset_info = get_asset_info(asset)

    asset_name = asset_info["prefix"]
    asset_number = asset_info["number"]

    asset_type = asset_types.get(asset_name, "Unknown Asset Type")

    # The first digit of the asset number indicates the stage of the asset 
    asset_stage = int(asset_number[0])

    return {
        "asset": asset,
        "asset_name": asset_name,
        "asset_type": asset_type,
        "asset_number": asset_number,   
        "asset_stage": asset_stage,
    }

def get_asset_info(asset):
    match = re.match(r"([A-Z]+)(\d+)", asset)

    if match:
        return {
            "prefix": match.group(1),
            "number": match.group(2)
        }

    return None

def save_asset_classification(assets_info, path):
    inventory = pd.DataFrame({
        "S.no": range(1, len(assets_info) + 1),
        "Asset": assets_info
    })

    inventory.to_csv(path, index=False)