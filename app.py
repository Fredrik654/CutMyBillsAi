import streamlit as st
import os
from groq import Groq
import stripe
import pandas as pd
import altair as alt

# ── Initialize Groq client ──
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing! Add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ── Stripe setup ──
stripe.api_key = os.environ.get("STRIPE_API_KEY")

if not stripe.api_key:
    st.warning("Stripe key not set — paywall will not work. Add STRIPE_API_KEY in secrets.")

# ── Disclaimer ──
st.markdown("""
**Important Disclaimer**  
This tool provides general estimates and ideas only. It is **not financial, legal, or professional advice**.  
Savings amounts are approximate and depend on your actual usage, location, and provider.  
Investments carry risk of loss — past performance does not guarantee future results.  
Always consult a licensed financial advisor or professional before making decisions.  
Use at your own risk.
""")

st.title("CutMyBillsAI – Cut Bills, Invest the Savings")

# ── Sliders for Bill Categories ──
st.markdown("### Adjust Your Bills (Slide to Edit)")
col1, col2 = st.columns(2)

with col1:
    electricity = st.slider("Electricity ($100–140 avg)", 50, 200, 120)
    gas = st.slider("Gas/Heating ($80–150 winter avg)", 50, 200, 100)

with col2:
    water = st.slider("Water ($90 avg)", 50, 150, 90)
    internet = st.slider("Internet ($60–100 avg)", 50, 150, 80)

total_bills = electricity + gas + water + internet
st.markdown(f"**Estimated Monthly Total: ${total_bills}**")

household = st.text_input("Household details (e.g., house, winter high heat)")
energy_level = st.slider("Motivation level (1-10)", 1, 10, 7)
goal = st.text_input("Savings goal (e.g., emergency fund, invest)")

if st.button("Get Free Savings Estimate"):
    prompt = f"""
    You are a practical Ontario bill optimizer for 2025.
    User: electricity ${electricity}, gas ${gas}, water ${water}, internet ${internet}, total ${total_bills}, 
    household {household}, motivation {energy_level}/10, goal {goal}.
    Estimate current breakdown using Ontario averages.
    Give 5-8 quick tips to cut bills + estimated $ savings (tease $2200/year potential).
    Short, encouraging, honest. No investments yet.
    """
    with st.spinner("Calculating savings..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            st.markdown("### Free Savings Preview")
            st.markdown(response.choices[0].message.content)
            st.info("Unlock full investment strategy, rebates, and 10-year projections for $4.99 CAD!")
        except Exception as e:
            st.error(f"AI error: {str(e)}. Try again or check API key/credits.")

    # ── Sneak Peek Teaser Chart ──
    st.markdown("### Sneak Peek: Potential Savings Growth Over 10 Years")
    years = list(range(1, 11))
    monthly_save = 2200 / 12
    savings = [monthly_save * 12 * year for year in years]  # Basic linear tease
    df = pd.DataFrame({'Year': years, 'Projected Savings ($)': savings})
    chart = alt.Chart(df).mark_line(color="#10B981").encode(
        x='Year',
        y='Projected Savings ($)',
        tooltip=['Year', 'Projected Savings ($)']
    ).properties(width=600, height=300)
    st.altair_chart(chart, use_container_width=True)
    st.info("This is a basic tease — unlock the full personalized compound plan!")

# ── Paywall with direct Stripe Checkout ──
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
        st.markdown(f"<a href='{session.url}' target='_blank' style='font-size:20px; color:#fff; background:#10B981; padding:12px 24px; border-radius:8px; text-decoration:none; display:inline-block;'>Pay with Apple Pay / Card ($4.99 CAD)</a>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Payment setup error: {str(e)}")

# ── Premium content ──
if "success" in st.query_params:
    st.success("Payment successful! Here's your full strategy to turn savings into reality.")
    prompt_premium = f"""
    Aggressive Ontario optimizer. User: electricity ${electricity}, gas ${gas}, water ${water}, internet ${internet}, total ${total_bills}, household {household}, motivation {energy_level}/10, goal {goal}.
    Give detailed step-by-step plan for cutting bills, applying rebates, and investing savings.
    Include rebates (Home Renovation Savings™ up to 30% on insulation/heat pumps).
    Mix low-risk (GICs/HISAs ~3-4.5%) with higher-risk (tech/AI ETFs QQQ/ARKK ~8-10% returns, renewables TAN).
    5/10-year projections (assume 8-10% average returns, compound monthly).
    Tease long-term boom potential like early tech investors. Disclaimers.
    """
    with st.spinner("Generating full plan..."):
        try:
            response_prem = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt_premium}],
                max_tokens=1000
            )
            st.markdown(response_prem.choices[0].message.content)
        except Exception as e:
            st.error(f"Premium AI error: {str(e)}")

    # ── Full Projection Chart ──
    st.markdown("### Your Personalized 10-Year Savings Growth")
    years = list(range(1, 11))
    monthly_save = 2200 / 12
    savings = [monthly_save * 12 * year * (1 + 0.08) ** year for year in years]  # Compound at 8%
    df = pd.DataFrame({'Year': years, 'Projected Savings ($)': savings})
    chart = alt.Chart(df).mark_area(color="#10B981").encode(
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
        - Investment setup for {total_bills} savings.
        """
        with st.spinner("Generating..."):
            response_continue = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": continue_prompt}],
                max_tokens=600
            )
            st.markdown(response_continue.choices[0].message.content)
