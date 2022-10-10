from om_int_common.web.async_web import generic_web


class AccountsWeb(generic_web.GenericWebClient):
    ACCOUNT_URL = 'https://api.ordermark.com/account'

    def __init__(self, om_auth_token, oos_name):
        self._oos_name = oos_name
        headers = {'om-auth': om_auth_token}
        super().__init__(url=self.ACCOUNT_URL, **headers)

    async def get_provider_config(self, key, value):
        path = f'provider-configs?provider={self._oos_name}&{key}={value}'
        data = await self.get(path)
        return data['results'][0] if data.get('results') else None

    async def get_kitchen(self, app_id=None, location_id=None, merchant_id=None):
        if app_id:
            return await self.get('kitchens', app_id)
        elif location_id:
            return await self.get(f'kitchens?id={location_id}')
        elif merchant_id:
            app_id = await self.get_app_id(merchant_id)
            return await self.get('kitchens', app_id)
        else:
            raise Exception('must specify one of app_id, location_id, merchant_id to get a kitchen')

    async def get_app_id(self, merchant_id):
        config = await self.get_provider_config('merchant_id', merchant_id)
        if config.get('order_integration_type') in ('api', 'om-api'):
            return config['kitchen']

    async def get_merchant_id(self, location_id):
        kitchen = await self.get_kitchen(location_id=location_id)
        config = await self.get_provider_config('app_id', kitchen['app_id'])
        return config['merchant_id']

    async def get_location_id(self, app_id=None, merchant_id=None):
        kitchen = await self.get_kitchen(app_id=app_id, merchant_id=merchant_id)
        return kitchen['id']

