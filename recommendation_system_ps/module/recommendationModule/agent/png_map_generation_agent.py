from pathlib import Path

from sc_client.models import ScAddr
from sc_client.constants import sc_types

from sc_kpm.sc_agent import ScAgentClassic, ScResult
from sc_kpm.sc_keynodes import ScKeynodes
from sc_kpm.sc_sets import ScSet

import sc_kpm.utils as utils

from sc_client.constants import sc_types
from sc_client.client import get_link_content
from sc_client.models import ScLinkContentType

from ..recommendation_idtfs import RecommendationIdentifiers

from staticmap import StaticMap, CircleMarker
from geopy.geocoders import Nominatim
import os


class PngMapGenerationAgent(ScAgentClassic):
    def __init__(self):
        super().__init__(RecommendationIdentifiers.ACTION_GENERATE_PNG_MAP)

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        sight_tuple = utils.get_element_by_role_relation(action_element, ScKeynodes.rrel_index(1))
        sight_set = ScSet(set_node=sight_tuple)
        just_set = set(sight_set)
        addresses = [utils.search_element_by_non_role_relation(sight, RecommendationIdentifiers.NREL_ADDRESS) for sight in just_set]
    
        locations = [PngMapGenerationAgent.get_coordinates(address) for address in addresses if PngMapGenerationAgent.get_coordinates(address)]

        map_obj = StaticMap(1920, 1280, url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')

        for coord in locations:
            marker = CircleMarker((coord[1], coord[0]), 'red', 30)
            map_obj.add_marker(marker)
            
        image = map_obj.render()
        image.save('map.png')
        path = os.getcwd()
        map_link = utils.create_link(str(path) + 'map.png')
        utils.create_edge(
            sc_types.EDGE_ACCESS_CONST_POS_PERM, 
            ScKeynodes.get("nrel_format"),
            utils.create_edge(
                sc_types.EDGE_D_COMMON_CONST,
                map_link,
                ScKeynodes.get("format_png")
            )
        )
        utils.create_edge(
            sc_types.EDGE_ACCESS_CONST_POS_PERM,
            map_link,
            ScKeynodes.resolve("maps", sc_types.NODE_CONST)
        )
        
        utils.action_utils.create_action_result(action_element, map_link)
        utils.action_utils.finish_action_with_status(action_element)
        return ScResult.OK
                    
        
        
    @staticmethod
    def get_coordinates(address: str):
        geolocator = Nominatim(user_agent="location_mapper")
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None