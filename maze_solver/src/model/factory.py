from model import Model
from model.llm_model import LLMModel
from model.phony_model import PhonyModel
from model.random_model import RandomModel

def llm_model(name: str) -> Model:
    return LLMModel(name)

def phony_model(name: str) -> Model:
    return PhonyModel(name)

def random_model(name: str) -> Model:
    return RandomModel(name)

