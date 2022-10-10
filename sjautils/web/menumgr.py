from om_int_common.web import om_services_web as osw
        
                
class MenuMgrClient(osw.OMWebClient):
    def __init__(self, om_auth_token):
        super().__init__('https://api.ordermark.com/menu-manager', om_auth_token)

    def get_menuset(self, app_id, response_only=False):
        return self.get('menusets', app_id, response_only=response_only)
