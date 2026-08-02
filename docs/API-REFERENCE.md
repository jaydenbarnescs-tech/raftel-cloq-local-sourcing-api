# Raftel / CLOQ 国内ソーシングAPIリファレンス

フォーム営業用の会社調査データを入力・確認するためのAPIです。

瀬戸山さんはフォーム営業に必要な会社情報を入力します。メール営業用のメールソーシング、送信管理、送信履歴管理はJayden側で扱います。

ベースURL:

```text
https://mgc-pass-proxy.duckdns.org/setoyama-api
```

認証ヘッダー:

```text
Authorization: Bearer <token>
```

## エンドポイント

- `GET /openapi.json`: OpenAPI定義
- `GET /health`: APIの状態確認
- `GET /tables`: テーブル一覧
- `GET /schema`: スキーマ概要
- `GET /schema/{table}`: 指定テーブルのスキーマ
- `GET /tables/{table}/rows?limit=100&offset=0`: 指定テーブルの行一覧
- `POST /tables/{table}/rows`: 行を追加
- `GET /tables/{table}/rows/{rowid}`: 指定行を取得
- `PATCH /tables/{table}/rows/{rowid}`: 指定行を更新
- `DELETE /tables/{table}/rows/{rowid}`: 指定行を削除
- `POST /sql/query`: SELECT / WITH クエリを実行
- `POST /sql/execute`: SQLを実行
- `GET /devices`: 承認済み・承認待ち端末一覧
- `POST /devices/approve`: 新しい端末を承認
- `POST /devices/revoke`: 端末承認を取り消し

## クエリ例

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/sql/query \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT company_name, website_url, industry_primary FROM partner_company_enrichment LIMIT 20"}'
```

## 更新例

```bash
curl --compressed -X PATCH https://mgc-pass-proxy.duckdns.org/setoyama-api/tables/partner_company_enrichment/rows/1 \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"row":{"industry_primary":"製造業","confidence":0.9}}'
```

## 端末承認

最初に認証されたブラウザ・端末は自動で承認されます。

別の端末からアクセスすると、次のようなレスポンスが返ります。

```json
{
  "ok": false,
  "error": "device_pending_approval",
  "device_id": "dev_...",
  "approval_code": "123456"
}
```

すでに承認済みの端末から、承認コードを使って新しい端末を承認してください。

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/devices/approve \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"approval_code":"123456","label":"瀬戸山さん 作業PC"}'
```
