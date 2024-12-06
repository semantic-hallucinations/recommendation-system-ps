from sc_client.models import ScAddr
from sc_kpm import ScResult, ScKeynodes
from sc_kpm.sc_agent import ScAgentClassic
import sc_kpm.utils as utils
from sc_kpm.sc_sets import ScStructure
from sc_kpm.identifiers import CommonIdentifiers
from ..recommendation_idtfs import RecommendationIdentifiers


class ClassicRecommendationAgent(ScAgentClassic):
    def __init__(self):
        super().__init__(RecommendationIdentifiers.ACTION_GET_CLASSIC_RECOMMENDATION)

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        user = utils.search_element_by_role_relation(action_element, ScKeynodes.rrel_index(1))

        if not user:
            utils.action_utils.finish_action_with_status(action_element, False)
            return ScResult.ERROR_INVALID_PARAMS

        recommendation_action_instance, success = utils.action_utils.execute_agent(
            {
                user: False
            },
            [
                CommonIdentifiers.ACTION,
                RecommendationIdentifiers.ACTION_GET_RECOMMENDATION
            ]
        )

        if not success:
            utils.action_utils.finish_action_with_status(action_element, False)
            return ScResult.NO

        recommendation_action_answer = utils.action_utils.get_action_result(recommendation_action_instance)
        recommendation_action_answer = ScStructure(set_node=recommendation_action_answer)

        utils.action_utils.generate_action_result(action_element, *recommendation_action_answer)
        utils.action_utils.finish_action_with_status(action_element)
        return ScResult.OK