import pandas as pd
import streamlit as st
from api.database import engine  # Import your database engine
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Revenue Report 📊")

def fetch_revenue_data():
    query = """
    SELECT 
        sundaes.id AS sundae_id,
        sundaes.name AS sundae_name,
        COUNT(*) AS volume,
        COALESCE(SUM(sales.price), 0) AS revenue
    FROM sundaes
    LEFT JOIN sales ON sundaes.id = sales.sundae_id
    GROUP BY sundaes.id, sundaes.name
    ORDER BY revenue DESC;
    """
    with engine.connect() as connection:
        return pd.read_sql(query, connection)

def main():
    try:
        st.write("### Revenue Analysis")
        df = fetch_revenue_data()

        if df.empty:
            st.warning("No revenue data available.")
        else:
            st.dataframe(df)

            # Plot revenue data
            st.write("### Revenue and Volume Comparison")

            # Matplotlib for customized visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Use seaborn for a better bar plot with distinct colors
            sns.barplot(
                x="sundae_name",
                y="revenue",
                data=df,
                palette="coolwarm",
                ax=ax,
                label="Revenue",
            )

            # Add values above bars
            for bar in ax.patches:
                ax.annotate(
                    f"${bar.get_height():,.2f}",
                    (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    color="black",
                )

            # Customization
            ax.set_title("Revenue per Sundae", fontsize=16, weight="bold")
            ax.set_xlabel("Sundae Name", fontsize=12)
            ax.set_ylabel("Revenue ($)", fontsize=12)
            ax.tick_params(axis="x", rotation=45)
            ax.grid(axis="y", linestyle="--", alpha=0.7)

            # Render the chart
            st.pyplot(fig)

            st.write("### Insights")
            st.info(f"**Top Revenue Sundae:** {df.iloc[0]['sundae_name']} with ${df.iloc[0]['revenue']:.2f}")
            st.info(f"**Total Revenue:** ${df['revenue'].sum():,.2f}")

    except Exception as e:
        st.error(f"Error fetching revenue data: {e}")

if __name__ == "__main__":
    main()
