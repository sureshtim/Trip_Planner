import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            try:
                llm = ChatGroq(model=model_name, api_key=groq_api_key)
            except Exception as e:
                print(f"Groq model load failed for '{model_name}': {e}")
                fallback_models = ["llama-3.3-70b-versatile", "openai/gpt-oss-120b"]
                llm = None
                for fallback in fallback_models:
                    try:
                        print(f"Trying fallback Groq model: {fallback}")
                        llm = ChatGroq(model=fallback, api_key=groq_api_key)
                        print(f"Successfully loaded fallback model {fallback}")
                        break
                    except Exception as ex:
                        print(f"Fallback model {fallback} failed: {ex}")
                if llm is None:
                    raise RuntimeError(
                        f"Could not load a Groq model. Tried {model_name} and fallbacks {fallback_models}. "
                        "Update config/config.yaml with a valid Groq model, or switch to provider=openai."
                    )
        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI..............")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model_name=model_name, api_key=openai_api_key)
        
        return llm