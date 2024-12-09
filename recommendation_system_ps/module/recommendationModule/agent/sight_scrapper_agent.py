from sc_client.models import ScAddr
from sc_kpm import ScResult, ScKeynodes
from sc_kpm.sc_agent import ScAgentClassic
import sc_kpm.utils as utils
from sc_kpm.sc_sets import ScStructure, ScSet
from sc_kpm.identifiers import CommonIdentifiers
from sc_client.constants import sc_types
from ..recommendation_idtfs import RecommendationIdentifiers

import subprocess
import sys
import os


class ClassicRecommendationAgent(ScAgentClassic):
    def __init__(self):
        super().__init__("action_scrap_sights")

    def on_event(self, event_element: ScAddr, event_edge: ScAddr, action_element: ScAddr) -> ScResult:
        project_path = "sight_scrapper_env"
        res = self.run_docker_compose(project_path)
        
        if not res:
            utils.action_utils.finish_action_with_status(action_element, is_success=False)
            return ScResult.NO

        utils.action_utils.generate_action_result(action_element, res)
        utils.action_utils.finish_action_with_status(action_element)
        return ScResult.OK
    
    def run_docker_compose(self, container_path) -> ScAddr | None:
        try:
            process = subprocess.Popen(
                ["docker-compose", "up", "-d", "--build"],
                cwd=container_path,            
                stdout=subprocess.PIPE,   
                stderr=subprocess.PIPE,   
                text=True                 
            )
            
            for line in process.stdout:
                print(line, end="")  

            for line in process.stderr:
                print(line, end="", file=sys.stderr)  

            process.wait()
            
            if process.returncode == 0:
                self.logger.info("Docker Compose exited with code 0")
                data_path = "output"
                return self.get_jsons(container_path + '/' + data_path)
            else:
                self.logger.info("Docker Compose exited with error")
                return None

        except Exception as e:
            self.logger.error("Error in running docker comtainer: %s", e)
            return None

    def get_jsons(self, directory: str) -> ScAddr | None:
        try:
            json_buffer = ScKeynodes.resolve(RecommendationIdentifiers.JSON_BUFFER, sc_types.CONST_NODE_CLASS)
            res = ScSet(json_buffer)
            json_class_node = ScKeynodes.resolve(RecommendationIdentifiers.JSON_FILE_CLASS, sc_types.CONST_NODE_CLASS)
            
            for root, dirs, files in os.walk(directory):
                for file in files:
                    res_link = utils.create_link('file://' + os.path.abspath(os.path.join(root, file)))
                    utils.create_edge(sc_types.EDGE_ACCESS_CONST_POS_PERM, json_class_node, res_link)
                    res.add(res_link)
            return res.set_node
        except Exception as e:
            self.logger.error("Error in adding new jsona to buffer: %s", e)
        return None
    