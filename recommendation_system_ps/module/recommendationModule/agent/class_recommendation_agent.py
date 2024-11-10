from sc_client.models import ScAddr
from sc_kpm import ScResult, ScKeynodes
from sc_kpm.sc_agent import ScAgentClassic
import sc_kpm.utils as utils
from sc_client.models import ScTemplate, ScConstruction, ScLinkContent, ScLinkContentType
from sc_client.client import template_search, check_elements, create_elements, delete_elements, set_link_contents
from sc_client.constants import sc_types
from sc_kpm.sc_sets import ScSet, ScStructure
from sc_kpm.identifiers import CommonIdentifiers





class ClassRecommendationAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_get_class_recommendation")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        
        return ScResult.OK