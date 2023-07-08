import os
import openai

def gpt_response(prompt, story,):
# Define a conversation with the model
    conversation = [
        {
        "role": "system", 
        "content": story
            },                               
        {
            "role": "user", 
            "content": prompt
        },
    ]

    # Send the conversation to the model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    # Get the model's reply
    reply = response['choices'][0]['message']['content']
    if len(reply) != 0:
        return reply
    else:
        return False

