#!/usr/bin/env python3
"""List companies that have a form URL and are not excluded."""

from api_client import post


sql = """
SELECT company_name, website_url, contact_form_url, industry_primary, target_relevance
FROM partner_company_enrichment
WHERE contact_form_url IS NOT NULL
  AND contact_form_url != ''
  AND (exclusion_reason IS NULL OR exclusion_reason = '')
ORDER BY updated_at DESC
LIMIT 20
"""

data = post("/sql/query", {"sql": sql})
for row in data.get("rows", []):
    print(f"{row['company_name']} | {row.get('industry_primary') or ''} | {row['contact_form_url']}")

