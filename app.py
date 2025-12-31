import streamlit as st
import os
from groq import Groq
from st_paywall import add_auth
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
            model="llama-3.1-8b-instant",  # Fast, reliable, always available
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        st.write("### Free Savings Preview")
        st.write(response.choices[0].message.content)
        st.info("Unlock full investment strategy, rebates, and 10-year projections for $4.99!")
from st_paywall import add_auth
add_auth(
    required=True,
    price=499,  # $4.99
    name="Full Investment Strategy Unlock",
    stripe_api_key=os.environ.get("STRIPE_API_KEY"),
   

# Premium content after payment
st.success("Payment successful! Here's your full strategy.")
prompt_premium = f"""
Aggressive Ontario optimizer. User: bills ${total_bills}, household {household}, motivation {energy_level}/10, goal {goal}.
Add rebates (Home Renovation Savings™ up to 30% on insulation/heat pumps).
Mix low-risk (GICs/HISAs ~3-4.5%) with higher-risk (tech/AI ETFs QQQ/ARKK ~8-10% returns, renewables TAN).
5/10-year projections (assume 8-10% average returns, compound monthly).
Tease long-term boom potential like early tech investors. Disclaimers.
"""
with st.spinner("Generating premium plan..."):
    response_prem = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt_premium}],
        max_tokens=800
    )
    st.write(response_prem.choices[0].message.content)
