from om_int_common.web.async_web import generic_web
from om_shared_models.models.order import OrderPayload
from om_int_common.schemas import TaskResult

class ShimWebClient(generic_web.GenericWebClient):
    """
    Convenient to beat shim endpoints when deployed to aws.
    """

    def __init__(self, oos_name, is_staging=True, raw_gateway_id=None, use_direct_url=False):
        prefix = 'staging-' if is_staging else ''
        url = f'https://{prefix}{oos_name}.ordermark.com/api/v1'
        if use_direct_url and raw_gateway_id:
            url = f'https://{raw_gateway_id}.execute-api.us-east-2.amazonaws.com/prod/api/v1'
        super().__init__(url=url)


    async def ingest_order(self, order: OrderPayload):
        return await self.post('orders/', **order.dict())

    async def order_callback(self, task_result: TaskResult, *url_args):
        return await self.put('orders/callback', *url_args, **task_result.dict())

class StagingWebClient(ShimWebClient):
    """
    Convenient to beat shim staging endpoints.
    """

    def __init__(self, oos_name, raw_gateway_id=None, use_direct_url=False):
        super().__init__(oos_name, is_staging=True, raw_gateway_id=raw_gateway_id, use_direct_url=use_direct_url)


class ProductionWebClient(ShimWebClient):

    def __init__(self, oos_name, raw_gateway_id=None, use_direct_url=False):
        super().__init__(oos_name, raw_gateway_id=raw_gateway_id, use_direct_url=use_direct_url)

