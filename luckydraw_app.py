import streamlit as st
import random
import pandas as pd
import time

# Load data from CSV files using st.cache_data
@st.cache_data
def load_data(file_name):
    return pd.read_csv(file_name)

# Simulate random name animation
def animate_names(participants, delay=0.05):
    placeholder = st.empty()
    for _ in range(10):  # Simulate 10 quick randomizations
        name = random.choice(participants)["Name"]
        placeholder.markdown(f"<h2 style='text-align: center; color: #2C3E50;'>{name}</h2>", unsafe_allow_html=True)
        time.sleep(delay)
    placeholder.empty()

# Custom styles for UX/UI
def set_custom_styles():
    st.markdown(
        """
        <style>
        .stApp {
            margin: 0;
            padding: 0;
            background-color: #ecf0f1;
        }
        .title {
            text-align: center;
            color: #3498db;
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 20px;
        }
        .container {
            display: flex;
            justify-content: space-between;
            width: 100%;
            margin: 0;
            padding: 0;
        }
        .left-box, .right-box {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin: 10px;
        }
        .left-box {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .right-box {
            flex: 1;
            max-height: 700px;
            overflow-y: auto;
        }
        .winner-details {
            margin-top: 20px;
            text-align: center;
            color: #2C3E50;
        }
        .winner-details h2 {
            font-size: 24px;
            font-weight: 600;
        }
        .winner-details h4 {
            font-size: 16px;
            font-weight: 500;
        }
        .winner-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 14px;
        }
        .winner-table th, .winner-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        .winner-table th {
            background-color: #3498db;
            color: white;
            font-weight: 700;
        }
        .winner-table td {
            background-color: #f9f9f9;
        }
        .winner-table tr:nth-child(even) td {
            background-color: #f1f1f1;
        }
        .winner-table tr:nth-child(odd) td {
            background-color: #ffffff;
        }
        .start-button {
            background-color: #3498db;
            color: white;
            font-size: 18px;
            padding: 10px 30px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            margin-bottom: 20px;  /* Space above the button */
        }
        .start-button:hover {
            background-color: #2980b9;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Main Streamlit App
def main():
    set_custom_styles()

    st.markdown("<h1 class='title'>🎉 Company Retreat Lucky Draw 🎉</h1>", unsafe_allow_html=True)

    # Load data
    participants = load_data("participants.csv").to_dict(orient="records")
    prizes = load_data("prizes.csv").to_dict(orient="records")

    # Session state
    if "remaining_participants" not in st.session_state:
        st.session_state.remaining_participants = participants
        st.session_state.remaining_prizes = prizes
        st.session_state.winners = []

    # Select a prize group
    groups = {prize["Group"] for prize in st.session_state.remaining_prizes}
    selected_group = st.selectbox("Select a prize group:", list(groups))

    # Filter prizes in the selected group
    group_prizes = [prize for prize in st.session_state.remaining_prizes if prize["Group"] == selected_group]

    # Layout containers for fixed boxes
    st.markdown('<div class="container">', unsafe_allow_html=True)
    left_col, right_col = st.columns([1, 1])

    # Left box (dynamic display)
    with left_col:
        st.markdown('<div class="left-box">', unsafe_allow_html=True)
        st.markdown("### Drawing Winner...")
        animation_placeholder = st.empty()
        winner_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

    # Right box (group winner display)
    with right_col:
        st.markdown('<div class="right-box">', unsafe_allow_html=True)
        st.markdown("### Winners List for Selected Group")
        group_winners_table_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

    # Start lucky draw
    if st.button("Start Lucky Draw", key="start_draw", help="Click to start drawing winners for the selected prize group", 
                 use_container_width=True):
        if len(st.session_state.remaining_participants) < len(group_prizes):
            st.error("Not enough participants for this group. Select a different group.")
            return

        for idx, prize in enumerate(group_prizes):
            # Simulate animation
            with left_col:
                animation_placeholder.empty()
                animate_names(st.session_state.remaining_participants)

            # Pick a winner
            winner = random.choice(st.session_state.remaining_participants)
            st.session_state.winners.append({"Winner Number": idx + 1, "Name": winner["Name"], "Prize": prize["Prize"]})

            # Display winner details
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
                if "Image" in prize and pd.notna(prize["Image"]):
                    st.image(prize["Image"], caption=prize["Prize"], use_column_width=True)

            # Update the winners table on the right (only for this group)
            with right_col:
                with group_winners_table_placeholder:
                    group_winners_df = pd.DataFrame(st.session_state.winners)
                    group_winners_df_filtered = group_winners_df[group_winners_df["Prize"] == prize["Prize"]]
                    
                    # Determine the number of winners and split into columns if needed
                    num_winners = len(group_winners_df_filtered)
                    num_columns = 1
                    if num_winners > 10 and num_winners <= 20:
                        num_columns = 2
                    elif num_winners > 20:
                        num_columns = 3
                    
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

            # Remove winner and prize
            st.session_state.remaining_participants.remove(winner)

        # Remove prizes from the selected group
        st.session_state.remaining_prizes = [
            prize for prize in st.session_state.remaining_prizes if prize["Group"] != selected_group
        ]

    # Summary of all winners at the bottom
    st.markdown("### All Winners Summary")
    all_winners_df = pd.DataFrame(st.session_state.winners)
    st.markdown(
        all_winners_df.to_html(
            index=False,
            classes="winner-table",
            escape=False,
        ),
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
