import streamlit as st
import os
from groq import Groq
import stripe.error
import pandas as pd
import altair as alt
import stripe.error  # Required for stripe.error.InvalidRequestError
st.markdown("""
<style>
    .stApp { background-color: #000814 !important; }
    .stButton>button { 
        background-color: #00FFA3 !important; 
        color: #000814 !important; 
        border-radius: 12px !important; 
        padding: 12px 24px !important; 
        box-shadow: 0 0 15px #00FFA3 !important; 
        font-weight: bold !important;
    }
    h1 { color: #00FFA3 !important; text-shadow: 0 0 10px #00FFA3 !important; }
</style>
""", unsafe_allow_html=True)
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
# ── Stripe Paywall - Interrogation Style (Ask → Confirm → Pay) ──
st.markdown("### Unlock Full Strategy")
st.markdown("Get detailed investment plan, rebates steps, and 10-year projections for just **$4.99 CAD** (one-time).")

# Step 1: Interrogation - Confirm they want it
if 'unlock_step' not in st.session_state:
    st.session_state.unlock_step = 'ask'

if st.session_state.unlock_step == 'ask':
    st.markdown("**Ready to see how your savings could grow?**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes – Unlock Now ($4.99 CAD)", type="primary"):
            st.session_state.unlock_step = 'confirm'
            st.rerun()
    with col2:
        if st.button("No thanks, just free tips"):
            st.session_state.unlock_step = 'ask'  # Reset if needed
            st.info("Enjoy the free estimate! Come back anytime.")

# Step 2: Confirmation & Payment
elif st.session_state.unlock_step == 'confirm':
    st.markdown("**Quick confirmation**")
    st.markdown(f"- Monthly bills: **${total_bills}**")
    st.markdown(f"- Goal: **{goal}**")
    st.markdown("One-time payment of **$4.99 CAD** to unlock everything.")
    
    col_confirm, col_back = st.columns(2)
    with col_confirm:
        if st.button("Confirm & Pay with Apple Pay / Card", type="primary"):
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],  # Auto-includes Apple Pay on iOS
                    line_items=[{
                        'price_data': {
                            'currency': 'cad',
                            'product_data': {'name': 'Full Investment Strategy Unlock'},
                            'unit_amount': 499,  # $4.99 CAD in cents
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url = "https://cutmybillsai-4xvx5lmgtsymg5rz6taant.streamlit.app/?payment=success",
                    cancel_url = "https://cutmybillsai-4xvx5lmgtsymg5rz6taant.streamlit.app/?payment=cancel",
                )
                st.markdown(f"""
                    <a href='{session.url}' target='_blank' style='
                        display: inline-block;
                        font-size: 20px;
                        color: white;
                        background: linear-gradient(45deg, #10B981, #059669);
                        padding: 14px 30px;
                        border-radius: 12px;
                        text-decoration: none;
                        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
                        font-weight: bold;
                    '>Proceed to Secure Payment</a>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Payment setup failed: {str(e)}. Try again or contact support.")
    
    with col_back:
        if st.button("Back"):
            st.session_state.unlock_step = 'ask'
            st.rerun()

# ── Premium Content (unlocked after success) ──
if "payment" in st.query_params and st.query_params["payment"] == "success":
    st.session_state.unlock_step = 'unlocked'  # Keep unlocked in session
    st.success("Payment successful! Welcome to the full plan.")
    
    prompt_premium = f"""
    Aggressive Ontario optimizer. User: bills ${total_bills}, household {household}, motivation {energy_level}/10, goal {goal}.
    Give detailed step-by-step plan for cutting bills, applying rebates, and investing savings.
    Include rebates (Home Renovation Savings™ up to 30% on insulation/heat pumps).
    Mix low-risk (GICs/HISAs ~3-4.5%) with higher-risk (tech/AI ETFs QQQ/ARKK ~8-10% returns, renewables TAN).
    5/10-year projections (assume 8-10% average returns, compound monthly).
    Tease long-term boom potential like early tech investors. Disclaimers.
    """
    with st.spinner("Generating your personalized premium plan..."):
        try:
            response_prem = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt_premium}],
                max_tokens=1000
            )
            st.markdown(response_prem.choices[0].message.content)
        except Exception as e:
            st.error(f"Premium plan error: {str(e)}")
