'''Poloniex API wrapper

See: https://poloniex.com/support/api/

Handles public and private calls
ToDo: Streaming API

Notes
-----
Markets are called as 'BTC_LTC' - caps with underscore
'returnTradeHistory' both as public and private command
'''
import requests
import time
import hashlib
import hmac
import urllib
import json
import os
from urllib.parse import urlencode
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .api_utils import loop

BASE_URL = 'https://poloniex.com/{url_type}'
PUBLIC_SET = {
    'returnTicker',
    'return24hVolume',
    'returnOrderBook',
    'returnTradeHistory',
    'returnChartData',
    'returnCurrencies',
    'returnLoanOrders'}
PRIVATE_SET = {
    'returnBalances',
    'returnCompleteBalances',
    'returnDepositAddresses',
    'generateNewAddress',
    'returnDepositsWithdrawals',
    'returnOpenOrders',
    'returnTradeHistory',
    'returnOrderTrades',
    'buy',
    'sell',
    'cancelOrder',
    'moveOrder',
    'withdraw',
    'returnFeeInfo',
    'returnAvailableAccountBalances',
    'returnTradableBalances',
    'transferBalance',
    'returnMarginAccountSummary',
    'marginBuy',
    'marginSell',
    'getMarginPosition',
    'closeMarginPosition',
    'createLoanOffer',
    'cancelLoanOffer',
    'returnOpenLoanOffers',
    'returnActiveLoans',
    'returnLendingHistory',
    'toggleAutoRenew'}


class PoloniexApiError(Exception):
    pass


class Poloniex():
    def __init__(self, *args, **kwargs):
        """Create Poloniex instance

        Checks args and kwargs for key/secret or file.
        If it is supplied they get added, else they are ''.
        API-documentation at: https://poloniex.com/support/api/"""
        self.n_tries = kwargs.get('n_tries', 1)
        self.sleep = kwargs.get('sleep', 10)
        self.key = kwargs.get('key', '')
        self.secret = kwargs.get('secret', '')

        if len(args) == 1 and os.path.isfile(args[0]):
            self.load_key(args[0])
            logger.info('Load keys from file')
        if len(args) == 2:
            self.key = args[0]
            self.secret = args[1]
            logger.info('Add key and secret from args')

    def add_key(self, key, secret):
        """Add key via arguments"""
        self.key = key
        self.secret = secret

    def load_key(self, filepath):
        """Load key from file"""
        with open(filepath, 'r') as f:
            lines = f.readlines()
            self.key, self.secret = [l.strip() for l in lines[:2]]

    @loop
    def api_query(self, command, **kwargs):
        """Query the Poloniex API

        Parameters
        ----------
        command : string
            Required argument for the API query
        kwargs : dict
            Other parameters, required or optional, as described in
            https://poloniex.com/support/api/

        Returns
        -------
        dict
            Request result is a JSON, will be parsed to a dict

        Raises
        ------
        PoloniexApiError
            It the command is unknown
            If the request is not `ok`
            If the API does not return `success`
        """
        # First handle the command to check which API to use
        if command in PUBLIC_SET:
            url_type = 'public'
        elif command in PRIVATE_SET:
            url_type = 'tradingApi'
        elif command == 'returnMyTradeHistory':
            command = 'returnTradeHistory'
            url_type = 'tradingApi'
        else:
            # logger.error(f'Command `{command}` not found')
            raise PoloniexApiError('Command not found')
        if command == 'returnTradeHistory':
            logger.warning(
                f'Command {command} is ambiguous -',
                'using public API. For the private API use',
                '`returnMyTradeHistory`')

        # Now perform the actual GET or POST query
        url = BASE_URL.format(url_type=url_type)
        kwargs['command'] = command
        if url_type == 'public':
            r = requests.get(url, params=kwargs)
        elif url_type == 'tradingApi':
            kwargs['nonce'] = int(time.time() * 1000)
            apisign = hmac.new(self.secret.encode(),
                               urlencode(kwargs).encode(),
                               hashlib.sha512).hexdigest()
            headers = {'Sign': apisign, 'Key': self.key}

            r = requests.post(url, data=kwargs, headers=headers)

        # Minor error-handling and return
        if not r.ok:
            raise Exception('Request went wrong')
        return r.json()

    def return_loan_orders(self, currency, limit=9999999999):
        """Return the list of loan offers and demands for a given currency

        Parameters
        ----------
        currency : str
        limit : int

        Returns
        -------
        dict

        Sample output
        -------------
        {"offers":[{"rate":"0.00200000",
                    "amount":"64.66305732",
                    "rangeMin":2,
                    "rangeMax":8},
                   ... ],
         "demands":[{"rate":"0.00170000",
                     "amount":"26.54848841",
                     "rangeMin":2,
                     "rangeMax":2},
                    ... ]}

        Call
        ----
        https://poloniex.com/public?command=returnLoanOrders&currency=BTC
        """
        return self.api_query(
            'returnLoanOrders',
            currency=currency,
            limit=limit)

    def return_loan_offers(self, currency):
        """Return the list of loan offers as a well-formatted dict

        Parameters
        ----------
        currency : str

        Returns
        -------
        dict

        Sample output
        -------------
        {0.002: 64.66305732, 0.0017: 26.54848841, ...}
        """
        loan_orders = self.return_loan_orders(currency)
        offers = loan_orders['offers']
        offers = {float(o['rate']): float(o['amount']) for o in offers}
        return offers


def examples():
    polo = Poloniex('sensitive/poloniex.key')
    polo.call_private('returnBalances')


def main():
    pass


if __name__ == '__main__':
    main()
