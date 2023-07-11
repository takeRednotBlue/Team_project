import json
import os 
import openai
from openai.error import AuthenticationError, ServiceUnavailableError, APIConnectionError

from openai_gpt.handlers import *
from utilities import commands_parser


def set_story(args: list) -> None:
    story = ' '.join(args)
    return story



COMMANDS = {
    'story': set_story
}

END_COMMANS = ['exit', 'good bye', 'close']

def gpt_app():
    try:
        file_path = os.path.join(os.path.expanduser("~"), "key.json")
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as fh:
                openai.api_key = fh.read().strip('"')
        else:
            key = input('>>> будь ласка, введіть ключ AI:')
            if key:
                choose = input('>>> ви хочете зберегти свій ключ API?, введіть так|ні:')
                if choose == 'так':
                    with open(file_path, 'w') as fh:
                        json.dump(key, fh)
                    openai.api_key = key
                    print('>>> Ваш ключ успiшно збережено')
                else:
                    openai.api_key = key
            else:
                gpt_app()

        is_working = True
        while is_working:
            story = 'Ви - енциклопедія під назвою "Валера" і навчені коротко пояснювати різні теми та терміни.'
            user_input = input('>>> (valera) ')

            command, arguments = commands_parser(user_input)
            if command in COMMANDS:
                command_handler = COMMANDS[command]
                story = command_handler(arguments)
                print(story)
            elif command in END_COMMANS:
                print('>>> Сподіваюсь, ти скоро повернешся та не забудеш поповнити свій баланс.')
                is_working = False
            else:
                gpt_answer(arguments, story)

    except KeyboardInterrupt:
        print('\n>>> Будь ласка, користуйся командами для завершення роботи боту.')
    except AuthenticationError:
        print('>>> Упс... відбулася помилка аутентифікації. Будь ласка, введи коректний API ключ, який можна отримати на сайті: https://platform.openai.com/account/api-keys')
        if os.path.exists(file_path):
            os.remove(file_path)
            gpt_app()
        else:
            gpt_app()
    except ServiceUnavailableError:
        print('>>> На даний момент сервер переповнений. Будь ласка, повтори спробу пізніше або перевір з\'єднання з Інтернетом.')
        gpt_app()
    except APIConnectionError:
        print('>>> будь ласка перевірте своє поєднання з інтернетом')
        gpt_app()

if __name__ == "__main__":
    print('Привіт, це короткий гайд використання бота помічника:\
перше що тобі потрібно зробити це ввести коректний API ключ, який можна отримати на сайті: https://platform.openai.com/account/api-keys, якщо у вас немає коштів на балансі - бот працювати не буде. Якщо ключ введено або вказано неправильно - після перевірки бот запросить ввести його по-новому. Далі потрібно буде ввести питання, що цікавить тебе, і бот з радістю відповість на всі питання) Вихід з бота здійснюється командами exit, good byе, close')
    print('>>> Привіт, я ваш персональний бот-помічник.\n')
    gpt_app()

       
                    