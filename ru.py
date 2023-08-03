# отдельный класс - список ассетов?

import pandas as pd
import numpy as np
import yfinance as yf

goog = yf.download(['LKOH.ME', 'GMKN.ME', 'DSKY.ME'])['Adj Close'] #start= end=YYYY-MM-DD

nullin_df = pd.DataFrame(goog, columns=['LKOH.ME', 'GMKN.ME', 'DSKY.ME'])
print(nullin_df.isnull().sum())
