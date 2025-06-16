from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chatbot
chatbot = ChatBot('PortfolioBot')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot with English corpus
trainer.train("chatterbot.corpus.english")

# Function to get a response from the chatbot
def get_response(message):
    return chatbot.get_response(message)

