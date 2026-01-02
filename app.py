import streamlit as st
import os
from groq import Groq
import stripe
import pandas as pd
import altair as alt

# ── Groq setup ──
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing! Add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ── Stripe setup ──
stripe.api_key = os.environ.get("STRIPE_API_KEY")

if not stripe.api_key:
    st.warning("Stripe key not set — paywall will not work. Add STRIPE_API_KEY in secrets.")

# ── Theme & Style (dark + green pop) ──
st.markdown("""
<style>
    .stApp { background-color: #000814 !important; color: #E0F2FE !important; }
    .stButton>button { 
        background: linear-gradient(45deg, #10B981, #059669) !important; 
        color: white !important; 
        border-radius: 12px !important; 
        padding: 12px 24px !important; 
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4) !important; 
        font-weight: bold !important;
        border: none !important;
    }
    h1 { color: #00FFA3 !important; text-shadow: 0 0 10px #00FFA3 !important; }
    .stSlider { color: #00FFA3 !important; }
</style>
""", unsafe_allow_html=True)

st.title("CutMyBillsAI – Cut Bills, Invest the Savings")

# ── Disclaimer ──
st.markdown("""
**Important Disclaimer**  
This tool provides general estimates and ideas only. It is **not financial, legal, or professional advice**.  
Savings amounts are approximate. Investments carry risk. Consult a professional.
""")

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
# ── Paywall with direct Stripe Checkout ──
st.markdown("---")
st.markdown("**Ready to turn these savings into real wealth?**")
if st.button("Unlock Full Strategy ($4.99 CAD)"):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],  # Auto-adds Apple Pay on iOS
            line_items=[{
                'price_data': {
                    'currency': 'cad',
                    'product_data': {'name': 'Full Investment Strategy Unlock'},
                    'unit_amount': 499,  # $4.99 CAD
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url = "https://cutmybillsai-4xvx5lmgtsymg5rz6taant.streamlit.app/?success=true",
            cancel_url = "https://cutmybillsai-4xvx5lmgtsymg5rz6taant.streamlit.app/?cancel=true",
        )
        st.markdown(f"<a href='{session.url}' target='_blank' style='font-size:20px; color:#000; background:#00FFA3; padding:14px 30px; border-radius:12px; text-decoration:none; box-shadow: 0 0 15px #00FFA3; display:inline-block; font-weight:bold;'>Proceed to Secure Payment</a>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Payment setup error: {str(e)}")

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
chart = alt.Chart(df).mark_bar(color='#00FFA3').encode(
    x='Category',
    y='Amount',
    tooltip=['Category', 'Amount']
).properties(width=600, height=300)
st.altair_chart(chart, use_container_width=True)

# ── Teaser 10-Year Projection Chart ──
st.markdown("**Sneak Peek: What $200/month Saved Could Grow To**")
years = list(range(1, 11))
monthly_save = 200
savings = [monthly_save * 12 * year * (1 + 0.08) ** year for year in years]  # 8% compound
df_growth = pd.DataFrame({'Year': years, 'Potential Value ($)': savings})
teaser_chart = alt.Chart(df_growth).mark_area(color="#00FFA3").encode(
    x='Year',
    y='Potential Value ($)',
    tooltip=['Year', 'Potential Value ($)']
).properties(width=600, height=300)
st.altair_chart(teaser_chart, use_container_width=True)
st.info("This is a basic tease — unlock the **full personalized plan**, rebates, and detailed 10-year growth for just $4.99 CAD!")
# ── Paywall with direct Stripe Checkout ──
st.markdown("---")
st.markdown("**Ready to turn these savings into real wealth?**")
if st.button("Unlock Full Strategy ($4.99 CAD)", key="unlock_button"):  # Add unique key to avoid duplicate ID
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],  # Auto-adds Apple Pay on iOS
            line_items=[{
                'price_data': {
                    'currency': 'cad',
                    'product_data': {'name': 'Full Investment Strategy Unlock'},
                    'unit_amount': 499,  # $4.99 CAD
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url = "https://cutmybillsai-4xvx5lmgtsymg5rz6taant.streamlit.app/?success=true",
            cancel_url = "https://cutmybillsai-4xvx5lmgtsymg5rz6taant.streamlit.app/?cancel=true",
        )
        st.markdown(f"<a href='{session.url}' target='_blank' style='font-size:20px; color:#000; background:#00FFA3; padding:14px 30px; border-radius:12px; text-decoration:none; box-shadow: 0 0 15px #00FFA3; display:inline-block; font-weight:bold;'>Proceed to Secure Payment</a>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Payment setup error: {str(e)}")
# ── Premium content ──
if "success" in st.query_params:
    st.success("Payment successful! Here's your full strategy to turn savings into reality.")
    prompt_premium = f"""
    Aggressive Ontario optimizer. User: bills ${monthly_bills}, household {household}, motivation {motivation}/10, goal {goal}.
    Give detailed step-by-step plan for cutting bills, applying rebates, and investing savings.
    Include rebates (Home Renovation Savings™ up to 30% on insulation/heat pumps).
    Mix low-risk (GICs/HISAs ~3-4.5%) with higher-risk (tech/AI ETFs QQQ/ARKK ~8-10% returns, renewables TAN).
    5/10-year projections (assume 8-10% average returns, compound monthly).
    Tease long-term boom potential like early tech investors. Disclaimers.
    """
    with st.spinner("Generating full plan..."):
        response_prem = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt_premium}],
            max_tokens=1000
        )
        st.markdown(response_prem.choices[0].message.content)

    # ── Full Projection Chart ──
    st.markdown("### Your Personalized 10-Year Savings Growth")
    years = list(range(1, 11))
    monthly_save = 2200 / 12
    savings = [monthly_save * 12 * year * (1 + 0.08) ** year for year in years]  # Compound at 8%
    df = pd.DataFrame({'Year': years, 'Projected Savings ($)': savings})
    chart = alt.Chart(df).mark_area(color="#00FFA3").encode(
        x='Year',
        y='Projected Savings ($)',
        tooltip=['Year', 'Projected Savings ($)']
    ).properties(width=600, height=300)
    st.altair_chart(chart, use_container_width=True)

    # ── Continue Button ──
    if st.button("Continue with In-Depth Plan"):
        st.write("Generating detailed next steps...")
        continue_prompt = f"""
        Provide step-by-step in-depth plan for {goal}, including:
        - How to apply for Ontario rebates.
        - Investment setup (e.g., open TFSA for GICs).
        - Monthly check-in tips.
        - Investment setup for {monthly_bills} savings.
        """
        with st.spinner("Generating..."):
            response_continue = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": continue_prompt}],
                max_tokens=600
            )
            st.markdown(response_continue.choices[0].message.content)
