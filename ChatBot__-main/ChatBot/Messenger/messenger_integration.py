# messenger/messenger_integration.py
from flask import Flask, request, jsonify
from bot.bot import chatbot  # Importing the chatbot function from bot.py

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    user_input = data.get('message').get('text')
    sender_id = data.get('sender').get('id')

    bot_response = chatbot(user_input)
    
    # You would need to handle sending responses back to Messenger here
    # For now, we'll just print the response
    
    print(f"User: {user_input}")
    print(f"Bot: {bot_response}")

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(port=5000)
