from sc_kpm import sc_module

from .agent.classic_recommendation_agent import ClassicRecommendationAgent
from .agent.recommendation_agent import RecommendationAgent
from .agent.class_recommendation_agent import ClassRecommendationAgent
from .agent.sight_scrapper_agent import SightScraperAgent

class RecommendationModule(sc_module.ScModule):
    def __init__(self):
        super().__init__(
            RecommendationAgent(),
            ClassRecommendationAgent(),
            ClassicRecommendationAgent(),
            SightScraperAgent()
        )