import asyncio
import os
import logging
import json

import httpx
from agentipy.agent import SolanaAgentKit
from agentipy.tools.get_token_data import TokenDataManager
from solders.pubkey import Pubkey
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Type
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get Google API Key
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY is not set. Please export it in your environment.")

# Initialize Gemini 2.0 Flash
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=google_api_key)

# Define the TokenCheck Pydantic model
class TokenMeta(BaseModel):
    name: str | None = Field(default=None)
    symbol: str | None = Field(default=None)
    uri: str | None = Field(default=None)
    mutable: bool | None = Field(default=None)
    updateAuthority: str | None = Field(default=None)

class Token(BaseModel):
    mintAuthority: str | None = Field(default=None)
    supply: int | None = Field(default=None)
    decimals: int | None = Field(default=None)
    isInitialized: bool | None = Field(default=None)
    freezeAuthority: str | None = Field(default=None)

class Risks(BaseModel):
    name: str | None = Field(default=None)
    value: str | None = Field(default=None)
    description: str | None = Field(default=None)
    score: int | None = Field(default=None)
    level: str | None = Field(default=None)

class CreatorToken(BaseModel):
    mint: str | None = Field(default=None)
    marketCap: float | None = Field(default=None)
    createdAt: str | None = Field(default=None)

class TokenCheck(BaseModel):
    tokenProgram: str | None = Field(default=None)
    tokenType: str | None = Field(default=None)
    risks: List[Risks] | None = Field(default=None)
    score: int | None = Field(default=None)
    score_normalised: int | None = Field(default=None)
    tokenMeta: TokenMeta | None = Field(default=None, alias="tokenMeta")
    token: Token | None = Field(default=None)
    fileMeta: Dict[str, Any] | None = Field(default=None)
    markets: List[Dict[str, Any]] | None = Field(default=None)
    totalMarketLiquidity: float | None = Field(default=None)
    totalLPProviders: int | None = Field(default=None)
    totalHolders: int | None = Field(default=None)
    price: float | None = Field(default=None)
    rugged: bool | None = Field(default=None)
    creatorTokens: List[CreatorToken] | None = Field(default=None)
    verification: Optional[Dict[str, Any]] = Field(default=None)
    graphInsidersDetected: int | None = Field(default=None)
    insiderNetworks: Any | None = Field(default=None)
    detectedAt: str | None = Field(default=None)

# RugCheckManager class
class RugCheckManager:
    BASE_URL = "https://api.rugcheck.xyz/v1"
    API_KEY = os.environ.get("RUGCHECK_API_KEY")

    @staticmethod
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def _make_request(method, url, headers=None, params=None, data=None):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(method, url, headers=headers, params=params, data=data)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP Error: {method} {url}: {e.response.status_code} - {e}")
                if e.response and hasattr(e.response, 'text'):
                    logger.error(f"Response text: {e.response.text[:200]}...")
                raise
            except Exception as e:
                logger.error(f"Request failed: {method} {url}: {e}")
                raise

    @staticmethod
    async def fetch_token_report_summary(mint: str) -> TokenCheck:
        headers = {"Authorization": f"Bearer {RugCheckManager.API_KEY}"}
        response = await RugCheckManager._make_request("GET", f"{RugCheckManager.BASE_URL}/tokens/{mint}/report/summary", headers=headers)
        return TokenCheck(**json.loads(response.text))

    @staticmethod
    async def fetch_token_detailed_report(mint: str) -> TokenCheck:
        headers = {"Authorization": f"Bearer {RugCheckManager.API_KEY}"}
        response = await RugCheckManager._make_request("GET", f"{RugCheckManager.BASE_URL}/tokens/{mint}/report", headers=headers)
        return TokenCheck(**json.loads(response.text))

    @staticmethod
    async def fetch_token_lp_lockers(token_id: str) -> dict:
        headers = {"Authorization": f"Bearer {RugCheckManager.API_KEY}"}
        response = await RugCheckManager._make_request("GET", f"{RugCheckManager.BASE_URL}/tokens/{token_id}/lockers", headers=headers)
        return response.json()

    @staticmethod
    async def get_trending_tokens():
        try:
            response = await RugCheckManager._make_request("GET", f"{RugCheckManager.BASE_URL}/stats/trending")
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching trending tokens from RugCheck: {e}")
            return None

