import json
from http import HTTPStatus

from marshmallow import ValidationError
from nameko.exceptions import safe_for_serialization, BadRequest
from nameko.web.handlers import HttpRequestHandler
from werkzeug import Response

from gateway.exceptions import OrderNotFound


class HttpEntrypoint(HttpRequestHandler):
    """ Overrides `response_from_exception` so we can customize error handling.
    """

    mapped_errors = {
        BadRequest: (HTTPStatus.BAD_REQUEST, 'BAD_REQUEST'),
        ValidationError: (HTTPStatus.BAD_REQUEST, 'VALIDATION_ERROR'),
        OrderNotFound: (HTTPStatus.NOT_FOUND, 'ORDER_NOT_FOUND'),
    }

    def response_from_exception(self, exc):
        status_code, error_code = HTTPStatus.INTERNAL_SERVER_ERROR, 'UNEXPECTED_ERROR'

        if isinstance(exc, self.expected_exceptions):
            if type(exc) in self.mapped_errors:
                status_code, error_code = self.mapped_errors[type(exc)]
            else:
                status_code = HTTPStatus.BAD_REQUEST
                error_code = 'BAD_REQUEST'

        return Response(
            json.dumps({
                'error': error_code,
                'message': safe_for_serialization(exc),
            }),
            status=status_code,
            mimetype='application/json'
        )


http = HttpEntrypoint.decorator
