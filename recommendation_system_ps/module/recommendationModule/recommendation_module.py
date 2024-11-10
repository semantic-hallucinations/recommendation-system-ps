from sc_kpm import sc_module
from recommendation_system_ps.module.recommendationModule.agent.recommendation_agent import RecommendationAgent


class RecommendationModule(sc_module.ScModule):
    def __init__(self):
        super().__init__(
            RecommendationAgent()
        )