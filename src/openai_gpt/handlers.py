import time
import threading
from .gpt_response import gpt_response

response_received = False

def show_loading_animation():
    global response_received
    animation = "|/-\\"
    i = 0
    while True:
        print("Waiting for model response... " + animation[i % len(animation)], end="\r")
        i += 1
        time.sleep(0.1)

        # Break the loop when response is received
        if response_received:
            break

def set_story(args: list) -> None:
    story = ' '.join(args)
    return story
    

def gpt_answer(args: list, story: str) -> None:
    global response_received 
    prompt = ' '.join(args)
    animation_thread = threading.Thread(target=show_loading_animation)
    animation_thread.start()
    response = gpt_response(prompt, story)
    response_received = True
    animation_thread.join()
    # index = 0
    # while index < len(response):
    #     print(response[index:index+90])
    #     index += 90

    print(f'\n{response}\n')
