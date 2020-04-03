#!/usr/bin/env python3

import json

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Cancel the previously created order
order_hash = '0x1707e427a9d32406f4919a7bd796c207438069e27ab7159c7bf639a0a74b5b53'
canceled_order = client.cancel_order( hash=order_hash )

print ( canceled_order )
