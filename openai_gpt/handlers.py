from gpt_response import gpt_response



def set_story(args: list) -> None:
    story = ' '.join(args)
    return story


def gpt_answer(args: list, story: str) -> None:
    prompt = ' '.join(args)
    response = gpt_response(prompt, story)
    
    
    print(f'ur unswer:\n{response}\n')
