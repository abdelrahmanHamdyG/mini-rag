from ..LLMInterface import LLMInterface
from openai import OpenAI
from helpers import Logger
from ..LLMEnums import LLMEnums 


class OpenAiProvider(LLMInterface):
    
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

        self.client= OpenAI(

            api_key=self.api_key,
            api_url=self.api_url

        )

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

        chat_history.append(self.construct_prompt(prompt,LLMEnums.OPENAI_USER))

        response= self.client.chat.completion.create(
            model =self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_token,
            temperature=temperature
        )

        if not response or not response.choices or len(response.choices)==0:
            return None
        
        return response.choices[0].message["content"]
    


    def embed_text(self, text, document_type):
        if not self.client or not self.embedding_model_id  :
            return None
        
        response=self.client.embedding.create(

            model=self.embedding_model_id,
            input=text
        )

        if not response or not response.data or len(response.data)==0  or not response.data[0].embedding:
            return None
        
        
        return response.data[0].embedding
        

    def construct_prompt(self, prompt, role):
        return {
            "role":role,
            "content":self.process_text(prompt)
        }
    
    def process_text(self,text:str):
        return text[:self.default_input_max_charachters].strip()
    


    
        


        