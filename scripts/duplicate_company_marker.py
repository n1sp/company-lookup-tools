#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def process_company_duplicates(input_file_path, output_file_path=None):
	"""
	企業名の重複をチェックし、最初の出現に（重複元）、2つ目以降に（重複先）を付けて保存する
	
	Args:
		input_file_path (str): 入力ファイルのパス
		output_file_path (str, optional): 出力ファイルのパス。Noneの場合は元ファイルを上書き
	"""
	
	# ファイルを読み込み
	try:
		with open(input_file_path, 'r', encoding='utf-8') as file:
			lines = [line.strip() for line in file.readlines() if line.strip()]
	except FileNotFoundError:
		print(f"エラー: ファイル '{input_file_path}' が見つかりません。")
		return
	except Exception as e:
		print(f"ファイル読み込みエラー: {e}")
		return
	
	# 企業名の出現回数をカウント
	company_count = {}
	for company in lines:
		company_count[company] = company_count.get(company, 0) + 1
	
	# 重複している企業名をリスト化
	duplicates = [company for company, count in company_count.items() if count > 1]
	
	print("=== 重複している企業名一覧 ===")
	if duplicates:
		for i, company in enumerate(duplicates, 1):
			print(f"{i}. {company} (出現回数: {company_count[company]}回)")
	else:
		print("重複している企業名はありません。")
	print()
	
	# 重複している企業名に（重複元）または（重複先）を付ける
	processed_lines = []
	first_occurrence = {}  # 各企業名の最初の出現を記録
	
	for company in lines:
		if company in duplicates:
			if company not in first_occurrence:
				# 最初の出現：重複元
				first_occurrence[company] = True
				processed_lines.append(f"{company}（重複元）")
			else:
				# 2回目以降の出現：重複先
				processed_lines.append(f"{company}（重複先）")
		else:
			processed_lines.append(company)
	
	# 出力ファイルパスの決定
	if output_file_path is None:
		output_file_path = input_file_path
	
	# ファイルに書き込み
	try:
		with open(output_file_path, 'w', encoding='utf-8') as file:
			for line in processed_lines:
				file.write(line + '\n')
		print(f"処理完了: {output_file_path} に保存しました。")
	except Exception as e:
		print(f"ファイル書き込みエラー: {e}")
		return
	
	# 処理結果の表示
	print("\n=== 処理結果 ===")
	for line in processed_lines:
		print(line)


def create_sample_file(file_path):
	"""
	サンプルファイルを作成する（テスト用）
	"""
	sample_data = """A社
B社
B社
C社
A社"""
	
	with open(file_path, 'w', encoding='utf-8') as file:
		file.write(sample_data)
	print(f"サンプルファイル '{file_path}' を作成しました。")


if __name__ == "__main__":
	import sys
	
	print("企業名重複チェック・修正スクリプト（重複元・重複先識別版）")
	print("=" * 40)
	
	# コマンドライン引数をチェック
	if len(sys.argv) < 2:
		print("使用方法:")
		print(f"  python {sys.argv[0]} <入力ファイルパス> [出力ファイルパス]")
		print(f"  python {sys.argv[0]} --sample  # サンプルファイルを作成")
		print()
		
		# サンプル実行の提案
		create_sample = input("サンプルファイルを作成して実行しますか？ (y/n): ")
		if create_sample.lower() == 'y':
			sample_file = "sample_companies.txt"
			create_sample_file(sample_file)
			print()
			process_company_duplicates(sample_file)
		sys.exit(1)
	
	# サンプルファイル作成オプション
	if sys.argv[1] == "--sample":
		create_sample_file("sample_companies.txt")
		sys.exit(0)
	
	# メイン処理
	input_file = sys.argv[1]
	output_file = sys.argv[2] if len(sys.argv) > 2 else None
	
	process_company_duplicates(input_file, output_file)