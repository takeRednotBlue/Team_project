from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def completer_input(user_prompt: str = '', commands: list[str] = None, complete_while_typing=False) -> str:

    command_completer = WordCompleter(
        commands,
        ignore_case=True,
    )

    user_input = prompt(
                user_prompt, completer=command_completer, complete_while_typing=complete_while_typing
            )
    
    return user_input

