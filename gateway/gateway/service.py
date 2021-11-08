from nameko.rpc import RpcProxy
from werkzeug import Response

from nameko.web.handlers import http
from gateway.schemas import (
    VolumeSchema
)


class GatewayService(object):
    """
    Service acts as a gateway to other services over http.
    """

    name = 'gateway'

    listener_rpc = RpcProxy('listener')

    @http("GET", "/volume")
    def get_volume(self, request):
        volume = {'amount': 42}  # TODO Replace placeholder
        return Response(
            VolumeSchema().dumps(volume).data,
            mimetype='application/json'
        )
