#Load your dataset
import pandas as pd

df = pd.read_csv("indian_banking_transactions.csv")

print("Dataset loaded successfully!")
print("Rows and columns:", df.shape)

#overall Banking Transaction KPIs
total_transactions = len(df)

total_success = (df["transaction_status"] == "Success").sum()
total_failed = (df["transaction_status"] == "Failed").sum()
total_fraud_flagged = df["is_fraud"].sum()

success_rate = round(total_success / total_transactions * 100, 2)
failure_rate = round(total_failed / total_transactions * 100, 2)
fraud_flag_rate = round(total_fraud_flagged / total_transactions * 100, 2)

print("\n--- BANKING TRANSACTION KPIs ---")
print("Total Transactions:", total_transactions)
print("Successful Transactions:", total_success)
print("Failed Transactions:", total_failed)
print("Fraud-Flagged Transactions:", total_fraud_flagged)
print("Success Rate:", success_rate, "%")
print("Failure Rate:", failure_rate, "%")
print("Fraud-Flag Rate:", fraud_flag_rate, "%")

#Transaction status analysis
status_analysis = (
    df["transaction_status"]
    .value_counts()
    .reset_index()
)

status_analysis.columns = [
    "Transaction Status",
    "Transaction Count"
]

status_analysis["Percentage"] = (
    status_analysis["Transaction Count"]
    / len(df) * 100
).round(2)

print("\n--- TRANSACTION STATUS ANALYSIS ---")
print(status_analysis.to_string(index=False))

#Save this analysis to CSV
status_analysis.to_csv(
    "transaction_status_analysis.csv",
    index=False
)

print("Transaction status analysis exported successfully!")

#Transaction type analysis
type_analysis = (
    df.groupby("transaction_type")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_amount=("transaction_amount", "sum"),
        average_amount=("transaction_amount", "mean")
    )
    .round(2)
    .sort_values("transaction_count", ascending=False)
)

print("\n--- TRANSACTION TYPE ANALYSIS ---")
print(type_analysis.to_string())

#Save the analysis to CSV
type_analysis.to_csv(
    "transaction_type_analysis.csv",
    index=True
)

print("Transaction type analysis exported successfully!")

state_analysis = (
    df.groupby("state")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_amount=("transaction_amount", "sum"),
        average_amount=("transaction_amount", "mean")
    )
    .round(2)
    .sort_values("transaction_count", ascending=False)
)

print("\n--- STATE-WISE TRANSACTION ANALYSIS ---")
print(state_analysis.head(10).to_string())

#Export the state analysis
state_analysis.to_csv(
    "state_transaction_analysis.csv",
    index=True
)

print("State analysis exported successfully!")


fraud_analysis = (
    df.groupby("is_fraud")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_amount=("transaction_amount", "sum"),
        average_amount=("transaction_amount", "mean")
    )
    .round(2)
)

fraud_analysis.index = [
    "Not Flagged" if value == 0 else "Fraud Flagged"
    for value in fraud_analysis.index
]

print("\n--- FRAUD ANALYSIS ---")
print(fraud_analysis.to_string())


fraud_analysis.to_csv("fraud_analysis_summary.csv", index=True)

print("Fraud analysis exported successfully!")


#Python analysis summary create pannuvom
print("\n--- BUSINESS INSIGHTS ---")

print("1. Total transactions:", len(df))

print(
    "2. Successful transactions:",
    (df["transaction_status"] == "Success").sum()
)

print(
    "3. Fraud-flagged transactions:",
    df["is_fraud"].sum()
)

print(
    "4. Highest transaction count type:",
    df["transaction_type"].value_counts().idxmax()
)

print(
    "5. Highest transaction count state:",
    df["state"].value_counts().idxmax()
)


#indha 5 findings-ai oru separate CSV report-la save pannuvom
business_insights = pd.DataFrame({
    "Insight": [
        "Total Transactions",
        "Successful Transactions",
        "Fraud-Flagged Transactions",
        "Top Transaction Type",
        "Top State by Transaction Count"
    ],
    "Value": [
        len(df),
        (df["transaction_status"] == "Success").sum(),
        df["is_fraud"].sum(),
        df["transaction_type"].value_counts().idxmax(),
        df["state"].value_counts().idxmax()
    ]
})

business_insights.to_csv("business_insights.csv", index=False)

print("Business insights exported successfully!")