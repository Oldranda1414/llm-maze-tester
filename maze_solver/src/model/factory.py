from model import Model, PartialModel
from model.llm_model import LLMModel
from model.phony_model import PhonyModel
from model.random_model import RandomModel

def llm_model(name: str) -> PartialModel:
    return lambda system_prompt: LLMModel(name, system_prompt)

def phony_model() -> Model:
    return PhonyModel()

def random_model() -> Model:
    return RandomModel()

