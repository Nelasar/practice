import pandas as pd
import numpy as np
import scipy.optimize as sco
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.lines as mlines
from tqdm import tqdm_notebook

# Для отрисовки сетки за графиком
plt.rc('axes', axisbelow=True)

stocks = ["AFKS",
          "AFLT",
          "ALRS",
          "CBOM",
          "CHMF",
          "DSKY",
          "FEES",
          "GAZP",
          "GMKN",
          "HYDR",
          "IRAO",
          "LKOH",
          "MAGN",
          "MGNT",
          "MOEX",
          "MTLR",
          "MTSS",
          "MVID",
          "NLMK",
          "NVTK",
          "PHOR",
          "PIKK",
          "PLZL",
          "POLY",
          "RNFT",
          "ROSN",
          "RTKM",
          "RUAL",
          "SBER",
          "SBERP",
          "SNGS",
          "SNGSP",
          "TATN",
          "TATNP",
          "TRMK",
          "TRNFP",
          "UPRO",
          "UWGN",
          "VTBR",
          "YNDX"]

imoex = pd.read_csv('./csv/'+'IMOEX.csv', parse_dates=['Date'], index_col=0)['Close']['2013-01-01':'2018-10-31']
imoex.plot();
plt.show()

price = pd.DataFrame()
for symbol in stocks:
    price[symbol] = pd.read_csv('./csv/'+symbol+'.csv', parse_dates=['Date'], index_col=0)['Close']['2013-01-01':'2018-10-31']

print(price.head())
# How NaN rows
price.isnull().sum()

isnull = price.isnull().sum()
for ticker in stocks:     #если слишком много значений null исключаем акцию из анализа
    try:
        if isnull[ticker] > 50:
            price.drop(ticker, axis=1, inplace=True)
    except:
        pass

# How NaN rows
price.isnull().sum()

# Delete NaN rows
#price.dropna(inplace=True)

risk_free_rate = 0.0 # Безрисковая процентная ставка
num_periods_annually = 252 # Количество операционных дней в году

returns = price.pct_change()
mean_returns = returns.mean()
cov_matrix = returns.cov()

a_rsk = np.std(returns) * np.sqrt(num_periods_annually)
a_ret = mean_returns*num_periods_annually


# Функция вычисляющая риск и доходность для конкретного портфеля
def portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns*weights ) * num_periods_annually
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(num_periods_annually)
    return std, returns


def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    p_var, p_ret = portfolio_performance(weights, mean_returns, cov_matrix)
    return -(p_ret - risk_free_rate) / p_var


def max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0, 1.0)
    bounds = tuple(bound for asset in range(num_assets))

    result = sco.minimize(neg_sharpe_ratio, num_assets * [1. / num_assets, ], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
    return result


def portfolio_risk(weights, mean_returns, cov_matrix):
    return portfolio_performance(weights, mean_returns, cov_matrix)[0]


def min_risk(mean_returns, cov_matrix):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0,1.0)
    bounds = tuple(bound for asset in range(num_assets))

    result = sco.minimize(portfolio_risk, num_assets*[1./num_assets,], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)

    return result


def neg_portfolio_return(weights, mean_returns, cov_matrix):
    return -1*portfolio_performance(weights, mean_returns, cov_matrix)[1]


def neg_portfolio_return(weights, mean_returns, cov_matrix):
    return -1*portfolio_performance(weights, mean_returns, cov_matrix)[1]


def max_return(mean_returns, cov_matrix):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0,1.0)
    bounds = tuple(bound for asset in range(num_assets))

    result = sco.minimize(neg_portfolio_return, num_assets*[1./num_assets,], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)

    return result


def efficient_return(mean_returns, cov_matrix, target):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)

    def portfolio_return(weights):
        return portfolio_performance(weights, mean_returns, cov_matrix)[1]

    constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    result = sco.minimize(portfolio_risk, num_assets * [1. / num_assets, ], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
    return result


def efficient_frontier(mean_returns, cov_matrix, returns_range):
    efficients = []
    for ret in returns_range:
        efficients.append(efficient_return(mean_returns, cov_matrix, ret))
    return efficients


sharpe_max = max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate)
risk_min = min_risk(mean_returns, cov_matrix)
return_max = max_return(mean_returns, cov_matrix)

