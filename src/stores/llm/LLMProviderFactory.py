from .LLMEnums import LLMEnums
from .providers import CohereProvider,OpenAiProvider
from helpers import Logger
class LLMProviderFactory():
    def __init__(self,config):
        self.config=config
    


    def create(self,provider:str):
        
        
        if provider==LLMEnums.OPEN_AI.value:
            
            return OpenAiProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL)

        if provider==LLMEnums.COHERE.value:
            return CohereProvider(
                api_key=self.config.COHERE_API_KEY,
                api_url="https://api.cohere.ai",

            )
        return provider

