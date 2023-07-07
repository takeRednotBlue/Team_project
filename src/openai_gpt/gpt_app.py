from handlers import *
# from utilities.commands_parser import commands_parser
from commands_parser import commands_parser

COMMANDS = {
    'story': set_story
}

END_COMMANS = ['exit', 'good bye', 'close']


def gpt_app():

    is_working = True
    print('Hello, I\'m your personal bot-assistant.')
    story = "You are a enceclopedia named 'Valera' and trained to explain different topics and terms in short."

    while is_working:
        
        user_input = input('>>> (valera) ')
        command, arguments = commands_parser(user_input)
        if command in COMMANDS:
            command_handler = COMMANDS[command]
            story = command_handler(arguments)
            print(story)
        elif command in END_COMMANS:
            print('Сподіваюсь ти скоро повернешся та не забудь поповнити свій баланс.')
            is_working = False
        else:
            gpt_answer(arguments, story)

if __name__ == "__main__":
    try:
        gpt_app()
    except KeyboardInterrupt:
        print('\nБудь ласка, користуйся командами для завершення роботи боту.')