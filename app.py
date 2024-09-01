import sys
from configparser import ConfigParser 
from Chatbot import ChatBot

def main():
    # Load API key from configuration file
    config = ConfigParser()
    config.read('credentials.ini')
    api_key = config['gemini_api']['API_KEY']

    # Initialize chatbot
    chatbot = ChatBot(api_key=api_key)
    chatbot.start_conversation()

    print("Welcome to jakir's Bot supported by Gemini CLI")

    # Main chatbot loop
    while True:
        user_input = input("YOU: ")
        if user_input.lower() == "quit":
            sys.exit("Exiting chatbot...")

        try:
            response = chatbot.send_prompt(user_input)
            print(f"{chatbot.CHATBOT_NAME}: {response}")
        except Exception as e:
            print(f"Error: {e}")

# Entry point of the script
if __name__ == "__main__":
    main()
