from helpers.validation_models import Reservation
import logging

def validate_json(incoming_dict):
    try:
        res_obj = Reservation(**incoming_dict)
        return res_obj.model_dump()
    except Exception as e:
        logging.error(f"Validation/Conversion error: {e}")
        raise