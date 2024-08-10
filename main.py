import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from ai import AI

from random import randint, choice
from datetime import datetime

#TODO : 
	#reset

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SERGE_CHAR_TOKEN = os.getenv('SERGE_CHAR_TOKEN')
CAI_CLIENT_TOKEN = os.getenv('CAI_CLIENT_TOKEN')
MYLO_DISCORD_ID = int(os.getenv('MYLO_DISCORD_ID'))

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = '!', intents = intents)

ai = AI(SERGE_CHAR_TOKEN, CAI_CLIENT_TOKEN)

@bot.event
async def on_ready() -> None:
	try:
		synced = await bot.tree.sync()
		print(f'Synced {len(synced)} commands')

		await ai.connect()
		print("connected to Character AI")

	except Exception as e:
		print(e)

	print(f'{bot.user.name} is ready !')


@bot.event
async def on_message(message, interaction = discord.Interaction):
	username = str(message.author)
	user_message = message.content
	channel = str(message.channel)

	print(f'{channel} | {username} : {user_message}')

	if message.author.bot:
		return

	if 'café' in message.content.lower() or 'cookie' in message.content.lower() or 'gaston' in message.content.lower():
		if 'café' in message.content.lower():
			await message.add_reaction('☕')
		if 'cookie' in message.content.lower():
			await message.add_reaction('🍪')
		if 'gaston' in message.content.lower():
			await message.add_reaction("<:gastonwhat:994375129679265792>")

	if randint(1, 4096) == 1:
		print(f'{username} sent a shiny message !')
		await message.add_reaction('✨')
		await message.reply("Bravo ! Vous venez d'envoyer un message :sparkles:**SHINY**:sparkles: !")

	if bot.user.mentioned_in(message) or message.guild is None:
		print(f'{username} asked from ai, waiting for answer...')

		prompt = message.content.replace("<@1270422152583053435>", "")
		
		try:
			answer = await ai.send_serge(prompt, message.author.display_name)
			print(f'answer for {username} got !')
			if message.guild != None:
				await message.reply(answer)
			else:
				await message.author.send(answer)
		except Exception as e:
			print(e)
			await message.author.send("Veuillez m'excuser, mon IA à eu une erreur en essayant de vous répondre :\n" + str(e))


@bot.tree.command(name = 'help', description = "Envoie la documentation")
async def help_slash(interaction : discord.Interaction):
	await interaction.response.send_message("Voici ma documentation :\nhttps://docs.google.com/document/d/1j6cd-iMmG14l6B4xuUAMYGfkEo00qKB0opaGiYQOaK4/edit?usp=sharing")

@bot.tree.command(name = 'time', description = "Donne l'heure")
async def time_slash(interaction : discord.Interaction):
	time = datetime.now().strftime("%H:%M:%S")
	heure = int(time[:2])
	message = ""
	if heure <= 5:
		message = "Ne devriez-vous pas être couché ?"
	elif heure <= 11:
		message = "Bonne matiné à vous !"
	elif heure <= 12:
		message = "Souhaitez dejeuner ?"
	elif heure <= 17:
		message = "C'est l'après-midi."
	elif heure <= 18:
		message = "C'est le soir."
	elif heure <= 20:
		message = "C'est l'heure de souper."
	else:
		message = "C'est le soir. Ne vous couchez pas trop tard !"
	await interaction.response.send_message(f"Il est actuellement : {time}. {message}")


@bot.tree.command(name = 'roll', description = "Donne un nombre aléatoire")
async def roll_slash(interaction : discord.Interaction, min : int, max : int):
	await interaction.response.send_message(f"vous avez tirez le numéro : {randint(min, max)}")


@bot.tree.command(name = 'pfc', description = "Jouez à pierre feuille ciseaux avec moi.")
async def rps_slash(interaction : discord.Interaction, choix : str):
	chart = {"pierre":"ciseaux", "ciseaux":"feuille", "feuille":"pierre"}
	serge_choice = choice(["pierre", "feuille", "ciseaux"])
	choix = choix.lower()
	if choix in ["pierre", "p"]:
		choix = "pierre"
	elif choix in ["feuille", "f"]:
		choix = "feuille"
	elif choix in ["ciseaux", "c"]:
		choix = "ciseaux"
	else:
		choix = None
	if choix == None:
		await interaction.response.send_message(f'vous devez choisir entre "pierre", "feuille" et "ciseaux" (ou "p", "f" et "c").', ephemeral=True)	
	elif chart[serge_choice] == choix:	
		await interaction.response.send_message(f"Je choisis : {serge_choice},\n{serge_choice} bat {choix}, j'ai gagné. Encore une preuve de la superiorité des IA.")
	elif chart[choix] == serge_choice: 
		await interaction.response.send_message(f"Je choisis : {serge_choice},\n{choix} bat {serge_choice}, vous avez gagné. Bien joué.")
	elif choix == serge_choice:
		await interaction.response.send_message(f"Je choisis : {serge_choice},\nEgalité !.")


@bot.tree.command(name = 'choose', description = "choisis aléatoirement entre plusieurs termes séparé de virgules")
async def choose_slash(interaction : discord.Interaction, termes : str):
	list_termes = termes.split(",")

	if len(list_termes) <= 1:
		await interaction.response.send_message(f"Vous devez donner au moins 2 termes.", ephemeral=True)
		return

	m = "Entre "
	for i in range(len(list_termes)):
		m += list_termes[i]
		if i != len(list_termes)-1:
			if list_termes[i] == list_termes[-2]:
				m += " et "
			else:
				m += ", "
	await interaction.response.send_message(f"{m}\nJe choisis : {choice(list_termes)}")


@bot.tree.command(name = '8b', description = "Répond à une question fermée")
async def eight_ball_slash(interaction : discord.Interaction, question : str):
	answers = ['Tout a fait !', 'Il se pourrait bien...', 'Oui.', 'Bien-sûr, Comme tout le monde', 'Non.', 'Oh que non !', 'Jamais de la vie !', 'Et bien pourquoi pas ?']
	await interaction.response.send_message(f'"{question}"\n{choice(answers)}')


@bot.tree.command(name = 'avatar', description = "Renvoie l'avatar d'un membre")
async def avatar_slash(interaction : discord.Interaction, membre : discord.User = None):
	if membre is None:
		membre = interaction.user

	if membre.avatar is None:
		embed = discord.Embed(title=f"{membre.name} ne possède pas d'avatar... Petit manque de personalité de sa part.")
	else:
		embed = discord.Embed(title= f"Voici le magnifique avatar de {membre.name} :")
		embed.set_image(url=membre.avatar.url)

	await interaction.response.send_message(embed = embed)


# @bot.tree.command(name = 'reset', description = 'Démarre une nouvelle conversation.')
# async def reset_slash(interaction : discord.Interaction):
# 	print("new chat")
# 	await ai.new_chat()
# 	embed = discord.Embed(title = 'Nouveau chat')
# 	await interaction.response.send_message(embed=embed)


@bot.tree.command(name = 'quit', description = 'Arrête le bot')
async def quit_slash(interaction : discord.Interaction):
	if interaction.user.id != MYLO_DISCORD_ID:
		await interaction.response.send_message("Vous n'avez pas les droits pour utiliser cette commande.", ephemeral=True)
	else:
		await interaction.response.send_message("Passez une agréable soirée.")
		print("Quitting...")
		await bot.close()
		exit()


if __name__ == '__main__':
	bot.run(token=DISCORD_TOKEN)