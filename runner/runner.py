from envyaml import EnvYAML
from nameko.standalone.rpc import ServiceRpcProxy

config = EnvYAML('config.yml')

CC = 'bnbbtc'
STREAM = 'depth'
SPEED = '1000ms'
LIMIT = 1000

with ServiceRpcProxy('listener', config) as proxy:
    proxy.get_order_book(CC, LIMIT)
    proxy.start_stream(CC, STREAM, SPEED)
