import sqlite3
from prettytable import PrettyTable

# Database Connection
conn = sqlite3.connect("inventory_management.db")
cursor = conn.cursor()

# Create Tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    product_id INTEGER,
    quantity INTEGER,
    total_price REAL,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
)''')

conn.commit()

# Display Products
def display_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    table = PrettyTable(["ID", "Name", "Price", "Stock"])
    for prod in products:
        table.add_row(prod)
    print(table)

# Add a New Product (Seller)
def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock quantity: "))
    cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    conn.commit()
    print("Product added successfully!")

# Update Product (Seller)
def update_product():
    display_products()
    prod_id = int(input("Enter product ID to update: "))
    new_price = float(input("Enter new price: "))
    new_stock = int(input("Enter new stock quantity: "))
    cursor.execute("UPDATE products SET price = ?, stock = ? WHERE id = ?", (new_price, new_stock, prod_id))
    conn.commit()
    print("Product updated successfully!")

# Delete Product (Seller)
def delete_product():
    display_products()
    prod_id = int(input("Enter product ID to delete: "))
    cursor.execute("DELETE FROM products WHERE id = ?", (prod_id,))
    conn.commit()
    print("Product deleted successfully!")

# Purchase a Product (Customer)
def purchase_product():
    display_products()
    customer_name = input("Enter your name: ")
    prod_id = int(input("Enter product ID to purchase: "))
    quantity = int(input("Enter quantity: "))

    cursor.execute("SELECT name, price, stock FROM products WHERE id = ?", (prod_id,))
    product = cursor.fetchone()

    if product and product[2] >= quantity:
        total_price = product[1] * quantity
        cursor.execute("INSERT INTO purchases (customer_name, product_id, quantity, total_price) VALUES (?, ?, ?, ?)",
                      (customer_name, prod_id, quantity, total_price))
        cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (quantity, prod_id))
        conn.commit()
        print(f"Purchase successful! You bought {quantity} of {product[0]} for ${total_price}.")
    else:
        print("Invalid purchase. Insufficient stock or incorrect product ID.")

# View Purchase History
def view_purchase_history():
    cursor.execute("SELECT * FROM purchases")
    purchases = cursor.fetchall()
    table = PrettyTable(["ID", "Customer", "Product ID", "Quantity", "Total Price", "Date"])
    for purchase in purchases:
        table.add_row(purchase)
    print(table)

# Main Menu
def main():
    while True:
        print("\n1. Add Product (Seller)")
        print("2. Update Product (Seller)")
        print("3. Delete Product (Seller)")
        print("4. View Products")
        print("5. Purchase Product (Customer)")
        print("6. View Purchase History")
        print("7. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            add_product()
        elif choice == "2":
            update_product()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            display_products()
        elif choice == "5":
            purchase_product()
        elif choice == "6":
            view_purchase_history()
        elif choice == "7":
            print("Exiting program.")
            conn.close()
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
