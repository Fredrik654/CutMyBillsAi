import streamlit as st
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.title("CutMyBillsAI – Cut Bills, Invest the Savings")

total_bills = st.number_input("Monthly total bills $", min_value=100, max_value=1000, value=350)
household = st.text_input("Household details (e.g., house, winter high heat)")
energy_level = st.slider("Motivation level (1-10)", 1, 10, 7)
goal = st.text_input("Savings goal (e.g., emergency fund)")

if st.button("Get Free Savings Estimate"):
    prompt = f"""
    You are a practical Ontario bill optimizer for 2025.
    User: bills ${total_bills}, household {household}, motivation {energy_level}/10, goal {goal}.
    Estimate current breakdown using Ontario averages (electricity $100-140, gas $80-150 winter, water $90, internet $60-100).
    Give 5-8 quick tips to cut bills + estimated $ savings (tease $2200/year potential).
    Short, encouraging, honest. No investments yet.
    """
    with st.spinner("Calculating..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Free-tier friendly Grok model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        st.write("### Free Savings Preview")
        st.write(response.choices[0].message.content)
        st.info("Unlock full investment strategy, rebates, and 10-year projections for $4.99!")

# Paywall tease - we'll add full paywall next
from st_paywall import add_auth

# After free estimate...
add_auth(
    required=True,
    price=499,  # $4.99
    name="Full Investment Unlock",
    stripe_api_key="sk_test_your-secret-key-here",  # Paste your test secret key
    payment_methods=["apple_pay", "card", "google_pay"]  # Apple Pay first
)

# Premium content (only after pay)
st.success("Unlocked! Here's the full strategy.")
prompt_premium = f"""
Aggressive Ontario optimizer. User: bills ${total_bills}, household {household}, motivation {energy_level}/10, goal {goal}.
Add rebates, investments (GICs + tech ETFs), 5/10-year projections at 8-10% returns, boom tease.
"""
response_prem = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt_premium}]
)
st.write(response_prem.choices[0].message.content)
