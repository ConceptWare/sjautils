from om_int_common.web import generic_web
from om_int_common.schemas.location import AvailableStatus, AvailablePatch
from om_shared_models.models.order import OrderPayload
from om_int_common.schemas import TaskResult  # TODO move to om_shared_models


class ShimWebClient(generic_web.GenericWebClient):
    """
    Convenient to beat shim endpoints when deployed to aws.
    """

    def __init__(self, oos_name, api_version="/api/v1", is_staging=True, raw_gateway_id=None, use_direct_url=False, local_server=False, local_port=8080):
        prefix = 'staging-' if is_staging else ''
        url = f'https://{prefix}{oos_name}.ordermark.com'
        if use_direct_url and raw_gateway_id:
            url = f'https://{raw_gateway_id}.execute-api.us-east-2.amazonaws.com/prod'
        elif local_server:
            url = f'http://localhost:{local_port}'
        url = f'{url}{api_version}'
        super().__init__(url=url)


    def post_order(self, order):
        return self.post('orders/', **order.dict())

    def order_callback(self, task_result: TaskResult, *url_args):
        return self.put('orders/callback', *url_args, **task_result.dict())


    def set_store_availability(self, status: AvailableStatus, callback_url, location_id):
        patch = AvailablePatch(callback_url=callback_url, status={'status': status})
        return self.patch('sync/locations', location_id, 'available', **patch.dict())

    def get_store_availability(self, location_id):
        return self.get('sync/locations', location_id, 'available')



class StagingWebClient(ShimWebClient):
    """
    Convenient to beat shim staging endpoints.
    """

    def __init__(self, oos_name, raw_gateway_id=None, use_direct_url=False):
        super().__init__(oos_name, is_staging=True, raw_gateway_id=raw_gateway_id, use_direct_url=use_direct_url)


class ProductionWebClient(ShimWebClient):

    def __init__(self, oos_name, raw_gateway_id=None, use_direct_url=False):
        super().__init__(oos_name, is_staging=False, raw_gateway_id=raw_gateway_id, use_direct_url=use_direct_url)