print(return_max)

# вычисляем риски и доходности найденных портфелей
sharpe_std, sharpe_ret = portfolio_performance(sharpe_max['x'], mean_returns, cov_matrix)
min_std, min_ret = portfolio_performance(risk_min['x'], mean_returns, cov_matrix)
max_std, max_ret = portfolio_performance(return_max['x'], mean_returns, cov_matrix)

target = np.linspace(min_ret, max_ret, 20)
efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)

print("-"*80)
print("Портфель с максимальным коэффициентом Шарпа\n")
print("Доходность:", round(sharpe_ret,3))
print("Риск:", round(sharpe_std,3))
print("Коэффициент Шарпа:", round((sharpe_ret - risk_free_rate)/sharpe_std, 3))
print("-"*80)
print("Портфель с минимальным риском\n")
print("Доходность:", round(min_ret,3))
print("Риск:", round(min_std,3))
print("Коэффициент Шарпа:", round((min_ret - risk_free_rate)/min_std, 3))
print("-"*80)
print("Портфель с максимальным показателем доходности\n")
print("Доходность:", round(max_ret,3))
print("Риск:", round(max_std,3))
print("Коэффициент Шарпа::", round((max_ret - risk_free_rate)/max_std, 3))

plt.figure(figsize=(10, 7))

#plt.scatter(results[0,:],results[1,:],c=results[2,:],cmap='YlGnBu', marker='o', s=10, alpha=0.3)

plt.scatter(sharpe_std, sharpe_ret, marker='s', color='r', s=150, label='Макс. коэф-т Шарпа')
plt.scatter(min_std, min_ret, marker='s', color='g', s=150, label='Мин. риск')
plt.scatter(max_std, max_ret, marker='s', color='b', s=150, label='Макс. доходность')

plt.scatter(a_rsk, a_ret, marker='o', s=20, c='red', edgecolors='black')
for i, txt in enumerate(price.columns):
    plt.annotate(txt, (a_rsk[i], a_ret[i]), xytext=(10,0), textcoords='offset points')

plt.plot([p['fun'] for p in efficient_portfolios], target, 'k-x', label='граница эффективности')

plt.grid(True, linestyle='--')
plt.title('Граница эффективности с Максимальным коэффициентом Шарпа, Минимальным риском и Максимальной доходностью')
plt.xlabel('Риск (годовой)')
plt.ylabel('Доходность (годовая)')
plt.legend(labelspacing=0.8)

#plt.xlim(0.1, 0.5)
#plt.ylim(-0.05, 0.25)

plt.tight_layout();
plt.show()

# ВЫЧИСЛЕНИЕ ДОХОДНОСТИ
# С ЗАДАННЫМ ПОКАЗАТЕЛЕМ РИСКА
# И ЗАДАННЫМ УРОВНЕМ ДОХОДНОСТИ

TargetReturn = 0.20
TargetRisk = 0.15


def portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns*weights ) * num_periods_annually
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(num_periods_annually)
    return std, returns


def portfolio_risk(weights, mean_returns, cov_matrix):
    return portfolio_performance(weights, mean_returns, cov_matrix)[0]


