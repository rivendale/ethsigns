from app.api.models.signs import Zodiacs


def check_existing_signs(ns, sign):
    """
    Function to check if signs already exists
    Args:
        ns(obj): namespace object
        sign(dict): sign object
    Return:
        user(obj): sign object
    """
    z_sign = Zodiacs.query.filter_by(
        name=sign['name']).first()
    if z_sign:
        ns.abort(400, errors={"sign": "Sign already exist"}, message="sign exists!")
    return z_sign


def return_not_found(ns, entity):
    """
    Function return a not found message
    Args:
        entity (str): entity name
    Return:
        (str): entity not found message
    """
    ns.abort(404, errors={"sign": f"{entity} not found!"},
             message="Entity not found")
