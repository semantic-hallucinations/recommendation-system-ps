from sc_client.client import get_link_content
from sc_client.models import ScAddr
from sc_kpm import ScAgentClassic, ScResult, utils, ScKeynodes
from sc_kpm.sc_sets import ScSet, ScNumberedSet
from sc_kpm.utils import action_utils
from surprise import SVD, dump

from recommendation_system_ps.module.recommendationModule.recommendation_idtfs import RecommendationIdentifiers

TOP_N = 10

class RecommendationAgent(ScAgentClassic):

    def __init__(self):
        super().__init__(RecommendationIdentifiers.ACTION_GET_RECOMMENDATION)
        self.__model = self._get_model()

    def _get_username(self, user_node: ScAddr) -> str:
        user_name_addr = utils.get_element_by_norole_relation(user_node,
                                                              ScKeynodes.get(RecommendationIdentifiers.NREL_USER_IDTF))
        link_content = get_link_content(user_name_addr)[0].data
        return str(link_content)

    def _get_model(self) -> SVD:
        model_addr = ScKeynodes.get(RecommendationIdentifiers.RECOMMENDATION_MODEL)
        model_link_addr = utils.get_element_by_norole_relation(
            model_addr,
            ScKeynodes.get(RecommendationIdentifiers.NREL_SERIALIZED)
        )
        link_content = get_link_content(model_link_addr)[0].data
        _, model = dump.load(link_content.removeprefix('file://'))
        return model

    def _get_places_ids(self, places_set: ScSet) -> dict[str, ScAddr]:
        result_dict = {}
        for place in places_set:
            place_name = get_link_content(utils
                                          .get_element_by_norole_relation(place, ScKeynodes.get(
                RecommendationIdentifiers.NREL_PLACE_IDTF)))[0].data
            result_dict[place_name] = place
        return result_dict

    def _get_recommendations(self, user_id, place_ids, algo, n=5):
        predictions = [algo.predict(user_id, place_id) for place_id in place_ids]
        recommendations = sorted(predictions, key=lambda x: x.est, reverse=True)
        return recommendations[:n]

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        user, places_set = utils.action_utils.get_action_arguments(action_element, 2)
        user_id = self._get_username(user)
        unrated_places = self._get_places_ids(ScSet(set_node=places_set))

        top_recommendations = self._get_recommendations(user_id, list(unrated_places.keys()), self.__model, n=TOP_N)

        action_utils.create_action_answer(action_element, *(unrated_places[rec.iid] for rec in top_recommendations))
        action_utils.finish_action_with_status(action_element)
        return ScResult.OK
