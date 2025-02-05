import requests

from agentipy.utils.stork.constants import STORK_HTTPS_ENDPOINT


def get_stork_price(asset_id: str, api_token: str):
    url = f"{STORK_HTTPS_ENDPOINT}/v1/prices/latest/?assets={asset_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Basic {api_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {
            "error": str(e)
        }
    
