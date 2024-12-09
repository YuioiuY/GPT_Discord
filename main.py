import discord, os, config
from discord.ext import commands
from GPT import GPT

# create gpt
gpt = GPT()

# initialize
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix=config.settings["prefix"], intents=intents)

# Bot States
bot.is_busy = False

@bot.event
async def on_ready():
    print(f'Bot {bot.user} running!')

@bot.command(name='info')
async def info(ctx):
    '''bot info'''
    await ctx.send("🤖 This bot can answer questions and generate images.\n"
                   "Commands:\n"
                   "`!gpt [text]` — Get a response from ChatGPT\n"
                   "`!img [prompt]` — Generate an image based on the description")

@bot.command(name='gpt')
async def gpt_command(ctx, *, request=None):
    '''Processing the command !gpt'''
    if bot.is_busy:
        await ctx.send("⏳ The bot is busy processing another request. Wait a bit.")
        return

    if not request:
        await ctx.send("❌ Incorrect input. Use `!gpt [your request]`.")
        return

    bot.is_busy = True
    await ctx.send(f"🤔 Processing your request: `{request}`")
    
    try:
        response = gpt.get_response(request)
        await ctx.send(f"📢 Response: {response}")
    except Exception as e:
        await ctx.send("❌ An error occurred while processing your request.")
        print(f"Error: {e}")
    finally:
        bot.is_busy = False

@bot.command(name='img')
async def img_command(ctx, *, request=None):
    '''Processing the command !img'''
    if bot.is_busy:
        await ctx.send("⏳ The bot is busy processing another request. Wait a bit.")
        return

    if not request:
        await ctx.send("❌ Incorrect input. Use `!img [prompt]`.")
        return

    bot.is_busy = True
    await ctx.send(f"🎨 I'm generating an image based on the description: `{request}`")
    
    try:
        image_url = gpt.get_img_gen(request)
        if "http" in image_url:
            await ctx.send(f"🖼️ Here is your image: {image_url}")
        else:
            await ctx.send("❌ An error occurred while generating the image.")
    except Exception as e:
        await ctx.send("❌ An error occurred while generating the image.")
        print(f"Error: {e}")
    finally:
        bot.is_busy = False

@bot.event
async def on_command_error(ctx, error):
    '''Command error handling'''
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Incorrect input. Check the correctness of the command.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ There is no such command. Available commands:\n"
                       "`!info`, `!gpt [text]`, `!img [prompt]`")
    else:
        await ctx.send("❌ An unknown error has occurred.")
        print(f"Error: {error}")

# run
bot.run(config.settings["token"])
