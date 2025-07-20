import streamlit as st
from decimal import Decimal

# Static July 2025 exchange rates snapshot (USD base)
EXCHANGE_RATES = {
    "usd": Decimal("1.00"),
    "eur": Decimal("0.91"),
    "gbp": Decimal("0.78"),
    "cny": Decimal("7.25"),
    "jpy": Decimal("155.35"),
    "twd": Decimal("32.5"),
    "aud": Decimal("1.48"),
    "sgd": Decimal("1.35"),
    "thb": Decimal("36.2"),
    "myr": Decimal("4.69"),
}

# Currency emojis or flag alternatives
CURRENCY_FLAGS = {
    "usd": "💵",   # 🇺🇸 not supported reliably on some platforms
    "eur": "💶",
    "gbp": "💷",
    "cny": "💴",
    "jpy": "💴",
    "twd": "💵",
    "aud": "💵",
    "sgd": "💵",
    "thb": "💵",
    "myr": "💵",
}

# Optional full currency names
CURRENCY_NAMES = {
    "usd": "US Dollar",
    "eur": "Euro",
    "gbp": "British Pound",
    "cny": "Chinese Yuan",
    "jpy": "Japanese Yen",
    "twd": "New Taiwan Dollar",
    "aud": "Australian Dollar",
    "sgd": "Singapore Dollar",
    "thb": "Thai Baht",
    "myr": "Malaysian Ringgit",
}

# Converts between currencies using USD as base
def convert(amount: float, base: str, target: str) -> float:
    base = base.lower()
    target = target.lower()
    if base not in EXCHANGE_RATES or target not in EXCHANGE_RATES:
        raise ValueError("Unsupported currency code.")
    usd_amount = Decimal(str(amount)) / EXCHANGE_RATES[base]
    return float(usd_amount * EXCHANGE_RATES[target])

# --- Streamlit App ---
st.set_page_config(page_title="Currency Converter", layout="wide")
st.title("💱 Currency Converter")

# Currency options
currency_options = list(EXCHANGE_RATES.keys())

amount = st.number_input("Enter amount", min_value=0.0, value=1.0, step=1.0)
base = st.selectbox("From currency", currency_options, index=currency_options.index("myr"))
target = st.selectbox("To currency (optional)", ["(Show all currencies)"] + currency_options, index=0)

st.divider()

# Conversion display
if target != "(Show all currencies)":
    try:
        result = convert(amount, base, target)
        emoji = CURRENCY_FLAGS.get(target.lower(), "")
        full_name = CURRENCY_NAMES.get(target.lower(), "")
        st.subheader(f"{emoji} {target.upper()} — {full_name}")
        st.markdown(f"### 💰 {result:.2f} {target.upper()}")
    except Exception as e:
        st.error(f"Conversion failed: {e}")
else:
    st.subheader("🌍 Conversion Results:")
    cols = st.columns(3)
    for i, cur in enumerate(EXCHANGE_RATES):
        if cur.lower() == base.lower():
            continue
        try:
            result = convert(amount, base, cur)
            emoji = CURRENCY_FLAGS.get(cur.lower(), "")
            full_name = CURRENCY_NAMES.get(cur.lower(), "")
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div style="padding:1rem;border-radius:10px;">
                            <h4 style="margin-bottom:0;">{emoji} {cur.upper()} — {full_name}</h4>
                            <p style="font-size:20px;margin-top:0;"><strong>{result:.2f} {cur.upper()}</strong></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        except Exception as e:
            with cols[i % 3]:
                st.error(f"{cur.upper()}: Error")

st.divider()
st.caption("📅 Rates are based on a static snapshot as of July 2025")