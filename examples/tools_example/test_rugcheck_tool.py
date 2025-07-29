import asyncio
from agentipy.tools.rugcheck import RugCheckManager

TOKEN_MINT = "5GDock6poXmDqPzRsajcRyNfxxXtZhumQuKQcFsmpump"

async def main():
    rugcheck = RugCheckManager() 

    print(f"🔍 Fetching rug check summary for token ({TOKEN_MINT})...\n")

    try:
        summary = await rugcheck.fetch_token_report_summary(TOKEN_MINT)

        print("Token Summary:")
        print(f"Program: {summary.tokenProgram}")
        print(f"Score: {summary.score} (Normalized: {summary.score_normalised})")
        print(f"LP Locked %: {summary.lpLockedPct * 100:.2f}%")

        print("\n Risk Factors:")
        for risk in summary.risks:
            print(f"- [{risk.level.upper()}] {risk.name}: {risk.description} (Score: {risk.score})")

    except Exception as e:
        print(f"Failed to fetch token summary: {e}")

if __name__ == "__main__":
    asyncio.run(main())
