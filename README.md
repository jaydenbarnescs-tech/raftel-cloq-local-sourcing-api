# Raftel / CLOQ 国内ソーシング・フォーム営業API 利用ガイド

このGitHubリポジトリ自体が、瀬戸山さん向けの利用ドキュメントです。

このAPIは、Raftel / CLOQ の国内ソーシングで使います。目的は「フォーム営業に使える会社情報」を集め、私たちの本番システムに根拠付きで同期することです。

## 役割分担

| 担当 | やること | 主に見る情報 |
| --- | --- | --- |
| 瀬戸山さん | フォーム営業用の会社調査 | 問い合わせフォームURL、公式サイト、業界、業務内容、フォーム営業対象としての理由 |
| Jayden側 | メール営業用のソーシング・送信管理 | メールアドレス、送信履歴、除外・重複管理、CLOQ/RAFTELの送信制御 |

瀬戸山さん側でメールアドレスを見つけた場合も入力して大丈夫です。ただし、瀬戸山さんの主目的は「フォーム営業で使える問い合わせ先・会社理解」を集めることです。

## 重要URL

API:

```text
https://mgc-pass-proxy.duckdns.org/setoyama-api
```

OpenAPI:

```text
https://mgc-pass-proxy.duckdns.org/setoyama-api/openapi.json
```

APIのURLには歴史的な理由で `setoyama-api` が入っていますが、用途は Raftel / CLOQ の国内ソーシング・フォーム営業APIです。

ドキュメントはこのGitHub READMEを正本にします。API側の `/docs` は使いません。

APIトークンは別途共有します。GitHub、Slack、Notionなど公開される場所には絶対に貼らないでください。

## 5分で動作確認

まず、ターミナルで次を実行してください。

```bash
export SETOYAMA_API_TOKEN="ここに共有されたAPIトークンを貼り付け"
```

次にテーブル一覧を取得します。

```bash
curl --compressed -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  https://mgc-pass-proxy.duckdns.org/setoyama-api/tables
```

成功すると、次のようなJSONが返ります。

```json
{
  "tables": [
    "api_devices",
    "companies",
    "enrichment_fields",
    "enrichment_targets",
    "incoming_enrichment",
    "partner_company_enrichment",
    "sync_meta"
  ]
}
```

`device_pending_approval` が返った場合は、別端末として扱われています。後述の「端末承認」を見てください。

スクリプトで毎回同じ端末として扱いたい場合は、任意の固定IDを設定できます。

```bash
export SETOYAMA_DEVICE_ID="setoyama-main-pc"
```

この値を使う場合、Pythonサンプルは `X-Setoyama-Device-Id` ヘッダーを自動で送ります。`curl` で使う場合は次のように追加してください。

```bash
curl --compressed -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "X-Setoyama-Device-Id: setoyama-main-pc" \
  https://mgc-pass-proxy.duckdns.org/setoyama-api/tables
```

## 一番大事なテーブル

通常はこのテーブルだけ使えば大丈夫です。

```text
partner_company_enrichment
```

このテーブルに、会社ごとのフォーム営業用ソーシング情報を入れます。

テーブル名に `enrichment` が入っていますが、ここでは「フォーム営業用の国内ソーシング情報」と考えてください。

## 法人番号は必須ではありません

`corporate_number` は分かる場合だけ入力してください。

フォーム営業用のソーシングでは、法人番号が分からなくても次の情報があれば登録して大丈夫です。

- `company_name`: 会社名
- `website_url`: 公式Webサイト
- `contact_form_url`: 問い合わせフォームURL
- `business_description`: 業務内容
- `industry_primary`: 業界
- `evidence_url`: 根拠URL

法人番号がない例:

```json
{
  "company_name": "法人番号未確認サンプル株式会社",
  "website_url": "https://example.jp/",
  "contact_form_url": "https://example.jp/contact",
  "business_description": "食品工場向け包装資材の製造・販売",
  "industry_primary": "製造業",
  "target_relevance": "公式問い合わせフォームがあるためフォーム営業候補。",
  "confidence": 0.78,
  "evidence_url": "https://example.jp/company"
}
```

`corporate_number` を空文字で送っても、API側では未入力として扱います。

## まず何を入力すればいいか

優先順位は次の通りです。

