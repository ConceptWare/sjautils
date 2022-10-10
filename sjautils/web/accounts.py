from om_int_common.web import om_services_web as osw

class AccountsWeb(osw.OMWebClient):
    ACCOUNT_URL = 'https://api.ordermark.com/account'
    def __init__(self, om_auth_token, oos_name):
        self._oos_name = oos_name
        super().__init__(self.ACCOUNT_URL, om_auth_token)

    def get_provider_config(self, key, value):
        path = f'provider-configs?provider={self._oos_name}&{key}={value}'
        data = self.get(path)
        results = data.get("results")
        return results[0] if results else None

    def get_configs_for_provider(self, provider=None):
        provider = provider or self._oos_name
        path = f'provider-configs?provider={provider}'
        return self.get(path)

    def get_kitchen(self, app_id=None, location_id=None, merchant_id=None):
        if app_id:
            return self.get('kitchens', app_id)
        elif location_id:
            return self.get(f'kitchens?id={location_id}')
        elif merchant_id:
            app_id = self.get_app_id(merchant_id)
            return self.get('kitchens', app_id)
        else:
            raise Exception('must specify one of app_id, location_id, merchant_id to get a kitchen')

    def get_app_id(self, merchant_id=None, location_id=None):
        if not any((merchant_id, location_id)):
            raise ValueError("you must provide an merchant_id or a location_id")
        key_value_pair = ('merchant_id', merchant_id) if merchant_id else ('id', location_id)
        config = self.get_provider_config(*key_value_pair)
        if config and config.get('order_integration_type') in ('api', 'om-api'):
            return config['kitchen']

    def get_merchant_id(self, location_id):
        kitchen = self.get_kitchen(location_id=location_id)
        config = self.get_provider_config('app_id', kitchen['app_id'])
        return config['merchant_id']

    def get_location_id(self, app_id=None, merchant_id=None, merchant_secondary_id=None):
        kitchen = None
        if app_id or merchant_id:
            kitchen = self.get_kitchen(app_id=app_id, merchant_id=merchant_id)
        elif merchant_secondary_id:
            pc = self.get_provider_config('merchant_secondary_id', merchant_secondary_id)
            if pc:
                kitchen = self.get_kitchen(merchant_id=pc['merchant_id'])
        return kitchen['id'] if kitchen else None

    def update_provider_config(self, app_id=None, location_id=None, **provider_config):
        if not any((app_id, location_id)):
            raise ValueError("you must provide an app_id or a location_id")
        if not app_id:
            app_id = self.get_app_id(location_id=location_id)
            if not app_id:
                raise ValueError(f"could not find an app_id for location_id:{location_id}")
        return app_id, self.put(f'kitchens', app_id, 'provider-configs', self._oos_name, **provider_config)

    def get_store_hours(self, app_id=None, location_id=None, merchant_id=None):
        if not app_id:
            if location_id:
                app_id = self.get_app_id(location_id=location_id)
            elif merchant_id:
                app_id = self.get_app_id(merchant_id=merchant_id)
            else:
                raise ValueError(f'not enough information to get app_id in order to get store_hours')
        return self.get('kitchens', app_id, 'store-hours')
