import os
import asyncio

from agentipy.tools.create_image import ImageGenerator
from agentipy.agent import SolanaAgentKit

async def main():
    api_key = "sk-proj----"
    #api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")

    agent = SolanaAgentKit(openai_api_key=api_key)

    prompt = "A cartoon green python snake wearing tiny glasses, typing Python code on a glowing laptop. The screen shows Solana blockchain code (e.g., 'async def transaction()') with Solana logo (purple S-shaped vortex) floating nearby. Snake’s tail forms a blockchain symbol (🔗) and a tiny SOL coin. Background: clean digital workspace with abstract crypto nodes. Style: friendly, minimalist 2D flat design with mint green and purple accents."
    size = "1024x1024" 
    num_images = 1

    try:
        response = await ImageGenerator.create_image(agent, prompt, size=size, n=num_images)
        images = response.get("images", [])

        for i, url in enumerate(images, start=1):
            print(f"Image {i}: {url}")
    except Exception as err:
        print(f"Failed to generate images: {err}")

if __name__ == "__main__":
    asyncio.run(main())
