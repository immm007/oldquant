# -*- coding: utf-8 -*-
from datasource import Maintainer
import requests

requests.adapters.DEFAULT_RETRIES = 3
ma = Maintainer()
ma.downloadIndexes()
ma.complementAll()
