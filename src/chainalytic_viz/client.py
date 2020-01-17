import traceback
from pprint import pprint
from typing import Any, Dict, Optional

from jsonrpcclient.clients.http_client import HTTPClient


def call_aiohttp(endpoint: str, **kwargs) -> Dict:
    try:
        client = HTTPClient(f'http://{endpoint}')
        r = client.request("_call", **kwargs)
        return {'status': 1, 'data': r.data.result}
    except Exception as e:
        return {'status': 0, 'data': f'{str(e)}\n{traceback.format_exc()}'}


class Client(object):
    """Client of Chainalytic Provider service."""

    def __init__(self, endpoint: str):
        super(Client, self).__init__()
        self.endpoint = endpoint

    def _call(self, api_id: str, api_params: dict, verbose: bool = 1) -> Optional[Any]:
        r = call_aiohttp(self.endpoint, call_id='api_call', api_id=api_id, api_params=api_params)
        if r['status']:
            if verbose:
                pprint(r['data']['result'])
            return r['data']['result']

    def last_block_height(self, transform_id: str):
        return self._call('last_block_height', {'transform_id': transform_id})

    def get_staking_info_last_block(self):
        return self._call('get_staking_info_last_block', {})

    def get_staking_info(self, height: int):
        return self._call('get_staking_info', {'height': height})

    def latest_unstake_state(self, verbose=1):
        r = self._call('latest_unstake_state', {}, verbose=0)
        if verbose:
            for k, v in r['wallets'].items():
                print(k, v)
            print(f'Height: {r["height"]}')

    def latest_stake_top100(self, verbose=1):
        r = self._call('latest_stake_top100', {}, verbose=0)
        if verbose:
            for k, v in r['wallets'].items():
                print(k, v)
            print(f'Height: {r["height"]}')

    def recent_stake_wallets(self, verbose=1):
        r = self._call('recent_stake_wallets', {}, verbose=0)
        if verbose:
            for k, v in r['wallets'].items():
                print(k, v)
            print(f'Height: {r["height"]}')

    def abstention_stake(self, verbose=1):
        r = self._call('abstention_stake', {}, verbose=0)
        if verbose:
            for k, v in r['wallets'].items():
                print(k, v)
            print(f'Height: {r["height"]}')
            print(f'Number of wallets: {len(r["wallets"])}')

    def funded_wallets(self, min_balance: float, verbose=1):
        r = self._call('funded_wallets', {'min_balance': min_balance}, verbose=0)
        if verbose:
            for k, v in r['wallets'].items():
                print(k, v)
            print(f'Height: {r["height"]}')
            print(f'Number of wallets: {r["total"]}')

    def passive_stake_wallets(self, max_inactive_duration: int, verbose=1):
        r = self._call('passive_stake_wallets', {'max_inactive_duration': max_inactive_duration}, verbose=0)
        if verbose:
            for k, v in r['wallets'].items():
                print(k, v)
            print(f'Height: {r["height"]}')
            print(f'Number of wallets: {r["total"]}')
