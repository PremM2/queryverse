import streamlit as st
import pandas as pd

st.set_page_config(page_title="QueryVerse - Search Insight Engine", layout="wide")
st.title("🔍 QueryVerse: SQL-Powered Search Insight Engine")

st.markdown("""
Upload your own CSVs for the following tables:
- **Products** (`sample_products.csv`)
- **Search Queries** (`sample_search_queries.csv`)
- **Click Logs** (`sample_click_logs.csv`)
- **Purchase Logs** (`sample_purchase_logs.csv`)
""")

# File uploaders
products_file = st.file_uploader("Upload Products CSV", type=["csv"])
search_file = st.file_uploader("Upload Search Queries CSV", type=["csv"])
clicks_file = st.file_uploader("Upload Click Logs CSV", type=["csv"])
purchase_file = st.file_uploader("Upload Purchase Logs CSV", type=["csv"])

if all([products_file, search_file, clicks_file, purchase_file]):
    products_df = pd.read_csv(products_file)
    search_df = pd.read_csv(search_file)
    clicks_df = pd.read_csv(clicks_file)
    purchase_df = pd.read_csv(purchase_file)

    st.success("✅ Files uploaded successfully!")

    with st.expander("📦 Preview Data"):
        st.subheader("Products")
        st.dataframe(products_df.head())
        st.subheader("Search Queries")
        st.dataframe(search_df.head())
        st.subheader("Click Logs")
        st.dataframe(clicks_df.head())
        st.subheader("Purchase Logs")
        st.dataframe(purchase_df.head())

    # CTR Calculation
    ctr_df = search_df.groupby("query_id").size().reset_index(name="search_count")
    click_counts = clicks_df.groupby("query_id").size().reset_index(name="click_count")
    ctr_df = ctr_df.merge(click_counts, on="query_id", how="left").fillna(0)
    ctr_df["CTR (%)"] = round(100 * ctr_df["click_count"] / ctr_df["search_count"], 2)

    # CVR Calculation
    click_purchase = clicks_df.merge(purchase_df, on=["user_id", "product_id"], how="left", indicator=True)
    click_purchase["is_purchase"] = click_purchase["_merge"] == "both"
    cvr_df = click_purchase.groupby("query_id")["is_purchase"].mean().reset_index(name="CVR (%)")
    cvr_df["CVR (%)"] = round(100 * cvr_df["CVR (%)"], 2)

    funnel_df = ctr_df.merge(cvr_df, on="query_id", how="left").fillna(0)
    funnel_df = funnel_df.merge(search_df[["query_id", "raw_query"]].drop_duplicates(), on="query_id")

    st.markdown("---")
    st.subheader("📊 Funnel Metrics (CTR & CVR by Query)")
    st.dataframe(funnel_df[["query_id", "raw_query", "search_count", "click_count", "CTR (%)", "CVR (%)"]])

else:
    st.info("⬆️ Please upload all four required CSV files to begin analysis.")




Add app.py (main Streamlit script)

