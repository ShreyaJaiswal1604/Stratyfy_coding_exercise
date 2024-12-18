import streamlit as st
import matplotlib.pyplot as plt
import requests

# Streamlit Title
st.title("Ice Cream Revenue Analysis 🍦")

# Load Ice Cream Image
st.image(
    "https://via.placeholder.com/600x200?text=Delicious+Ice+Cream",
    caption="Analyze Ice Cream Sales Revenue!",
    use_container_width=True,  # Updated parameter
)

# API Base URL
API_BASE_URL = "http://127.0.0.1:8000"  # Replace with your actual API URL if different

def fetch_sundae_data(sundae_id):
    """
    Fetch revenue and volume data for a specific sundae_id from the API.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/sundaes/{sundae_id}")
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch data for Sundae ID '{sundae_id}': {e}")
        return None

def main():
    # User Input for Sundae ID
    st.subheader("Get Revenue and Volume for a Sundae")
    sundae_id = st.text_input("Enter Sundae ID:", placeholder="e.g., mango-magic")

    if sundae_id:
        if st.button("Fetch Data"):
            # Fetch data for the given sundae ID
            data = fetch_sundae_data(sundae_id)

            if data:
                # Display data in a neat table
                st.write("### Sundae Details")
                st.json(data)

                # Extract volume and revenue
                volume = data.get("volume", 0)
                revenue = round(data.get("revenue", 0.0), 2)

                # Visualization
                st.write("### Revenue and Volume Chart")
                fig, ax = plt.subplots(figsize=(6, 4))

                # Bar chart for revenue and volume
                bars = ax.bar(["Volume", "Revenue"], [volume, revenue], color=["lightgreen", "skyblue"])
                ax.bar_label(bars, fmt="%.2f", padding=3)

                # Add labels and title
                ax.set_ylabel("Values")
                ax.set_title(f"Revenue and Volume for Sundae: {sundae_id}")
                st.pyplot(fig)

# Run the main function
if __name__ == "__main__":
    main()
