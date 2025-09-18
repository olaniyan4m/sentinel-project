Sentinel Project Package
========================

This package contains:
- openapi.yaml : OpenAPI v3 spec for evidence ingest and basic APIs
- data_model.json : JSON describing core entities and fields
- rbac.json : RBAC policy templates
- roadmap.csv : Phase-based roadmap (weeks)
- ml_brief.md : ML & Edge model brief
- pitch_onepager.md : Investor / partner one-pager
- sample_data/ : Synthetic sample CSVs (evidence, plates)
- download_real_data.sh : Script to download publicly available datasets referenced below
- sources.json : List of referenced web sources (with notes)

Important: This environment cannot fetch all external files automatically. The download script will attempt to retrieve public PDFs. If any URL changes, please visit the source page to get the latest link.

Authoritative sources and starter links (please review and download for your instance):
- SAPS Crime Statistics page and quarterly PDFs: https://www.saps.gov.za/services/crimestats.php
- SAPS Q4 2024/2025 crime stats PDF (example): https://www.saps.gov.za/services/downloads/2024/2024-2025_Q4_crime_stats.pdf
- SAPS Annual crime report 2023/24: https://www.saps.gov.za/services/downloads/annual_crime_report/SAPS_2023_24_Annual%20Crime%20Report_JG25.pdf
- PSIRA Annual Report 2023/24: https://www.psira.co.za/dmdocuments/PSiRA%20-%20Annual%20Report%202023-24.pdf
- News & analysis: Reuters, AP, ProtectionWeb, Africanews (search queries used in research)
- Note: For each URL above, verify freshness and integrity before ingestion.