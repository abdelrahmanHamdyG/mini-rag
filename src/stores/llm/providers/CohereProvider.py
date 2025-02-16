from ..LLMInterface import LLMInterface
from helpers import Logger
import cohere
from ..LLMEnums import LLMEnums 


class CohereProvider(LLMInterface):
    
    def __init__(self,api_key : str, api_url:str,default_input_max_charachters: int =1000
                 ,default_generation_max_characters: int=1000
                 ,default_generation_max_output_tokens: int =1000
                 ,default_generation_temperature: float=0.1):
        

        self.api_key=api_key
        self.api_url=api_url
        self.default_input_max_charachters=default_input_max_charachters
        self.default_generation_max_characters=default_generation_max_characters
        self.default_generation_max_output_tokens=default_generation_max_output_tokens
        self.default_generation_temperature=default_generation_temperature
        self.generation_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None

        self.client=cohere.Client(api_key=self.api_key)
        self.logger=Logger.get_logger()
    
    def set_generation_model(self,model_id:str):
        self.generation_model_id= model_id

    def set_embedding_model(self, model_id:str,embedding_size):
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size


    def generate_text(self, prompt, max_output_token, chat_history = [], temperature = None):
        
        if not self.client or not self.embedding_model_id or not self.generation_model_id :
            return None
        
        max_output_token=max_output_token if max_output_token is not None else self.default_generation_max_output_tokens    
        temperature=temperature if temperature is not None else self.default_generation_temperature

        response= self.client.chat(
            model =self.generation_model_id,
            chat_history=chat_history,
            message=self.process_text(prompt),
            temperature=temperature,
            max_tokens= max_output_token
        )

        if not response or not response.text:
            return None
        
        return response.text
    
    
    def construct_prompt(self, prompt, role):
        return {
            "role":role,
            "content":self.process_text(prompt)
        }
    
    def process_text(self,text:str,document_type):
        return text[:self.default_input_max_charachters].strip()
    

    def embed_text(self, text, document_type):
        if not self.client or not self.embedding_model_id:
            return None
        

        input_type=LLMEnums.COHERE_DOCUMENT
        if document_type== LLMEnums.QEURY:
            input_type=LLMEnums.COHERE_QUERY

        response= self.client.embed(


            model=self.embedding_model_id,
            text=[text],
            input_type=input_type,
            embedding_type=['float'],
        )
        
        if not response or not response.embeddings:
            return None
        
        

        
    
