import asyncio
from agentipy.agent import SolanaAgentKit
from agentipy.tools.get_tps import SolanaPerformanceTracker

async def main():
    agent = SolanaAgentKit(private_key="")

    tracker = SolanaPerformanceTracker(agent)

    print("\n Fetching Solana TPS samples...\n")
    for _ in range(3):  # Collect 3 samples
        metric = await tracker.record_latest_metrics()
        print(f" Current TPS: {metric.transactions_per_second:.2f} tx/s")
        await asyncio.sleep(2)  

    avg_tps = tracker.calculate_average_tps()
    max_tps = tracker.find_maximum_tps()

    print("\n Performance Summary:")
    print(f" Average TPS: {avg_tps:.2f}")
    print(f" Max TPS:     {max_tps:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
