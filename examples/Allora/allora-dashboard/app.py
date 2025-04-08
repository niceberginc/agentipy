import os
import asyncio
from threading import Thread
from flask import Flask, render_template, jsonify
from agentipy.agent import SolanaAgentKit
from agentipy.tools.use_allora import (
    AlloraManager,
    PriceInferenceToken,
    PriceInferenceTimeframe,
    ChainSlug
)

app = Flask(__name__)

loop = asyncio.new_event_loop()
agent = None
allora = None

def run_async_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

Thread(target=run_async_loop, daemon=True).start()

async def initialize_allora():
    global agent, allora
    try:
        api_key = os.getenv('ALLORA_API_KEY', 'Your_allora_API')
        
        # Validate API key format
        if not api_key.startswith('UP-'):
            raise ValueError("Invalid API key format. Must start with 'UP-'")
        
        agent = SolanaAgentKit(allora_api_key=api_key)
        chain = ChainSlug.MAINNET if os.getenv("ALLORA_ENV", "MAINNET").upper() == "MAINNET" else ChainSlug.TESTNET
        allora = AlloraManager(agent=agent, chain=chain)
        print("Allora initialized successfully")
    except Exception as e:
        print(f"Initialization failed: {str(e)}")

loop.call_soon_threadsafe(lambda: asyncio.ensure_future(initialize_allora()))

# JSON error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict/<asset>/<timeframe>')
async def get_prediction(asset, timeframe):
    if not allora:
        return jsonify({
            "status": "error",
            "message": "Service initializing, please try again later"
        }), 503
        
    try:
        token = PriceInferenceToken[asset.upper()]
        timeframe_enum = PriceInferenceTimeframe[timeframe.upper()]
        result = await allora.get_price_prediction(token, timeframe_enum)
        return jsonify({
            "status": "success",
            "asset": asset.upper(),
            "timeframe": timeframe,
            "data": result
        })
    except KeyError:
        return jsonify({
            "status": "error",
            "message": f"Invalid asset or timeframe. Use: {[e.name for e in PriceInferenceToken]} and {[e.name for e in PriceInferenceTimeframe]}"
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/topics')
async def get_topics():
    if not allora:
        return jsonify({
            "status": "error",
            "message": "Service initializing, please try again later"
        }), 503
        
    try:
        response = await allora.get_all_topics()
        return jsonify({
            "status": "success",
            "topics": response.get('topics', [])[:3]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
