from dataclasses import dataclass

from sc_kpm.sc_keynodes import Idtf


@dataclass(frozen=True)
class RecommendationIdentifiers:
    JSON_BUFFER = "json_buffer"
    JSON_FILE_CLASS = "json_file"
    NREL_USER_IDTF: Idtf = "nrel_user_idtf"
    NREL_PLACE_IDTF: Idtf = "nrel_place_idtf"
    RECOMMENDATION_MODEL: Idtf = "recommendation_model"
    NREL_SERIALIZED: Idtf = "nrel_serialized"
    ACTION_SCRAP_SIGHTS: Idtf = "action_scrap_sights"
    ACTION_GET_RECOMMENDATION: Idtf = "action_get_recommendation"
    ACTION_GET_CLASSIC_RECOMMENDATION: Idtf = "action_get_classic_recommendation"
    ACTION_GET_CLASS_RECOMMENDATION: Idtf = "action_get_class_recommendation"
    ACTION_GET_EXPERIMENTAL_RECOMMENDATION: Idtf = "action_get_experimental_recommendation"
    CONCEPT_PLACE: Idtf = "concept_place"
    