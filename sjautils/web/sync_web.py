from requests import Response
from om_int_common.aws.aws import secret_value
from om_int_common.config import settings
from om_int_common.schemas.location import ActivationStatus
from om_int_common.web import generic_web
from om_int_common.schemas.shared_override import OrderPayload
import json


class SyncWebClient(generic_web.GenericWebClient):
    Shim_Config = None

    @classmethod
    def shim_config(cls):
        if not cls.Shim_Config:
            cls.Shim_Config = secret_value(settings.SECRETS_MANAGER_NAME)
        return cls.Shim_Config

    @classmethod
    def _sync_headers(cls, api_key=''):
        return {
            'x-api-key': (api_key if api_key else cls.shim_config().get('SYNC_API_KEY')),
            'Content-Type': 'application/json'
        }

    def __init__(self, api_key=''):
        super().__init__(settings.SYNC_BASE_URL, **self._sync_headers(api_key=api_key))

    def sync_headers(self):
        return self._headers

    def get_order(self, store_location_id, order_id):
        data = self.get('locations', store_location_id, 'orders', order_id)
        return data['order']

    def place_order(self, store_location_id, order:OrderPayload, callback_url: str, response_only=False):
        payload = dict(
            order = json.loads(order.json(exclude_none=True, exclude_unset=True, by_alias=True)),
            callback_url = callback_url
        )
        return self.put('locations', store_location_id, 'orders', order.order_id, **payload, response_only=response_only)

    def get_menuset(self, location_id):
        info = self.get('locations', location_id, 'menuset')
        print(info)
        ms_resp = self._session.get(info['menuset_url'])
        if 200 <= ms_resp.status_code < 300:
            return ms_resp.json()

    def items_to_sections(self, location_id: str) -> dict:
        menu = self.get_menuset(location_id)
        if menu:
            mapping = {}
            for section in menu['sections']:
                for item_id in section['item_ids']:
                    mapping[str(item_id)] = str(section['id'])
            return mapping
        else:
            raise Exception(f'no menu found for location {location_id}')

    def get_location_information(self, location_id:str):
        return self.get('locations', location_id, 'information')

    def set_activation_status(self, location_id: str, callback_url: str, status: ActivationStatus) -> Response:
        payload = {"callback_url": callback_url, "status": {"status": status}}
        return self.patch('locations', location_id, 'activation', **payload, response_only=True)

