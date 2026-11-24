# Duka Sales Exploration and Agent Network Clean-Up

## Project Overview
This repository contains the completed work for **PLP Data Analytics - Assignment 3**, covering two engagements:
1. **Duka Electronics Sales Exploration (`duka_sales_exploration.ipynb`)** - Exploratory data analysis of H1 2026 sales across branches, products, channels, weekdays/weekends, and months, plus filtering for Premium Online orders from Nairobi and Mombasa.
2. **Mobile-Money Agent Transaction Cleanup (`cleaning_pipeline.py` & `agent_cleanup.ipynb`)** - Data quality auditing, deduplication, transaction type standardisation, ISO date parsing, missing-amount flagging and median imputation, IQR outlier flagging, and safe left-join merging against the agent register.

## Repository Structure
- `requirements.txt` - Python dependencies (`pandas`, `numpy`).
- `generate_data.py` - Script that generates the synthetic raw datasets (`duka_sales.csv`, `agents.csv`, `agent_transactions.csv`).
- `duka_sales_exploration.ipynb` - Engagement 1 exploration and summary analysis notebook.
- `cleaning_pipeline.py` - Reusable `clean_agent_data(txns, agents)` function returning `(clean_df, log)`.
- `agent_cleanup.ipynb` - Engagement 2 cleaning, join comparison, and validation notebook.
- `.gitignore` - Excludes cache files, checkpoints, and raw generated CSVs.

## How to Run
1. Install the packages listed in `requirements.txt`.
2. Run `generate_data.py` to generate the raw CSV files locally (these are excluded from Git via `.gitignore`).
3. Run `duka_sales_exploration.ipynb` and `agent_cleanup.ipynb` to execute the analysis and generate the cleaned output files.
