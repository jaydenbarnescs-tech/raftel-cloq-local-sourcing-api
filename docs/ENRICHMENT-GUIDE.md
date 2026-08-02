# フォーム営業ソーシングガイド

このページでは、Raftel / CLOQ の国内ソーシングで、瀬戸山さんにどの情報を優先して調査・入力してほしいかを説明します。

目的はフォーム営業です。メール営業用のメールソーシング、送信管理、送信履歴管理はJayden側で行います。

## 優先して調査・入力してほしい項目

| 優先度 | フィールド名 | 日本語ラベル | 入れてほしい内容 | 良い情報源 |
| --- | --- | --- | --- | --- |
| 1 | `contact_form_url` | 問い合わせフォームURL | 問い合わせフォームに直接アクセスできるURL。フォーム営業では最重要。 | 公式サイト |
| 2 | `website_url` | 公式Webサイト | 会社の公式サイトURL。ポータルサイトや一覧ページではなく公式サイト。 | 公式サイト、検索結果、会社プロフィール |
| 3 | `primary_email` | メールアドレス | 会社ドメインの公開メールアドレス。問い合わせ・営業・採用窓口など。メール営業側でも参考にする。 | 公式サイトの問い合わせ・会社概要・採用ページ |
| 4 | `employee_count` / `employee_count_text` | 従業員数 | 従業員数、または「10〜50名」のような規模感。 | 会社概要、gBizINFO、採用ページ |
| 5 | `industry_primary` | 業界 | 主な業界・カテゴリ。日本語で入力。 | 会社概要、事業内容、サービスページ |
| 6 | `business_description` | 業務内容 | その会社が何をしている会社かの短い説明。 | 会社概要、事業内容、商品・サービスページ |
| 7 | `phone_number` | 電話番号 | 代表電話番号。 | 公式サイト、会社概要 |
| 8 | `representative_name` | 代表者名 | 公開されている代表者名。 | 会社概要、登記・公開情報 |
| 9 | `employee_accounts_json` | 社員アカウント | 公開されている社員、チーム、採用、Wantedly、LinkedIn、SNSなど。 | 公開プロフィールのみ |
| 10 | `target_relevance` | フォーム営業対象としての理由 | なぜフォーム営業対象として良さそうか。 | 人の判断、AI判定、根拠URL |
| 11 | `exclusion_reason` | 除外理由 | なぜ営業対象から外すべきか。 | 人の判断、AI判定、根拠URL |

## 品質ルール

完璧な形式よりも、根拠があることを優先してください。

可能な限り `evidence_url` に根拠URLを入れてください。

`confidence` は `0.0` から `1.0` で入力してください。

- `0.95`: 公式情報で、会社名・内容が明確に一致している
- `0.80`: かなり信頼できる公開情報だが、公式情報ではない
- `0.60`: おそらく正しいが、後で確認したい
- `0.60` 未満: `notes` に不確実な理由を書いてください

非公開の個人メールアドレスは収集しないでください。会社として公開されている代表メール、問い合わせメール、採用メールなどは問題ありません。

## 推奨する入力形式

通常は `partner_company_enrichment` に入力してください。テーブル名には `enrichment` が入っていますが、ここでの用途はフォーム営業用の国内ソーシング情報の入力です。

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

## 除外理由の例

フォーム営業対象から外すべき場合は、`exclusion_reason` に理由を入れてください。

例:

- `競合`
- `行政・自治体`
- `学校・教育機関`
- `採用代理店`
- `営業代行会社`
- `すでに送信済みの可能性`
- `会社閉鎖・事業停止`
- `問い合わせ先が見つからない`

瀬戸山さん側のデータベースで行を削除しても、私たちの会社マスターデータは削除されません。件数が大きく減った場合は、同期側で確認用アラートを出します。
