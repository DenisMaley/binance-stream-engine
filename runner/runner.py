from envyaml import EnvYAML
from nameko.standalone.rpc import ServiceRpcProxy

config = EnvYAML('config.yml')

CC = 'bnbbtc'
STREAM = 'depth'
SPEED = '1000ms'

with ServiceRpcProxy('listener', config) as proxy:
    socket = f'wss://stream.binance.com:9443/ws/{CC}@{STREAM}@{SPEED}'
    proxy.start_stream(socket)
