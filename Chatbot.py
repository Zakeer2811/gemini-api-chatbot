import google.generativeai as genai

# Define a custom exception for the chatbot
class GenAIException(Exception):
    """GenAI Exception base class"""
    pass

class ChatBot:
    CHATBOT_NAME = "jakir's bot"

    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel('gemini-pro')
        self.conversation = None
        self._conversation_history = []
        self.preload_conversation()

    def send_prompt(self, prompt, temperature=0.1):
        if temperature < 0 or temperature > 1:
            raise GenAIException('temperature must be between 0 and 1')
        if not prompt:
            raise GenAIException('prompt cannot be empty')
        try:
            response = self.conversation.send_message(
                content=prompt,
                generation_config=self._generation_config(temperature)
            )
            response.resolve()
            return f'{response.text}\n' + "-------" * 20
        except Exception as e:
            raise GenAIException(str(e))

    @property
    def history(self):
        conversation_history = [
            {'role': message.role, 'text': message.parts[0].text} for message in self.conversation.history
        ]
        return conversation_history

    def clear_conversation(self):
        self.conversation = self.model.start_chat(history=[])

    def start_conversation(self):
        self.conversation = self.model.start_chat(history=self._conversation_history)

    def _generation_config(self, temperature):
        return genai.types.GenerationConfig(
            temperature=temperature
        )

    def _construct_message(self, text, role='user'):
        return {
            'role': role,
            'parts': [text]
        }

    def preload_conversation(self, conversation_history=None):
        if isinstance(conversation_history, list):
            self._conversation_history = conversation_history
        else:
            self._conversation_history = [
                self._construct_message(
                    'from now onwards return the output of a JSON object that can be loaded in python with key as \'text\'.'),
                self._construct_message(
                    '{"text":"Sure, I can return the output as a regular JSON object with the key as \'text\'. Here is an example: {"text":"Your OUTPUT"}."}', 'model')
            ]
