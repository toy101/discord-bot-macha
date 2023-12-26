import logging
import os

import discord
from discord.ext import commands

from macha import Macha

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
EMOJI_CHECKED = "✅"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

macha = Macha(logger=logger)


@bot.command("ping")
async def ping(ctx):
    await ctx.send('pong')


@bot.listen()
async def on_message(ctx):

    if macha.is_target_channel(ctx):
        logger.info("target text channel")

        if macha.exist_png_image(ctx):

            result = macha.valid_images(ctx)

            if result:
                await ctx.reply("これらの画像はいずれも透過にならない可能性があります")
            else:
                await ctx.add_reaction(EMOJI_CHECKED)
        else:
            logger.info("Not png files")
    else:
        logger.info("Not target text channel")


def main():
    logger.info("start bot")
    bot.run(TOKEN, root_logger=True)


if __name__ == '__main__':
    main()
