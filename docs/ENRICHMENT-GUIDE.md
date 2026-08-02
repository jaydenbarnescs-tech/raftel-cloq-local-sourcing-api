# Enrichment Guide

This guide explains what information is most useful and how to record it.

## Best Enrichment Fields

| Priority | Field | Japanese label | What to collect | Good source |
| --- | --- | --- | --- | --- |
| 1 | `primary_email` | メールアドレス | Public company-domain contact/sales/recruiting email. | Official contact/recruiting page |
| 2 | `contact_form_url` | 問い合わせフォームURL | Direct inquiry/contact form URL. | Official website |
| 3 | `website_url` | 公式Webサイト | Canonical official company site. | Official site/search/company profile |
| 4 | `employee_count` / `employee_count_text` | 従業員数 | Count or range, plus source. | Company profile, gBizINFO, recruiting page |
| 5 | `industry_primary` | 業界 | Primary industry/category in Japanese. | Company profile, official services page |
| 6 | `business_description` | 業務内容 | Short factual description of what the company does. | About/services/product pages |
| 7 | `phone_number` | 電話番号 | Main company phone number. | Official site/company profile |
| 8 | `representative_name` | 代表者名 | Public representative name. | Company profile/filings |
| 9 | `employee_accounts_json` | 社員アカウント | Public staff, team, recruiting, Wantedly, LinkedIn, or SNS accounts. | Public profiles only |
| 10 | `target_relevance` | 営業対象としての理由 | Why this company is relevant for form/email outreach. | Human or AI review |
| 11 | `exclusion_reason` | 除外理由 | Why this company should not be contacted. | Human or AI review |

## Quality Rules

Evidence is more important than perfect formatting.

Use `evidence_url` whenever possible. Use `confidence` from `0.0` to `1.0`:

- `0.95`: official company source and exact match
- `0.80`: strong public source but not directly official
- `0.60`: likely match, needs later review
- below `0.60`: put details in `notes` and treat as uncertain

Do not collect private personal email addresses. Public company/team contact addresses are fine.

## Recommended Row Shape

Use `partner_company_enrichment` for normal work.

```json
{
  "corporate_number": "1234567890123",
  "company_name": "サンプル株式会社",
  "website_url": "https://example.jp/",
  "primary_email": "info@example.jp",
  "contact_form_url": "https://example.jp/contact",
  "phone_number": "03-1234-5678",
  "employee_count": 52,
  "employee_source_url": "https://example.jp/company",
  "industry_primary": "製造業",
  "industry_tags_json": "[\"包装資材\", \"B2B\"]",
  "business_description": "食品工場向け包装資材の製造・販売",
  "representative_name": "山田 太郎",
  "representative_position": "代表取締役",
  "employee_accounts_json": "[{\"name\":\"採用ページ\",\"url\":\"https://example.jp/recruit\"}]",
  "target_relevance": "フォーム営業対象。B2B商材で公式問い合わせフォームあり。",
  "exclusion_reason": "",
  "confidence": 0.86,
  "evidence_url": "https://example.jp/company",
  "notes": "公式サイト確認済み"
}
```

## Exclusion Examples

Use `exclusion_reason` when a company should not be contacted.

Examples:

- `競合`
- `行政・自治体`
- `学校・教育機関`
- `採用代理店`
- `営業代行会社`
- `すでに送信済みの可能性`
- `会社閉鎖・事業停止`
- `問い合わせ先が見つからない`

Deletion in Setoyama's database does not delete our master data. If a large count drop happens, the sync sends an alert for review.

