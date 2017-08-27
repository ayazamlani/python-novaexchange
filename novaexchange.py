'''
See https://novaexchange.com/remote/faq/
'''

import time
import hmac
import hashlib
import base64
import requests


public_set = {"markets", "market/info", "market/orderhistory", "market/openorders"}  # optional
private_set = {"getbalances", "getbalance", "getdeposits", "getwithdrawals", "getnewdepositaddress", "getdepositaddress", "myopenorders",
               "myopenorders_market", "cancelorder", "withdraw", "trade", "tradehistory", "getdeposithistory", "getwithdrawalhistory", "walletstatus"}


class NovaExchange(object):
    """
    Used for requesting NovaExchange with API key and API secret
    """

    def __init__(self, api_key, api_secret):
        self.api_key = str(api_key) if api_key is not None else ''
        self.api_secret = str(api_secret) if api_secret is not None else ''

    def api_query(self, method, req=None):
        """
        Queries NovaExchange with given method and options

        :param method: Query method for getting info
        :type method: str

        :req options: Extra options for query
        :type options: dict

        :return: JSON response from NovaExchange
        :rtype : dict
        """
        url = "https://novaexchange.com/remote/v2/"
        if not req:
            req = {}
        if method.split('/')[0][0:6] == 'market':
            r = requests.get(url + method + '/', timeout=60)
        elif method.split('/')[0] in private_set:
            url += 'private/' + method + '/' + '?nonce=' + str(int(time.time()))
            req["apikey"] = self.api_key
            req["signature"] = base64.b64encode(
                hmac.new(self.api_secret.encode('utf-8'), msg=url.encode('utf-8'), digestmod=hashlib.sha512).digest())
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            r = requests.post(url, data=req, headers=headers, timeout=60)
        return(r.text)

    '''
    PUBLIC METHODS  (no API key needed)
    '''

    def markets(self):
        """
        Used to retrieve the public trading market datafrom NovaExchange.
        Lists markets summary, including cached tickerdata.

        :return: Info for all markets in JSON
        :rtype : dict
        """
        return self.api_query('markets')

    def market_info(self, market):
        """
        Used to retrieve the public trading market data from NovaExchange.
        Lists Market summary for a single market.

        # 1 required parameter
        market = string

        example:
        "market": "LTC_MEOW"

        :return: Info for single market in JSON
        :rtype : dict
        """
        return self.api_query('market/info/' + str(market))

    def market_order_history(self, market):
        """
        Used to retrieve the Ticker / Order history for
        a singlemarket from NovaExchange.

        # 1 required parameter
        market = string

        example:
        "market": "LTC_MEOW"

        :return: Info for single market order history in JSON
        :rtype : dict
        """
        return self.api_query('market/orderhistory/' + str(market))

    # UnicodeEncodeError: 'ascii' codec can't encode characters in position 12918-12919: ordinal not in range(128)

    def market_open_orders(self, market, ordertype):
        """
        Used to retrieve the open orders for
        a singlemarket from NovaExchange.

        # 2 required parameters
        market = string
        ordertype = string

        example:
        "market": "LTC_MEOW"
        "ordertype": "BOTH"

        :return: Info for single market public open orders in JSON
        :rtype : dict
        """
        order_options = ['BUY', 'SELL', 'BOTH']
        if str(ordertype) in order_options:
            return self.api_query(('market/openorders/' + str(market) + '/' + str(ordertype)))
        else:
            return(ordertype, 'is not a valid ordertype. please use BUY, SELL, or BOTH.')

    '''
    PRIVATE METHODS  (must have permissions enabled w/ api key and secret)
    '''

    def get_balances(self):
        """
        Used to retrieve your current balances from NovaExchange.

        :return: Info for balances in account in JSON
        :rtype : dict
        """
        return self.api_query('getbalances')

    def get_balance(self, currency):
        """
        Used to retrieve your balance of a specific currency from NovaExchange.

        #1 required parameters
        currency: string

        example
        "currency": "BTC"

        :return: Info for specific currency balance in JSON
        :rtype : dict
        """
        return self.api_query('getbalance/' + str(currency))

    def get_deposits(self):
        """
        Used to gretrieve the current incoming deposits from NovaExchange.

        :return: Info on incoming deposits in JSON
        :rtype : dict
        """
        return self.api_query('getdeposits')

    # not working? even with all api permissions turned on
    def get_withdrawals(self):
        """
        Used to get current outgoing withdrawals from NovaExchange.

        :return: Info on outgoing withdrawals in JSON
        :rtype : dict
        """
        return self.api_query('getwithdrawals')

    def get_new_deposit_address(self, currency):
        """
        Used to get a new deposit address for currency from NovaExchange.

        #1 required parameters
        currency: string

        example
        "currency": "BTC"

        :return: Info on new deposit address in JSON
        :rtype : dict
        """
        return self.api_query('getnewdepositaddress/' + str(currency))

    def get_deposit_address(self, currency):
        """
        Used to retrieve the deposit address for currency from NovaExchange.

        #1 required parameters
        currency: string

        example
        "currency": "BTC"

        :return: Info on specific currency depsoit address in JSON
        :rtype : dict
        """
        return self.api_query('getdepositaddress/' + str(currency))

    def my_open_orders(self):
        """
        Used to retrieve your open orders data from NovaExchange.

        :return: Info on open orders in JSON
        :rtype : dict
        """
        return self.api_query('myopenorders')

    def my_open_orders_market(self, market):
        """
        Used to retrieve your open orders data on a
        specific market from NovaExchange.

        # 1 required parameter
        market = string

        example:
        "market": "LTC_MEOW"

        :return: Info on a specific market's open orders in JSON
        :rtype : dict
        """
        return self.api_query('myopenorders_market/' + str(market))

    def cancel_order(self, order_id):
        """
        Used to cancel a current open order on NovaExchange.

        #1 required parameters
        order_id: integer

        example
        "orderid": 258

        :return: Info on the order that is being cancelled in JSON
        :rtype : dict
        """
        return self.api_query('cancelorder/' + str(order_id))

    def withdraw(self, currency, amount, address):
        """
        Used to withdraw currency to another wallet on NovaExchange.

        #3 required parameters
        currency: string
        amount: float
        address: string

        example:
        "currency": "MEOW"
        "amount": 1000.12345678
        "address": KF2yLFLcZwYigRDw5Uo9U4B9hEaLqwkVxL

        :return: Info on the withdrawal in JSON
        :rtype : dict
        """
        return self.api_query(('withdraw/' + str(currency)), req={"currency": str(currency), "amount": float(amount), "address": str(address)})

    def trade(self, market, tradetype, tradeamount, tradeprice, tradebase=0):
        """
        Used to trade currency on NovaExchange.

        #4 required parameters
        tradetype: string (BUY or SELL)
        tradeamount: float
        tradeprice: float
        tradebase: int (Set as 0 for market currency or 1 for basecurrency as tradeamount)

        example:
        "tradetype": "SELL"
        "tradeamount": 8000.00000000
        "tradeprice": 0.00000008
        "tradebase": 0

        :return: Info on the trade in JSON
        :rtype : dict
        """
        tradetype = str(tradetype)
        tradebase = int(tradebase)
        tradeamount = float(tradeamount)
        tradeprice = float(tradeprice)
        if (tradetype == 'BUY' or tradetype == 'SELL'):
            pass
        else:
            return('trade type', str(tradetype), 'is invalid. (Set as  BUY or SELL)')
        if (tradebase == 0 or tradebase == 1):
            pass
        else:
            return('tradebase', str(tradebase), 'is invalid (Set as 0 for market currency or 1 for basecurrency as tradeamount)')

        return self.api_query(('trade/' + str(market)), req={'tradetype': tradetype, 'tradebase': tradebase, 'tradeprice': tradeprice, 'tradeamount': tradeamount})

    # additional page param not working?
    # def trade_history(self, page=1):
        # return self.api_query('tradehistory', req={'page': int(page)})

    def trade_history(self):
        """
        Used to retrieve trade history data from NovaExchange.

        :return: Info on your trade history in JSON
        :rtype : dict
        """
        return self.api_query('tradehistory')

    def get_deposit_history(self):
        """
        Used to retrieve all deposit history data on NovaExchange.

        :return: Info on deposit history in JSON
        :rtype : dict
        """
        return self.api_query('getdeposithistory')

    def get_withdrawal_history(self):
        """
        Used to retrieve withdrawal history on NovaExchange.

        :return: Info on withdrawal history in JSON
        :rtype : dict
        """
        return self.api_query('getwithdrawalhistory')

    def wallet_status(self, currency=None):
        """
        Used to retrieve the status of
        a specific wallet or all wallets
        on NovaExchange.

        #1 optional parameter
        currency: string

        example
        "currency": "LTC"

        :return: Info on the order that is being cancelled in JSON
        :rtype : dict
        """
        if currency == None:
            return self.api_query('walletstatus')
        else:
            return self.api_query('walletstatus/' + str(currency))
