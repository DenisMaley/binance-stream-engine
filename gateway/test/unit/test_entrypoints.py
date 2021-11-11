import json
import pytest
from http import HTTPStatus
from marshmallow import ValidationError

from gateway.entrypoints import HttpEntrypoint
from gateway.exceptions import OrderNotFound


class TestHttpEntrypoint(object):

    @pytest.mark.parametrize(
        ('exc', 'expected_error', 'expected_status_code',
            'expected_message'), [
            (ValueError('unexpected'), 'UNEXPECTED_ERROR', HTTPStatus.INTERNAL_SERVER_ERROR, 'unexpected'),
            (ValidationError('v1'), 'VALIDATION_ERROR', HTTPStatus.BAD_REQUEST, 'v1'),
            (OrderNotFound('o1'), 'ORDER_NOT_FOUND', HTTPStatus.NOT_FOUND, 'o1'),
            (TypeError('t1'), 'BAD_REQUEST', HTTPStatus.BAD_REQUEST, 't1'),
        ]
    )
    def test_error_handling(
        self, exc, expected_error, expected_status_code, expected_message
    ):
        entrypoint = HttpEntrypoint('GET', 'url')
        entrypoint.expected_exceptions = (
            ValidationError,
            OrderNotFound,
            TypeError,
        )

        response = entrypoint.response_from_exception(exc)
        response_data = json.loads(response.data.decode())

        assert response.mimetype == 'application/json'
        assert response.status_code == expected_status_code
        assert response_data['error'] == expected_error
        assert response_data['message'] == expected_message
