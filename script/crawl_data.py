import requests
import pandas as pd
from io import StringIO

'''
Balance Sheet: 資產負債表
Income Statement: 綜合損益表
Cash Flow Statement: 現金流量表
'''

BASE_URLS = {
    "bs": "https://mops.twse.com.tw/mops/web/t164sb03",
    "is": "https://mops.twse.com.tw/mops/web/t164sb04",
    "cf": "https://mops.twse.com.tw/mops/web/t164sb05",
}

def fetch_report(
    co_id: str, 
    year: str, 
    season: str, 
    report_type: str
) -> pd.DataFrame:
    """
    report_type: "bs", "is", or "cf"
    """
    url = BASE_URLS[report_type]
    params = {
        "dataType": "2",
        "companyId": co_id,
        "year": year,
        "season": season,
        "subsidiaryCompanyId": ""
    }
    print(f"GET {url} with params: {params}")
    print(url)
    r = requests.get(url, params=params)
    print("Requested URL:", r.url)
    r.encoding = "utf8"
    print(r.text)
    df_list = pd.read_html(StringIO(r.text))
    df = pd.concat(df_list[1:], ignore_index=True, sort=False)
    return df

def main():
    ai_companies = ["2330", "1504"]  # replace with actual AI-sector IDs
    years = ["114"]           # ROC years
    seasons = ["1", "2", "3", "4"]
    reports = {}

    for cid in ai_companies:
        for y in years:
            for s in seasons:
                key = f"{cid}_{y}_Q{s}"
                reports[key] = {
                    "bs": fetch_report(cid, y, s, "bs"),
                    "is": fetch_report(cid, y, s, "is"),
                    "cf": fetch_report(cid, y, s, "cf")
                }
                print(f"Fetched: {key}")

    # Example: show one
    print(reports[f"{ai_companies[0]}_{years[0]}_Q1"]["bs"].head())

if __name__ == "__main__":
    main()
