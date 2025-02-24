import os 
from helpers import Logger
class TemplateParser():

    def __init__(self,language:str='en'):
        self.current_path=os.path.dirname(os.path.abspath(__file__))
        self.language=language
        self.logger=Logger().get_logger()
    
    def set_language(self,language: str):

        language_path=os.path.join(self.current_path,"locales",language)
        if language and os.path.exists(language_path):
            self.language=language
        else:
            self.language="en"
    

    def get(self,group:str,key:str,vars: dict={}):
        if not group or not key :
            return None
        
        group_path=os.path.join(self.current_path,"locales",self.language,f"{group}.py")
        self.logger.debug(f" group path {group_path}")
        if not os.path.exists(group_path):
            self.logger.debug(f" group path doesn't exist")
            return None
        

        module=__import__(f"stores.llm.templates.locales.{self.language}.{group}",fromlist=[group])

        if not module:
            self.logger.debug(f" module  doesn't exist")
            return None 
        key_attr=getattr(module,key)
        return key_attr.substitute(vars)
    