| 優先度 | フィールド | 日本語 | 何を入れるか | 例 |
| --- | --- | --- | --- | --- |
| 1 | `contact_form_url` | 問い合わせフォームURL | フォーム営業で送信できるフォームURL | `https://example.jp/contact` |
| 2 | `website_url` | 公式Webサイト | 会社の公式サイト | `https://example.jp/` |
| 3 | `business_description` | 業務内容 | 何をしている会社か | `食品工場向け包装資材の製造・販売` |
| 4 | `industry_primary` | 業界 | 主な業界 | `製造業` |
| 5 | `target_relevance` | フォーム営業対象としての理由 | なぜ営業対象として良いか | `B2B商材で公式問い合わせフォームあり` |
| 6 | `exclusion_reason` | 除外理由 | 送らない方がいい理由 | `学校`, `行政`, `競合`, `会社閉鎖` |
| 7 | `employee_count` / `employee_count_text` | 従業員数 | 人数または規模感 | `52`, `10〜50名` |
| 8 | `phone_number` | 電話番号 | 代表電話番号 | `03-1234-5678` |
| 9 | `representative_name` | 代表者名 | 公開されている代表者 | `山田 太郎` |
| 10 | `primary_email` | メールアドレス | 公開されている会社メール | `info@example.jp` |
| 11 | `employee_accounts_json` | 社員・採用アカウント | 採用ページや公開プロフィール | `[{"name":"採用ページ","url":"https://example.jp/recruit"}]` |
| 12 | `evidence_url` | 根拠URL | 情報を確認したページ | `https://example.jp/company` |
| 13 | `confidence` | 確度 | 0.0〜1.0 | `0.86` |
| 14 | `notes` | メモ | 補足 | `公式サイト確認済み` |

## 良い入力例

```json
{
  "corporate_number": "1234567890123",
  "company_name": "サンプル株式会社",
  "website_url": "https://example.jp/",
  "contact_form_url": "https://example.jp/contact",
  "business_description": "食品工場向け包装資材の製造・販売",
  "industry_primary": "製造業",
  "target_relevance": "B2B商材で公式問い合わせフォームがあり、フォーム営業対象として適切。",
  "employee_count": 52,
  "phone_number": "03-1234-5678",
  "primary_email": "info@example.jp",
  "confidence": 0.86,
  "evidence_url": "https://example.jp/company",
  "notes": "公式サイトの会社概要と問い合わせページを確認済み"
}
```

## 悪い入力例

これは使いにくいです。

```json
{
  "company_name": "サンプル",
  "notes": "よさそう"
}
```

理由:

- 公式サイトがない
- 問い合わせフォームURLがない
- 何の会社か分からない
- なぜフォーム営業対象なのか分からない
- 根拠URLがない

## 1件登録する

`examples/company-enrichment.json` を使う場合:

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/tables/partner_company_enrichment/rows \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d @examples/company-enrichment.json
```

直接JSONを書く場合:

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/tables/partner_company_enrichment/rows \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "row": {
      "corporate_number": "1234567890123",
      "company_name": "サンプル株式会社",
      "website_url": "https://example.jp/",
      "contact_form_url": "https://example.jp/contact",
      "business_description": "食品工場向け包装資材の製造・販売",
      "industry_primary": "製造業",
      "target_relevance": "B2B商材で公式問い合わせフォームあり。",
      "confidence": 0.86,
      "evidence_url": "https://example.jp/company"
    }
  }'
```

成功例:

```json
{
  "ok": true,
  "table": "partner_company_enrichment",
  "rowid": 1
}
```

## 登録済みデータを見る

最新100件を見る:

```bash
curl --compressed -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  "https://mgc-pass-proxy.duckdns.org/setoyama-api/tables/partner_company_enrichment/rows?limit=100"
```

見やすく整形する:

```bash
curl --compressed -sS -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  "https://mgc-pass-proxy.duckdns.org/setoyama-api/tables/partner_company_enrichment/rows?limit=20" \
  | python3 -m json.tool
```

## 条件を指定して検索する

SQLの `SELECT` が使えます。

フォームURLがある会社だけ見る:

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/sql/query \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "sql": "SELECT company_name, website_url, contact_form_url, industry_primary FROM partner_company_enrichment WHERE contact_form_url IS NOT NULL AND contact_form_url != '' LIMIT 20"
}
JSON
```

業界で検索する:

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/sql/query \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "sql": "SELECT company_name, industry_primary, business_description, contact_form_url FROM partner_company_enrichment WHERE industry_primary LIKE ? LIMIT 20",
  "params": ["%製造%"]
}
JSON
```

除外対象を見る:

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/sql/query \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON'
{
  "sql": "SELECT company_name, exclusion_reason, evidence_url FROM partner_company_enrichment WHERE exclusion_reason IS NOT NULL AND exclusion_reason != '' LIMIT 20"
}
JSON
```

## 登録済みデータを更新する

まず行IDを確認します。レスポンス内の `_rowid` が行IDです。

```bash
curl --compressed -sS -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  "https://mgc-pass-proxy.duckdns.org/setoyama-api/tables/partner_company_enrichment/rows?limit=10" \
  | python3 -m json.tool
```

行ID `1` を更新する例:

```bash
curl --compressed -X PATCH https://mgc-pass-proxy.duckdns.org/setoyama-api/tables/partner_company_enrichment/rows/1 \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "row": {
      "contact_form_url": "https://example.jp/inquiry",
      "confidence": 0.92,
      "notes": "問い合わせフォームURLを更新"
    }
  }'
