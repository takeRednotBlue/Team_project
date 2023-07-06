
import os

import openai
from dotenv import load_dotenv
load_dotenv()
# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


def gpt_response(prompt, story):
# Define a conversation with the model
    conversation = [
        {"role": "system", "content": story},
        {"role": "user", "content": prompt},
        # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        # {"role": "user", "content": "Where was it played?"}
    ]

    # Send the conversation to the model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    # Get the model's reply
    reply = response['choices'][0]['message']['content']
    return reply

