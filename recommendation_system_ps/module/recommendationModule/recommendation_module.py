from sc_kpm import sc_module

from .agent.classic_recommendation_agent import ClassicRecommendationAgent
from .agent.recommendation_agent import RecommendationAgent
from .agent.class_recommendation_agent import ClassRecommendationAgent

class RecommendationModule(sc_module.ScModule):
    def __init__(self):
        super().__init__(
            RecommendationAgent(),
            ClassRecommendationAgent(),
            ClassicRecommendationAgent()
        )