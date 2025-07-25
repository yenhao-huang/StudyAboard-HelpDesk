import requests
import pandas as pd
import numpy as np

def financial_statement(year, season, type='綜合損益彙總表'):
    """
    抓取 MOPS 財報彙總資料（全市場，不是個別公司）

    Parameters:
    - year (int): 民國年 或 西元年（>= 1911）
    - season (int): 第幾季（1~4）
    - type (str): 彙總報表種類，可選：
        - '綜合損益彙總表'
        - '資產負債彙總表'
        - '營益分析彙總表'

    Returns:
    - pandas.DataFrame
    """
    if year >= 1000:
        year -= 1911

    url_map = {
        '綜合損益彙總表': 'https://mops.twse.com.tw/mops/web/ajax_t163sb04',
        '資產負債彙總表': 'https://mops.twse.com.tw/mops/web/ajax_t163sb05',
        '營益分析彙總表': 'https://mops.twse.com.tw/mops/web/ajax_t163sb06',
    }

    if type not in url_map:
        raise ValueError("❌ Invalid report type. Must be one of: " + ", ".join(url_map.keys()))

    url = url_map[type]

    payload = {
        'encodeURIComponent': '1',
        'step': '1',
        'firstin': '1',
        'off': '1',
        'TYPEK': 'sii',
        'year': str(year),
        'season': str(season),
    }

    r = requests.post(url, data=payload)
    r.encoding = 'utf8'

    try:
        dfs = pd.read_html(r.text, header=None)
        df = pd.concat(dfs[1:], axis=0, ignore_index=True, sort=False)
    except Exception as e:
        print("⚠️ Failed to parse tables:", e)
        return pd.DataFrame()

    # 將數值欄轉為數字型態
    df = df.set_index('公司代號', drop=False)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

df = financial_statement(2024, 1, type='綜合損益彙總表')
print(df.head())