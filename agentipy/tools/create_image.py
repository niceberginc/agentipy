from openai import AsyncOpenAI 
from agentipy.agent import SolanaAgentKit


class ImageGenerator:
    @staticmethod
    async def create_image(agent:SolanaAgentKit, prompt, size="1024x1024", n=1):
        try:
            if not agent.openai_api_key:
                raise ValueError("OpenAI API key not found in agent configuration")

            client = AsyncOpenAI(
                api_key=agent.openai_api_key
            )

            # "dall-e-2" supports 256x256, 512x512, 1024x1024
            # "dall-e-3" usually requires 1024x1024, 1792x1024, or 1024x1792
            print(f"--- Using OpenAI model: dall-e-2 for size {size} ---")
            response = await client.images.generate(
                model="dall-e-2",
                prompt=prompt,
                n=n,
                size=size
            )

            return {
                "images": [img.url for img in response.data]
            }

        except Exception as error:
            import traceback
            print(traceback.format_exc())
            raise Exception(f"Image generation failed: {str(error)}")