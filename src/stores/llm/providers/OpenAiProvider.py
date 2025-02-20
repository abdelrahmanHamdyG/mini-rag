from ..LLMInterface import LLMInterface
from helpers import Logger
from ..LLMEnums import LLMEnums 
import openai

class OpenAiProvider(LLMInterface):
    
    def __init__(self, api_key: str, api_url: str, 
                 default_input_max_charachters: int = 1000,
                 default_generation_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_charachters = default_input_max_charachters
        self.default_generation_max_characters = default_generation_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature
        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        # Configure the OpenAI module
        openai.api_key = self.api_key
        if self.api_url:
            openai.api_base = self.api_url

        # Instead of instantiating a client, use the module-level settings
        self.client = openai

        # Make sure to call the logger getter function
        self.logger = Logger().get_logger()

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def generate_text(self, prompt, max_output_token, chat_history=None, temperature=None):
        if chat_history is None:
            chat_history = []
        if not self.client or not self.embedding_model_id or not self.generation_model_id:
            return None

        max_output_token = max_output_token if max_output_token is not None else self.default_generation_max_output_tokens    
        temperature = temperature if temperature is not None else self.default_generation_temperature

        chat_history.append(self.construct_prompt(prompt, LLMEnums.OPENAI_USER))

        response = self.client.ChatCompletion.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_token,
            temperature=temperature
        )

        if not response or not response.choices or len(response.choices) == 0:
            return None
        
        return response.choices[0].message["content"]

    def embed_text(self, text, document_type):
        if not self.client or not self.embedding_model_id:
            return None
        
        response = self.client.Embedding.create(
            model=self.embedding_model_id,
            input=text
        )

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            return None
        
        return response.data[0].embedding

    def construct_prompt(self, prompt, role):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }
    
    def process_text(self, text: str):
        return text[:self.default_input_max_charachters].strip()
