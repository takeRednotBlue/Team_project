from openai_gpt.gpt_response import gpt_response




def set_story(args: list) -> None:
    story = ' '.join(args)
    return story



def gpt_answer(args: list, story: str) -> None:
    prompt = ' '.join(args)
    print('я думаю... зачекайте будь ласка')
    response = gpt_response(prompt, story)
    
    print(f'твоя відповідь:\n{response}\n')
