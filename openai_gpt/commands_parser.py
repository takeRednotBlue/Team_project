def commands_parser(input: str) -> tuple:
    words_list = input.split()
    if not words_list:
        return None, None
    
    elif words_list[0].lower() == 'show' or words_list[0].lower() == 'good':
        command = ' '.join(words_list[:2]).lower()
        arguments = words_list[2:]
        
    else:
        command = words_list[0].lower()
        arguments = words_list[1:]
    
    return command, arguments
