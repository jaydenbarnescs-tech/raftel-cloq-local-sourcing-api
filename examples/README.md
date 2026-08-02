# examples

このフォルダには、Raftel / CLOQ 国内ソーシングAPIを実際に使うためのサンプルがあります。

## 事前準備

```bash
export SETOYAMA_API_TOKEN="ここに共有されたAPIトークンを貼り付け"
export SETOYAMA_DEVICE_ID="setoyama-main-pc"
```

## 接続確認

```bash
python3 examples/check_connection.py
```

## 1件だけ登録

```bash
python3 examples/create_one_company.py
```

## CSVから登録

CSVテンプレート:

```text
examples/form-sales-sourcing.csv
```

実行:

```bash
python3 examples/upload_csv.py examples/form-sales-sourcing.csv
```

## フォーム営業対象を一覧表示

```bash
python3 examples/query_form_targets.py
```

## ファイル説明

- `api_client.py`: API接続用の小さいPythonクライアント
- `check_connection.py`: トークン・端末承認・テーブル取得の確認
- `create_one_company.py`: フォーム営業用の会社調査データを1件登録
- `upload_csv.py`: CSVから複数件登録
- `query_form_targets.py`: 問い合わせフォームURLがある会社を一覧表示
- `company-enrichment.json`: 1件登録用JSON例
- `form-sales-sourcing.csv`: CSVテンプレート

