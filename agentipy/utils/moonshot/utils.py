import json
import logging
import time

import requests
from solana.rpc.api import Client
from solders.signature import Signature

from agentipy.agent import SolanaAgentKit

logger = logging.getLogger(__name__)

def find_data(data, field):
    if isinstance(data, dict):
        if field in data:
            return data[field]
        else:
            for value in data.values():
                result = find_data(value, field)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = find_data(item, field)
            if result is not None:
                return result
    return None

def get_token_balance(agent:SolanaAgentKit, pub_key: str, token: str):
    try:

        headers = {"accept": "application/json", "content-type": "application/json"}

        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "getTokenAccountsByOwner",
            "params": [
                pub_key,
                {"mint": token},
                {"encoding": "jsonParsed"},
            ],
        }
        
        response = requests.post(agent.rpc_url, json=payload, headers=headers)
        ui_amount = find_data(response.json(), "uiAmount")
        return float(ui_amount)
    except Exception as e:
        return None

def confirm_txn(agent:SolanaAgentKit ,txn_sig, max_retries=20, retry_interval=3):
    retries = 0
    client = Client(agent.rpc_url)
    if isinstance(txn_sig, str):
        txn_sig = Signature.from_string(txn_sig)
    while retries < max_retries:
        try:
            txn_res = client.get_transaction(txn_sig, encoding="json", commitment="confirmed", max_supported_transaction_version=0)
            txn_json = json.loads(txn_res.value.transaction.meta.to_json())
            if txn_json['err'] is None:
                logger.info(f"Transaction confirmed... try count: {retries+1}")
                return True
            logger.error("Error: Transaction not confirmed. Retrying...")
            if txn_json['err']:
                logger.error("Transaction failed.")
                return False
        except Exception as e:
            logger.info(f"Awaiting confirmation... try count: {retries+1}" )
            retries += 1
            time.sleep(retry_interval)
    logger.error("Max retries reached. Transaction confirmation failed.")
    return None