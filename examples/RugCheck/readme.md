# Solana Token Analysis with RugCheck and Gemini 2.0 Flash

This repository demonstrates how to analyze Solana tokens using data from RugCheck and the Gemini 2.0 Flash language model, leveraging the Agentipy framework.

## Prerequisites

Before you begin, make sure you have the following:

1.  **Python 3.8+:** Ensure you have Python installed.
2.  **Agentipy Installation:** You should have followed the installation instructions from the previous tutorials. If not, run:

    ```bash
    pip install agentipy
    pip install httpx
    pip install tenacity
    pip install langchain
    pip install langchain-google-genai
    ```

3.  **Environment Variables:** Set the following environment variables:

    *   `SOLANA_PRIVATE_KEY`: Your Solana wallet's private key (base58-encoded).  **IMPORTANT: Treat your private key with extreme care. Do not share it publicly.**
    *   `RUGCHECK_API_KEY`: Your RugCheck API key. You'll need to sign up for an API key on their website.
    *   `GOOGLE_API_KEY`: Your Google API Key, obtain it from Google Cloud Console.
4.  **API Keys and Accounts:**
    *   **RugCheck API Key:** Sign up for a RugCheck API key on their website: [https://rugcheck.xyz/](https://rugcheck.xyz/). You'll need an API key to access their token analysis data.
    *   **Google API Key:** Obtain a Google API key from the Google Cloud Console: [https://console.cloud.google.com/](https://console.cloud.google.com/). Enable the Gemini 2.0 Flash API. You may need to set up billing.

## Files

*   `rugcheck.py`:  The main Python script that performs the Solana token analysis.

## Code Overview

The `rugcheck.py` script utilizes the Agentipy framework, RugCheck API, and Gemini 2.0 Flash to perform a comprehensive analysis of Solana tokens.  Here's a breakdown of the key components:

*   **Imports:** Imports necessary libraries including Agentipy components, httpx for API requests, tenacity for retries, and libraries for the Gemini API.

*   **Logging:** Sets up logging for debugging and informational purposes.

*   **Environment Variables and Gemini Initialization:** Retrieves API keys from environment variables and initializes the Gemini 2.0 Flash language model.

*   **Pydantic Models:** Defines Pydantic models (`TokenMeta`, `Token`, `Risks`, `CreatorToken`, `TokenCheck`) to structure and validate the data fetched from the RugCheck API, ensuring data integrity.

*   **`RugCheckManager` Class:**  Manages interactions with the RugCheck API:

    *   `_make_request()`: Handles HTTP requests with retries.
    *   `fetch_token_report_summary()`: Fetches a summary report.
    *   `fetch_token_detailed_report()`: Fetches a detailed report.
    *   `fetch_token_lp_lockers()`: Fetches LP locker information.
    *   `get_trending_tokens()`: Get trending tokens.

*   **Custom Agentipy Tools:**

    *   `TokenHolderAnalysisTool`: Analyzes token holder distribution.
    *   `SolanaRugCheckTokenReportSummaryTool`: Fetches a summary report using RugCheck.
    *   `SolanaRugCheckTokenDetailedReportTool`: Fetches a detailed report, includes Market Cap, symbol, and other metadata, and handles cases with missing data.
    *   `TokenRiskAnalysisTool`: Uses Gemini 2.0 Flash to generate a risk analysis.

*   **`create_solana_tools()` Function:** Creates a list of Agentipy tools.

*   **`main()` Function:**

    *   Initializes the Solana Agent.
    *   Gets user input for a token (ticker or contract address).
    *   Uses `create_solana_tools()` to create and load tools.
    *   Executes each tool to fetch summary reports, detailed reports, holder analysis, and risk analysis.
    *   Prints the results to the console.

## Running the Script

1.  **Save the Code:** Save the code as `rugcheck.py`.
2.  **Set Environment Variables:**

    *   **Linux/macOS:**
        ```bash
        export SOLANA_PRIVATE_KEY='your_base58_private_key_here'
        export RUGCHECK_API_KEY='your_rugcheck_api_key_here'
        export GOOGLE_API_KEY='your_google_api_key_here'
        ```

    *   **Windows (Command Prompt):**
        ```bash
        set SOLANA_PRIVATE_KEY=your_base58_private_key_here
        set RUGCHECK_API_KEY=your_rugcheck_api_key_here
        set GOOGLE_API_KEY=your_google_api_key_here
        ```

    *   **Windows (PowerShell):**
        ```bash
        $env:SOLANA_PRIVATE_KEY = 'your_base58_private_key_here'
        $env:RUGCHECK_API_KEY = 'your_rugcheck_api_key_here'
        $env:GOOGLE_API_KEY = 'your_google_api_key_here'
        ```

3.  **Run the Script:** Open a terminal and run:
    ```bash
    python rugcheck.py
    ```
4.  **Enter Token Information:** The script will prompt you for a token ticker or contract address.


## Important Considerations

*   **API Rate Limits:** Be mindful of RugCheck's API rate limits.
*   **Security:** Protect your `SOLANA_PRIVATE_KEY` and `RUGCHECK_API_KEY`.
*   **Data Accuracy:** Verify results and cross-reference with other sources.
*   **Cost:** Be aware of RugCheck and Gemini API costs.

## Contributing

We welcome contributions! See the [Contribution Guidelines](https://github.com/niceberginc/agentipy/blob/main/CONTRIBUTING.md).

## Resources and Further Reading

*   [Agentipy GitHub Repository](https://github.com/niceberginc/agentipy)
*   [RugCheck API Documentation](https://api.rugcheck.xyz/docs)
*   [Gemini API Documentation](https://cloud.google.com/gemini/docs)
*   [Solana Documentation](https://docs.solana.com/)
*   [Agentipy Examples](https://github.com/niceberginc/agentipy/tree/main/examples)

## Contact

Join the community on [X (@AgentiPy)](https://x.com/AgentiPy) to share your ideas and get support.  If you have questions or need help, reach out on [X (@AgentiPy)](https://x.com/AgentiPy) or open an issue on GitHub.