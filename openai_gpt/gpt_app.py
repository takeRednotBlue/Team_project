from handlers import *
from commands_parser import commands_parser
from openai.error import AuthenticationError, ServiceUnavailableError
import json
import openai
import os 

COMMANDS = {
    'story': set_story
}

END_COMMANS = ['exit', 'good bye', 'close']

def gpt_app():
    while True:
        try:
        
            print(
                '>>> Hello, I\'m your personal bot-assistant.'
            )
            if os.path.exists('key'):
                with open('key', 'r') as fh: openai.api_key = fh.read().strip('"')
            else:
                key = input(
                '>>> pls enter ur open AI key:'
            )
                if key:
                    choose = input(
                '>>> do u wanna save ur API key?, enter yes|not'
            )
                    if choose == 'yes':
                        with open('key','w') as fh:
                            json.dump(key,fh)
                        openai.api_key = key
                    else:
                        openai.api_key = key
                else:
                    gpt_app()
                 
            is_working = True 
            while is_working:
            
                story = 'You are a enceclopedia named "Valera" and trained to explain different topics and terms in short.'
                user_input = input(
                '>>> (valera) '
            )
                command, arguments = commands_parser(user_input)
                if command in COMMANDS:
                    command_handler = COMMANDS[command]
                    story = command_handler(arguments)
                    print(story)
                elif command in END_COMMANS:
                    print(
                '>>> Сподіваюсь ти скоро повернешся та не забудь поповнити свій баланс.'
            )
                    is_working = False
                else:
                    gpt_answer(arguments,
                                story
            )
        except KeyboardInterrupt:
            print(
                '\n>>> Будь ласка, користуйся командами для завершення роботи боту.'
            )
        except AuthenticationError:
            print(
                '>>> упс...відбулася помилка аунтефікації. Будь ласка, введіть коректний API ключ, який можна отримати на сайті: https://platform.openai.com/account/api-keys'
            )
            if os.path.exists('key'):
                os.remove('key')
                gpt_app()
            else:
                gpt_app()
        except ServiceUnavailableError:
            print(
                '>>> на даний момент сервер переповнений, будь ласка, повторіть спробу пізніше або відсутнє підключення до Інтернету'
            )
            gpt_app()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    gpt_app()
    
       
                    