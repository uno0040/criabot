import discord
import asyncio
from discord.ext import commands
import os
from datetime import datetime, timedelta
import pytz
import time
from dotenv import load_dotenv, dotenv_values 
import random

load_dotenv() 

intents = discord.Intents(messages=True, guilds=True)
intents.message_content = True
#client = discord.Client(intents=intents)
client = commands.Bot(command_prefix= "!", intents=intents)

video = "https://cdn.discordapp.com/attachments/404377042012995585/1203877295429783632/sexta_dos_crias.mp4?ex=65d2b11a&is=65c03c1a&hm=1fc268a6279b3cde9a39bd4d14ce983fc5788f079e2ec51a5831f6dc1583daac&"
gif_lilly = "https://tenor.com/view/lilly-satou-katawa-shoujo-gif-23469974"

# tempo de inicio do timer atual caso usuários tentem começar outros timers
# no caso de um timer já estiver ativo
tempo_inicio_timer_atual = ""
tempo_final_timer_atual = ""
# debug do de cima
debug_tempo_inicio_timer_atual = ""
debug_tempo_final_timer_atual = ""
# flag que controla se há um timer sob execução, evitando a criação de um segundo timer
# o segundo timer so mandaria uma cobrança repetida para o caraba
timer_flag = False
# flag para impedir que o caraba seja taxado mais de uma vez
caraba_flag = False

def tempo_ate_sexta():
    '''
    Retorna tempo até as 11:59 da próxima sexta-feira no fuso horário GMT+0.
    '''
    agora = datetime.now(pytz.timezone('GMT0'))
    dias_ate_sexta = (4 - agora.weekday() + 7) % 7
    # adiciona os dias restante para obter a data da próxima sexta
    # funciona caso a sexta seja do mes que vem
    proxima_sexta = agora + timedelta(days=dias_ate_sexta)
    meia_noite_prox_sexta = datetime(proxima_sexta.year, proxima_sexta.month, proxima_sexta.day, 7, 0, 0)
    # 15hrs UTC == 12hrs GMT-3
    agora = agora.replace(tzinfo=None)
    # problema: quando é sexta feira e ja passou da hora, as 15hrs UTC, se a função for chamada novamente ela vai passar um tempo negativo, resultando em um alarme instantaneo.
    # solucao: se for sexta feira depois do alarme, dias_ate_sexta = 7

    if dias_ate_sexta == 0 and (meia_noite_prox_sexta - agora).total_seconds() < 0:
      proxima_sexta = agora + timedelta(days=7)
      meia_noite_prox_sexta = datetime(proxima_sexta.year, proxima_sexta.month, proxima_sexta.day, 7, 0, 0)

    tempo_restante = meia_noite_prox_sexta - agora
    tempo_segundos = tempo_restante.total_seconds()
  
    return int(tempo_segundos)

async def cobrar_caraba():
  global caraba_flag

  # id do caraba: 257639764818264065
  # meu id : 257581347114057748

  caraba = await client.fetch_user(257639764818264065)
  print("Hoje é sexta, cobrando o senhor CarabaloneGraphics ™")
  await caraba.send("Caraba, chegou a hora. MANDE O VIDEO SENHOR CARABALONE GRAPHICS ™")
  await caraba.send(video)
  caraba_flag = False


async def tarefa_timer(ctx, tempo_segundos):
  '''
  Função que executa o timer em segundos de maneira assíncrona, permitindo o bot continuar respondendo outros prompts.
  Parâmetros: ctx ; tempo_segundos: int
  '''
  print("Iniciando timer. \nSegundos de espera: " + str(tempo_segundos))
  dias = tempo_segundos / 86400
  horas_dia = dias - int(dias)
  horas = horas_dia * 24
  int_horas = int(horas)
  minutos_hora = horas - int_horas
  minutos = minutos_hora * 60
  int_minutos = int(minutos)
  segundos = int((minutos - int_minutos) * 60)
  # todo: terminar
  #segundos = tempo_segundos % 60
  print('Em {dias} dias, {horas} horas, {minutos} minutos e {segundos} segundos.'.format(dias=int(dias), horas=int_horas, minutos=int_minutos, segundos=segundos))
  await ctx.send("Cobrando o caraba em {tempo_segundos} segundos.\nOu {dias} dias, {horas} horas, {minutos} minutos e {segundos} segundos para os seres humanos.".format(tempo_segundos=str(tempo_segundos), dias=int(dias), horas=int_horas, minutos=int_minutos, segundos=segundos))
  await asyncio.sleep(tempo_segundos)
  # depois que o timer acabar tudo abaixo da linha acima sera executado
  await ctx.send("Chegou a hora.")
  await cobrar_caraba()
  global timer_flag
  timer_flag = False
  
def dia_da_semana(hoje:int):
  '''
  Recebe o dia da semana do datetime no formato int retorna uma string do dia, se invalido retorna "dia de paz"
  '''
  match(hoje):
    case 0:
      return "segunda-feira"
    case 1:
      return "terça-feira"
    case 2:
      return "quarta-feira"
    case 3:
      return "quinta-feira"
    case 4:
      return "sexta-feira"
    case 5:
      return "sábado-feira"
    case 6:
      return "domingo-feira"
    case _:
      return "dia de paz"
  

