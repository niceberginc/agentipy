# Agentipy Elfa AI Integration Examples

This Example File contains two example scripts demonstrating the use of the Agentipy library to interact with the Elfa AI API for blockchain and crypto-related data analysis.  Agentipy simplifies interacting with various APIs, including the Elfa AI API, by providing a structured approach for authentication, tool creation, and asynchronous execution.

## Prerequisites

Before running these examples, you'll need to set up your environment:

1.  **Install Agentipy and Required Dependencies:**

    ```bash
    pip install agentipy
    ```

    This will install `agentipy` and its dependencies, including the `elfaai` integration, `langchain`, and any necessary libraries.

2.  **Set up Environment Variables:**

    You will need an Elfa AI API key and a Solana private key.  These should be set as environment variables:

    *   `ELFA_AI_API_KEY`: Your Elfa AI API key. You can obtain this from the [Elfa AI developer portal](https://dev.elfa.ai/).
    *   `SOLANA_PRIVATE_KEY`: Your Solana private key, encoded as a base58 string.  This is used by `agentipy` to authenticate API calls.

    You can set these in your terminal or in your `.env` file (make sure to load your `.env` file into your environment).

    **Example:**
    ```bash
    export ELFA_AI_API_KEY="YOUR_ELFA_AI_API_KEY"
    export SOLANA_PRIVATE_KEY="YOUR_SOLANA_PRIVATE_KEY"
    ```
    **Important:**  Do *not* hardcode your API key or private key directly into the scripts. Use environment variables to keep them secure.

## Example Scripts

### `elfaai1.py`: Demonstrating Basic Elfa AI API Calls

This script demonstrates a basic integration with the Elfa AI API using Agentipy.  It shows how to:

*   Initialize a `SolanaAgentKit` object.
*   Create and use Elfa AI tools provided by Agentipy.
*   Call different Elfa AI endpoints to retrieve information.

**Functionality:**

*   Retrieves smart mentions.
*   Retrieves top mentions for a given ticker (SOL).
*   Searches mentions by keywords within a specific time range.
*   Retrieves trending tokens.
*   Retrieves smart Twitter account statistics for a specified username.

**How to Run:**

1.  Make sure you have set the environment variables (see Prerequisites).
2.  Run the script from your terminal:

    ```bash
    python elfaai1.py
    ```

    The script will execute each Elfa AI tool in sequence and print the results to the console.

### `elfaai2.py`: Interactive Elfa AI Analysis

This script enhances the first example by making it interactive. It prompts the user to select which analysis to run.

**Functionality:**

*   Provides a menu-driven interface to select an Elfa AI analysis option.
*   Takes user input for parameters relevant to the selected analysis (e.g., ticker, keywords, dates, limits).
*   Validates the input, especially for dates, to ensure it conforms to the requirements of the API.
*   Provides a basic check of the date range to avoid potential errors
*   Presents results to the user

**How to Run:**

1.  Make sure you have set the environment variables (see Prerequisites).
2.  Run the script from your terminal:

    ```bash
    python elfaai2.py
    ```

    The script will present a menu, allowing you to choose which Elfa AI function to execute and prompting for any necessary inputs.

## Key Components and Concepts

*   **Agentipy's `SolanaAgentKit`:** This class handles the initialization of the agent.  It takes the Solana private key and Elfa AI API key as input.  It manages authentication and connection to both the Solana blockchain (though not directly used in this example) and the Elfa AI API.
*   **Elfa AI Tools:** Agentipy provides pre-built tools that wrap the Elfa AI API endpoints.  These tools are subclasses of Langchain's `BaseTool` and are designed for asynchronous execution.
*   **`get_elfaai_tools()` Function:** This function, defined in `agentipy.langchain.elfaai`, returns a list of pre-configured Elfa AI tools.
*   **Asynchronous Execution (`asyncio`)**: Both scripts utilize `asyncio` for asynchronous execution of API calls, which improves performance, especially when making multiple API calls. The  `_arun` method of the tools handles the asynchronous execution.
*   **Input Validation:**  Both examples include input validation and error handling. This protects against incorrect inputs, which can lead to unexpected behavior or API errors. The `validate_input` function from `agentipy.helpers` simplifies input validation.
*   **JSON Serialization/Deserialization**: The scripts use `json.dumps()` to serialize the input parameters to JSON strings, which are then passed to the API calls, and `json.loads()` to deserialize data returned by the API.

## How to Use the Scripts as a Starting Point

1.  **Adapt for your specific needs:**  Modify the input parameters (tickers, keywords, dates, etc.) to query the data you want to analyze.
2.  **Extend the Functionality:**  Add more Elfa AI API calls, integrate with other data sources, or build a more sophisticated user interface.
3.  **Integrate with Langchain Chains**: Agentipy and Langchain work well together. You can easily incorporate these tools into Langchain chains for more complex workflows, such as creating agents that can intelligently query Elfa AI for information and then use that information to perform other tasks.
4.  **Error Handling and Logging:** Implement comprehensive error handling and logging to make the scripts more robust and easier to debug.
5.  **Rate Limiting:** Be mindful of Elfa AI API rate limits and implement strategies (e.g., delays, retry mechanisms) to avoid exceeding them.

## Conclusion

These example scripts offer a solid foundation for interacting with the Elfa AI API using Agentipy. By understanding these examples, you can quickly build applications that leverage the power of Elfa AI to gain insights into the blockchain and cryptocurrency landscape. Remember to consult the Elfa AI API documentation ([https://dev.elfa.ai/](https://dev.elfa.ai/)) for detailed information about the API endpoints and their parameters.