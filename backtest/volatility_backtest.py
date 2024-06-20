import time
import numpy as np
from api.upbit_api import get_daily_candles
from utils import save_market_backtest_result, save_backtest_results, calculate_cumulative_return, calculate_mdd, calculate_win_rate


def calculate_range(df):
    """
    변동성 돌파 전략의 range를 계산하는 함수
    :param df: 데이터프레임 (OHLCV)
    :return: 데이터프레임에 range 컬럼 추가
    """
    df['range'] = df['high'].shift(1) - df['low'].shift(1)
    return df


def generate_signals(df, k=0.5):
    """
    변동성 돌파 전략을 사용하여 매수 신호를 생성하는 함수
    :param df: 데이터프레임 (OHLCV)
    :param k: 변동성 비율 (기본값 0.5)
    :return: 매수 신호가 추가된 데이터프레임
    """
    df['target'] = df['open'] + df['range'] * k
    df['signal'] = np.where(df['close'] >= df['target'], 1, 0)
    df['positions'] = df['signal'].diff()
    return df


def backtest_strategy(df, initial_capital, investment_fraction=0.2):
    cash = initial_capital
    shares = 0
    df['holdings'] = 0.0
    df['cash'] = float(initial_capital)
    df['total'] = float(initial_capital)

    for i in range(1, len(df)):
        if df['positions'].iloc[i] == 1:  # 매수 신호
            investment = cash * investment_fraction
            shares += investment / df['close'].iloc[i]
            cash -= investment
        elif df['positions'].iloc[i] == -1:  # 매도 신호
            cash += shares * df['close'].iloc[i]
            shares = 0
        df.loc[df.index[i], 'holdings'] = shares * df['close'].iloc[i]
        df.loc[df.index[i], 'cash'] = cash
        df.loc[df.index[i], 'total'] = df.loc[df.index[i], 'holdings'] + df.loc[df.index[i], 'cash']

    df['returns'] = df['total'].pct_change()

    return df


def run_backtest(market, count, initial_capital, k=0.5, investment_fraction=0.2):
    df = get_daily_candles(market, count)

    # 오래된 데이터부터 정렬
    df = df.sort_index()

    df = calculate_range(df)
    df = generate_signals(df, k)
    df = backtest_strategy(df, initial_capital, investment_fraction)

    # 결과를 파일로 저장
    if count == 200:
        save_market_backtest_result(market, df, count, "volatility")

    cumulative_return_percent = calculate_cumulative_return(df, initial_capital)
    win_rate = calculate_win_rate(df)
    mdd_percent = calculate_mdd(df)

    result = {
        "Market": market,
        "Count": count,
        "Investment Fraction": investment_fraction,
        "Cumulative Return (%)": cumulative_return_percent,
        "Win Rate (%)": win_rate,
        "Max Drawdown (MDD) (%)": mdd_percent
    }

    return result


def run_volatility_backtest(markets, count=200, initial_capital=10000):
    results = []

    print("\n{ Volatility Backtest }")

    for market in markets:
        print(f"Volatility backtest for {market}...")
        result = run_backtest(market, count, initial_capital, k=0.5, investment_fraction=1)
        results.append(result)
        time.sleep(2)  # 각 API 호출 사이에 2초 지연

    result_df = save_backtest_results(results, count, "volatility")

    print(result_df)


if __name__ == "__main__":
    run_volatility_backtest()