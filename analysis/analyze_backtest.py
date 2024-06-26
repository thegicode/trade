# analysis/analyze_backtest.py

import os
import sys
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from coins import coin_list

# CSV 파일 경로
CSV_PATHS = {
    'daily_average': 'results/backtest/daily_average_backtest_200.csv',
    'golden_cross': 'results/backtest/golden_dead_cross_backtest_200.csv',
    'volatility': 'results/backtest/volatility_backtest_200.csv',
    'volatility_ma': 'results/backtest/volatility_checkMA_backtest_200.csv',
    'volatility_volume': 'results/backtest/volatility_checkMA_checkVolume_backtest_200.csv',
    'afternoon': 'results/backtest/afternoon_backtest_200.csv'
}

# CSV 파일 불러오기
dataframes = {name: pd.read_csv(path) for name, path in CSV_PATHS.items()}

# 결과 저장 디렉토리 생성
output_dir = 'results/analysis'
os.makedirs(output_dir, exist_ok=True)


# 코인별로 분석하고 결과를 텍스트 파일로 저장하는 함수
def analyze_coin(coin, dataframes, output_file):
    backtests = ['daily_average', 'golden_cross', 'volatility', 'volatility_ma', 'volatility_volume', 'afternoon']
    backtest_names = ['Daily Average', 'Golden Cross', 'Volatility Breakout',
                      '+ (MA Check)', '+ (Volume Check)', 'Afternoon']

    # 결과를 하나의 데이터프레임으로 합치기
    combined_df = pd.DataFrame({
        'Backtest': backtest_names,
        'Cumulative Return (%)': [
            dataframes[bt][dataframes[bt]['Market'] == coin]['Cumulative Return (%)'].values[0]
            if not dataframes[bt][dataframes[bt]['Market'] == coin].empty else None
            for bt in backtests
        ],
        'Win Rate (%)': [
            dataframes[bt][dataframes[bt]['Market'] == coin]['Win Rate (%)'].values[0]
            if not dataframes[bt][dataframes[bt]['Market'] == coin].empty else None
            for bt in backtests
        ],
        'Max Drawdown (MDD) (%)': [
            dataframes[bt][dataframes[bt]['Market'] == coin]['Max Drawdown (MDD) (%)'].values[0]
            if not dataframes[bt][dataframes[bt]['Market'] == coin].empty else None
            for bt in backtests
        ]
    })

    # 결과를 텍스트 파일로 저장
    with open(output_file, 'a') as f:
        f.write(f"=== {coin} ===\n")
        f.write(combined_df.to_string(index=False))
        f.write("\n\n")

    # 결과 출력
    print(f"=== {coin} ===")
    print(combined_df)
    print("\n")


# 현재 날짜를 가져와 형식에 맞게 변환
current_date = datetime.datetime.now().strftime("%Y%m%d")

# 텍스트 파일 경로에 날짜 추가
output_file = os.path.join(output_dir, f'analysis_backtest_{current_date}.txt')

# 기존 텍스트 파일 삭제 (이미 존재할 경우)
if os.path.exists(output_file):
    os.remove(output_file)

# 각 코인별로 결과 분석 및 텍스트 파일 저장
for coin in coin_list:
    analyze_coin(coin, dataframes, output_file)
