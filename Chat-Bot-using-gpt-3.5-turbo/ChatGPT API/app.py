import os
import asyncio
from flask import Flask, render_template, request
import openai
from openai import OpenAI


app = Flask(__name__)

# Set up OpenAI API credentials

client = OpenAI(
    api_key="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",
)

# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="gpt-3.5-turbo",
        )
        if completion.choices[0].message!=None:
            return completion.choices[0].message.content

        else :
            return 'Failed to Generate response!'
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        return "The server could not be reached"
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
        return "A 429 status code was received; we should back off a bit."
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        return "Another non-200-range status code was received + " + str(e.status_code) + " + " + str(e.response)
        
    

if __name__=='__main__':
    app.run()

