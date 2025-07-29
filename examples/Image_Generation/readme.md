## Image Generation Tool for Agentipy

Integrate DALL·E image creation into your Solana-based workflows via the `ImageGenerator` utility, leveraging Agentipy's `SolanaAgentKit` for authentication and async handling.

---

## Key Features

-  **Secure Key Management**: Automatically uses the `openai_api_key` stored in a `SolanaAgentKit` instance.
-  **Async-First API**: All operations use the OpenAI `AsyncOpenAI` client for non-blocking calls.
-  **Flexible Models & Sizes**: Defaults to DALL·E 2 with support for 256×256, 512×512, and 1024×1024; easily switch to DALL·E 3 by adjusting the `model` parameter.
-  **Robust Error Handling**: Throws descriptive errors if the API key is missing or if generation fails, with stack traces for debugging.

---

## Installation

Ensure you have Python 3.8+ and install via pip:

```bash
pip install agentipy openai
```

> `agentipy` brings in `SolanaAgentKit`; `openai` provides the async client.

---

## Module Overview

### `agentipy/tools/create_image.py`

- **Class**: `ImageGenerator`
- **Method**: `create_image(agent: SolanaAgentKit, prompt: str, size: str = "1024x1024", n: int = 1) -> dict`
  - **agent**: Instance of `SolanaAgentKit` containing the `openai_api_key`.
  - **prompt**: Textual description for the image generation.
  - **size**: Resolution string (e.g., `"1024x1024"`).
  - **n**: Number of images to generate.
  - **Returns**: A dict with `images`, a list of URL strings.

Internally, this method:

1. Validates presence of the API key on the agent.
2. Instantiates `AsyncOpenAI` with the key.
3. Selects `dall-e-2` (or customized model).
4. Calls `client.images.generate(...)` and extracts URLs.
5. Catches exceptions, logs tracebacks, and rethrows with context.

---

## Example Entry Point: `gen_img.py`

A complete runnable example lives in `gen_img.py` at the repo root. It:

1. Loads `OPENAI_API_KEY` from the environment.
2. Constructs a `SolanaAgentKit` with the key.
3. Defines a rich prompt (e.g., a cartoon snake coding).
4. Calls `ImageGenerator.create_image(...)` and prints returned URLs.

Run it via:

```bash
python gen_img.py
```

Refer to that file for the full implementation details and customization tips.

---

## Configuration & Constraints

- **Model Selection**: Change the `model` argument in `create_image` to switch between DALL·E versions.
- **Image Sizes**:
  - DALL·E 2: 256×256, 512×512, 1024×1024
  - DALL·E 3: 1024×1024, 1792×1024, 1024×1792
- **Rate Limits**: Observe OpenAI quotas; handle retries/backoff as needed.

---

## Error Handling

- Raises `ValueError` if `agent.openai_api_key` is unset.
- On any generation error, prints a full traceback and raises an exception:
  ```python
  except Exception as error:
      print(traceback.format_exc())
      raise Exception(f"Image generation failed: {error}")
  ```

---

## Best Practices

1. **Prompt Engineering**: Use precise, descriptive language and style hints.
2. **Environment Security**: Store APIs keys in environment variables or secret managers.
3. **Throttling**: Avoid excessive parallel calls; implement rate-limit handling.
4. **Model Upgrades**: Test with both DALL·E 2 and 3 to find the best fit.

---

## Troubleshooting

| Issue                            | Solution                                                         |
|----------------------------------|------------------------------------------------------------------|
| `ValueError`: API key not found  | Ensure `OPENAI_API_KEY` is set or passed into `SolanaAgentKit`.  |
| Model/Size mismatch              | Use a valid size for the selected DALL·E version.                |
| Network or timeout errors        | Check connectivity; implement retry/backoff logic.               |

---

For the complete code and usage examples, see [`gen_img.py`](https://github.com/niceberginc/agentipy/blob/main/agentipy/tools/create_image.py).

