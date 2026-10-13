
import pandas as pd
import matplotlib.pyplot as plt

raw = {
    "Product": [
        "Cola", "Chips", "Milk", "Biscuits", "Juice",
        "Yogurt", "Water", "Cookies", "Cheese", "Soda"
    ],
    "Category": [
        "beverages ", "SNACKS", " Dairy", "Snacks",
        "BEVERAGES", "dairy ", " Beverages",
        "SNACKS ", "DAIRY", " beverages"
    ],
    "Price": [
        "Rs. 1,250", "Rs. 90", "Rs. 450", "Rs. 120",
        "Rs. 1,800", "Rs. 300", "Rs. 80",
        "Rs. 150", "Rs. 650", "Rs. 950"
    ],
    "Stock": [40, 120, 60, 100, 35, 50, 200, 80, 30, 45]
}

df = pd.DataFrame(raw)

print("Original Dataset:")
print(df)

df["Category"] = df["Category"].str.strip().str.title()

df["Price"] = (
    df["Price"]
    .str.replace("Rs. ", "", regex=False)
    .str.replace(",", "", regex=False)
)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

df["Category_Code"] = df["Category"].astype("category").cat.codes

print("\nCleaned Inventory Dataset:")
print(df)

print("\nCategory Encoding:")
print(
    df[["Category", "Category_Code"]]
    .drop_duplicates()
    .sort_values("Category_Code")
    .to_string(index=False)
)

avg_price = df.groupby("Category")["Price"].mean().sort_values(
    ascending=False
)

stock_by_category = df.groupby("Category")["Stock"].sum()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].bar(avg_price.index, avg_price.values)
axes[0].set_title("Average Price by Category")
axes[0].set_xlabel("Category")
axes[0].set_ylabel("Average Price (Rs.)")
axes[0].tick_params(axis="x", rotation=20)

axes[1].pie(
    stock_by_category.values,
    labels=stock_by_category.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[1].set_title("Share of Total Stock")

fig.suptitle("Product Inventory Analysis")
plt.tight_layout()

plt.savefig("inventory_plots.png", dpi=150)
print("\nSaved inventory_plots.png")

plt.show()
