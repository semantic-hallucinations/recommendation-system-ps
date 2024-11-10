from sc_client.models import ScAddr
from sc_kpm import ScResult, ScKeynodes
from sc_kpm.sc_agent import ScAgentClassic
import sc_kpm.utils as utils
from sc_client.models import ScTemplate
from sc_client.client import template_search
from sc_client.constants import sc_types
from sc_kpm.sc_sets import ScSet, ScStructure, ScNumberedSet
from sc_kpm.identifiers import CommonIdentifiers


class ClassRecommendationAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_get_class_recommendation")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        user = utils.get_element_by_role_relation(action_element, ScKeynodes.rrel_index(1))
        sight_type = utils.get_element_by_role_relation(action_element, ScKeynodes.rrel_index(2))
        
        if not user:
            utils.action_utils.finish_action_with_status(action_element, False)
            return ScResult.ERROR_INVALID_PARAMS
        
        if not sight_type:
            utils.action_utils.finish_action_with_status(action_element, False)
            return ScResult.ERROR_INVALID_PARAMS
        
        sight_template = ScTemplate()
        sight_template.triple(
            sight_type,
            sc_types.EDGE_ACCESS_VAR_POS_PERM,
            sc_types.NODE_VAR << "_sight"
        )
        
        results = template_search(sight_template)
        sights = ScSet(*(result.get("_sight") for result in results))
        
        recommendation_action = utils.action_utils.create_action("action_get_recommendation", CommonIdentifiers.ACTION)
        recommendation_action = ScNumberedSet(user, sights.set_node, set_node=recommendation_action)
        
        if not utils.action_utils.execute_action(
            recommendation_action.set_node
        ):
            utils.action_utils.finish_action_with_status(action_element, False)
            return ScResult.NO
        
        recommendation_action_answer = utils.action_utils.get_action_answer(recommendation_action)
        recommendation_action_answer = ScStructure(recommendation_action_answer)
        
        utils.action_utils.create_action_answer(action_element, *recommendation_action_answer)
        utils.action_utils.finish_action_with_status(action_element)
        return ScResult.OK