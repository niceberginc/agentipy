import asyncio
from agentipy.tools.use_pyth import PythManager

PYTH_FEEDS = {
    "SOL/USD": "H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG",
    "BTC/USD": "GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU",
    "AAVE/USD": "3wDLxH34Yz8tGjwHszQ2MfzHwRoaQgKA32uq2bRpjJBW",
    "AEVO/USD": "26emwftTvy4CcXUcPYCHF9PcPHar4kYKfzwM1onYHBCN"
}

async def fetch_all():
    async def one(symbol, addr):
        data = await PythManager.get_price(addr)
        if data["status"] == "TRADING":
            print(f"{symbol}: ${data['price']:.4f} ±${data['confidence_interval']:.4f}")
        else:
            print(f"{symbol}: {data['status']} — {data.get('message','')}")
    await asyncio.gather(*(one(s, a) for s, a in PYTH_FEEDS.items()))

if __name__ == "__main__":
    asyncio.run(fetch_all())
