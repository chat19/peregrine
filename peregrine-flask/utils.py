import json
import ccxt.async as ccxt
import networkx as nx
from subprocess import check_call


class SingularlyAvailableExchangeError(Exception):
    def __init__(self, market_ticker):
        super(SingularlyAvailableExchangeError, self).__init__("{} is available on only one exchange."
                                                               .format(market_ticker))


class ExchangeNotInCollectionsError(Exception):
    def __init__(self, market_ticker):
        super(ExchangeNotInCollectionsError, self).__init__("{} is either an invalid exchange or has a broken API."
                                                            .format(market_ticker))


def draw_graph_to_file(graph, dot_name: str, to_file: str):
    nx.drawing.nx_pydot.write_dot(graph, dot_name + '.dot')
    check_call(['dot', '-Tpng', dot_name + '.dot', '-o', to_file])


async def _get_exchange(exchange_name: str):
    exchange = getattr(ccxt, exchange_name)()
    await exchange.load_markets()
    return exchange


def get_exchanges_for_market(market_ticker):
    """
    Returns the list of exchanges on which a market is traded
    """
    with open('collections/collections.json') as f:
        collections = json.load(f)
    for market_name, exchanges in collections.items():
        if market_name == market_ticker:
            return exchanges

    with open('collections/singularly_available_markets.json') as f:
        singularly_available_markets = json.load(f)
    for market_name, exchange in singularly_available_markets:
        if market_name == market_ticker:
            raise SingularlyAvailableExchangeError(market_ticker)

    raise ExchangeNotInCollectionsError(market_ticker)
