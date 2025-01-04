import discord
from discord.ext import commands
import asyncio
import time

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='+', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')

@bot.command()
async def dmall(ctx, *, message):
    if any(role.permissions.administrator for role in ctx.author.roles):
        members_to_message = [member for member in ctx.guild.members if not member.bot]
        batch_size = 10  
        delay_between_batches = 10  
        delay_between_messages = 1  

        for i in range(0, len(members_to_message), batch_size):
            batch = members_to_message[i:i+batch_size] 

            for member in batch:
                try:
                    await member.send(message)
                    print(f"Message envoyé à {member.name}")
                    await asyncio.sleep(delay_between_messages)  
                except discord.errors.Forbidden:
                    print(f"Impossible d'envoyer un message à {member.name} (interdiction de DM)")
                except discord.errors.HTTPException as e:
                    if e.status == 429:

                        print(f"Rate limit atteint, attente... (Erreur 429)")
                        retry_after = e.response.get("Retry-After", 5)  
                        await asyncio.sleep(retry_after) 
                    else:
                        print(f"Erreur HTTP lors de l'envoi du message à {member.name}: {e}")
                except Exception as e:
                    print(f"Erreur lors de l'envoi du message à {member.name}: {e}")

            print(f"groupe de {len(batch)} messages envoyés.")

           
            if i + batch_size < len(members_to_message):
                print(f"Attente de {delay_between_batches} secondes avant d'envoyer le prochain groupe...")
                await asyncio.sleep(delay_between_batches)

        print("Tous les messages ont été envoyés.")
    else:
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")

@bot.command(name="customhelp")
async def help_command(ctx):
    help_message = (
        "+dmall [message] : Envoie un message privé à tous les membres du serveur.\n"
        "+customhelp : Affiche la liste des commandes disponibles."
    )
    await ctx.send(help_message)

# 'YOUR_TOKEN_HERE'= le token de votre bot
bot.run('YOUR_TOKEN_HERE')
