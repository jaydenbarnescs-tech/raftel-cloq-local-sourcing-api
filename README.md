# Raftel / CLOQ 国内ソーシング・フォーム営業API

このリポジトリは、Raftel / CLOQ の国内ソーシング作業で使うAPIの説明資料です。

役割分担:

- 瀬戸山さん: フォーム営業用の会社情報・問い合わせフォーム情報を集める
- Jayden側: メール営業用のメールソーシング、送信管理、送信履歴管理を行う

瀬戸山さんには、フォーム営業に必要な会社情報をこのAPIに入力していただきます。

APIのベースURL:

```text
https://mgc-pass-proxy.duckdns.org/setoyama-api
```

APIドキュメント:

```text
https://mgc-pass-proxy.duckdns.org/setoyama-api/docs
```

OpenAPI:

```text
https://mgc-pass-proxy.duckdns.org/setoyama-api/openapi.json
```

APIトークンは別途共有します。GitHubには絶対に載せないでください。

## これは何か

Raftel / CLOQ の国内ソーシング用に用意した、瀬戸山さん作業用の編集可能なデータベースです。

API経由で、会社情報の追加、行の編集、独自テーブルの作成、フォーム営業に必要な情報の登録ができます。

瀬戸山さんが入力した情報は、私たちの本番システム側には「フォーム営業用の調査情報・根拠情報」として同期されます。私たちの会社マスターデータを直接上書きするものではありません。そのため、瀬戸山さん側では柔軟に編集して大丈夫です。

## 最初のアクセス

トークンを環境変数に入れて、Cookieを保存しながらアクセスしてください。

最初に認証された端末は、自動で承認済み端末になります。

```bash
export SETOYAMA_API_TOKEN="ここにトークンを貼り付け"

curl --compressed -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  https://mgc-pass-proxy.duckdns.org/setoyama-api/tables
```

別のPCやブラウザからアクセスした場合、APIは承認コードを返します。すでに承認済みの端末から、そのコードを承認してください。

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/devices/approve \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"approval_code":"123456","label":"瀬戸山さん 作業PC"}'
```

## 主に使うテーブル

通常のフォーム営業用ソーシングに使う推奨テーブル:

```text
partner_company_enrichment
```

どの項目を調査・入力してほしいかの一覧:

```text
enrichment_targets
```

自由なキー・バリュー形式で追加調査情報を入れるテーブル:

```text
enrichment_fields
```

必要であれば、瀬戸山さん側で独自テーブルを作成しても大丈夫です。`/schema` や `/docs` は現在のデータベース構造を見に行くので、テーブル追加後も確認できます。

## まず調査・入力してほしい情報

現在の会社マスターデータで不足しやすく、フォーム営業・AI判定・営業対象の選定に役立つ情報を優先してください。

- `primary_email`: 会社の公開メールアドレス
- `contact_form_url`: 問い合わせフォームURL。フォーム営業では最優先
- `website_url`: 公式Webサイト
- `employee_count` / `employee_count_text`: 従業員数または従業員規模
- `industry_primary`: 業界
- `business_description`: 業務内容
- `phone_number`: 代表電話番号
- `representative_name` / `representative_position`: 代表者名・役職
- `employee_accounts_json`: 公開されている社員・採用・チーム関連アカウント
- `target_relevance`: なぜフォーム営業対象として良さそうか
- `exclusion_reason`: なぜ営業対象から外すべきか
- `confidence`: 情報の確度。`0.0` から `1.0`
- `evidence_url`: 情報の根拠URL

具体例は [docs/ENRICHMENT-GUIDE.md](docs/ENRICHMENT-GUIDE.md) を見てください。

## よく使うコマンド

テーブル一覧を見る:

```bash
curl --compressed -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  https://mgc-pass-proxy.duckdns.org/setoyama-api/tables
```

推奨テーブルの構造を見る:

```bash
curl --compressed -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  https://mgc-pass-proxy.duckdns.org/setoyama-api/schema/partner_company_enrichment
```

フォーム営業用の会社調査データを1件追加する:

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/tables/partner_company_enrichment/rows \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d @examples/company-enrichment.json
```

## 安全範囲

このAPIから、私たちのファイル、本番Postgres、メールボックスのシークレット、送信キュー、Mesh内部情報にはアクセスできません。

SQLiteのサンドボックスにより、`ATTACH`、`DETACH`、`PRAGMA`、拡張機能の読み込み、外部データベースへのアクセスは禁止されています。
