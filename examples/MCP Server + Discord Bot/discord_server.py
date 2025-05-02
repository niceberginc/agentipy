import os
import json
import traceback

import discord
from discord.ext import commands
from discord import app_commands

from agentipy import SolanaAgentKit
from agentipy.mcp.mcp_server import ALL_ACTIONS  

#  Configuration
DISCORD_TOKEN      = os.getenv("DISCORD_TOKEN")
SOLANA_PRIVATE_KEY = os.getenv("SOLANA_PRIVATE_KEY")
RPC_URL            = os.getenv("RPC_URL")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

agent = SolanaAgentKit(private_key=SOLANA_PRIVATE_KEY, rpc_url=RPC_URL)
selected_actions = ALL_ACTIONS

def chunk_text(text: str, size: int = 1900) -> list[str]:
    """Split text into <=size-char chunks (leaving room for markdown)."""
    return [ text[i : i + size] for i in range(0, len(text), size) ]

@bot.event
async def on_ready():
    print(f"Discord MCP Bot is online as {bot.user}")
    await bot.tree.sync()

# Classic text command: !mcp
@bot.command(name="mcp")
async def mcp_command(ctx, action: str, *args):
    """
    Usage: !mcp <action> [params]
    Example: !mcp COINGECKO_GET_TOP_GAINERS 24h 5
    """
    if action not in selected_actions:
        await ctx.send(f"Unknown action `{action}`. Available: {', '.join(selected_actions)}`")
        return

    try:
        tool = selected_actions[action]
        schema = getattr(tool, "inputSchema", {})
        kwargs = {}
        for i, (param_name, info) in enumerate(schema.items()):
            if i < len(args):
                val = args[i]
                if info["type"] == "integer":
                    val = int(val)
                elif info["type"] == "array":
                    val = val.split(",")
                kwargs[param_name] = val

        result = await tool.handler(agent, kwargs)
        pretty = json.dumps(result, indent=2)
        wrapped = f"```json\n{pretty}\n```"

        # Chunk and send each part
        for part in chunk_text(wrapped):
            await ctx.send(part)

    except Exception as e:
        await ctx.send(f"Error: {e}")
        print(traceback.format_exc())

# Slash command factory for each MCP action
def command_factory(action_name: str):
    base_name = f"mcp_{action_name.lower()}"
    cmd_name  = base_name[:32]

    @bot.tree.command(name=cmd_name, description=f"MCP action: {action_name}")
    @app_commands.describe(params="Space-separated parameters")
    async def generic_slash(interaction: discord.Interaction, params: str = ""):
        param_list = params.split() if params else []
        tool = selected_actions[action_name]
        schema = getattr(tool, "inputSchema", {})

        kwargs = {}
        for i, (param_name, info) in enumerate(schema.items()):
            if i < len(param_list):
                val = param_list[i]
                if info["type"] == "integer":
                    val = int(val)
                elif info["type"] == "array":
                    val = val.split(",")
                kwargs[param_name] = val

        try:
            result = await tool.handler(agent, kwargs)
            pretty = json.dumps(result, indent=2)
            wrapped = f"```json\n{pretty}\n```"

            # initial chunk
            parts = chunk_text(wrapped)
            await interaction.response.send_message(parts[0])
            # follow-ups
            for part in parts[1:]:
                await interaction.followup.send(part)

        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")
            print(traceback.format_exc())

def register_slash_commands():
    for name in selected_actions:
        command_factory(name)

register_slash_commands()

# Chunked Help Command
@bot.tree.command(name="mcp_help", description="List available MCP actions (chunked)")
async def mcp_help(interaction: discord.Interaction):
    lines = ["**Available MCP Actions:**"]
    for name, tool in selected_actions.items():
        desc = getattr(tool, "description", "No description.")
        lines.append(f"- `{name}`: {desc}")
    full = "\n".join(lines)

    chunks = chunk_text(full)
    await interaction.response.send_message(chunks[0])
    for chunk in chunks[1:]:
        await interaction.followup.send(chunk)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
