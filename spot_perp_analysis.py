import pandas as pd

# Load Data
spot_df = pd.read_csv(r"C:\Users\E16\spor-perpetual_analysis\spot.csv")
futures_df = pd.read_csv(r"C:\Users\E16\spor-perpetual_analysis\futures.csv")

print("Converting timestamps...")

# Flexible timestamp parsing
spot_df['time'] = pd.to_datetime(spot_df['time'], errors='coerce', utc=True)
futures_df['time'] = pd.to_datetime(futures_df['time'], errors='coerce', utc=True)

# Remove invalid timestamps
spot_df.dropna(subset=['time'], inplace=True)
futures_df.dropna(subset=['time'], inplace=True)

# Calculate mid-price
spot_df['mid_price'] = (spot_df['bid_price'] + spot_df['ask_price']) / 2
futures_df['mid_price'] = (futures_df['bid_price'] + futures_df['ask_price']) / 2

# Sort by time
spot_df.sort_values('time', inplace=True)
futures_df.sort_values('time', inplace=True)

# TEMP: Limit dataset for testing
spot_df = spot_df.head(50000)

print(f"Loaded {len(spot_df)} spot rows for testing...")

# Detect ±0.07% price moves within 3ms
price_threshold = 0.0007  # 0.07%
sudden_spot_events = []

for i in range(1, len(spot_df)):
    time_diff = (spot_df.iloc[i]['time'] - spot_df.iloc[i - 1]['time']).total_seconds() * 1000
    price_change = (spot_df.iloc[i]['mid_price'] - spot_df.iloc[i - 1]['mid_price']) / spot_df.iloc[i - 1]['mid_price']

    if abs(price_change) >= price_threshold and time_diff <= 3:
        sudden_spot_events.append({
            'time': spot_df.iloc[i]['time'],
            'price_change': round(price_change * 100, 5),
            'direction': 'up' if price_change > 0 else 'down'
        })
    if i % 500 == 0:
        print(f"Checked {i} rows...")

print(f"\nDetected {len(sudden_spot_events)} sudden spot price moves within 3ms.\n")

# Futures reaction detection
reaction_events = []
for event in sudden_spot_events:
    event_time = event['time']
    future_window = futures_df[(futures_df['time'] > event_time) & (futures_df['time'] <= event_time + pd.Timedelta(milliseconds=5))]

    if not future_window.empty:
        first_reaction = future_window.iloc[0]
        latest_before = futures_df[futures_df['time'] <= event_time].iloc[-1]
        price_change = (first_reaction['mid_price'] - latest_before['mid_price']) / latest_before['mid_price']

        if abs(price_change) >= price_threshold:
            reaction_events.append({
                'spot_event_time': event_time,
                'futures_reaction_time': first_reaction['time'],
                'price_change': round(price_change * 100, 5),
                'direction': 'up' if price_change > 0 else 'down'
            })

print(f"\nDetected {len(reaction_events)} futures reactions within 5ms after spot price moves.\n")

# Futures sudden moves
detected_futures_events = []
for i in range(1, len(futures_df)):
    time_diff = (futures_df.iloc[i]['time'] - futures_df.iloc[i - 1]['time']).total_seconds() * 1000
    price_change = (futures_df.iloc[i]['mid_price'] - futures_df.iloc[i - 1]['mid_price']) / futures_df.iloc[i - 1]['mid_price']

    if abs(price_change) >= price_threshold and time_diff <= 3:
        detected_futures_events.append({
            'time': futures_df.iloc[i]['time'],
            'price_change': round(price_change * 100, 5),
            'direction': 'up' if price_change > 0 else 'down'
        })

print(f"\nDetected {len(detected_futures_events)} sudden futures price moves within 3ms.\n")

# Spot reactions after futures moves
spot_reactions = []
for event in detected_futures_events:
    event_time = event['time']
    spot_window = spot_df[(spot_df['time'] > event_time) & (spot_df['time'] <= event_time + pd.Timedelta(milliseconds=5))]

    if not spot_window.empty:
        first_spot = spot_window.iloc[0]
        latest_before = spot_df[spot_df['time'] <= event_time].iloc[-1]
        price_change = (first_spot['mid_price'] - latest_before['mid_price']) / latest_before['mid_price']

        if abs(price_change) >= price_threshold:
            spot_reactions.append({
                'futures_event_time': event_time,
                'spot_reaction_time': first_spot['time'],
                'price_change': round(price_change * 100, 5),
                'direction': 'up' if price_change > 0 else 'down'
            })

print(f"\nDetected {len(spot_reactions)} spot reactions within 5ms after futures price moves.\n")

# Market leadership summary
spot_leads = len(reaction_events)
futures_leads = len(spot_reactions)
total_events = spot_leads + futures_leads

if total_events > 0:
    spot_lead_pct = round((spot_leads / total_events) * 100, 2)
    futures_lead_pct = round((futures_leads / total_events) * 100, 2)
else:
    spot_lead_pct = futures_lead_pct = 0

summary_text = f"""
Market Leadership Summary:
- Spot leads in {spot_lead_pct}% of events ({spot_leads} times)
- Futures leads in {futures_lead_pct}% of events ({futures_leads} times)
"""

print(summary_text)

with open(r"C:\Users\E16\spor-perpetual_analysis\market_summary.txt", "w") as f:
    f.write(summary_text)

# Save detailed results
with open(r"C:\Users\E16\spor-perpetual_analysis\output.txt", "w") as f:
    f.write(f"Detected {len(sudden_spot_events)} sudden spot price moves within 3ms.\n\n")
    for event in sudden_spot_events:
        f.write(f"{event}\n")

    f.write(f"\nDetected {len(reaction_events)} futures reactions within 5ms after spot price moves.\n\n")
    for reaction in reaction_events:
        f.write(f"{reaction}\n")

    f.write(f"\nDetected {len(detected_futures_events)} sudden futures price moves within 3ms.\n\n")
    for event in detected_futures_events:
        f.write(f"{event}\n")

    f.write(f"\nDetected {len(spot_reactions)} spot reactions within 5ms after futures price moves.\n\n")
    for reaction in spot_reactions:
        f.write(f"{reaction}\n")

print("\nFull analysis complete. Outputs saved.")
