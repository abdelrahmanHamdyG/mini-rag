from abc import abstractmethod, ABC 

class LLMInterface(ABC):

    @abstractmethod
    def set_generation_model(self, model_id:str):
        pass

    @abstractmethod
    def set_embedding_model(self,model_id:str):
        pass 

    @abstractmethod
    def generate_text(self,prompt:str,max_output_token:int,chat_history:list =[],temperature: float =None):
        pass

    @abstractmethod
    def embed_text(self,text:str,document_type: str):
        pass
    
    @abstractmethod
    def construct_prompt(self, prompt: str , role:str):
        pass 


        
