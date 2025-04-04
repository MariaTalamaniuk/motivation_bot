import telebot
from telebot import types
import random

TOKEN = '7736017272:AAG5nEOE7_NLGQTRsgNOvOgu-HFqos-Zru8'
bot = telebot.TeleBot(TOKEN)

quotes = []

user_language = {}

def get_main_keyboard(language='en'):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    if language == 'pt':
        markup.add(
            types.KeyboardButton('Adicionar Citação'),
            types.KeyboardButton('Ver Citações'),
            types.KeyboardButton('Citação Aleatória'),
            types.KeyboardButton('Editar Citação'),
            types.KeyboardButton('Remover Citação'),
            types.KeyboardButton('Mudar Idioma')
        )
    else:
        markup.add(
            types.KeyboardButton('Add Quote'),
            types.KeyboardButton('View Quotes'),
            types.KeyboardButton('Random Quote'),
            types.KeyboardButton('Edit Quote'),
            types.KeyboardButton('Remove Quote'),
            types.KeyboardButton('Change Language')
        )
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.chat.id not in user_language:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            types.KeyboardButton('English'),
            types.KeyboardButton('Português')
        )
        bot.send_message(message.chat.id, "Please choose your language / Por favor, escolha seu idioma:", reply_markup=markup)
    else:
        language = user_language[message.chat.id]
        welcome_text = """
        Welcome to the Motivational Quotes Bot!

        Use the buttons below to interact with the bot or send a command.

        Available commands:
        - Add Quote: Add a new quote
        - View Quotes: View all quotes
        - Random Quote: Get a random motivational quote
        - Edit Quote: Edit an existing quote
        - Remove Quote: Remove an existing quote
        """
        if language == 'pt':
            welcome_text = """
            Bem-vindo ao Bot de Citações Motivacionais!

            Use os botões abaixo para interagir com o bot ou enviar um comando.

            Comandos disponíveis:
            - Adicionar Citação: Adicione uma nova citação
            - Ver Citações: Veja todas as citações
            - Citação Aleatória: Obtenha uma citação motivacional aleatória
            - Editar Citação: Edite uma citação existente
            - Remover Citação: Remova uma citação existente
            """
        bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard(language))

@bot.message_handler(func=lambda message: message.text in ['English', 'Português'])
def set_language(message):
    if message.text == 'English':
        user_language[message.chat.id] = 'en'
    else:
        user_language[message.chat.id] = 'pt'

    language = user_language[message.chat.id]
    welcome_text = """
    Welcome to the Motivational Quotes Bot!

    Use the buttons below to interact with the bot or send a command.

    Available commands:
    - Add Quote: Add a new quote
    - View Quotes: View all quotes
    - Random Quote: Get a random motivational quote
    - Edit Quote: Edit an existing quote
    - Remove Quote: Remove an existing quote
    """
    if language == 'pt':
        welcome_text = """
        Bem-vindo ao Bot de Citações Motivacionais!

        Use os botões abaixo para interagir com o bot ou enviar um comando.

        Comandos disponíveis:
        - Adicionar Citação: Adicione uma nova citação
        - Ver Citações: Veja todas as citações
        - Citação Aleatória: Obtenha uma citação motivacional aleatória
        - Editar Citação: Edite uma citação existente
        - Remover Citação: Remova uma citação existente
        """
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard(language))

