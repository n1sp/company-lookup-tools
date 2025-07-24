import os
from duckduckgo_search import DDGS
import json


"""
	指定された企業名でDuckDuckGoを検索し、関連するURLを取得
	Args:
		company_name (str): 企業名
	Returns:
		List[Dict]: 検索結果のURLリスト
"""


def get_company_urls(company_name):
    with DDGS() as ddgs:
        results = list(ddgs.text(
            keywords=company_name,		# 検索ワード
            region='jp-jp',	   			# リージョン 日本は"jp-jp",指定なしの場合は"wt-wt"
            safesearch='on',	 		# セーフサーチOFF->"off",ON->"on",標準->"moderate"
            timelimit=None,	   			# 期間指定 指定なし->None,過去1日->"d",過去1週間->"w", 過去1か月->"m",過去1年->"y"
            max_results=1		 		# 取得件数
        ))
    return results[0]['href'] if results else None


# "企業名,url" 形式のcsvファイルパス
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(script_dir, '../data/company_urls.csv')
# csvファイルを読み込む
with open(csv_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 各行を[企業名, url]のリストに変換
company_urls = []
for line in lines:
    parts = line.strip().split(',')
    if len(parts) == 2:
        company_name, url = parts
        company_urls.append([company_name, url])
    else:
        # URLがない場合は空文字列を格納
        company_urls.append([parts[0], ''])

# URLを取得して更新
for i, (company_name, url) in enumerate(company_urls):
    if not url:  # URLが空の場合のみ取得
        print(f"Fetching URL for: {company_name}")
        url = get_company_urls(company_name)
        company_urls[i][1] = url if url else ''  # URLが取得できなかった場合は空文字列を格納
# 更新されたURLをCSVファイルに書き込む
with open(csv_file, 'w', encoding='utf-8') as file:
    for company_name, url in company_urls:
        file.write(f"{company_name},{url}\n")
print("URL fetching and updating completed.")
