import streamlit as st
import os
from groq import Groq
import stripe

# ── Initialize Groq client (runs once per rerun) ──
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing! Add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ── Stripe setup ──
stripe.api_key = os.environ.get("STRIPE_API_KEY")

if not stripe.api_key:
    st.warning("Stripe key not set — paywall will not work. Add STRIPE_API_KEY in secrets.")

st.title("CutMyBillsAI – Cut Bills, Invest the Savings")

total_bills = st.number_input("Monthly total bills $", min_value=100, max_value=10000, value=350)
household = st.text_input("Household details (e.g., mortgage, hydro/Water, winter heat, Summer A/C)")
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
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Reliable free-tier model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            st.markdown("### Free Savings Preview")
            st.markdown(response.choices[0].message.content)
            st.info("Unlock full investment strategy, rebates, and 10-year projections for $4.99 CAD!")
        except Exception as e:
            st.error(f"AI error: {str(e)}. Try again or check API key/credits.")

# ── Paywall with direct Stripe Checkout (supports Apple Pay 1-tap on iOS) ──
if st.button("Unlock Full Strategy ($4.99 CAD)"):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],  # Stripe auto-adds Apple Pay on iOS
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
        st.markdown(f"<a href='{session.url}' target='_blank' style='font-size:20px; color:#4CAF50;'>Pay with Apple Pay / Card ($4.99 CAD)</a>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Payment setup error: {str(e)}")

# ── Premium content (only shows after successful payment via query param) ──
if "success" in st.query_params:
    st.success("Payment successful! Here's your full strategy.")
    prompt_premium = f"""
    Aggressive Ontario optimizer. User: bills ${total_bills}, household {household}, motivation {energy_level}/10, goal {goal}.
    Add rebates (Home Renovation Savings™ up to 30% on insulation/heat pumps).
    Mix low-risk (GICs/HISAs ~3-4.5%) with higher-risk (tech/AI ETFs QQQ/ARKK ~8-10% returns, renewables TAN).
    5/10-year projections (assume 8-10% average returns, compound monthly).
    Tease long-term boom potential like early tech investors. Disclaimers.
    """
    with st.spinner("Generating premium plan..."):
        try:
            response_prem = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt_premium}],
                max_tokens=800
            )
            st.markdown(response_prem.choices[0].message.content)
        except Exception as e:
            st.error(f"Premium AI error: {str(e)}")
