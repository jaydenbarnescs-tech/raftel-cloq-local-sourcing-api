# Data Structure

The API exposes Setoyama-san's own SQLite database.

## `enrichment_targets`

Checklist of enrichment fields we want.

Important columns:

- `priority`
- `field_name`
- `japanese_label`
- `description`
- `example_value`
- `why_it_matters`
- `suggested_source`

## `partner_company_enrichment`

Recommended editable table for company enrichment.

Important columns:

- `corporate_number`
- `company_name`
- `website_url`
- `primary_email`
- `contact_form_url`
- `phone_number`
- `employee_count`
- `employee_count_text`
- `employee_source_url`
- `industry_primary`
- `industry_tags_json`
- `business_description`
- `representative_name`
- `representative_position`
- `capital`
- `recruiting_status`
- `employee_accounts_json`
- `target_relevance`
- `exclusion_reason`
- `confidence`
- `evidence_url`
- `notes`
- `created_at`
- `updated_at`

## `enrichment_fields`

Flexible key-value table for custom enrichment.

Useful when a field does not fit the recommended table.

Important columns:

- `corporate_number`
- `company_name`
- `field_name`
- `field_value`
- `value_json`
- `confidence`
- `evidence_url`
- `notes`

## Custom Tables

Setoyama-san can create extra tables with:

```bash
curl -X POST https://mgc-pass-proxy.duckdns.org/setoyama-api/sql/execute \
  -b setoyama.cookies -c setoyama.cookies \
  -H "Authorization: Bearer $SETOYAMA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sql":"CREATE TABLE IF NOT EXISTS custom_research (company_name TEXT, memo TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"}'
```

Custom tables remain inside Setoyama-san's SQLite database.

