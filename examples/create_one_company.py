#!/usr/bin/env python3
"""Create one realistic form-sales sourcing row."""

from api_client import post


row = {
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
    "notes": "公式サイト確認済み",
}

data = post("/tables/partner_company_enrichment/rows", {"row": row})
print(data)

