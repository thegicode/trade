import os
import pandas as pd

def save_market_backtest_result(market, df, count, name) :
    output_dir = f'results/{name}_backtest'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{name}_{market}_{count}.csv')
    df.to_csv(output_file, index=True) 

def save_backtest_results(results, count, name):
    """
    백테스트 결과를 저장하는 함수

    :param results: 백테스트 결과 리스트
    :param count: 데이터 개수
    :return: 저장된 결과의 데이터프레임
    """
    results_df = pd.DataFrame(results)

    # Win Rate 기준으로 정렬
    results_df = results_df.sort_values(by="Win Rate (%)", ascending=False)

    # 결과를 저장할 디렉터리 생성
    output_dir = 'results'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{name}_backtest_{count}.csv')

    # CSV 파일로 저장
    results_df.to_csv(output_file, index=False)
    print(f"Backtest ${name} results saved to '{output_file}'.")

    # CSV 파일 읽기
    result_df = pd.read_csv(output_file)
    
    return result_df