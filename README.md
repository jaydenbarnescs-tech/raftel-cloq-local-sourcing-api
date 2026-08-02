# Setoyama Partner Enrichment API

This repository is the public onboarding guide for Setoyama-san's enrichment workspace.

API base URL:

```text
https://mgc-pass-proxy.duckdns.org/setoyama-api
```

Live docs:

```text
https://mgc-pass-proxy.duckdns.org/setoyama-api/docs
```

OpenAPI:

```text
https://mgc-pass-proxy.duckdns.org/setoyama-api/openapi.json
```

The bearer token is shared separately. Do not commit it to GitHub.

## What This Is

Setoyama-san gets his own editable database. He can add tables, edit rows, and add enrichment data freely through the API.

His data is synced into our production system as sidecar enrichment evidence. It does not overwrite our canonical company master data. That means he can work flexibly without risking our production database.

## First Access

Use the token with a cookie jar. The first authenticated device is automatically approved.

```bash
export SETOYAMA_API_TOKEN="paste-token-here"

curl --compressed -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  https://mgc-pass-proxy.duckdns.org/setoyama-api/tables
```

If another device tries to connect, the API returns an approval code. Approve it from an already approved device:

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/devices/approve \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"approval_code":"123456","label":"Setoyama assistant laptop"}'
```

## Main Tables

Recommended daily work table:

```text
partner_company_enrichment
```

Checklist of fields we want enriched:

```text
enrichment_targets
```

Flexible key-value enrichment table:

```text
enrichment_fields
```

He may create custom tables if needed. The API docs/schema endpoints update from the live database structure.

## What To Enrich First

Prioritize fields that are missing or weak in the current master data:

- `primary_email`: public company email address
- `contact_form_url`: direct inquiry form URL
- `website_url`: official company website
- `employee_count` / `employee_count_text`: employee count or range
- `industry_primary`: 業界
- `business_description`: 業務内容
- `phone_number`: main phone number
- `representative_name` / `representative_position`: public representative info
- `employee_accounts_json`: public employee/team/recruiting/social accounts
- `target_relevance`: why this is a good outreach target
- `exclusion_reason`: why this company should not be contacted
- `confidence`: confidence score from 0.0 to 1.0
- `evidence_url`: source URL proving the enrichment

See [docs/ENRICHMENT-GUIDE.md](docs/ENRICHMENT-GUIDE.md) for examples.

## Useful Commands

List tables:

```bash
curl --compressed -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  https://mgc-pass-proxy.duckdns.org/setoyama-api/tables
```

Inspect the recommended table schema:

```bash
curl --compressed -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  https://mgc-pass-proxy.duckdns.org/setoyama-api/schema/partner_company_enrichment
```

Insert one enriched company:

```bash
curl --compressed -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/tables/partner_company_enrichment/rows \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d @examples/company-enrichment.json
```

## Safety Boundary

This API cannot read Jayden's files, production Postgres, mailbox secrets, sender queues, or mesh internals.

The SQLite sandbox denies `ATTACH`, `DETACH`, `PRAGMA`, extension loading, and access to non-main/temp databases.

