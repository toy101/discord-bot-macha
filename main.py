import logging
import os

import discord
from discord import Message
from discord.ext import commands

from macha import Macha

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
TARGET_CHANNEL_ID = os.environ["TARGET_CHANNEL_ID"]
EMOJI_CHECKED = "✅"
TARGET_MENTION_AUTHOR = ["644188408108941342"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

macha = Macha(target_channel_id=TARGET_CHANNEL_ID, logger=logger)


@bot.command("ping")
async def ping(ctx):
    await ctx.send('pong')


@bot.listen()
async def on_message(ctx: Message):

    if ctx.author.bot:
        logger.info("this message sent from BOT")
        return 0

    mention_author = macha.check_mention_to_me(ctx)
    if mention_author:
        if str(ctx.author.id) in TARGET_MENTION_AUTHOR:
            await ctx.reply(f"I love you, {mention_author}")
        else:
            await ctx.reply(f"Hello, {mention_author}")

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
