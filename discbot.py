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
facts_en = [
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


facts_ru = [
"Средняя температура поверхности Земли поднялась примерно на 1.18°C (2.12°F) с конца XIX века.",
"Основной причиной глобального потепления является увеличение выбросов парниковых газов, таких как углекислый газ (CO2), метан (CH4) и закись азота (N2O).",
"Человеческая деятельность, особенно сжигание ископаемого топлива и вырубка лесов, является крупнейшим источником выбросов парниковых газов.",
"Ледяной покров Арктики сокращается со скоростью 12,6% за десятилетие.",
"Уровень мирового океана поднялся примерно на 20 см (8 дюймов) за последний век, причем скорость подъема почти удвоилась за последние два десятилетия.",
"Глобальное потепление связано с более экстремальными погодными явлениями, включая более сильные ураганы, более интенсивные тепловые волны и более обильные дожди.",
"Верхние 700 метров (около 2300 футов) океана прогрелись более чем на 0.2°C (0.36°F) с 1960-х годов.",
"Океаны поглотили около 30% антропогенного CO2, что вызывает окисление океанов, влияющее на морскую жизнь, особенно на коралловые рифы.",
"Ледники по всему миру отступают, включая ледники в Альпах, Гималаях, Андах, Скалистых горах, Аляске и Африке.",
"Таяние вечной мерзлоты высвобождает метан, мощный парниковый газ, усугубляющий глобальное потепление.",
"Изменение климата представляет значительную угрозу для биоразнообразия, и многие виды сталкиваются с повышенным риском вымирания из-за изменения их среды обитания.",
"Глобальное потепление влияет на сельское хозяйство, изменяя характер осадков, повышая температуры и вызывая более частые экстремальные погодные явления, что снижает урожайность.",
"Изменение климата несет угрозы здоровью, включая тепловые удары, болезни, переносимые насекомыми (например, малярия), и респираторные проблемы из-за увеличения загрязнения воздуха.",
"Изменения в количестве осадков и таяние ледников влияют на водные ресурсы, что приводит к нехватке воды во многих регионах.",
"Экономические затраты на изменение климата значительны и влияют на инфраструктуру, здравоохранение, сельское хозяйство и общую экономическую продуктивность.",
"Переход на возобновляемые источники энергии, такие как солнечная, ветровая и гидроэлектрическая энергия, жизненно важен для смягчения глобального потепления.",
"Парижское соглашение направлено на ограничение глобального потепления до уровня значительно ниже 2°C, желательно до 1.5°C, по сравнению с доиндустриальным уровнем.",
"Сокращение индивидуального и коллективного углеродного следа через изменения в образе жизни и устойчивые практики может помочь смягчить глобальное потепление.",
"Повышение уровня моря и экстремальные погодные явления приводят к увеличению перемещения и миграции людей.",
"Частота и интенсивность тепловых волн увеличиваются из-за глобального потепления, что создает серьезные риски для здоровья.",
"Глобальное потепление способствует более частым и интенсивным лесным пожарам, создавая более сухие и жаркие условия.",
"Повышение температуры океанов вызывает обесцвечивание кораллов, угрожая коралловым рифовым экосистемам по всему миру.",
"Таяние морского льда уменьшает среду обитания для белых медведей, что ставит их под угрозу голодания и сокращения численности.",
"Положительные обратные связи, такие как эффект альбедо, усиливают глобальное потепление, снижая способность Земли отражать солнечный свет.",
"Повышение осведомленности общественности и понимания глобального потепления является важным для стимулирования коллективных действий по решению этой проблемы."]



#command to change the language of other commands
language = "eng"
@bot.slash_command(
        name="language",
        description="Change the language of the bot",
        guild_ids= GUILD_IDS
)
async def change_language(ctx, language_choice: discord.Option(str, "Choose language", choices=["eng", "ru"])):
    global language
    if language_choice == "eng":
        language = "eng"
        await ctx.respond("Changed the language to english!")
        
    elif language_choice == "ru":
        language = "ru"
        await ctx.respond("Язык был изменен на русский!")
        
        


@tasks.loop(seconds=60)
async def send_message_periodically():
    channel = bot.get_channel(1195734655702405202)
    if language == "eng":
        await channel.send(f"Here's a random fact about global warming: {random.choice(facts_en)}")
    elif language == "ru":
        await channel.send(f"Вот случайный факт о глобальном потеплении: {random.choice(facts_ru)}")



@bot.slash_command(
    name="gwranfact",
    description="Gives a random global warming fact!",
    guild_ids=GUILD_IDS
)
async def gwrandomfact(ctx, amount_of_facts: int):
    if amount_of_facts <= 10:
        print(language)
        if language == "eng":
            facts = facts_en
        elif language == "ru":
            facts = facts_ru

        for _ in range(amount_of_facts):
            await ctx.respond(random.choice(facts))
    else:
        if language == "eng":
            await ctx.respond("You can only have 1-10 facts at a time!")
        elif language == "ru":
            await ctx.respond("За раз можно брать только от 1 до 10 фактов!")

@bot.slash_command(
    name="writeyourfact",
    description="write your own fact/thoughts about global warming and save it to the database!",
    guild_ids=GUILD_IDS
)
async def writeyourfact(ctx, author: str, title: str, text: str):
    with app.app_context():
        
        fact = Facts(title=title, text=text, author=author, language=language)
        db.session.add(fact)
        db.session.commit()
        if language == "eng":
            await ctx.respond("Your fact has been saved to the database!")
        elif language == "ru":
            await ctx.respond("Ваш факт был добавлен в датабазу!")

@bot.slash_command(
    name="randomuserfact",
    description="Shows a random fact from the database of human-written facts about global warming!",
    guild_ids=GUILD_IDS
)
async def randomuserfact(ctx, amount: int):
    if amount < 1 or amount > 10:
        if language == "eng":
            await ctx.respond("You can only request between 1 and 10 facts at a time!")
        elif language == "ru":
            await ctx.respond("За раз можно брать только от 1 до 10 фактов!")


    for _ in range(amount):
        fact = random_fact_choice(language)

        if fact is not None:
            author = fact.author
            title = fact.title
            text = fact.text
            if language == "eng":
                await ctx.respond(f"This fact is made by '{author}'\nHis topic is '{title}', and he wants to say the following: {text}")
            elif language == "ru":
                await ctx.respond(f"Факт был написан '{author}'\n Его тема это '{title}', и его мысли которые он хочет передать это: {text}")
        else:
            await ctx.respond("No facts found for the specified language.")



#just a help command
@bot.slash_command(
        name="help",
        description="Provides the list of all commands for this bot!",
        guild_ids=GUILD_IDS
)
async def help_command(ctx: discord.ApplicationContext):
    embed = discord.Embed(title="Help", description="List of all commands", color=discord.Color.blue())
    commands_list_en = [
        {"name": "/language [ru/eng]", "description" : "Changes the language of the bot!"},
        {"name": "/gwranfact [amount 1-10]", "description": "Gives a random global warming fact!"},
        {"name": "/writeyourfact [author] [title] [text]", "description": "write your own fact/thoughts about global warming and save it to the database!"},
        {"name": "/randomuserfact [amount 1-10]", "description": "it shows a random fact from the database of human-written facts about the global warming!"}
    ]
    commands_list_ru = [
    {"name": "/language [ru/eng]", "description" : "Меняет язык бота!"},
    {"name": "/gwranfact [количество 1-10]", "description": "Выдает случайный факт о глобальном потеплении!"},
    {"name": "/writeyourfact [автор] [заголовок] [текст]", "description": "Напишите свой собственный факт/мысли о глобальном потеплении и сохраните их в базе данных!"},
    {"name": "/randomuserfact [количество 1-10]", "description": "Показывает случайный факт из базы данных о человеческих фактах о глобальном потеплении!"}
    ]

    if language == "eng":
        for command in commands_list_en:
            embed.add_field(name=command["name"], value=command["description"], inline=False)
            embed.set_footer(text="You can also see user-written facts about global warming on our website!")
    elif language == "ru":
        for command in commands_list_ru:
            embed.add_field(name=command["name"], value=command["description"], inline=False)
            embed.set_footer(text="Вы также можете увидеть факты, написанные пользователями, о глобальном потеплении на нашем веб-сайте!")

    
    await ctx.respond(embed=embed)



bot.run(token)
