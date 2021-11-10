from nameko.testing.services import worker_factory


from logger.service import LoggerService


def test_build_orders(db_session):
    service = worker_factory(LoggerService)
    order_details = {
        'e': 'depthUpdate',
        'E': 1636561427277,
        's': 'BNBBTC',
        'U': 2315876790,
        'u': 2315876805,
        'b': [
            ['0.00947500', '0.19300000'],
            ['0.00947000', '17.71500000'],
            ['0.00945400', '16.97400000'],
            ['0.00945300', '47.60000000']
        ],
        'a': [
            ['0.00947600', '32.49900000'],
            ['0.00947700', '17.29500000'],
            ['0.00947900', '17.07300000'],
            ['0.00948200', '13.52100000'],
            ['0.00948400', '19.63500000'],
            ['0.00948700', '0.32000000'],
            ['0.02842800', '0.00000000']
        ]
    }

    orders = service.build_orders(order_details)
    assert len(orders) == len(order_details['a']) + len(order_details['b'])
    order = orders[0]
    assert order.cc == 'BNBBTC'
    assert order.type == 'a'
    assert order.price == 0.00947600