```

## 行を削除する

間違って入れた行を削除する例:

```bash
curl --compressed -X DELETE https://mgc-pass-proxy.duckdns.org/setoyama-api/tables/partner_company_enrichment/rows/1 \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN"
```

瀬戸山さん側のデータベースで削除しても、私たちの会社マスターデータは削除されません。

## CSVからまとめて登録する

CSVテンプレート:

```text
examples/form-sales-sourcing.csv
```

アップロード:

```bash
python3 examples/upload_csv.py examples/form-sales-sourcing.csv
```

必要な環境変数:

```bash
export SETOYAMA_API_TOKEN="ここに共有されたAPIトークンを貼り付け"
```

CSVのカラム例:

```csv
corporate_number,company_name,website_url,contact_form_url,business_description,industry_primary,target_relevance,exclusion_reason,employee_count_text,phone_number,primary_email,confidence,evidence_url,notes
1234567890123,サンプル株式会社,https://example.jp/,https://example.jp/contact,食品工場向け包装資材の製造・販売,製造業,B2B商材で公式問い合わせフォームあり,,10〜50名,03-1234-5678,info@example.jp,0.86,https://example.jp/company,公式サイト確認済み
```

法人番号がない場合は、`corporate_number` 列を空のままにしてください。

## Pythonから使う

接続確認:

```bash
export SETOYAMA_DEVICE_ID="setoyama-main-pc"
python3 examples/check_connection.py
```

1件登録:

```bash
export SETOYAMA_DEVICE_ID="setoyama-main-pc"
python3 examples/create_one_company.py
```

## 端末承認

最初に認証された端末は自動承認されます。

別PCや別ブラウザからアクセスすると、次のようなレスポンスが返ることがあります。

```json
{
  "ok": false,
  "error": "device_pending_approval",
  "device_id": "dev_abc...",
  "approval_code": "123456"
}
```

その場合、すでに承認済みの端末から次を実行してください。

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/devices/approve \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"approval_code":"123456","label":"瀬戸山さん 作業PC"}'
```

## `confidence` の目安

| 値 | 意味 |
| --- | --- |
| `0.95` | 公式サイトで確認でき、会社名・内容が明確に一致 |
| `0.80` | かなり信頼できる公開情報だが、公式情報ではない |
| `0.60` | おそらく正しいが後で確認したい |
| `0.60` 未満 | 不確実。`notes` に理由を書く |

## `exclusion_reason` の例

フォーム営業対象から外す場合は、理由を書いてください。

- `競合`
- `行政・自治体`
- `学校・教育機関`
- `採用代理店`
- `営業代行会社`
- `会社閉鎖・事業停止`
- `問い合わせ先が見つからない`
- `フォーム送信禁止と明記`
- `すでに接触済みの可能性`

## 社員アカウントの書き方

`employee_accounts_json` はJSON文字列で入れてください。

```json
[
  {
    "name": "採用ページ",
    "url": "https://example.jp/recruit",
    "memo": "社員インタビューあり"
  },
  {
    "name": "Wantedly",
    "url": "https://www.wantedly.com/companies/example",
    "memo": "事業内容と社員情報の参考"
  }
]
```

APIに入れる時は、1行の文字列にします。

```json
{
  "employee_accounts_json": "[{\"name\":\"採用ページ\",\"url\":\"https://example.jp/recruit\",\"memo\":\"社員インタビューあり\"}]"
}
```

## よくあるエラー

### `401 missing or invalid bearer token`

APIトークンが入っていません。

確認:

```bash
echo "$SETOYAMA_API_TOKEN"
```

空なら、もう一度設定してください。

```bash
export SETOYAMA_API_TOKEN="ここに共有されたAPIトークンを貼り付け"
```

### `403 device_pending_approval`

新しい端末として扱われています。レスポンスに出た `approval_code` を、承認済み端末から `/devices/approve` に送ってください。

### `row has no valid columns for table`

JSONのキー名がテーブルのカラム名と違います。まずスキーマを見てください。

```bash
curl --compressed -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  https://mgc-pass-proxy.duckdns.org/setoyama-api/schema/partner_company_enrichment
```

### `not authorized`

禁止されているSQLを実行しています。`ATTACH`、`DETACH`、`PRAGMA`、拡張機能の読み込み、外部DBアクセスはできません。

## 安全範囲

このAPIから、私たちのファイル、本番Postgres、メールボックスのシークレット、送信キュー、Mesh内部情報にはアクセスできません。

瀬戸山さん用のSQLiteデータベースだけを編集できます。

## もっと詳しいページ

- [docs/API-REFERENCE.md](docs/API-REFERENCE.md): APIエンドポイント一覧
- [docs/DATA-STRUCTURE.md](docs/DATA-STRUCTURE.md): テーブル構造
- [docs/ENRICHMENT-GUIDE.md](docs/ENRICHMENT-GUIDE.md): 入力項目と品質ルール