@client.event
async def on_ready():
  '''
  Função executa todo o código nela quando o bot faz um login bem sucedido.
  Printa no console que o login foi bem sucedido.
  '''
  print("Login bem sucedido como {0.user}".format(client))


@client.command()
async def cria(ctx):
  '''
  Comando 
  '''
  await ctx.send("Salve, meu propósito é cobrar o senhor CarabaloneGraphics ™")


@client.command()
async def cria_cobra(ctx, user:discord.Member, *, message=None):
  message = "Você foi avisado."
  print("cobrando o senhor:",user.name)
  print("id do homem:", user.id)
  taxa = "Cobrado."
  await ctx.send(taxa)
  await user.send(message)


# id do caraba: 257639764818264065
# meu id : 257581347114057748
# id do nicholas: 275807354623229952
@client.command()
async def sextou(ctx, *, message=None):
  print("comando caraba acionado, checando para ver se hoje é sexta...")
  #hoje é a variavel usada para verificar se hoje é sexta
  #dia é a variavel utilizada para mostrar o dia da semana de hoje que o comédia quis cobrar
  hoje = datetime.today() 
  dia = dia_da_semana(hoje.weekday())

  print("nome do cobrador:",ctx.message.author)
  caraba = await client.fetch_user(257639764818264065)

  if hoje.weekday() == 4:
    print("Hoje é sexta, cobrando o senhor CarabaloneGraphics ™")
    await ctx.send("HOJE É SEXTA, CARABA SERA COBRADO PORRAAAAAAAAAAAAAAA")
    await caraba.send("Caraba, chegou a hora. MANDE O VIDEO SENHOR CARABALONE GRAPHICS ™")
    await caraba.send(video)

  else:
    print("Hoje não é sexta, avisando o senhor caraba que um bagre quis cobrar ele.")

    if hoje.weekday() == 5:
      mensagem = "Irmão o otário do " + ctx.message.author.name + " se acha engraçadão e quer te cobrar em pleno " + dia + ". Fica de olho que esse cara é estranhão jaé?"

    else:
      mensagem = "Irmão o otário do " + ctx.message.author.name + " se acha engraçadão e quer te cobrar em plena " + dia + ". Fica de olho que esse cara é estranhão jaé?"

    await ctx.send("O comédia, hoje não é sexta não criança.")
    await caraba.send(mensagem)    

@client.command()
async def caraba(ctx, *, message=None):
  global caraba_flag
  # checa se o caraba ja esta a caminho de ser cobrado
  if caraba_flag == False:
    segundos_ate_sexta = tempo_ate_sexta()
    caraba_flag = True
    caraba_timezone = datetime.now(pytz.timezone('GMT0'))
    target_time = caraba_timezone + timedelta(seconds=segundos_ate_sexta)
    print("Preparando para cobrar o caraba em:", segundos_ate_sexta, "segundos.")
    print("Hora estimada de envio da mensagem:", target_time.strftime("%d-%m-%Y, %H:%M:%S"), "UTC")
    asyncio.create_task(tarefa_timer(ctx, segundos_ate_sexta))

  else:
    # se sim:
    await ctx.send("O homem será taxado.")

@client.command()
async def nicholas(ctx, *, message=None):
  usuario = await client.fetch_user(275807354623229952) # bongolas
  # usuario = await client.fetch_user(257581347114057748) # eu

  mensagens = [
    "Tá fugindo da Lilly, Nicholas? Ela pode não ver o caminho, mas vê quem foge!",
    "A Lilly tá lá esperando, Nicholas… ou você vai deixar ela plantada no chá pra sempre?",
    "Você parou no meio, Nicholas… e a Lilly só queria que você segurasse a mão dela até o fim.",
    "Lilly confiou na sua palavra, Nicholas… pena que você confiou no botão de sair.",
    "A Lilly pode ser cega, mas ela viu que você largou ela na metade.",
    "Tem gente que atravessa oceanos pelo amor… e tem o Nicholas, que não atravessa nem o save file.",
    "E aí, Nicholas, a bengala da Lilly é pra se guiar… ou pra bater em quem não termina a rota dela?",
    "Enquanto você pensa, Nicholas, a Lilly tá lá, servindo chá… sozinha.",
    "A rota da Lilly não termina sozinha, Nicholas… só seu comprometimento que terminou.",
    "Nicholas, a Lilly já perdoou muita coisa… mas abandonar ela na metade é imperdoável.",
    "E a Lilly, hein Nicholas? Ela pode ser cega, mas ela vê seus vacilos."
  ]

  msg_enviada = mensagens[random.randint(0,10)]
  print(msg_enviada)
  print("Bingolando o Bingolas")
  await ctx.send("Ele será bingolado.")
  await usuario.send(msg_enviada)
  await usuario.send(gif_lilly)

client.run(os.getenv('BOT_KEY'))