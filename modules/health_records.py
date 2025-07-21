import streamlit as st
import pandas as pd

def run(db_manager):
    st.header("📋 Health Records Management")

    tab1, tab2 = st.tabs(["View Records", "Search"])

    with tab1:
        st.subheader("Recent Health Records")
        limit = st.slider("Records to show", 10, 100, 20)
        records = db_manager.get_health_records(limit=limit)
        if records:
            df = pd.DataFrame(records)
            st.dataframe(df)
        else:
            st.info("No records available.")

    with tab2:
        search = st.text_input("Search by Disease or Cow ID")
        if search:
            results = db_manager.search_records(search)
            if results:
                st.dataframe(pd.DataFrame(results))
            else:
                st.warning("No matching records.")
