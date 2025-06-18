import streamlit as st
import os
from databricks import sql
from databricks.sdk.core import Config

cfg = Config()

conn = sql.connect(
    server_hostname=cfg.host,
    http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
    credentials_provider=lambda: cfg.authenticate,
)

st.set_page_config(page_title="Request Impact Estimator", layout="centered")
st.title("📊 Request Impact Estimator")
st.markdown("Estimate cost savings or value enablement for business requests.")

# Select impact type
impact_type = st.radio("What type of impact will this request have?", ["Cost Savings", "Value Enablement", "Both"])

# Basic input fields
request_title = st.text_input("Request Title")
request_description = st.text_area("Brief Description of the Request")
stakeholder_name = st.text_input("Stakeholder Name")

st.markdown("---")

# Cost Savings Section
if impact_type in ["Cost Savings", "Both"]:
    st.subheader("💰 Cost Savings Calculation")
    num_people = st.number_input("How many people perform the task?", min_value=1)
    hours_saved_per_person = st.number_input("Hours saved per person per week", min_value=0.0, step=0.25)
    hourly_rate = st.number_input("Estimated hourly rate ($)", min_value=0.0, step=1.0)
    weeks_saved = st.number_input("How many weeks per year is this saving applicable?", min_value=1, max_value=52)

    total_cost_savings = num_people * hours_saved_per_person * hourly_rate * weeks_saved
    st.success(f"**Estimated Annual Cost Savings: ${total_cost_savings:,.2f}**")

# Value Enablement Section
if impact_type in ["Value Enablement", "Both"]:
    st.subheader("📈 Value Enablement Estimation")
    kpi_type = st.selectbox("Which KPI is impacted?", ["Customer Satisfaction", "Time to Insight", "Employee Productivity", "Revenue Impact", "Other"])
    baseline = st.number_input("Baseline KPI value (before change)", min_value=0.0)
    expected = st.number_input("Expected KPI value (after change)", min_value=0.0)
    improvement = expected - baseline

    if improvement > 0:
        st.success(f"**Expected improvement in {kpi_type}: {improvement:.2f} units**")
    elif improvement < 0:
        st.warning(f"**KPI value decreases by {-improvement:.2f} units**")
    else:
        st.info("**No improvement detected in KPI value**")

# Summary Output
if st.button("Generate Summary"):
    st.markdown("---")
    st.header("📄 Request Summary")
    st.write(f"**Title:** {request_title}")
    st.write(f"**Description:** {request_description}")
    st.write(f"**Stakeholder:** {stakeholder_name}")
    st.write(f"**Impact Type:** {impact_type}")

    if impact_type in ["Cost Savings", "Both"]:
        st.write(f"**Estimated Annual Cost Savings:** ${total_cost_savings:,.2f}")

    if impact_type in ["Value Enablement", "Both"]:
        st.write(f"**KPI Impacted:** {kpi_type}")
        st.write(f"**Baseline:** {baseline}")
        st.write(f"**Expected:** {expected}")
        st.write(f"**Improvement:** {improvement:.2f} units")

    st.markdown("---")
    st.success("Summary generated. You can copy/paste this into your intake form or records.")
