import requests
from agentipy.agent import SolanaAgentKit

# Send a request to the Block engine url using the JSON RPC methods 
def __send_request(agent: SolanaAgentKit, endpoint, method, params=None):
    if endpoint == None:
        return "Error: Please enter a valid endpoint."

    if agent.jito_uuid == None:
        headers = {
            'Content-Type': 'application/json', 
            "accept": "application/json"
        }
    else:
        headers = {
            'Content-Type': 'application/json', 
            "accept": "application/json",
            "x-jito-atuh": agent.jito_uuid
        }
    data = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": method,
        "params": [params]
    }

    print(data)
    try:
        resp = requests.post(agent.url + endpoint, headers=headers, json=data)
        resp.raise_for_status()
        return {"success": True, "data": resp.json()}
    except requests.exceptions.HTTPError as errh:
        return {"success": False, "error": f"HTTP Error: {errh}"}
    except requests.exceptions.ConnectionError as errc:
        return {"success": False, "error": f"Error Connecting: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"success": False, "error": f"Timeout Error: {errt}"}
    except requests.exceptions.InvalidHeader as err:
        return {"success": False, "error": f"Invalid Header error: {err}"}
    except requests.exceptions.InvalidURL as err:
        return {"success": False, "error": f"InvalidURL error: {err}"}
    except requests.exceptions.RequestException as err:
        return {"success": False, "error": f"An error occurred: {err}"}
