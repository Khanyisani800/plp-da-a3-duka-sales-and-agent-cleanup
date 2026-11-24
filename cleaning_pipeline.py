import numpy as np
import pandas as pd


def clean_agent_data(txns, agents):
    """Clean mobile-money agent transactions and merge with the agent register.

    Parameters
    ----------
    txns : pd.DataFrame
        Raw transactions DataFrame.
    agents : pd.DataFrame
        Agent register DataFrame.

    Returns
    -------
    tuple[pd.DataFrame, list[str]]
        A tuple of (clean_df, log) where clean_df is the cleaned, merged
        transactions DataFrame and log is a list of human-readable cleaning notes.
    """
    log = []

    # 1. Remove exact duplicate transaction rows
    before_dups = len(txns)
    df = txns.drop_duplicates().copy()
    removed_dups = before_dups - len(df)
    log.append(f"Removed {removed_dups} duplicate transaction rows")

    # 2. Standardise txn_type into 'Deposit' and 'Withdrawal'
    cleaned_type = (
        df["txn_type"]
        .astype("string")
        .str.strip()
        .str.lower()
        .map({"deposit": "Deposit", "withdrawal": "Withdrawal"})
    )
    invalid_types = int(cleaned_type.isna().sum())
    df["txn_type"] = cleaned_type.fillna("Unknown")
    log.append(
        f"Standardised txn_type to 'Deposit'/'Withdrawal' ({invalid_types} unmapped/missing rows set to 'Unknown')"
    )

    # 3. Convert txn_date to ISO format (YYYY-MM-DD)
    parsed_dates = pd.to_datetime(
        df["txn_date"].astype("string").str.strip().str.replace("/", "-", regex=False),
        errors="coerce",
    )
    bad_dates = int(parsed_dates.isna().sum())
    df["txn_date"] = parsed_dates.dt.strftime("%Y-%m-%d")
    log.append(
        f"Parsed txn_date to ISO format YYYY-MM-DD ({bad_dates} unparseable dates)"
    )

    # 4. Convert amount to numeric, flag missing/invalid before imputing with median
    numeric_amount = pd.to_numeric(
        df["amount"].astype("string").str.strip().str.replace(",", "", regex=False),
        errors="coerce",
    )
    df["amount_imputed"] = numeric_amount.isna()
    imputed_count = int(df["amount_imputed"].sum())
    median_amount = float(numeric_amount.median())
    df["amount"] = numeric_amount.fillna(median_amount)
    log.append(
        f"Flagged and imputed {imputed_count} missing/invalid amount values with median ({median_amount:.0f})"
    )

    # 5. Flag outliers using the 1.5 * IQR rule
    q1 = df["amount"].quantile(0.25)
    q3 = df["amount"].quantile(0.75)
    iqr = q3 - q1
    upper_fence = q3 + 1.5 * iqr
    lower_fence = q1 - 1.5 * iqr
    df["is_outlier"] = (df["amount"] < lower_fence) | (df["amount"] > upper_fence)
    outlier_count = int(df["is_outlier"].sum())
    log.append(
        f"Flagged {outlier_count} amount outliers using IQR fences [{lower_fence:.1f}, {upper_fence:.1f}]"
    )

    # 6. Left-join transactions to the agent register and keep county
    agents_clean = agents.drop_duplicates(subset=["agent_id"]).copy()
    merged = df.merge(
        agents_clean[["agent_id", "county"]],
        on="agent_id",
        how="left",
        validate="many_to_one",
    )
    unknown_agents = int(merged["county"].isna().sum())
    merged["county"] = merged["county"].fillna("Unknown")
    log.append(
        f"Merged with agent register ({unknown_agents} transactions with unknown agent_id labeled 'Unknown')"
    )

    return merged, log