def targeted_return(mean_returns, cov_matrix, target):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)

    def portfolio_return(weights):
        return portfolio_performance(weights, mean_returns, cov_matrix)[1]

    constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0,1) for asset in range(num_assets))
    result = sco.minimize(portfolio_risk, num_assets*[1./num_assets,], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
    return result


def neg_portfolio_return(weights, mean_returns, cov_matrix):
    return -1*portfolio_performance(weights, mean_returns, cov_matrix)[1]


def targeted_risk(mean_returns, cov_matrix, target):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)

    def portfolio_risk(weights):
        return portfolio_performance(weights, mean_returns, cov_matrix)[0]

    constraints = ({'type': 'eq', 'fun': lambda x: portfolio_risk(x) - target},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0,1) for asset in range(num_assets))
    result = sco.minimize(neg_portfolio_return, num_assets*[1./num_assets,], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
    return result


t_return = targeted_return(mean_returns, cov_matrix, TargetReturn)
t_risk = targeted_risk(mean_returns, cov_matrix, TargetRisk)


sdp_return, rp_return = portfolio_performance(t_return['x'], mean_returns, cov_matrix)
sdp_risk, rp_risk = portfolio_performance(t_risk['x'], mean_returns, cov_matrix)


plt.figure(figsize=(10, 7))

plt.scatter(sdp_return, rp_return, marker='s', color='g', s=150, label='Заданная Доходность')
plt.scatter(sdp_risk, rp_risk, marker='s', color='r', s=150, label='Заданный Риск')

plt.scatter(a_rsk, a_ret, marker='o', s=20, c='red', edgecolors='black')
for i, txt in enumerate(price.columns):
    plt.annotate(txt, (a_rsk[i], a_ret[i]), xytext=(10,0), textcoords='offset points')

plt.plot([p['fun'] for p in efficient_portfolios], target, 'k-x', label='граница эффективности')

plt.grid(True, linestyle='--')
plt.title('Граница эффективности с заданным портфелем')
plt.xlabel('Риск (годовой)')
plt.ylabel('Доходность (годовая)')
plt.legend(labelspacing=0.8)

#plt.xlim(0.1, 0.5)
#plt.ylim(-0.05, 0.5)

plt.tight_layout();
plt.show()

# МОЖЕТ БЫТЬ КЛАСС "ПРЕДСКАЗАННЫЙ ПОРТФЕЛЬ"

ind = np.arange(price.columns.size)

plt.figure(figsize=(6,8))

#plt.barh(ind, sharpe_max['x'], align='center')
plt.barh(ind, risk_min['x'], align='center')
#plt.barh(ind, return_max['x'], align='center')
#plt.barh(ind, t_return['x'], align='center')
#plt.barh(ind, t_risk['x'], align='center')

plt.yticks(ind, price.columns)
plt.xlabel('Вес акции в портфеле')
plt.title('Распределений акций в портфеле')
#plt.legend(('Max Sharpe Ratio', 'Minimum Volatility'))
plt.grid(b=True, linestyle='--')

plt.tight_layout();


# Построение графика всех акций и доходности конкретного портфеля
portfolio_alloc = sharpe_max['x']
#portfolio_alloc = risk_min['x']
#portfolio_alloc = return_max['x']
#portfolio_alloc = t_return['x']
#portfolio_alloc = t_risk['x']

index = price.index
p_returns = pd.DataFrame(columns=['returns'])
for day in range(1, price.index.size):
    # Calculating portfolio return
    date0 = index[day]
    date1 = index[day-1]
    a_return = (price.loc[date0] - price.loc[date1])/price.loc[date1]
    p_returns.loc[index[day]] = np.sum(a_return*portfolio_alloc)

plt.figure(figsize=(10,5))

gray_line = mlines.Line2D([], [], color='gray', linewidth=1, label='Доходность акций')
plt.plot(price.pct_change().cumsum(),'gray', linewidth=1, alpha=0.5)

red_line = mlines.Line2D([], [], color='red', linewidth=3, label='Доходность портфеля')
plt.plot(p_returns.cumsum(), 'red', linewidth=3)

blue_line = mlines.Line2D([], [], color='blue', linewidth=3, label='Индекс Московской Биржи')
plt.plot(imoex.pct_change().cumsum(), 'blue', linewidth=3)

plt.grid(True, linestyle='--')
plt.title('Доходность портфеля, доходности акций и Индекс Московской Биржи')
plt.xlabel('Дата')
plt.ylabel('Доходность')
plt.legend(handles=[gray_line, red_line, blue_line])
plt.tight_layout();


p = (-sharpe_max['fun'] * 100)/6
print('Cредняя годовая доходность портфеля:', str(round(p, 2))+'%')

im = (imoex.pct_change().cumsum()[-1] * 100)/6
print('Cредняя годовая доходность индекса Московской Биржи:', str(round(im, 2))+'%')

print('Cредняя годовая доходность портфеля / индекс Московской Биржи:', round(p/im, 2))

# Т.о. в результате оптимизации удалось собрать портфель с максимальным коэффициентом Шарпа,
# который по доходности больше доходности индекса Московской Биржи за последние 6 лет

