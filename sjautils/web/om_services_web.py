from om_int_common.web import generic_web
from om_int_common.aws import secret_value



class OMWebClient(generic_web.GenericWebClient):

    #TODO (sja) make this so
    """
    Assumes Microservices use common om-auth per project using mircroservice. Thus
    that om-auth is secret to project and reachable through settings.
    If heart of Microservices are in om_int_common then can have o_auth bit injected
    in a web_clients.py to produce local appropriate web clients once and only once per
    process that imports web_clients"
    """
    OM_AUTH = ''

    # TODO (sja) push heart of these things that need project settings to


    def __init__(self, url, om_auth_token):
        headers = {'om-auth': om_auth_token}
        super().__init__(url=url, **headers)