@bot.message_handler(func=lambda message: message.text == 'Change Language' or message.text == 'Mudar Idioma')
def change_language(message):
    language = user_language.get(message.chat.id, 'en')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton('English'),
        types.KeyboardButton('Português')
    )
    bot.send_message(message.chat.id, "Please choose a new language / Por favor, escolha um novo idioma:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    language = user_language.get(message.chat.id, 'en')
    text = message.text

    if text == ('Add Quote' if language == 'en' else 'Adicionar Citação'):
        msg = bot.send_message(message.chat.id, "Please enter the quote you want to add:" if language == 'en' else "Por favor, insira a citação que você deseja adicionar:")
        bot.register_next_step_handler(msg, add_quote)
    elif text == ('View Quotes' if language == 'en' else 'Ver Citações'):
        view_quotes(message, language)
    elif text == ('Random Quote' if language == 'en' else 'Citação Aleatória'):
        random_quote(message, language)
    elif text == ('Edit Quote' if language == 'en' else 'Editar Citação'):
        msg = bot.send_message(message.chat.id, "Please enter the number of the quote you want to edit:" if language == 'en' else "Por favor, insira o número da citação que você deseja editar:")
        bot.register_next_step_handler(msg, edit_quote_step1)
    elif text == ('Remove Quote' if language == 'en' else 'Remover Citação'):
        msg = bot.send_message(message.chat.id, "Please enter the number of the quote you want to remove:" if language == 'en' else "Por favor, insira o número da citação que você deseja remover:")
        bot.register_next_step_handler(msg, remove_quote)
    else:
        bot.send_message(message.chat.id, "Unknown command. Please use the menu buttons." if language == 'en' else "Comando desconhecido. Por favor, use os botões do menu.", reply_markup=get_main_keyboard(language))

def add_quote(message):
    quote = message.text.strip()
    if quote:
        quotes.append(quote)
        bot.send_message(message.chat.id, f'Quote added: "{quote}"', reply_markup=get_main_keyboard(user_language.get(message.chat.id, 'en')))
    else:
        bot.send_message(message.chat.id, 'Quote text cannot be empty.' , reply_markup=get_main_keyboard(user_language.get(message.chat.id, 'en')))

def view_quotes(message, language):
    if quotes:
        quote_list = "\n".join([f"{idx + 1}. {q}" for idx, q in enumerate(quotes)])
        bot.send_message(message.chat.id, "List of Quotes:\n" + quote_list if language == 'en' else "Lista de Citações:\n" + quote_list, reply_markup=get_main_keyboard(language))
    else:
        bot.send_message(message.chat.id, "No quotes added yet." if language == 'en' else "Ainda não há citações adicionadas.", reply_markup=get_main_keyboard(language))

def random_quote(message, language):
    if quotes:
        quote = random.choice(quotes)
        bot.send_message(message.chat.id, quote, reply_markup=get_main_keyboard(language))
    else:
        bot.send_message(message.chat.id, "No quotes available. Add some first!" if language == 'en' else "Não há citações disponíveis. Adicione algumas primeiro!", reply_markup=get_main_keyboard(language))

def edit_quote_step1(message):
    index = int(message.text) - 1
    if 0 <= index < len(quotes):
        msg = bot.send_message(message.chat.id, "Enter the new text for the quote:" if user_language.get(message.chat.id, 'en') == 'en' else "Insira o novo texto para a citação:")
        bot.register_next_step_handler(msg, lambda msg: edit_quote_step2(msg, index))
    else:
        bot.send_message(message.chat.id, "Invalid quote number.", reply_markup=get_main_keyboard(user_language.get(message.chat.id, 'en')))

def edit_quote_step2(message, index):
    new_text = message.text.strip()
    if new_text:
        quotes[index] = new_text
        bot.send_message(message.chat.id, "Quote updated successfully.", reply_markup=get_main_keyboard(user_language.get(message.chat.id, 'en')))
    else:
        bot.send_message(message.chat.id, "Quote text cannot be empty.", reply_markup=get_main_keyboard(user_language.get(message.chat.id, 'en')))

def remove_quote(message):
    index = int(message.text) - 1
    if 0 <= index < len(quotes):
        removed_quote = quotes.pop(index)
        bot.send_message(message.chat.id, f"Removed quote: '{removed_quote}'", reply_markup=get_main_keyboard(user_language.get(message.chat.id, 'en')))
    else:
        bot.send_message(message.chat.id, "Invalid quote number.", reply_markup=get_main_keyboard(user_language.get(message.chat.id, 'en')))

bot.polling(none_stop=True)
