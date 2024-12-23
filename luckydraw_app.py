import streamlit as st
import random
import pandas as pd
import time

# Load data from CSV files
@st.cache_data
def load_data(file_name):
    return pd.read_csv(file_name)


# Calculate dynamic delay for adding results to the table
def get_dynamic_delay(num_winners):
    # Scale the delay linearly between 6 sec for 4 winners and 1 sec for 32 winners
    min_delay = 1  # 1 second for 32 winners
    max_delay = 6  # 6 seconds for 4 winners
    if num_winners <= 4:
        return max_delay  # Return 6 seconds for 4 or fewer winners
    elif num_winners >= 32:
        return min_delay  # Return 1 second for 32 or more winners
    else:
        # Linear interpolation between 6 sec and 1 sec based on number of winners
        return max_delay - (num_winners - 4) * (max_delay - min_delay) / (32 - 4)

# Simulate name animation with fast animation
def animate_names(participants, placeholder, iterations=10):
    for _ in range(iterations):
        name = random.choice(participants)["Name"]
        placeholder.markdown(
            f"<p style='text-align: center;'>{name}</p>",
            unsafe_allow_html=True
        )
        time.sleep(0.1)  # Fast animation with small delay

# Load custom CSS
def load_custom_css(css_file_path="style/style.css"):
    with open(css_file_path, "r") as f:
        css_content = f.read()
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="🎄 MRC Retreat 2024 🎅", page_icon=":gift:", layout="wide")

# Main application function
def main():
    load_custom_css()

    # Load Animation
    snow = "❄"
    money = "💸"
    tree = "🎄"

    st.markdown(
    f"""
    <div class="snowflake">{snow}</div>
    <div class="snowflake">{snow}</div>
    <div class="snowflake">{snow}</div>
    <div class="snowflake">{snow}</div>
    <div class="snowflake">{snow}</div>
    <div class="snowflake">{snow}</div>
    <div class="snowflake">{tree}</div>
    <div class="snowflake">{tree}</div>
    <div class="snowflake">{snow}</div>
    <div class="snowflake">{snow}</div>
    <div class="snowflake">{snow}</div>
    <div class="snowflake">{snow}</div>
    <div class="snowflake">{snow}</div>
    <div class="snowflake">{money}</div>
    <div class="snowflake">{money}</div>
    <div class="snowflake">{money}</div>
    <div class="snowflake">{money}</div>
    """,
    unsafe_allow_html=True,
    )

    # Header
    st.markdown("<h1 class='title'>🎅 MRC Retreat 2024 - Lucky Draw 🎁</h1>", unsafe_allow_html=True)
    start_lucky_draw = st.button("Start Lucky Draw", key="start_draw")

    # Load participant and prize data
    participants = load_data("participants.csv").to_dict(orient="records")
    prizes = load_data("prizes.csv").to_dict(orient="records")

    # Initialize session state
    if "remaining_participants" not in st.session_state:
        st.session_state.remaining_participants = participants
        st.session_state.remaining_prizes = prizes
        st.session_state.winners = []

    # Select prize group
    groups = {prize["Group"] for prize in st.session_state.remaining_prizes}
    selected_group = st.selectbox("Select a prize group:", list(groups))

    # Layout containers
    left_col, right_col = st.columns([1, 3])

    with left_col:
        st.markdown(
        '''
        <div class="left-box">
            <h4>Looking for the winners...</h4>
        </div>'''
        ,unsafe_allow_html=True
        )
        animation_placeholder = st.empty()
        winner_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

    # Right column: winner table
    with right_col:
        # Display selected group and winner count dynamically
        group_prizes = [prize for prize in st.session_state.remaining_prizes if prize["Group"] == selected_group]
        total_prizes = len(group_prizes)

        st.markdown(
        f'''
        <div class="left-box">
            <h4>{total_prizes} winners for {selected_group}</h4>
        </div>''',
            unsafe_allow_html=True)
        group_winners_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

    if start_lucky_draw:
        group_prizes = [prize for prize in st.session_state.remaining_prizes if prize["Group"] == selected_group]

        if len(st.session_state.remaining_participants) < len(group_prizes):
            st.error("Not enough participants for this group.")
            return

        for idx, prize in enumerate(group_prizes):
            # Animate names (always fast)
            animate_names(st.session_state.remaining_participants, animation_placeholder)

            # Select winner and immediately stop animation
            winner = random.choice(st.session_state.remaining_participants)

            # Add winner to session state
            st.session_state.winners.append({"No.": len(st.session_state.winners) + 1, "Name": winner["Name"], "Prize": prize["Prize"]})

            # Delay before hiding the animation and revealing the winner's name
            delay = get_dynamic_delay(len(group_prizes))  # Get dynamic delay based on the number of winners
            time.sleep(delay)

            # Stop and hide the animation
            animation_placeholder.empty()  # Stop and hide the animation

            # Show winner details after delay
            winner_placeholder.markdown(
                f"""
                <div class="winner-details">
                    <h2 style="">🎉 Winner {idx + 1}</h2>
                    <h2 style="">{winner['Name']}</h2>
                    <h2 style="">{prize['Prize']}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Update right column with winner details
            with group_winners_placeholder:
                winners_df = pd.DataFrame(st.session_state.winners)
                group_winners = winners_df[winners_df["Prize"].isin([pr["Prize"] for pr in group_prizes])]

                num_columns = 1 if len(group_winners) <= 10 else 2 if len(group_winners) <= 20 else 3
                cols = st.columns(num_columns)

                start_idx = 0
                winners_per_col = len(group_winners) // num_columns
                for i in range(num_columns):
                    end_idx = start_idx + winners_per_col if i < num_columns - 1 else len(group_winners)
                    with cols[i]:
                        st.markdown(
                            group_winners.iloc[start_idx:end_idx].to_html(
                                index=False, classes="winner-table", escape=False
                            ),
                            unsafe_allow_html=True,
                        )
                    start_idx = end_idx

            # Remove the winner from the participants
            st.session_state.remaining_participants = [
                participant for participant in st.session_state.remaining_participants if participant != winner
            ]

        # Remove prizes from the selected group
        st.session_state.remaining_prizes = [
            prize for prize in st.session_state.remaining_prizes if prize["Group"] != selected_group
        ]

    # Summary of all winners
    st.markdown("### All Winners Summary")
    all_winners_df = pd.DataFrame(st.session_state.winners)

    if not all_winners_df.empty:
        all_winners_df["No."] = range(1, len(all_winners_df) + 1)
        st.markdown(
            all_winners_df.to_html(index=False, classes="winner-table", escape=False),
            unsafe_allow_html=True,
        )
    else:
        st.markdown("<p>No winners yet. Start the draw to see results.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