# TokenHolderAnalysisTool
class TokenHolderAnalysisTool(BaseTool):
    name: str = "solana_token_holder_analysis"
    description: str = "Analyzes the holder distribution of a Solana token based on total holders."
    agent_kit: SolanaAgentKit

    async def _arun(self, mint: str) -> Dict[str, Any]:
        try:
            detailed_report = await RugCheckManager.fetch_token_detailed_report(mint)
            total_holders = detailed_report.totalHolders

            if total_holders is None:
                return {
                    "status": "error",
                    "message": "Total holders data not available."
                }

            distribution_analysis = {
                "total_holders": total_holders,
                "distribution_note": (
                    "Highly concentrated" if total_holders < 100 else
                    "Moderately distributed" if total_holders < 1000 else
                    "Widely distributed"
                )
            }

            return {
                "status": "success",
                "analysis": distribution_analysis
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _run(self, mint: str) -> Dict[str, Any]:
        raise NotImplementedError("This tool only supports async execution via _arun.")

# SolanaRugCheckTokenReportSummaryTool
class SolanaRugCheckTokenReportSummaryTool(BaseTool):
    name: str = "solana_rugcheck_token_summary"
    description: str = "Fetches a summary report for a Solana token using RugCheck API."
    agent_kit: SolanaAgentKit

    async def _arun(self, mint: str) -> Dict[str, Any]:
        try:
            summary = await RugCheckManager.fetch_token_report_summary(mint)
            return {
                "status": "success",
                "report": summary.model_dump()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _run(self, mint: str) -> Dict[str, Any]:
        raise NotImplementedError("This tool only supports async execution via _arun.")

# Updated SolanaRugCheckTokenDetailedReportTool
class SolanaRugCheckTokenDetailedReportTool(BaseTool):
    name: str = "solana_rugcheck_token_detailed"
    description: str = "Fetches a detailed report for a Solana token using RugCheck API."
    agent_kit: SolanaAgentKit

    async def _arun(self, mint: str) -> Dict[str, Any]:
        try:
            report = await RugCheckManager.fetch_token_detailed_report(mint)
            detailed_data = report.model_dump()

            token_meta = report.tokenMeta or TokenMeta()
            token = report.token or Token()
            creator_tokens = report.creatorTokens or []

            # Calculate market cap, defaulting to 0 if no creator tokens are available
            market_cap = sum(ct.marketCap or 0 for ct in creator_tokens) if creator_tokens else 0
            if not creator_tokens:
                logger.warning(f"No creatorTokens data available for token {mint}. Market cap set to 0.")

            additional_features = {
                "token_name": token_meta.name,
                "symbol": token_meta.symbol,
                "mint_authority": token.mintAuthority,
                "freeze_authority": token.freezeAuthority,
                "score": report.score,
                "rugged_status": report.rugged,
                "market_cap": market_cap,
                "total_holders": report.totalHolders,
                "market_cap_source": "creatorTokens" if creator_tokens else "default (no data)"
            }

            detailed_data.update(additional_features)
            return {
                "status": "success",
                "report": detailed_data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _run(self, mint: str) -> Dict[str, Any]:
        raise NotImplementedError("This tool only supports async execution via _arun.")

# TokenRiskAnalysisTool
class TokenRiskAnalysisTool(BaseTool):
    name: str = "solana_token_risk_analysis"
    description: str = "Uses Gemini 2.0 Flash to generate a human-readable risk analysis based on RugCheck data."
    agent_kit: SolanaAgentKit

    async def _arun(self, mint: str) -> Dict[str, Any]:
        try:
            detailed_report = await RugCheckManager.fetch_token_detailed_report(mint)
            detailed_data = detailed_report.model_dump()

            prompt = (
                "Based on the following Solana token data from RugCheck, provide a concise risk analysis in plain English. "
                "Focus on the token's score, rugged status, holder distribution, market cap, and any notable risks:\n"
                f"Token Name: {detailed_report.tokenMeta.name if detailed_report.tokenMeta else 'Unknown'}\n"
                f"Symbol: {detailed_report.tokenMeta.symbol if detailed_report.tokenMeta else 'Unknown'}\n"
                f"Score: {detailed_report.score}\n"
                f"Rugged Status: {detailed_report.rugged}\n"
                f"Total Holders: {detailed_report.totalHolders}\n"
                f"Market Cap: {sum(ct.marketCap or 0 for ct in detailed_report.creatorTokens) if detailed_report.creatorTokens else 'N/A'}\n"
                f"Risks: {[risk.model_dump() for risk in detailed_report.risks] if detailed_report.risks else 'None listed'}\n"
                "Keep the analysis short and clear for a general audience."
            )

            response = llm.invoke(prompt)
            analysis_text = response.content if hasattr(response, 'content') else str(response)

            return {
                "status": "success",
                "analysis": analysis_text
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _run(self, mint: str) -> Dict[str, Any]:
        raise NotImplementedError("This tool only supports async execution via _arun.")

# Updated create_solana_tools function
def create_solana_tools(solana_kit: SolanaAgentKit) -> List[BaseTool]:
    return [
        SolanaRugCheckTokenReportSummaryTool(agent_kit=solana_kit),
        SolanaRugCheckTokenDetailedReportTool(agent_kit=solana_kit),
        TokenHolderAnalysisTool(agent_kit=solana_kit),
        TokenRiskAnalysisTool(agent_kit=solana_kit),
    ]

# Updated main function
async def main():
    # Retrieve private key from environment variable
    PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY")
    if not PRIVATE_KEY:
        print("Error: SOLANA_PRIVATE_KEY is not set in the environment.")
        print("Please set it with a valid base58-encoded Solana private key using:")
        print("export SOLANA_PRIVATE_KEY='your_base58_private_key_here'")
        return

    # Initialize the Solana Agent
    try:
        agent = SolanaAgentKit(
            private_key=PRIVATE_KEY,
            rpc_url="https://api.mainnet-beta.solana.com"
        )
    except Exception as e:
        print(f"Failed to initialize SolanaAgentKit: {e}")
        print("Please ensure SOLANA_PRIVATE_KEY is a valid base58-encoded Solana private key.")
        return

    # Get User Input
    token_input = input("Enter Token Ticker (e.g., SOL, USDC) or Contract Address: ").strip()
    token_mint_address = None

    try:
        Pubkey.from_string(token_input)
        token_mint_address = token_input
        print(f"Interpreting input as Contract Address: {token_mint_address}")
    except ValueError:
        print(f"Interpreting input as Token Ticker: {token_input}")
        try:
            resolved_address = TokenDataManager.get_token_address_from_ticker(token_input)
            if resolved_address:
                token_mint_address = resolved_address
                print(f"Resolved ticker '{token_input}' to Contract Address: {token_mint_address}")
            else:
                raise ValueError(f"Could not resolve ticker '{token_input}' to a Contract Address.")
        except Exception as resolve_error:
            print(f"Error resolving ticker: {resolve_error}")
            print("Please ensure you entered a valid Token Ticker or Contract Address.")
            return

    if token_mint_address:
        tools = create_solana_tools(agent)

        # Fetch and display summary report
        try:
            rugcheck_summary_tool = tools[0]
            print(f"Fetching summary report for token {token_mint_address}...")
            summary_report = await rugcheck_summary_tool._arun(token_mint_address)

            if summary_report["status"] == "success" and summary_report["report"]:
                print("Summary Report:")
                summary = TokenCheck.model_validate(summary_report["report"])
                if summary.tokenMeta:
                    print(f"  Token Name: {summary.tokenMeta.name}")
                    print(f"  Symbol: {summary.tokenMeta.symbol}")
                    print(f"  Is Verified: {summary.verification is not None}")
                else:
                    print("No tokenMeta data available.")
            else:
                print(f"Failed to fetch summary report: {summary_report.get('message')}")
        except Exception as e:
            print(f"Error fetching summary report: {e}")
        print("-" * 40)

        # Fetch and display detailed report with updated market cap handling
        try:
            rugcheck_detailed_tool = tools[1]
            print(f"Fetching detailed report for token {token_mint_address}...")
            detailed_report = await rugcheck_detailed_tool._arun(token_mint_address)

            if detailed_report["status"] == "success" and detailed_report["report"]:
                print("Detailed Report:")
                detailed = TokenCheck.model_validate(detailed_report["report"])
                print(f"  Token Name: {detailed_report['report']['token_name']}")
                print(f"  Symbol: {detailed_report['report']['symbol']}")
                print(f"  Mint Authority: {detailed_report['report']['mint_authority']}")
                print(f"  Freeze Authority: {detailed_report['report']['freeze_authority']}")
                print(f"  Score: {detailed_report['report']['score']}")
                print(f"  Rugged Status: {detailed_report['report']['rugged_status']}")
                print(f"  Market Cap: {detailed_report['report']['market_cap']} (Source: {detailed_report['report']['market_cap_source']})")
                print(f"  Total Holders: {detailed_report['report']['total_holders']}")
                print(f"  Total Market Liquidity: {detailed.totalMarketLiquidity}")
                print(f"  Number of LP Providers: {detailed.totalLPProviders}")
            else:
                print(f"Failed to fetch detailed report: {detailed_report.get('message')}")
        except Exception as e:
            print(f"Error fetching detailed report: {e}")
        print("-" * 40)

        # Fetch and display holder distribution analysis
        try:
            holder_analysis_tool = tools[2]
            print(f"Analyzing holder distribution for token {token_mint_address}...")
            holder_analysis = await holder_analysis_tool._arun(token_mint_address)

            if holder_analysis["status"] == "success" and holder_analysis["analysis"]:
                print("Holder Distribution Analysis:")
                print(f"  Total Holders: {holder_analysis['analysis']['total_holders']}")
                print(f"  Distribution Note: {holder_analysis['analysis']['distribution_note']}")
            else:
                print(f"Failed to analyze holder distribution: {holder_analysis.get('message')}")
        except Exception as e:
            print(f"Error analyzing holder distribution: {e}")
        print("-" * 40)

        # Fetch and display Gemini risk analysis
        try:
            risk_analysis_tool = tools[3]
            print(f"Generating risk analysis with Gemini 2.0 Flash for token {token_mint_address}...")
            risk_analysis = await risk_analysis_tool._arun(token_mint_address)

            if risk_analysis["status"] == "success" and risk_analysis["analysis"]:
                print("Gemini Risk Analysis:")
                print(f"  {risk_analysis['analysis']}")
            else:
                print(f"Failed to generate risk analysis: {risk_analysis.get('message')}")
        except Exception as e:
            print(f"Error generating risk analysis: {e}")
        print("-" * 40)
    else:
        print("No valid token address (ticker or contract address) provided.")

if __name__ == "__main__":
    asyncio.run(main())