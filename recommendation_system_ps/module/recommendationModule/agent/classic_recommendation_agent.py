from sc_client.models import ScAddr
from sc_kpm import ScResult, ScKeynodes
from sc_kpm.sc_agent import ScAgentClassic
import sc_kpm.utils as utils
from sc_client.models import ScTemplate, ScConstruction
from sc_client.client import create_elements
from sc_client.constants import sc_types
from sc_kpm.sc_sets import ScStructure
from sc_kpm.identifiers import CommonIdentifiers
from ..recommendation_idtfs import RecommendationIdentifiers


class ClassicRecommendationAgent(ScAgentClassic):
    def __init__(self):
        super().__init__(RecommendationIdentifiers.ACTION_GET_CLASSIC_RECOMMENDATION)

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        user = utils.get_element_by_role_relation(action_element, ScKeynodes.rrel_index(1))

        if not user:
            utils.action_utils.finish_action_with_status(action_element, False)
            return ScResult.ERROR_INVALID_PARAMS

        recommendation_action = utils.action_utils.create_action(
            RecommendationIdentifiers.ACTION_GET_RECOMMENDATION,
            CommonIdentifiers.ACTION
        )
        recommendation_action_construction = ScConstruction()
        recommendation_action_construction.create_edge(
            sc_types.EDGE_ACCESS_CONST_POS_PERM,
            recommendation_action,
            user,
            "user_edge"
        )
        recommendation_action_construction.create_edge(
            sc_types.EDGE_ACCESS_CONST_POS_PERM,
            ScKeynodes.rrel_index(1),
            "user_edge"
        )
        recommendation_action_construction.create_edge(
            sc_types.EDGE_ACCESS_CONST_POS_PERM,
            recommendation_action,
            ScKeynodes[RecommendationIdentifiers.CONCEPT_PLACE],
            "places_edge"
        )
        recommendation_action_construction.create_edge(
            sc_types.EDGE_ACCESS_CONST_POS_PERM,
            ScKeynodes.rrel_index(2),
            "places_edge"
        )
        create_elements(recommendation_action_construction)

        if not utils.action_utils.execute_action(
                recommendation_action,
                wait_time=60
        ):
            utils.action_utils.finish_action_with_status(action_element, False)
            return ScResult.NO

        recommendation_action_answer = utils.action_utils.get_action_answer(recommendation_action)
        recommendation_action_answer = ScStructure(set_node=recommendation_action_answer)

        utils.action_utils.create_action_answer(action_element, *recommendation_action_answer)
        utils.action_utils.finish_action_with_status(action_element)
        return ScResult.OK