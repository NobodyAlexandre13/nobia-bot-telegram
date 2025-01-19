import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
import telebot
from langchain_community.document_loaders import PyPDFLoader

# CRIADO POR ALEXANDRE SAMPAIO

# Puxando dados do PDF para informar sobre mim 
caminho = 'Profile.pdf'
loader = PyPDFLoader(caminho)
lista_documentos = loader.load()

documento = ''
for doc in lista_documentos:
    documento = documento + doc.page_content

api_key = 'API-DO-LANGCHAIN'
os.environ['GROQ_API_KEY'] = api_key
chat = ChatGroq(model='llama-3.3-70b-versatile')

KEY_BOT = 'API-DO-BOT-TELEGRAM'
bot = telebot.TeleBot(KEY_BOT)

#Função para o comando /start
@bot.message_handler(commands=["start"])
def comando_ajuda(msg):
    bot.reply_to(msg, """
        Olá! Eu sou a NobIa!

        ESSES SÃO ALGUNS DOS MEUS COMANDOS:

        /start
        /ajuda
        /criador
        /sobre
        /traduzir

        Ou envia uma mensagem
    """)

#Função para o comando /ajuda
@bot.message_handler(commands=["ajuda"])
def comando_ajuda(msg):
    bot.reply_to(msg, "Olá! Eu sou a NobIa, como posso ajudar-te?!")

@bot.message_handler(commands=["criador"])
def comando_criador(msg):
    bot.reply_to(msg, 'O que queres saber Alexandre Sampaio')

@bot.message_handler(commands=["sobre"])
def comando_sobre(msg):
    bot.reply_to(msg, "Sou uma assistente virtual chamada NobIa. Posso ajudar com tradução, responder perguntas e muito mais!")

@bot.message_handler(commands=["traduzir"])
def comando_traduzir(msg):
    bot.reply_to(msg, "Para traduzir algo, basta enviar o texto que deseja traduzir e língua que pretende traduzir o texto, e eu ajudarei com prazer!")

    @bot.message_handler(func=lambda message: True)
    def tradutor(msg):
        sms = msg.text.lower()

        template = ChatPromptTemplate.from_messages([
            ('system', 'Você é uma assistente amigável chamada NobIa que traduz qualquer texto'),
            ('user', '{input}')
        ])
        chain = template | chat

        traduzido = chain.invoke({'input': sms})
        bot.reply_to(msg, tradutor.content)

@bot.message_handler(func=lambda message: True)
def responder_mensagem(msg):
    texto = msg.text.lower()
    print(texto)
    template = ChatPromptTemplate.from_messages([
        ('system', '''Você é uma assistente amigável chamada NobIa que ajuda com 
                    qualquer assunto e aqui tu tens mais informações sobre o teu criador {info_creator}.'''),
        ('user', '{input}')
    ])
    
    chain = template | chat
    
    resp = chain.invoke({'info_creator': documento, 'input': texto})
    
    bot.reply_to(msg, resp.content)
    print(resp.content)
    
bot.infinity_polling()
