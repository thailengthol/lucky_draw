import streamlit as st
import random
import pandas as pd
import time

# Load data from CSV files with caching for efficiency
@st.cache_data
def load_data(file_name):
    return pd.read_csv(file_name)

# Simulate random name animation
def animate_names(participants, placeholder, delay=0.5):
    for _ in range(10):  # Simulate 10 quick randomizations
        name = random.choice(participants)["Name"]
        placeholder.markdown(
            f"<h2 style='text-align: center; color: #2C3E50;'>{name}</h2>", 
            unsafe_allow_html=True
        )
        time.sleep(delay)
    placeholder.empty()

# Function to load custom CSS from an external file
def load_custom_css(css_file_path="style/style.css"):
    with open(css_file_path, "r") as f:
        css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="MRC Retreat 2024", page_icon=":tada:", layout="wide")

# Main Streamlit App
def main():
    # Load custom styles from external CSS file
    load_custom_css()

    # Header section
    header_col1, header_col2 = st.columns([1, 0.2])
    with header_col1:
        st.markdown("<h1 class='title'>🎉 MRC Retreat 2024 - Lucky Draw 🎉</h1>", unsafe_allow_html=True)
    with header_col2:
        start_lucky_draw = st.button("Start Lucky Draw", key="start_draw", help="Click to start drawing winners")

    # Load participant and prize data
    participants = load_data("participants.csv").to_dict(orient="records")
    prizes = load_data("prizes.csv").to_dict(orient="records")

    # Session state initialization
    if "remaining_participants" not in st.session_state:
        st.session_state.remaining_participants = participants
        st.session_state.remaining_prizes = prizes
        st.session_state.winners = []

    # Select prize group from available prize groups
    groups = {prize["Group"] for prize in st.session_state.remaining_prizes}
    selected_group = st.selectbox("Select a prize group:", list(groups))

    # Layout containers for fixed boxes
    st.markdown('<div class="container">', unsafe_allow_html=True)
    left_col, right_col = st.columns([0.2, 1])

    # Left box: drawing winner animation and display
    with left_col:
        st.markdown('<div class="left-box">', unsafe_allow_html=True)
        st.markdown("### Looking for the winner...")
        animation_placeholder = st.empty()
        winner_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

    # Right box: display winners for selected prize group
    with right_col:
        st.markdown('<div class="right-box">', unsafe_allow_html=True)
        st.markdown("### Winners List for selected prize")
        group_winners_table_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

    # Start lucky draw logic
    if start_lucky_draw:
        # Filter prizes for the selected group
        group_prizes = [prize for prize in st.session_state.remaining_prizes if prize["Group"] == selected_group]
        if len(st.session_state.remaining_participants) < len(group_prizes):
            st.error("Not enough participants for this group. Select a different group.")
            return

        for idx, prize in enumerate(group_prizes):
            # Simulate random name animation
            with left_col:
                animate_names(st.session_state.remaining_participants, animation_placeholder)

            # Select a winner
            winner = random.choice(st.session_state.remaining_participants)
            st.session_state.winners.append({"No.": idx + 1, "Name": winner["Name"], "Prize": prize["Prize"]})

            # Display winner details in the left column
            with left_col:
                winner_placeholder.markdown(
                    f"""
                    <div class="winner-details">
                        <h2>🎉 Winner {idx + 1}</h2>
                        <h4>Name: {winner['Name']}</h4>
                        <h4>Prize: {prize['Prize']}</h4>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Display the group winners list in the right column
            with right_col:
                with group_winners_table_placeholder:
                    group_winners_df = pd.DataFrame(st.session_state.winners)
                    group_winners_df_filtered = group_winners_df[group_winners_df["Prize"] == prize["Prize"]]
                    
                    # Split winners into multiple columns based on the number of winners
                    num_winners = len(group_winners_df_filtered)
                    num_columns = 3 if num_winners >= 12 else 2 if num_winners >= 8 else 1
                    cols = st.columns(num_columns)

                    # Distribute winners among columns
                    start_idx = 0
                    winners_per_col = num_winners // num_columns
                    for i in range(num_columns):
                        end_idx = start_idx + winners_per_col if i < num_columns - 1 else num_winners
                        with cols[i]:
                            st.markdown(
                                group_winners_df_filtered.iloc[start_idx:end_idx].to_html(
                                    index=False, classes="winner-table", escape=False
                                ),
                                unsafe_allow_html=True,
                            )
                        start_idx = end_idx
            # Remove the winner and prize from session state
            st.session_state.remaining_participants.remove(winner)

        # Remove prizes from the selected group
        st.session_state.remaining_prizes = [
            prize for prize in st.session_state.remaining_prizes if prize["Group"] != selected_group
        ]

    # Display a summary of all winners at the end
    st.markdown("### All Winners Summary")
    all_winners_df = pd.DataFrame(st.session_state.winners)
    # Ensure the DataFrame has the correct columns and add winner number for better clarity
    # Assuming you have columns like "Name" and "Prize" when adding winners
    if not all_winners_df.empty:
        # Add a "Winner Number" column for sequential numbering
        all_winners_df["No."] = range(1, len(all_winners_df) + 1)

        # Select the columns to display: "Winner Number", "Name", and "Prize"
        all_winners_df = all_winners_df[["No.", "Name", "Prize"]]

        # Display winners summary table with better formatting
        st.markdown(
            all_winners_df.to_html(index=False, classes="winner-table", escape=False),
            unsafe_allow_html=True,
        )
    else:
        st.markdown("<p>No winners selected yet. Start the draw to see results.</p>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
