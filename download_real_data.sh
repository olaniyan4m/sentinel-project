#!/bin/bash
# Script to download public data referenced in README.
mkdir -p real_data
# Examples (replace with working URLs if needed)
echo "Downloading SAPS Q4 crime stats..."
curl -L -o real_data/saps_q4_2024.pdf 'https://www.saps.gov.za/services/downloads/2024/2024-2025_Q4_crime_stats.pdf'
echo "Downloading PSIRA annual report..."
curl -L -o real_data/psira_2023_24.pdf 'https://www.psira.co.za/dmdocuments/PSiRA%20-%20Annual%20Report%202023-24.pdf'
echo "Attempt other downloads as needed..."