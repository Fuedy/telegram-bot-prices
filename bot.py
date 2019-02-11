from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import csv
import io
import time

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(token='792809349:AAGBkNF6OINbQ6hQv1heLK0Jdii28zcwk7k')
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Oi, sou o bot de precos. Envie pra mim um GTIN que eu te devolvo os precos")

def getPrices(bot, update):
    resposta = ''
    listaVendedores = []
    listaPrecos = []

    #Define as opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless") #Ativa o modo sem janelas
    chrome_options.add_argument("--window-size=1920x1080") #Define a resolução da janela
    browser = webdriver.Chrome(options=chrome_options, executable_path='./chromedriver') #Inicia o browser passando as opções e o caminho do browser

    codigoProduto = update.message.text
    codigoProduto = codigoProduto.rstrip()
    bot.send_message(chat_id=update.message.chat_id, text='Buscando o produto ' + str(codigoProduto) + '...')

    print("Buscando preços do produto: " + codigoProduto + "... Deve demorar alguns segundos")

    browser.get('https://www.google.com.br/search?tbm=shop&hl=pt-BR&q='+ codigoProduto) #Navega até a página pedida
    time.sleep(1)
    try:
        browser.find_element_by_class_name("sh-dlr__thumbnail").click() #Procura o elemento e clica
        time.sleep(1)
        browser.find_element_by_partial_link_text("Comparar preços de").click()
        time.sleep(1)
        browser.find_element_by_id("os-price-col-txt").click()
        time.sleep(1)
        vendedores = browser.find_element_by_id('os-sellers-table').find_elements_by_class_name('os-seller-name') #Pega todos os nomes de vendedores e coloca num vetor
        precos = browser.find_element_by_id('os-sellers-table').find_elements_by_class_name('os-price-col') #Pega todos os preços e coloca num vetor

        #Extrai apenas os textos dos elementos
        for vendedor in vendedores:
            listaVendedores.append(vendedor.text)

        #Extrai apenas os textos dos elementos
        for preco in precos:
            listaPrecos.append(preco.text)

        #Cria o CSV com os vetores de vendedores e preços
        print(listaVendedores)
        print(listaPrecos)

        # resposta = str(listaVendedores) + '   '  + str(listaPrecos)

        for i in range(0,len(vendedores)):
            resposta = resposta + str(listaVendedores[i]) + ' : ' + str(listaPrecos[i+1]) + "\n"



    except NoSuchElementException as e:
        resposta = "Erro2 ao buscar esse produto"
        print(str(e))

    #Fecha o browser
    browser.close()
    print("Todos os precos foram atualizados")

    bot.send_message(chat_id=update.message.chat_id, text=resposta)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

getPrices_handler = MessageHandler(Filters.text, getPrices)
dispatcher.add_handler(getPrices_handler)

updater.start_polling()