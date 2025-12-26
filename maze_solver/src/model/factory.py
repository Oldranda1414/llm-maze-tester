from model import Model
from model.llm_model import LLMModel
from model.phony_model import PhonyModel

def llm_model(name: str) -> Model:
    return LLMModel(name)

def phony_model(name: str) -> Model:
    return PhonyModel(name)

