import streamlit as st
import pandas as pd

st.set_page_config(page_title="SplitTicket Prototype", page_icon="🚆", layout="centered")

st.title("🚆 SplitTicket — Smart Train Seat Optimization (Prototype)")
st.write("Demo: suggests split-ticket options when direct seats are unavailable.")

# Load data
data = pd.read_csv("sample_data.csv")

st.subheader("📊 Sample Seat Availability Data")
st.dataframe(data)

st.subheader("🔍 Find Split Ticket Options")
# stations for selection: union of From and To
stations = sorted(list(set(data["From"]) | set(data["To"])))
source = st.selectbox("From Station", stations, index=0)
destination = st.selectbox("To Station", [s for s in stations if s != source], index=0)

if st.button("Find Routes"):
    # Direct check
    direct = data[(data["From"] == source) & (data["To"] == destination)]
    if not direct.empty and int(direct.iloc[0]["Available_Seats"]) > 0:
        st.success(f"✅ Direct booking available: {int(direct.iloc[0]['Available_Seats'])} seats")
    else:
        st.info("🔎 Checking for split-ticket options...")
        possible_routes = []
        for mid in stations:
            if mid in (source, destination): 
                continue
            part1 = data[(data["From"] == source) & (data["To"] == mid) & (data["Available_Seats"] > 0)]
            part2 = data[(data["From"] == mid) & (data["To"] == destination) & (data["Available_Seats"] > 0)]
            if not part1.empty and not part2.empty:
                possible_routes.append({
                    "via": mid,
                    "part1_seats": int(part1.iloc[0]["Available_Seats"]),
                    "part2_seats": int(part2.iloc[0]["Available_Seats"]),
                    "train1": part1.iloc[0]["Train"],
                    "train2": part2.iloc[0]["Train"],
                })

        if possible_routes:
            st.success("✅ Split-ticket options found!")
            for r in possible_routes:
                st.markdown(f"**Route:** {source} → {r['via']} → {destination}")
                st.write(f"• {r['train1']}: {source} → {r['via']} — Seats: {r['part1_seats']}")
                st.write(f"• {r['train2']}: {r['via']} → {destination} — Seats: {r['part2_seats']}")
                st.markdown("---")
        else:
            st.error("❌ No split-ticket options found.")
