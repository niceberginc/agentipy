from agentipy.agent import SolanaAgentKit


def get_headers(agent: SolanaAgentKit) -> dict:
        """
        Get the headers for Elfa AI API requests.

        Args:
            agent (SolanaAgentKit): The Solana agent instance.

        Returns:
            dict: Headers including the API key.
        """
        api_key = agent.elfa_ai_api_key
        if not api_key:
            raise Exception("ELFA_AI_API_KEY is not configured in SolanaAgentKit config.")
        return {
            "x-elfa-api-key": api_key,
            "Content-Type": "application/json"
        }