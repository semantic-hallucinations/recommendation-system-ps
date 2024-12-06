from sc_kpm import sc_module
from .agent.recommendation_agent import RecommendationAgent
from .agent.class_recommendation_agent import ClassRecommendationAgent
from .agent.png_map_generation_agent import PngMapGenerationAgent

class RecommendationModule(sc_module.ScModule):
    def __init__(self):
        super().__init__(
            RecommendationAgent(),
            ClassRecommendationAgent(),
            PngMapGenerationAgent(),
        )