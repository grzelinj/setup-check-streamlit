import streamlit as st
import pandas as pd
from io import BytesIO
import time

def przetworz_dane(df):
    # WYCIAGANIE UNIKALNYCH WARTOSCI 
    df_unique_plan_ids = df['PLAN'].unique()
    df_unique_FMV_Rules_ids = df['FMV RULE ID'].unique()
    df_unique_participation_ids = df['PARTICIPATION ID'].unique()
    df_unique_Underlying_vehicle_ids = df['UNDERLYING VEHICLE'].unique()
    df_unique_Vehicle_ids = df['VEHICLE'].unique()
    df_unique_distribution_rule_ids = df['DISTRIBUTION RULE ID'].unique()

    # FORMATOWANIE WARTOSCI
    formatted_plan_ids = ',\n'.join([f"'{pid}'"for pid in df_unique_plan_ids])
    formatted_FMV_Rules_ids = ',\n'.join([f"'{pid}'"for pid in df_unique_FMV_Rules_ids])
    formatted_participation_ids = ',\n'.join([f"'{pid}'"for pid in df_unique_participation_ids])
    formatted_rollovers_ids = ',\n'.join([f"'R-{pid}'"for pid in df_unique_participation_ids])
    formatted_Underlying_vehicle_ids = ',\n'.join([f"'{pid}'"for pid in df_unique_Underlying_vehicle_ids])
    formatted_Vehicle_ids = ',\n'.join([f"'{pid}'"for pid in df_unique_Vehicle_ids])
    formatted_distribution_rule_ids = ',\n'.join([f"'{pid}'"for pid in df_unique_distribution_rule_ids])

    # TEMPLATY
    Template_1 = f"""
SELECT
PLAN,
PRODUCT_TYPE,
EXCEPTION_NAME,
EXCEPTION_TYPE,
PAYMENT_METHOD_STC AS STC,
PAYMENT_METHOD_SELL AS SELL,
PAYMENT_METHOD_WTC AS WTC,
PAYMENT_METHOD_PAYROLL AS PAYROLL,
PAYMENT_METHOD_CASH AS CASH,
PAYMENT_METHOD_CASHPAYOUT AS CASH_PAYOUT,
DEFAULT_PAYMENT_METHOD
FROM LAPSE_PRODUCT_TYPES, LAPSE_PAYMENT_METHODS
WHERE LAPSE_PRODUCT_TYPES.LAPSE_ID = LAPSE_PAYMENT_METHODS.LAPSE_ID
-- PASTE YOUR PLAN ID(S) BELOW
AND PLAN IN ({formatted_plan_ids})
"""

    Template_2 = f"""
SELECT
FMV_RULE_ID,
TRANSACTION_TYPE,
FMV_EVENT,
PRICE_TYPE,
START_DISPLACEMENT,
END_DISPLACEMENT,
DISPLACEMENT_UNIT
FROM FMV_RULES
-- PASTE YOUR FMV RULE(S) BELOW
WHERE FMV_RULE_ID IN ({formatted_FMV_Rules_ids})
ORDER BY TRANSACTION_TYPE
"""

    Template_3 = f"""
SELECT PARTICIPATION_ID, ROLLOVER_PARTICIPATION_ID
FROM PARTICIPATIONS
WHERE PARTICIPATION_ID IN
-- PASTE YOUR PARTICIPATION ID(S) BELOW
({formatted_participation_ids})
"""

    Template_4 = f"""
SELECT
PARTICIPATION_ID,
VEHICLE,
CONTRIBUTION_TYPE,
DISTRIBUTION_RULE_ID,
FMV_RULE_ID,
TAV_FMV_BASE_DATE_DRIVER,
EVENT_RULE_ID,
FORFEITABLE_PCT,
ASSET_TYPE_IN_OMNIBUS
FROM PARTICIPATION_VEHICLE_DEFAULTS
WHERE PARTICIPATION_ID IN
-- PASTE YOUR PARTICIPATION AND ROLLOVER PARTICIPATION IDS BELOW
({formatted_participation_ids},
{formatted_rollovers_ids})

-- PASTE YOUR NOTIONAL AND UNDERLYING VEHICLES BELOW
AND VEHICLE IN
({formatted_Underlying_vehicle_ids},
{formatted_Vehicle_ids})
ORDER BY DISTRIBUTION_RULE_ID
"""

    Template_5 = f"""
SELECT
PARTICIPATION_ID,
VEHICLE,
ROLLOVER_CONTRIBUTION_TYPE,
CONTRIBUTION_TYPE,
BASE_DATE_SOURCE,
DEFERAL_IMPACT_DAYS,
DEFERAL_IMPACT_MONTHS,
RESTRICTION_IMPACT_DAYS,
RESTRICTION_IMPACT_MONTHS,
VESTING_IMPACT_DAYS,
VESTING_IMPACT_MONTHS
FROM PARTICIPATION_ROLLOVER_SETUP
WHERE PARTICIPATION_ID IN
-- PASTE YOUR ROLLOVER PARTICIPATION ID(S) BELOW
({formatted_rollovers_ids})
"""

    Template_6 = f"""
SELECT
DISTRIBUTION_RULE_ID,
CASH_PROCEEDS_ACCOUNT_TYPE,
SELL_TO_COVER_ALLOWED,
SELL_ALLOWED,
TRANSFER_ALLOWED,
PAYROLL_ALLOWED,
WTC_ALLOWED,
EXERCISE_ALLOWED,
EXERSALE_ALLOWED,
PAY_CASH_ALLOWED,
CASH_PAYOUT_ALLOWED,
FEE_GROUP_ID,
JOURNAL_GROUP_ID,
BATCH_CONFIG_ID,
ROLLOVER_INSTRUCTION,
SUPPRESS_JOURNALS
FROM DISTRIBUTION_RULES
-- PASTE YOUR DISTRIBUTION RULE(S) BELOW
WHERE DISTRIBUTION_RULE_ID IN ({formatted_distribution_rule_ids})
"""

    # LACZENIE W CALOSC
    separator = "\n\n\n"
    Setup_check_all = separator.join([Template_1, Template_2, Template_3, Template_4, Template_5, Template_6]) 

    return Setup_check_all

st.set_page_config(page_title="Setup Check Generator", layout="wide")

st.title("✅ Setup Check Generator")
st.write("""
Wgraj swój plik Excel, a aplikacja automatycznie wyciągnie unikalne wartości
i wygeneruje gotowe zapytania SQL do setup checków.
""")

uploaded_file = st.file_uploader("Wybierz plik Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Dodaj pasek postępu tutaj
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)

    przetworzone_dane = przetworz_dane(df)

    st.text_area("Wynik", przetworzone_dane, height=500)

    def to_text(data):
        return data.encode('utf-8')

    text_data = to_text(przetworzone_dane)

    st.download_button(label='Pobierz wyniki jako plik tekstowy', data=text_data, file_name='Setup_check_all.txt')

st.markdown("<br>", unsafe_allow_html=True)
st.image("logo.png", width=150, caption="", output_format="PNG")
