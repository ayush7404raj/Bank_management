import streamlit as st
import json
import random
import string
from pathlib import Path

# ---------------- BANK CLASS ---------------- #

class Bank:

    database = "data.json"
    data = []

    if Path(database).exists():
        with open(database, "r") as f:
            data = json.load(f)

    @classmethod
    def save(cls):
        with open(cls.database, "w") as f:
            json.dump(cls.data, f, indent=4)

    @classmethod
    def generate_account(cls):
        letters = random.choices(string.ascii_uppercase, k=3)
        digits = random.choices(string.digits, k=4)
        acc = letters + digits
        random.shuffle(acc)
        return "".join(acc)

    @classmethod
    def find_user(cls, acc, pin):
        for user in cls.data:
            if user["account"] == acc and user["pin"] == pin:
                return user
        return None


# ---------------- STREAMLIT UI ---------------- #

st.set_page_config(
    page_title="Digital Bank",
    page_icon="🏦",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align: center; color: green;'>🏦 Digital Bank Management System</h1>
    <hr>
    """,
    unsafe_allow_html=True
)

menu = st.sidebar.selectbox(
    "🏦 Banking Menu",
    [
        "🏠 Home",
        "🧾 Create Account",
        "💰 Deposit",
        "💸 Withdraw",
        "📊 Account Details",
        "✏ Update Account",
        "🗑 Delete Account"
    ]
)

bank = Bank()

# ---------------- HOME ---------------- #

if menu == "🏠 Home":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🧾 Create Bank Account")

    with col2:
        st.success("💰 Deposit & Withdraw")

    with col3:
        st.warning("📊 Manage Your Account")

    st.markdown(
        """
        ### 🏦 Welcome to Digital Bank
        
        - Secure Banking 🔐  
        - Fast Transactions ⚡  
        - Easy Account Management 📊  
        - Professional Banking System 💼
        """
    )

# ---------------- CREATE ACCOUNT ---------------- #

elif menu == "🧾 Create Account":

    st.subheader("🧾 Open New Bank Account")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("👤 Full Name")
        age = st.number_input("🎂 Age", min_value=1)

    with col2:
        email = st.text_input("📧 Email")
        pin = st.text_input("🔐 4 Digit PIN", type="password")

    if st.button("🏦 Create Account"):

        if age < 18 or len(pin) != 4:
            st.error("❌ Age must be 18+ and PIN must be 4 digits")

        else:
            account = Bank.generate_account()

            new_user = {
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "account": account,
                "balance": 0
            }

            Bank.data.append(new_user)
            Bank.save()

            st.success("✅ Account Created Successfully")
            st.info(f"🏦 Your Account Number: {account}")

# ---------------- DEPOSIT ---------------- #

elif menu == "💰 Deposit":

    st.subheader("💰 Deposit Money")

    acc = st.text_input("🏦 Account Number")
    pin = st.text_input("🔐 PIN", type="password")
    amount = st.number_input("💵 Amount", min_value=1)

    if st.button("💰 Deposit Now"):

        user = Bank.find_user(acc, int(pin))

        if user:
            user["balance"] += amount
            Bank.save()
            st.success("✅ Money Deposited Successfully")
        else:
            st.error("❌ Invalid Account or PIN")

# ---------------- WITHDRAW ---------------- #

elif menu == "💸 Withdraw":

    st.subheader("💸 Withdraw Money")

    acc = st.text_input("🏦 Account Number")
    pin = st.text_input("🔐 PIN", type="password")
    amount = st.number_input("💵 Amount", min_value=1)

    if st.button("💸 Withdraw Now"):

        user = Bank.find_user(acc, int(pin))

        if user:

            if user["balance"] < amount:
                st.error("❌ Insufficient Balance")

            else:
                user["balance"] -= amount
                Bank.save()
                st.success("✅ Money Withdrawn")

        else:
            st.error("❌ Invalid Account")

# ---------------- DETAILS ---------------- #

elif menu == "📊 Account Details":

    st.subheader("📊 Account Information")

    acc = st.text_input("🏦 Account Number")
    pin = st.text_input("🔐 PIN", type="password")

    if st.button("📊 Show Details"):

        user = Bank.find_user(acc, int(pin))

        if user:

            st.success("✅ Account Found")

            st.write("👤 Name:", user["name"])
            st.write("📧 Email:", user["email"])
            st.write("🎂 Age:", user["age"])
            st.write("🏦 Account:", user["account"])
            st.write("💰 Balance:", user["balance"])

        else:
            st.error("❌ Invalid Account")

# ---------------- UPDATE ---------------- #

elif menu == "✏ Update Account":

    st.subheader("✏ Update Account Details")

    acc = st.text_input("🏦 Account Number")
    pin = st.text_input("🔐 PIN", type="password")

    user = Bank.find_user(acc, int(pin)) if acc and pin else None

    if user:

        name = st.text_input("👤 New Name", user["name"])
        email = st.text_input("📧 New Email", user["email"])
        new_pin = st.text_input("🔐 New PIN", user["pin"])

        if st.button("✏ Update Now"):

            user["name"] = name
            user["email"] = email
            user["pin"] = int(new_pin)

            Bank.save()
            st.success("✅ Account Updated")

# ---------------- DELETE ---------------- #

elif menu == "🗑 Delete Account":

    st.subheader("🗑 Delete Account")

    acc = st.text_input("🏦 Account Number")
    pin = st.text_input("🔐 PIN", type="password")

    if st.button("🗑 Delete Now"):

        user = Bank.find_user(acc, int(pin))

        if user:
            Bank.data.remove(user)
            Bank.save()
            st.success("✅ Account Deleted")

        else:
            st.error("❌ Invalid Account")