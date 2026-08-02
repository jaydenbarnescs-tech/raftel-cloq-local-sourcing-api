# データ構造

このAPIは、Raftel / CLOQ の国内ソーシングで使う瀬戸山さん作業用SQLiteデータベースを公開しています。

用途はフォーム営業のための会社調査です。メール営業用のソーシング・送信管理はJayden側の別フローで扱います。

## `enrichment_targets`

フォーム営業のために調査・入力してほしい項目のチェックリストです。

主なカラム:

- `priority`: 優先度
- `field_name`: フィールド名
- `japanese_label`: 日本語ラベル
- `description`: 説明
- `example_value`: 入力例
- `why_it_matters`: なぜ重要か
- `suggested_source`: 推奨される情報源

## `partner_company_enrichment`

会社ごとのフォーム営業用ソーシング情報を入力する推奨テーブルです。

主なカラム:

- `corporate_number`: 法人番号
- `company_name`: 会社名
- `website_url`: 公式Webサイト
- `primary_email`: メールアドレス
- `contact_form_url`: 問い合わせフォームURL。フォーム営業では最優先
- `phone_number`: 電話番号
- `employee_count`: 従業員数
- `employee_count_text`: 従業員規模のテキスト
- `employee_source_url`: 従業員数の根拠URL
- `industry_primary`: 業界
- `industry_tags_json`: 業界・特徴タグ。JSON文字列
- `business_description`: 業務内容
- `representative_name`: 代表者名
- `representative_position`: 代表者役職
- `capital`: 資本金
- `recruiting_status`: 採用状況
- `employee_accounts_json`: 社員・採用・チーム関連アカウント。JSON文字列
- `target_relevance`: フォーム営業対象としての理由
- `exclusion_reason`: 除外理由
- `confidence`: 情報の確度
- `evidence_url`: 根拠URL
- `notes`: メモ
- `created_at`: 作成日時
- `updated_at`: 更新日時

## `enrichment_fields`

自由なキー・バリュー形式で追加調査情報を入れるテーブルです。

推奨テーブルに入らないフォーム営業・国内ソーシング関連情報を記録したい場合に使ってください。

主なカラム:

- `corporate_number`: 法人番号
- `company_name`: 会社名
- `field_name`: 項目名
- `field_value`: 値
- `value_json`: JSON形式の値
- `confidence`: 情報の確度
- `evidence_url`: 根拠URL
- `notes`: メモ

## 独自テーブル

必要であれば、瀬戸山さん側で追加テーブルを作成できます。

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/sql/execute \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sql":"CREATE TABLE IF NOT EXISTS custom_research (company_name TEXT, memo TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"}'
```

独自テーブルは、瀬戸山さん専用のSQLiteデータベース内にだけ作成されます。
