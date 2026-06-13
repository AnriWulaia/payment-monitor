import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "http://localhost:8000"

st.title("💳 Payment Monitor Dashboard")

# --- Load data ---
payments = requests.get(f"{API}/payments").json()
stats = requests.get(f"{API}/payments/stats").json()
suspicious = requests.get(f"{API}/payments/suspicious").json()

df = pd.DataFrame(payments)
df_suspicious = pd.DataFrame(suspicious)

# --- Stats row ---
st.subheader("📊 Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Volume", f"${stats['total_volume']:,.2f}")
col2.metric("Average Amount", f"${stats['average_amount']:,.2f}")
col3.metric("Success Rate", f"{stats['success_rate']:.1f}%")

# --- All transactions table ---
st.subheader("📋 All Transactions")
st.dataframe(df, use_container_width=True)

# --- Charts ---
st.subheader("📈 Volume by Merchant")
fig1 = px.bar(df.groupby("merchant")["amount"].sum().reset_index(),
              x="merchant", y="amount", color="merchant")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🟢 Status Breakdown")
fig2 = px.pie(df, names="status", title="Success vs Failed")
st.plotly_chart(fig2, use_container_width=True)

# --- Suspicious transactions ---
st.subheader("🚨 Suspicious Transactions (over $10,000)")
if df_suspicious.empty:
    st.success("No suspicious transactions found")
else:
    st.dataframe(df_suspicious.style.highlight_max(subset=["amount"], color="red"),
                 use_container_width=True)