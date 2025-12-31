from st_paywall import add_auth

# ... (your free estimate code here) ...

# Paywall - Apple Pay priority
add_auth(
    required=True,
    price=499,  # $4.99 (in cents)
    name="Full Investment Strategy Unlock",
    stripe_api_key=os.environ.get("STRIPE_API_KEY"),  # From secrets
    checkout_button_text="Unlock with Apple Pay / Card ($4.99)",
    payment_methods=["apple_pay", "card", "google_pay"]  # Prioritizes Apple Pay on iOS
)

# This section only shows after successful payment
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
