import streamlit as st
from pymongo import MongoClient
import bcrypt

# -------------------------------
# MongoDB Connection
# -------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["shopping_portal"]
users = db["users"]
products = db["products"]
orders = db["orders"]

# -------------------------------
# Authentication Functions
# -------------------------------
def create_user(username, password, role):
    if users.find_one({"username": username}):
        st.warning("User already exists!")
        return
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users.insert_one({"username": username, "password": hashed_pw, "role": role})
    st.success(f"User '{username}' created successfully as {role}!")

def login_user(username, password):
    user = users.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return user
    return None

# -------------------------------
# Admin Page
# -------------------------------
def admin_page():
    st.title("🛒 Admin Dashboard")
    st.subheader("Manage Users and Products")

    # Add user
    st.write("### ➕ Create New User")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])
    if st.button("Create User"):
        create_user(new_user, new_pass, role)

    # Add products
    st.write("### 📦 Add Product")
    product_name = st.text_input("Product Name")
    product_price = st.number_input("Product Price", min_value=0)
    if st.button("Add Product"):
        products.insert_one({"name": product_name, "price": product_price})
        st.success(f"Product '{product_name}' added successfully!")

    # Show products
    st.write("### 🧾 Product List")
    for prod in products.find():
        st.write(f"🛍 {prod['name']} — ₹{prod['price']}")

# -------------------------------
# User Page
# -------------------------------
def user_page(username):
    st.title(f"Welcome, {username} 👋")
    st.subheader("🛍 Available Products")

    all_products = list(products.find())
    if not all_products:
        st.info("No products available yet.")
        return

    for prod in all_products:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{prod['name']}** — ₹{prod['price']}")
        with col2:
            if st.button(f"Buy {prod['name']}", key=prod['_id']):
                orders.insert_one({"username": username, "product": prod['name'], "price": prod['price']})
                st.success(f"You bought {prod['name']}!")

    # Order history
    st.write("### 🧾 Your Orders")
    user_orders = list(orders.find({"username": username}))
    if user_orders:
        for order in user_orders:
            st.write(f"- {order['product']} — ₹{order['price']}")
    else:
        st.info("You have no orders yet.")

# -------------------------------
# Login Page
# -------------------------------
def login_page():
    st.title("🛍 Shopping Portal Login")
    st.write("Please login to continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state["user"] = user
            st.success(f"Welcome {user['username']}!")
        else:
            st.error("Invalid username or password.")

# -------------------------------
# Main App Logic
# -------------------------------
def main():
    st.sidebar.title("Navigation")

    if "user" not in st.session_state:
        page = "login"
    else:
        page = st.sidebar.radio("Go to", ["Home", "Logout"])

    if page == "login":
        login_page()

    elif page == "Home":
        user = st.session_state["user"]
        if user["role"] == "admin":
            admin_page()
        else:
            user_page(user["username"])

    elif page == "Logout":
        st.session_state.pop("user", None)
        st.success("Logged out successfully!")

if _name_ == "_main_":
    main()