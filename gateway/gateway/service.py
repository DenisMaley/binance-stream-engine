import json
from http import HTTPStatus
from nameko.rpc import RpcProxy
from nameko.exceptions import BadRequest
from werkzeug import Response

from gateway.entrypoints import http
from gateway.exceptions import OrderNotFound
from gateway.schemas import GetOrderSchema


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
            status=HTTPStatus.OK,
            mimetype='application/json'
        )

    @http("GET", "/orders/<int:order_id>", expected_exceptions=OrderNotFound)
    def get_order(self, request, order_id):
        """Gets the order details for the order given by `order_id`.

        Enhances the order details from the logger-service.
        """
        order = self._get_order(order_id)
        return Response(
            GetOrderSchema().dumps(order).data,
            status=HTTPStatus.OK,
            mimetype='application/json'
        )

    def _get_order(self, order_id):
        # Note - this may raise a remote exception that has been mapped to
        # raise``OrderNotFound``

        return self.logger_rpc.get_order(order_id)

    def _get_volume(self, o_type, price, operator):
        # Retrieve volume from the logger service.
        try:
            price = float(price)
        except ValueError as exc:
            raise BadRequest("Invalid json: {}".format(exc))

        return self.logger_rpc.get_volume(o_type, price, operator)
