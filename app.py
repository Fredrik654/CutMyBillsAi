import streamlit as st
import os
from groq import Groq
import pandas as pd
import altair as alt

# ── Groq setup ──
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing! Add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

st.title("CutMyBillsAI – Cut Bills, Invest the Savings")

# ── Super Simple 3 Sliders ──
st.markdown("### Quick Setup (3 Sliders Only)")
col1, col2, col3 = st.columns(3)

with col1:
    monthly_bills = st.slider("Monthly Bills Total $", 200, 1000, 500, step=50)

with col2:
    monthly_income = st.slider("Monthly Household Income $", 2000, 10000, 5000, step=100)

with col3:
    motivation = st.slider("Motivation to Save (1-10)", 1, 10, 7)

# ── Free Section: Big Visuals, Minimal Text ──
st.markdown("### Your Potential Savings Sneak Peek")

# Simple AI tip (short & visual)
prompt = f"""
Quick Ontario bill savings tip for 2025. Bills ${monthly_bills}, motivation {motivation}/10.
Give 3-4 ultra-short tips + estimated monthly savings (tease $200+/mo potential).
Very short, bold, exciting. No long reading.
"""
with st.spinner("Finding your savings..."):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    st.markdown("**Quick Wins:**")
    st.markdown(f"**{response.choices[0].message.content}**")

# ── Big Savings Tease Number ──
potential_monthly_save = 200  # Tease number - can make dynamic later
st.markdown(f"**You could save up to ${potential_monthly_save}/month!**")
st.markdown(f"**That's ~${potential_monthly_save * 12}/year**")

# ── Simple Bar Chart (Visual Savings Impact) ──
st.markdown("**Your Monthly Bill Breakdown & Savings**")
data = {
    'Category': ['Electricity', 'Gas', 'Water', 'Internet', 'Potential Savings'],
    'Amount': [monthly_bills * 0.35, monthly_bills * 0.25, monthly_bills * 0.2, monthly_bills * 0.2, potential_monthly_save]
}
df = pd.DataFrame(data)
chart = alt.Chart(df).mark_bar(color='#10B981').encode(
    x='Category',
    y='Amount',
    tooltip=['Category', 'Amount']
).properties(width=600, height=300)
st.altair_chart(chart, use_container_width=True)

# ── Teaser 10-Year Projection Chart ──
st.markdown("**Sneak Peek: What $200/month Saved Could Grow To**")
years = list(range(1, 11))
savings = [potential_monthly_save * 12 * year * (1 + 0.08) ** year for year in years]  # 8% compound
df_growth = pd.DataFrame({'Year': years, 'Potential Value ($)': savings})
teaser_chart = alt.Chart(df_growth).mark_area(color="#10B981").encode(
    x='Year',
    y='Potential Value ($)',
    tooltip=['Year', 'Potential Value ($)']
).properties(width=600, height=300)
st.altair_chart(teaser_chart, use_container_width=True)
st.info("This is a basic tease — unlock the **full personalized plan**, rebates, and detailed 10-year growth for just $4.99 CAD!")

# ── Ultimate Unlock Button ──
st.markdown("---")
st.markdown("**Ready to turn these savings into real wealth?**")
if st.button("Unlock Full Plan & Projections ($4.99 CAD)"):
    # Your Stripe Checkout code here (keep your existing one)
    st.info("Payment flow starts... (Stripe/Apple Pay integration)")
    # Add your full Stripe session creation code from previous messages
