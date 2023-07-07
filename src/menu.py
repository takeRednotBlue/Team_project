from openai_gpt import gpt_app
from cli_bot import address_book_app
from logo import LOGO, NEW_LOGO
def exit_bot():
    print('Чекаю твого найшвидшого повернення!')

def print_menu():
    print(
        f'''
        {NEW_LOGO}
                        Menu
                        1. Address book
                        2. Notebook
                        3. File sorter
                        4. Ask gpt
                        5. Exit
        '''
    )

MENU_MAPING = {
    ('1', "Address book"): address_book_app,
    ('2', "Notebook"): None,
    ('3', "File sorter"): None,
    ('4', "Ask gpt"): gpt_app,
    ('5', "Exit"): None,
}

def main():
    is_working = True
    program_start = True

    # if program_start:
    while is_working:
        print_menu()
        print('Виберіть програму з якою хочете працювати.')
        user_input = input('>>> ')
        for menu_line, app in MENU_MAPING.items():
            if user_input.strip().startswith(menu_line):
                app()
                break
            elif user_input.strip().startswith('exit'):
                exit_bot()
                is_working = False
                break
        else:
            print('Невірно введений пункт меню. Спробуйте ще раз.')
        
if __name__ == '__main__':
    main()
   

