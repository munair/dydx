#!/usr/bin/env python3

import json
import datetime
from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get a limited number of all WETH-DAI orders created over the period defined below
resultlimit = Decimal("5")
period = 5
timedelta = datetime.datetime.now() - datetime.timedelta(days=period)
all_orders = client.get_orders(
    market=['WETH-DAI'],
    limit=resultlimit,  # optional
    startingBefore=timedelta  # optional
)

jsondata = json.dumps( all_orders, sort_keys=True, indent=4, separators=(',', ': ') )

print ( jsondata )
print ( "The above is a list of all the orders created over the last " , period , " days.")
print ( "The results are limited to the most recent " , resultlimit , " orders.")
