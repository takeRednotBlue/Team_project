# from openai_gpt import gpt_app
# from cli_bot import address_book_app
from utilities import completer_input, kb_interrupt_error
from logo import LOGO
from notebook import note_book


def exit_bot():
    print('Чекаю твого найшвидшого повернення!')

def print_menu():
    print(
        f'''
        {LOGO}
                        Menu
                        1. Address book
                        2. Notebook
                        3. File sorter
                        4. Ask gpt
                        0. Exit
        '''
    )

MENU_MAPING = {
    ('1', "Address book"): None,
    ('2', "Notebook"): note_book,
    ('3', "File sorter"): None,
    ('4', "Ask gpt"): None,
    ('0', "Exit"): None,
}

menu_commands_list = []

for _, command in MENU_MAPING:
    menu_commands_list.append(command)

@kb_interrupt_error
def main():
    is_working = True

    while is_working:
        print_menu()
        print('Виберіть програму з якою хочете працювати.')
        valid_input = False
        
        while not valid_input:
            user_input = completer_input('>>> ', menu_commands_list)
            for menu_line, app in MENU_MAPING.items():
                if user_input.strip().startswith(menu_line):
                    app()
                    valid_input = True
                    break
                elif user_input.strip().lower().startswith('0'):
                    exit_bot()
                    valid_input = True
                    is_working = False
                    break
            else:
                print('Невірно введений пункт меню. Спробуйте ще раз.')


        
if __name__ == '__main__':
    main()
   

