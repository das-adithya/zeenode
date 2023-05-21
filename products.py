# Catalog with product details
catalog = {
    "Product A": 20,
    "Product B": 40,
    "Product C": 50
}

# Discount rules
discount_rules = {
    "flat_10_discount": {"threshold": 200, "discount_amount": 10},
    "bulk_5_discount": {"threshold": 10, "discount_percentage": 5},
    "bulk_10_discount": {"threshold": 20, "discount_percentage": 10},
    "tiered_50_discount": {"total_threshold": 30, "single_product_threshold": 15, "discount_percentage": 50}
}

# Fees
gift_wrap_fee = 1
shipping_fee_per_package = 5
units_per_package = 10

# Function to calculate the discount amount based on the discount rule applied
def calculate_discount(rule, quantity, price):
    discount_amount = 0

    if rule == "flat_10_discount":
        if quantity * price > discount_rules[rule]["threshold"]:
            discount_amount = discount_rules[rule]["discount_amount"]

    elif rule == "bulk_5_discount":
        if quantity > discount_rules[rule]["threshold"]:
            discount_amount = (quantity * price) * (discount_rules[rule]["discount_percentage"] / 100)

    elif rule == "bulk_10_discount":
        total_quantity = sum(product_quantities.values())
        if total_quantity > discount_rules[rule]["threshold"]:
            discount_amount = (sum(product_quantities.values()) * price) * (discount_rules[rule]["discount_percentage"] / 100)

    elif rule == "tiered_50_discount":
        total_quantity = sum(product_quantities.values())
        max_single_product_quantity = max(product_quantities.values())
        if total_quantity > discount_rules[rule]["total_threshold"] and max_single_product_quantity > discount_rules[rule]["single_product_threshold"]:
            discount_amount = (max_single_product_quantity - discount_rules[rule]["single_product_threshold"]) * price * (discount_rules[rule]["discount_percentage"] / 100)

    return discount_amount

# Function to calculate the shipping fee based on the number of packages needed
def calculate_shipping_fee(total_quantity):
    num_packages = total_quantity // units_per_package
    if total_quantity % units_per_package != 0:
        num_packages += 1
    return num_packages * shipping_fee_per_package

# Function to calculate the total cost
def calculate_total_cost(product_quantities):
    subtotal = 0
    discount_applied = None
    discount_amount = 0
    shipping_fee = 0
    gift_wrap_total = 0

    for product, quantity in product_quantities.items():
        price = catalog[product]
        subtotal += quantity * price

        for rule in discount_rules.keys():
            current_discount = calculate_discount(rule, quantity, price)
            if current_discount > discount_amount:
                discount_applied = rule
                discount_amount = current_discount

        if quantity > 0:
            gift_wrap_total += quantity * gift_wrap_fee

    total_quantity = sum(product_quantities.values())
    shipping_fee = calculate_shipping_fee(total_quantity)

    total = subtotal - discount_amount + shipping_fee + gift_wrap_total

    return subtotal, discount_applied, discount_amount, shipping_fee, gift_wrap_total, total

# Main program
product_quantities = {}

for product in catalog.keys():
    quantity = int(input(f"Enter the quantity of {product}: "))
    product_quantities[product] = quantity

    gift_wrap = input(f"Is {product} wrapped as a gift? (yes/no): ")
    if gift_wrap.lower() == "yes":
        gift_wrap_total = gift_wrap_fee * quantity
        product_quantities[product] -= quantity  # Subtracting the gift-wrapped items from the quantity

subtotal, discount_applied, discount_amount, shipping_fee, gift_wrap_total, total = calculate_total_cost(product_quantities)

print("Product Details:")
for product, quantity in product_quantities.items():
    print(f"{product} - Quantity: {quantity} - Total Amount: ${catalog[product] * quantity}")

print(f"\nSubtotal: ${subtotal}")
if discount_applied:
    print(f"Discount Applied ({discount_applied}): ${discount_amount}")
else:
    print("No applicable discounts")

print(f"Shipping Fee: ${shipping_fee}")
print(f"Gift Wrap Fee: ${gift_wrap_total}")
print(f"Total: ${total}")
