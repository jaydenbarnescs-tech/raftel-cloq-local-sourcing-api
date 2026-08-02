# API Reference

Base URL:

```text
https://mgc-pass-proxy.duckdns.org/setoyama-api
```

Auth header:

```text
Authorization: Bearer <token>
```

## Endpoints

- `GET /docs`
- `GET /openapi.json`
- `GET /health`
- `GET /tables`
- `GET /schema`
- `GET /schema/{table}`
- `GET /tables/{table}/rows?limit=100&offset=0`
- `POST /tables/{table}/rows`
- `GET /tables/{table}/rows/{rowid}`
- `PATCH /tables/{table}/rows/{rowid}`
- `DELETE /tables/{table}/rows/{rowid}`
- `POST /sql/query`
- `POST /sql/execute`
- `GET /devices`
- `POST /devices/approve`
- `POST /devices/revoke`

## Query Example

```bash
curl -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/sql/query \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT company_name, website_url, industry_primary FROM partner_company_enrichment LIMIT 20"}'
```

## Update Example

```bash
curl -X PATCH https://mgc-pass-proxy.duckdns.org/setoyama-api/tables/partner_company_enrichment/rows/1 \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"row":{"industry_primary":"製造業","confidence":0.9}}'
```

## Device Approval

The first authenticated browser/device is approved automatically.

New devices receive:

```json
{
  "ok": false,
  "error": "device_pending_approval",
  "device_id": "dev_...",
  "approval_code": "123456"
}
```

Approve from an already-approved device:

```bash
curl -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/devices/approve \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"approval_code":"123456","label":"assistant laptop"}'
```

