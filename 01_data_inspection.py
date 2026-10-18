#Python-la CSV read
import pandas as pd

df = pd.read_csv("indian_banking_transactions.csv")

print(df.head())

#Dataset size check
print("Dataset Shape:", df.shape)
print("Column Names:", df.columns.tolist())

#Data quality check
print(df.isnull().sum())

#Business logic validation
print(df["has_loan"].value_counts(dropna=False))

print(pd.crosstab(df["has_loan"], df["loan_type"].isnull()))

#Check duplicate transactions
print("Duplicate transaction IDs:", df["transaction_id"].duplicated().sum())

#Check transaction status distribution
print(df["transaction_status"].value_counts())

#Calculate transaction percentages
status_counts = df["transaction_status"].value_counts()

status_percentage = (
    df["transaction_status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(status_percentage)

#check datatypes before sql business analysis
print(df.dtypes)

#Convert transaction date to datetime
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

print("Invalid dates:", df["transaction_date"].isna().sum())
print(df["transaction_date"].head())

#Indha dataset endha period-ai cover pannudhu?

print("First transaction date:", df["transaction_date"].min())
print("Last transaction date:", df["transaction_date"].max())

#Endha month-la transaction volume adhigama irukku?

monthly_transactions = (
    df.groupby(df["transaction_date"].dt.to_period("M"))
      .size()
      .sort_values(ascending=False)
)

print(monthly_transactions.head(10))

#Endha month-la total transaction value highest-ah irukku?

monthly_amount = (
    df.groupby(df["transaction_date"].dt.to_period("M"))["transaction_amount"]
      .sum()
      .sort_values(ascending=False)
)

print(monthly_amount.head(10))

#Successful transactions mattum eduthaa, monthly total value evlo?

successful_df = df[df["transaction_status"] == "Success"]

monthly_success_amount = (
    successful_df.groupby(
        successful_df["transaction_date"].dt.to_period("M")
    )["transaction_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(monthly_success_amount.head(10))

#Endha month-la transaction success rate highest?

monthly_success_rate = (
    df.assign(is_success=df["transaction_status"].eq("Success"))
      .groupby(df["transaction_date"].dt.to_period("M"))["is_success"]
      .mean()
      .mul(100)
      .round(2)
      .sort_values(ascending=False)
)

print(monthly_success_rate.head(10))

#Which transaction type has the highest transaction volume?

print(df["transaction_type"].value_counts())

#Find each transaction type's share
transaction_share = (
    df["transaction_type"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(transaction_share)

#endha transaction type-la total money movement highest
transaction_amount_by_type = (
    df.groupby("transaction_type")["transaction_amount"]
    .sum()
    .sort_values(ascending=False)
)

print(transaction_amount_by_type)

#Calculate average transaction amount by type
avg_amount_by_type = (
    df.groupby("transaction_type")["transaction_amount"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print(avg_amount_by_type)

#Check fraud distribution
print(df["is_fraud"].value_counts())

#Calculate Fraud Rate
fraud_rate = df["is_fraud"].mean() * 100

print(f"Fraud Rate: {fraud_rate:.2f}%")

#Fraud amount analysis
fraud_df = df[df["is_fraud"] == 1]

print("Fraud transactions:", len(fraud_df))
print(
    "Total flagged transaction amount:",
    round(fraud_df["transaction_amount"].sum(), 2)
)
print(
    "Average flagged transaction amount:",
    round(fraud_df["transaction_amount"].mean(), 2)
)

#Fraud by transaction status
fraud_status = pd.crosstab(
    df["transaction_status"],
    df["is_fraud"]
)

print(fraud_status)

#Calculate fraud rate by transaction type
fraud_rate_by_type = (
    df.groupby("transaction_type")["is_fraud"]
    .mean()
    .mul(100)
    .round(2)
    .sort_values(ascending=False)
)

print(fraud_rate_by_type)

#Check fraud counts by transaction type
fraud_count_by_type = (
    df[df["is_fraud"] == 1]["transaction_type"]
    .value_counts()
)

print(fraud_count_by_type)

#Analyse fraud by transaction channel
fraud_by_channel = (
    df.groupby("channel")["is_fraud"]
    .agg(["sum", "count", "mean"])
)

fraud_by_channel["fraud_rate_pct"] = (
    fraud_by_channel["mean"] * 100
).round(2)

print(fraud_by_channel.sort_values("fraud_rate_pct", ascending=False))

#Find missing KYC records
print(df["kyc_status"].value_counts(dropna=False))

#Fraud rate by KYC status
fraud_by_kyc = (
    df.groupby("kyc_status")["is_fraud"]
    .agg(["sum", "count", "mean"])
)

fraud_by_kyc["fraud_rate_pct"] = (
    fraud_by_kyc["mean"] * 100
).round(2)

print(fraud_by_kyc)

#Analyse fraud by loan status
fraud_by_loan = (
    df.groupby("has_loan")["is_fraud"]
    .agg(["sum", "count", "mean"])
)

fraud_by_loan["fraud_rate_pct"] = (
    fraud_by_loan["mean"] * 100
).round(2)

print(fraud_by_loan)

#Check transaction direction
fraud_by_direction = (
    df.groupby("transaction_direction")["is_fraud"]
    .agg(["sum", "count", "mean"])
)

fraud_by_direction["fraud_rate_pct"] = (
    fraud_by_direction["mean"] * 100
).round(2)

print(fraud_by_direction)

#Analyse fraud by transaction amount
print(
    df.groupby("is_fraud")["transaction_amount"]
    .agg(["count", "mean", "median"])
    .round(2)
)

#Check transaction amount percentiles
print(
    df.groupby("is_fraud")["transaction_amount"]
    .quantile([0.50, 0.75, 0.90, 0.95, 0.99])
    .unstack()
    .round(2)
)

#Validate transaction amount data
print("Zero amounts:", (df["transaction_amount"] == 0).sum())
print("Negative amounts:", (df["transaction_amount"] < 0).sum())
print("Missing amounts:", df["transaction_amount"].isna().sum())

#Check transaction status vs fraud flags
fraud_rate_by_status = (
    df.groupby("transaction_status")["is_fraud"]
    .mean()
    .mul(100)
    .round(2)
    .sort_values(ascending=False)
)

print(fraud_rate_by_status)

#Check customer-level transaction activity
customer_transaction_count = df.groupby("customer_id").size()

print("Unique customers:", df["customer_id"].nunique())
print("Average transactions per customer:", round(customer_transaction_count.mean(), 2))
print("Maximum transactions by one customer:", customer_transaction_count.max())

#Find the most active customers
top_customers = (
    df.groupby("customer_id")
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print(top_customers)

#Calculate total transaction amount by customer
top_customers_by_amount = (
    df.groupby("customer_id")["transaction_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_customers_by_amount.round(2))

#Find each customer's transaction count and total amount together
customer_summary = (
    df.groupby("customer_id")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_amount=("transaction_amount", "sum"),
        average_amount=("transaction_amount", "mean")
    )
    .sort_values("total_amount", ascending=False)
    .head(10)
)

print(customer_summary.round(2))

#Analyse transaction amounts by account type
account_type_summary = (
    df.groupby("account_type")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_amount=("transaction_amount", "sum"),
        average_amount=("transaction_amount", "mean")
    )
    .sort_values("total_amount", ascending=False)
)

print(account_type_summary.round(2))

#Fraud rate by account type
fraud_by_account = (
    df.groupby("account_type")["is_fraud"]
    .agg(["sum", "count", "mean"])
)

fraud_by_account["fraud_rate_pct"] = (
    fraud_by_account["mean"] * 100
).round(2)

print(fraud_by_account.sort_values("fraud_rate_pct", ascending=False))

#Analyse transaction amount by state
state_summary = (
    df.groupby("state")
    .agg(
        transaction_count=("transaction_id", "count"),
        total_amount=("transaction_amount", "sum"),
        average_amount=("transaction_amount", "mean")
    )
    .sort_values("total_amount", ascending=False)
)

print(state_summary.head(10).round(2))

#Fraud rate by state
fraud_by_state = (
    df.groupby("state")["is_fraud"]
    .agg(["sum", "count", "mean"])
)

fraud_by_state["fraud_rate_pct"] = (
    fraud_by_state["mean"] * 100
).round(2)

print(
    fraud_by_state
    .sort_values("fraud_rate_pct", ascending=False)
    .head(10)
)

#transaction amounts differ across states
amount_by_state = (
    df.groupby("state")["transaction_amount"]
    .agg(["count", "mean", "sum"])
    .round(2)
)

print(
    amount_by_state
    .sort_values("mean", ascending=False)
    .head(10)
)

#fraud rate and average transaction amount together
state_analysis = (
    df.groupby("state")
    .agg(
        total_transactions=("transaction_id", "count"),
        fraud_count=("is_fraud", "sum"),
        avg_transaction_amount=("transaction_amount", "mean")
    )
)

state_analysis["fraud_rate_pct"] = (
    state_analysis["fraud_count"]
    / state_analysis["total_transactions"] * 100
).round(2)

state_analysis["avg_transaction_amount"] = (
    state_analysis["avg_transaction_amount"].round(2)
)

print(
    state_analysis
    .sort_values("fraud_rate_pct", ascending=False)
    .head(10)
)

print(
    state_analysis
    .sort_values("fraud_rate_pct", ascending=False)
    .head(10)
    .to_string()
)

#analyze transaction success rate
success_by_state = (
    df.assign(
        is_success=df["transaction_status"].eq("Success")
    )
    .groupby("state")["is_success"]
    .agg(["sum", "count", "mean"])
)

success_by_state["success_rate_pct"] = (
    success_by_state["mean"] * 100
).round(2)

print(
    success_by_state
    .sort_values("success_rate_pct", ascending=False)
    .head(10)
    .to_string()
)

#find failed transaction rate by state
failed_by_state = (
    df.assign(
        is_failed=df["transaction_status"].eq("Failed")
    )
    .groupby("state")["is_failed"]
    .agg(["sum", "count", "mean"])
)

failed_by_state["failed_rate_pct"] = (
    failed_by_state["mean"] * 100
).round(2)

print(
    failed_by_state
    .sort_values("failed_rate_pct", ascending=False)
    .head(10)
    .to_string()
)

#failure rate by channel
failed_by_channel = (
    df.assign(
        is_failed=df["transaction_status"].eq("Failed")
    )
    .groupby("channel")["is_failed"]
    .agg(["sum", "count", "mean"])
)

failed_by_channel["failed_rate_pct"] = (
    failed_by_channel["mean"] * 100
).round(2)

print(
    failed_by_channel
    .sort_values("failed_rate_pct", ascending=False)
    .to_string()
)

#channel-wise transaction status
channel_status = pd.crosstab(
    df["channel"],
    df["transaction_status"],
    normalize="index"
).mul(100).round(2)

print(channel_status.to_string())

#analyze transaction type by status
type_status = pd.crosstab(
    df["transaction_type"],
    df["transaction_status"],
    normalize="index"
).mul(100).round(2)

print(
    type_status
    .sort_values("Failed", ascending=False)
    .to_string()
)

#compare transaction amount by status
amount_by_status = (
    df.groupby("transaction_status")["transaction_amount"]
    .agg(["count", "mean", "median", "sum"])
    .round(2)
)

print(amount_by_status.to_string())

#compare transaction amount by status
amount_by_status = (
    df.groupby("transaction_status")["transaction_amount"]
    .agg(["count", "mean", "median", "sum"])
    .round(2)
)

print(amount_by_status.to_string())

#check high-value transaction failures
df["amount_band"] = pd.cut(
    df["transaction_amount"],
    bins=[0, 1000, 5000, 20000, 100000, float("inf")],
    labels=[
        "0-1000",
        "1000-5000",
        "5000-20000",
        "20000-100000",
        "100000+"
    ],
    include_lowest=True
)

failure_by_amount = (
    df.assign(
        is_failed=df["transaction_status"].eq("Failed")
    )
    .groupby("amount_band", observed=False)["is_failed"]
    .agg(["sum", "count", "mean"])
)

failure_by_amount["failure_rate_pct"] = (
    failure_by_amount["mean"] * 100
).round(2)

print(failure_by_amount.to_string())

#prepare a KPI summary
total_transactions = len(df)

total_failed = (
    df["transaction_status"] == "Failed"
).sum()

total_success = (
    df["transaction_status"] == "Success"
).sum()

total_fraud_flagged = df["is_fraud"].sum()

print("Total Transactions:", total_transactions)
print("Successful Transactions:", total_success)
print("Failed Transactions:", total_failed)
print("Fraud-Flagged Transactions:", total_fraud_flagged)

print(
    "Success Rate (%):",
    round(total_success / total_transactions * 100, 2)
)

print(
    "Failure Rate (%):",
    round(total_failed / total_transactions * 100, 2)
)

print(
    "Fraud-Flag Rate (%):",
    round(total_fraud_flagged / total_transactions * 100, 2)
)
#KPI summary
kpi_summary = pd.DataFrame({
    "Metric": [
        "Total Transactions",
        "Successful Transactions",
        "Failed Transactions",
        "Fraud-Flagged Transactions",
        "Success Rate (%)",
        "Failure Rate (%)",
        "Fraud-Flag Rate (%)"
    ],
    "Value": [
        total_transactions,
        total_success,
        total_failed,
        total_fraud_flagged,
        round(total_success / total_transactions * 100, 2),
        round(total_failed / total_transactions * 100, 2),
        round(total_fraud_flagged / total_transactions * 100, 2)
    ]
})

print(kpi_summary.to_string(index=False))

#Format the KPI output
kpi_summary["Value"] = kpi_summary.apply(
    lambda row: (
        f"{int(row['Value']):,}"
        if "(%)" not in row["Metric"]
        else f"{row['Value']:.2f}%"
    ),
    axis=1
)

print(kpi_summary.to_string(index=False))

#Export KPI summary to CSV
kpi_summary.to_csv("banking_kpi_summary.csv", index=False)
