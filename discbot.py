#disord imports for the bot
import discord
from discord.ext import commands, tasks
from dctoken import token #this is just my discord bot token



#database managing imports
from main import app,Facts, create_app, get_db

#miscellaneous imports
import random
from qol import random_fact_choice

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)



app = create_app()
db = get_db()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "akdqwenqknlnlcashodonasdlkaksd"


GUILD_IDS = [1195734655106818069]


@bot.event
async def on_ready():
    print(f'I am in! My codename is: "{bot.user}"')
    send_message_periodically.start()


#stuff below will probably be brand new, i believe in you, future me....


#empty command template:
#@bot.slash_command(
#    name="",
#    description="",
#    guild_ids=GUILD_IDS
#)


#this is for choosing a random one later.
facts = [
"The Earth's average surface temperature has risen about 1.18°C (2.12°F) since the late 19th century.",
"The primary cause of global warming is the increase in greenhouse gases like carbon dioxide (CO2), methane (CH4), and nitrous oxide (N2O).",
"Human activities, particularly the burning of fossil fuels and deforestation, are the largest contributors to greenhouse gas emissions.",
"Arctic sea ice is declining at a rate of 12.6% per decade.",
"Global sea levels have risen by about 20 cm (8 inches) in the last century, with the rate of increase nearly doubling in the last two decades.",
"Global warming is linked to more extreme weather events, including stronger hurricanes, more intense heatwaves, and heavier rainfall.",
"The top 700 meters (about 2,300 feet) of the ocean have warmed by more than 0.2°C (0.36°F) since the 1960s.",
"Oceans have absorbed about 30% of the emitted anthropogenic CO2, causing ocean acidification which affects marine life, especially coral reefs.",
"Glaciers around the world are retreating, including those in the Alps, Himalayas, Andes, Rockies, Alaska, and Africa.",
"Thawing permafrost is releasing methane, a potent greenhouse gas, exacerbating global warming.",
"Climate change is a significant threat to biodiversity, with many species facing increased risk of extinction due to changing habitats.",
"Global warming affects agriculture by altering rainfall patterns, increasing temperatures, and causing more frequent extreme weather events, impacting crop yields.",
"Climate change poses health risks, including heat-related illnesses, vector-borne diseases (like malaria), and respiratory issues from increased air pollution.",
"Changes in precipitation and melting glaciers are affecting freshwater resources, leading to water scarcity in many regions.",
"The economic costs of climate change are significant, impacting infrastructure, health care, agriculture, and overall economic productivity.",
"Transitioning to renewable energy sources like solar, wind, and hydroelectric power is crucial to mitigating global warming.",
"The Paris Agreement aims to limit global warming to well below 2°C, preferably to 1.5°C, compared to pre-industrial levels.",
"Reducing individual and collective carbon footprints through lifestyle changes and sustainable practices can help mitigate global warming.",
"Rising sea levels and extreme weather events are leading to increased displacement and migration of people.",
"The frequency and intensity of heatwaves are increasing due to global warming, posing severe health risks.",
"Global warming is contributing to more frequent and intense wildfires by creating drier and hotter conditions.",
"Warmer ocean temperatures are causing coral bleaching, threatening coral reef ecosystems worldwide.",
"Melting sea ice is reducing the habitat for polar bears, putting them at risk of starvation and population decline.",
"Positive feedback loops, such as the ice-albedo effect, amplify global warming by reducing the Earth's ability to reflect sunlight.",
"Raising public awareness and understanding of global warming is essential for driving collective action to address the crisis."]


@tasks.loop(seconds=60)
async def send_message_periodically():
    channel = bot.get_channel(1195734655702405202)
    if channel:
        await channel.send(f"Here's a random fact about global warming: {random.choice(facts)}")



@bot.slash_command(
    name="gwranfact",
    description="Gives a random global warming fact!",
    guild_ids=GUILD_IDS
)
async def gwrandomfact(ctx,
                    amount_of_facts: int):
    if amount_of_facts <= 10:
        for _ in range(amount_of_facts):
            await ctx.respond(random.choice(facts))
    else:
        await ctx.respond("You can only have 1-10 facts at a time!")

@bot.slash_command(
    name="writeyourfact",
    description="write your own fact/thoughts about global warming and save it to the database!",
    guild_ids=GUILD_IDS
)
async def writeyourfact(ctx, author: str, title: str, text: str):
    with app.app_context():
        
        fact = Facts(title=title, text=text, author=author)
        db.session.add(fact)
        db.session.commit()
        
        await ctx.respond("Your fact has been saved to the database!")


@bot.slash_command(
    name="randomuserfact",
    description="it shows a random fact from the database of human-written facts about the global warming!",
    guild_ids=GUILD_IDS
)
async def randomuserfact(ctx, amount: int):
    for _ in range(amount):
        
        fact = random_fact_choice()

        if fact is not None:
            author = fact.author
            title = fact.title
            text = fact.text
            await ctx.respond(f"This fact is made by '{author}'\nHis topic is '{title}', and he wants to say the following: {text}")
        else:
            await ctx.respond("No facts found.")



#just a help command
@bot.slash_command(
        name="help",
        description="Provides the list of all commands for this bot!",
        guild_ids=GUILD_IDS
)
async def help_command(ctx: discord.ApplicationContext):
    embed = discord.Embed(title="Help", description="List of all commands", color=discord.Color.blue())
    commands_list = [
        {"name": "/gwranfact [amount 1-10]", "description": "Gives a random global warming fact!"},
        {"name": "/writeyourfact [author] [title] [text]", "description": "write your own fact/thoughts about global warming and save it to the database!"},
        {"name": "/randomuserfact [amount 1-10]", "description": "it shows a random fact from the database of human-written facts about the global warming!"}
    ]

    for command in commands_list:
        embed.add_field(name=command["name"], value=command["description"], inline=False)

    embed.set_footer(text="You can also see user-written facts about global warming on our website!")
    await ctx.respond(embed=embed)



bot.run(token)
