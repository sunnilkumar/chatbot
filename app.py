from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = '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'

# Initialize conversation history list
conversation_history = []


# Define the default route to return the index.html file
@app.route("/")
def index():
    # Ajouter la phrase d'introduction à la conversation history
    conversation_history.append({
        "role": "system",
        "content": "Tu es un avocat avec 20 ans d'experience. \n"
    })

    # Retourner le template HTML
    return render_template("index.html")


# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    global conversation_history  # Access the conversation history list

    # Get the message from the POST request
    message = request.json.get("message")

    # Add the user's message to the conversation history
    conversation_history.append({"role": "user", "content": message})

    # Limit the conversation history to the last 5 messages
    conversation_history = conversation_history[-5:]

    # Send the message and conversation history to OpenAI's API and receive the response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history  # Send the entire conversation history
    )

    if completion.choices[0].message != None:
        return completion.choices[0].message
    else:
        return 'Failed to Generate response!'

# Define a route to handle resetting conversation history
@app.route("/reset-history", methods=["POST"])
def reset_history():
    global conversation_history
    conversation_history = []  # Empty the conversation history list
    return "Conversation history reset successfully.", 200

if __name__ == '__main__':
    app.run()
