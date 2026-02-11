"""
Generate realistic sample sales data for the Sales Performance Analysis project.
"""

import csv
import random
import os
from datetime import datetime, timedelta

# Configuration
NUM_ROWS = 1500
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)
REGIONS = ["North", "South", "East", "West"]
PRODUCTS = [
    {"id": "P001", "name": "Laptop Pro", "base_price": 1299.99},
    {"id": "P002", "name": "Wireless Mouse", "base_price": 29.99},
    {"id": "P003", "name": "Mechanical Keyboard", "base_price": 89.99},
    {"id": "P004", "name": "USB-C Hub", "base_price": 49.99},
    {"id": "P005", "name": "Monitor 27in", "base_price": 399.99},
    {"id": "P006", "name": "Webcam HD", "base_price": 79.99},
    {"id": "P007", "name": "Headset Pro", "base_price": 149.99},
    {"id": "P008", "name": "SSD 1TB", "base_price": 109.99},
    {"id": "P009", "name": "Tablet 10in", "base_price": 449.99},
    {"id": "P010", "name": "Phone Charger", "base_price": 19.99},
]

random.seed(42)


def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)


def generate_sales_data():
    """Generate sample sales records."""
    rows = []
    order_id = 10000

    for _ in range(NUM_ROWS):
        date = random_date(START_DATE, END_DATE)
        region = random.choice(REGIONS)
        product = random.choice(PRODUCTS)

        # Seasonal multiplier (Q4 holiday boost)
        month = date.month
        seasonal = 1.0
        if month in [11, 12]:
            seasonal = 1.6
        elif month in [1, 2]:
            seasonal = 0.8
        elif month in [6, 7]:
            seasonal = 1.2

        # Regional multiplier
        region_mult = {"North": 1.1, "South": 0.95, "East": 1.0, "West": 1.15}

        visitors = int(random.randint(80, 500) * seasonal * region_mult[region])
        orders = max(1, int(visitors * random.uniform(0.02, 0.12)))
        base_revenue = product["base_price"] * orders
        revenue = round(base_revenue * random.uniform(0.85, 1.15), 2)
        customers = max(1, int(orders * random.uniform(0.7, 1.0)))

        order_id += 1
        rows.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "order_id": f"ORD-{order_id}",
                "product_id": product["id"],
                "product_name": product["name"],
                "region": region,
                "visitors": visitors,
                "customers": customers,
                "orders": orders,
                "revenue": revenue,
            }
        )

    # Sort by date
    rows.sort(key=lambda x: x["date"])
    return rows


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "sales_data.csv")

    rows = generate_sales_data()

    fieldnames = [
        "date",
        "order_id",
        "product_id",
        "product_name",
        "region",
        "visitors",
        "customers",
        "orders",
        "revenue",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} sales records -> {output_path}")


if __name__ == "__main__":
    main()
