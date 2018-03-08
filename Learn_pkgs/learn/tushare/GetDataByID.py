# /usr/bin/env python
# -*- coding:utf-8 -*-

import tushare as ts

data=ts.get_hist_data('300032')
print(data)