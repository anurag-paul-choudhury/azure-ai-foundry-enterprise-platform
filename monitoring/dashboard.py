
import streamlit as st
import sqlite3
import pandas as pd

DATABASE_PATH = "monitoring/telemetry.db"

st.set_page_config(
    page_title="Enterprise AI Monitoring",
    page_icon="📊",
    layout="wide"
)

st.title("Enterprise AI Infrastructure Monitoring")

st.caption("Live operational metrics from the local Groq-powered AI application")

# Read database
def get_data():

    connection = sqlite3.connect(DATABASE_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM requests ORDER BY id DESC",
        connection
    )

    connection.close()

    return df


df = get_data()

if df.empty:

    st.warning("No request data available. Run the AI application first.")

else:

    # Calculate metrics
    total_requests = len(df)

    successful_requests = len(
        df[df["status"] == "success"]
    )

    failed_requests = total_requests - successful_requests

    success_rate = (
        successful_requests / total_requests
    ) * 100

    average_latency = df["latency"].mean()

    total_tokens = df["total_tokens"].sum()

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Requests", total_requests)

    col2.metric("Success Rate", f"{success_rate:.1f}%")

    col3.metric("Average Latency", f"{average_latency:.2f} sec")

    col4.metric("Total Tokens", int(total_tokens))

    st.divider()

    # Request status
    st.subheader("Request Status")

    status_counts = df["status"].value_counts()

    st.bar_chart(status_counts)

    # Latency chart
    st.subheader("Request Latency")

    latency_data = df.sort_values("id")

    st.line_chart(
        latency_data.set_index("id")["latency"]
    )

    # Token usage
    st.subheader("Token Consumption")

    st.bar_chart(
        latency_data.set_index("id")[
            ["prompt_tokens", "completion_tokens"]
        ]
    )

    # Request history
    st.subheader("Recent Request History")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.caption(
        "Data source: Local SQLite telemetry database. "
        "This is not Azure Monitor data."
    )
