# КЛАСТЕРИЗАЦИЯ АКЦИЙ С ИСПОЛЬЗОВАНИЕМ АЛГОРИТМА K-Means
# 04

import pandas as pd
import pandas_datareader as dr
import pickle
import math
import numpy as np
from sklearn.cluster import KMeans
from scipy.cluster.vq import kmeans,vq

import matplotlib.cm as cm
import matplotlib.pyplot as plt

stocks = ["MSNG",
"AGRO",
"ENPL",
"FIVE",
"POLY",
"RUAL",
"YNDX",
"QIWI",
"UNAC",
"DZRD",
"DZRDP",
"DIOD",
"ISKJ",
"LVHK",
"NAUK",
"NSVZ",
"RLMN",
"RLMNP",
"LIFE",
"AVAZ",
"AVAZP",
"ALRS",
"ALNU",
"ABRD",
"AVAN",
"AKRN",
"APTK",
"ARSA",
"ASSB",
"AMEZ",
"AFLT",
"BSPB",
"FTRE",
"BISV",
"BISVP",
"BANE",
"BANEP",
"BLNG",
"BELU",
"ALBK",
"BRZL",
"VSMO",
"VTBR",
"VLHZ",
"VDSB",
"VJGZ",
"VJGZP",
"VZRZ",
"VZRZP",
"VGSB",
"VGSBP",
"VSYD",
"VSYDP",
"GAZA",
"GAZAP",
"GAZT",
"GAZS",
"GAZC",
"GAZP",
"GRNT",
"GMKN",
"GTRK",
"RTGZ",
"SIBN",
"HALS",
"FESH",
"DVEC",
"DASB",
"DSKY",
"ZVEZ",
"ZILL",
"ZMZN",
"ZMZNP",
"RUSI",
"OPIN",
"IRKT",
"IGSTP",
"IGST",
"IDVP",
"IRAO",
"IRGZ",
"KMAZ",
"KMEZ",
"KTSB",
"KTSBP",
"KLSB",
"KCHE",
"KCHEP",
"TGKD",
"TGKDP",
"KOGK",
"KROTP",
"KROT",
"KRSB",
"KRSBP",
"KUBE",
"KBTK",
"KUZB",
"KAZT",
"KAZTP",
"KGKC",
"KGKCP",
"LSRG",
"LKOH",
"LPSB",
"LNZLP",
"LNZL",
"LNTA",
"LSNGP",
"LSNG",
"MVID",
"MGTSP",
"MGTS",
"MERF",
"CBOM",
"MAGN",
"MSRS",
"MRKZ",
"MRKK",
"MRKU",
"MRKP",
"MRKC",
"MRKV",
"MRKS",
"MRKY",
"MTSS",
"MAGE",
"MAGEP",
"MGNT",
"MISBP",
"MFON",
"MFGS",
"MFGSP",
"MTLR",
"MTLRP",
"MRSB",
"MORI",
"MOEX",
"MOBB",
"MSTT",
"MSST",
"MUGS",
"MUGSP",
"NKNC",
"NKNCP",
"NKHP",
"NLMK",
"NMTP",
"NFAZ",
"NKSH",
"NVTK",
"UWGN",
"OGKB",
"UCSS",
"OMZZP",
"OBUV",
"OMSH",
"KZOS",
"KZOSP",
"PIKK",
"PRTK",
"PAZA",
"PMSBP",
"PMSB",
"PLSM",
"PLZL",
"PRMB",
"RBCM",
"RGSS",
"RDRB",
"CHGZ",
"ROST",
"RASP",
"ROSB",
"ROSN",
"RSTI",
"RSTIP",
"RTKM",
"RTKMP",
"AQUA",
"HYDR",
"RUGR",
"ROLO",
"RUSP",
"RNFT",
"RZSB",
"SFIN",
"SZPR",
"MGNZ",
"SVAV",
"SAGO",
"SAGOP",
"KRKN",
"KRKNP",
"SARE",
"SAREP",
"SLEN",
"SBER",
"SBERP",
"CHMF",
"SELG",
"SELGP",
"SIBG",
"AFKS",
"JNOSP",
"JNOS",
"STSB",
"STSBP",
"SNGS",
"SNGSP",
"TANL",
"TGKA",
"TGKN",
"TGKB",
"TGKBP",
"TUZA",
"KRKO",
"KRKOP",
"TRMK",
"KBSB",
"VRSBP",
"VRSB",
"MISB",
"NNSB",
"NNSBP",
"RTSB",
"RTSBP",
"YRSB",
"YRSBP",
"TNSE",
"TORS",
"TORSP",
"TASB",
"TASBP",
"TATN",
"TATNP",
"TTLK",
"CNTL",
"CNTLP",
"TRCN",
"TRNFP",
"URKZ",
"USBN",
"URKA",
"FEES",
"NPOF",
"PHOR",
"HIMC",
"HIMCP",
"WTCM",
"WTCMP",
"PRFN",
"CHKZ",
"CHMK",
"CHEP",
"CLSB",
"CLSBP",
"GCHE",
"ELTZ",
"ENRU",
"RKKE",
"UTAR",
"UNKL",
"UKUZ",
"UPRO",
"YAKG",
"YKENP",
"YKEN"]

data = pd.DataFrame()
for symbol in stocks:
    data[symbol] = pd.read_csv('./csv/'+symbol+'.csv', parse_dates=['Date'], index_col=0)['Close']['2017-01-01':'2018-10-01']

isnull = data.isnull().sum()
for ticker in stocks:     #if too many null entries for given stock, exclude from analysis
    try:
        if isnull[ticker] > 50:
            data.drop(ticker, axis=1, inplace=True)
    except:
        pass

df = data.copy()



