import json
from nameko.rpc import RpcProxy
from nameko.exceptions import BadRequest
from werkzeug import Response

from nameko.web.handlers import http


class GatewayService:
    """
    Service acts as a gateway to other services over http.
    """

    name = 'gateway'

    logger_rpc = RpcProxy('logger')

    @http("GET", "/volume/<string:o_type>")
    def get_volume(self, request, o_type):
        """Gets the volume for the order type given by `type`.

        Enhances the volume details from the logger.
        """
        # TODO replace with proper filtering
        price = request.args.get('price')
        operator = request.args.get('operator')

        volume = self._get_volume(o_type, price, operator)

        # TODO dump with GetVolumeSchema
        return Response(
            json.dumps(volume),
            mimetype='application/json'
        )

    def _get_volume(self, o_type, price, operator):
        # Retrieve volume from the logger service.
        try:
            price = float(price)
        except ValueError as exc:
            raise BadRequest("Invalid json: {}".format(exc))

        return self.logger_rpc.get_volume(o_type, price, operator)
