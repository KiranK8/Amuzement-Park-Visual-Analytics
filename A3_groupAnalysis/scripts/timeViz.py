import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator
import numpy as np

# Load groups_df from the CSV file
groups_df = pd.read_csv('../../data/groups.csv')

# Create a new SQLite database connection
conn = sqlite3.connect('../../data/dinofun.db')

# Create a new table by joining movementFri and attractions on the x and y columns
conn.execute("""
CREATE TABLE IF NOT EXISTS movementFri_attractions_new_1 AS
SELECT movementFri.*, attractions.parkMapId, attractions.realWorldName as loc, attractions.dinoFunName, attractions.type as locType
FROM movementFri
JOIN attractions ON movementFri.x = attractions.x AND movementFri.y = attractions.y
ORDER BY movementFri.id ASC;
""")

# Load movementFri_attractions_new table into a DataFrame
movementFri_attractions_new_df = pd.read_sql_query("SELECT * FROM movementFri_attractions_new_1", conn, parse_dates=['timestamp'])

# Perform the inner join on the 'id' column
joined_df = pd.merge(movementFri_attractions_new_df, groups_df, on='id', how='inner')

# Select specific fields
selected_columns = ['timestamp', 'GroupId', 'SubgroupId', 'id', 'type', 'x', 'y', 'parkMapId', 'loc', 'dinoFunName', 'locType']
result_df = joined_df[selected_columns]

# Ensure timestamp is in datetime format
result_df['timestamp'] = pd.to_datetime(result_df['timestamp'])

# Order by timestamp in ascending order
result_df = result_df.sort_values(by='timestamp')

# Define the function to get stays for a specific GroupId
def getStays(group_id):
    # Filter the data for the specified GroupId
    group_df = result_df[result_df['GroupId'] == group_id]

    # Calculate the time difference and shift
    group_df['tdiff'] = group_df['timestamp'].diff().shift(-1)

    # Filter based on the given conditions
    group_df = group_df[((group_df['tdiff'] > pd.Timedelta('00:05:00')) & (group_df['type'] == 'movement')) |
                        (group_df['type'] == 'check-in')]

    # Check if the filtered DataFrame is empty
    if len(group_df) == 0:
        return group_df

    return group_df

# Function to create a vertical timeline plot for a specific GroupId
def plot_vertical_timeline(group_id, save_path='vertical_timeline.png'):
    group_df = getStays(group_id)
    
    if group_df.empty:
        print(f"No data available for GroupId: {group_id}")
        return
    
    fig, ax = plt.subplots(figsize=(10, 12))
    
    y_pos = np.arange(len(group_df))
    colors = ['green' if t == 'check-in' else 'purple' for t in group_df['type']]

    ax.barh(y_pos, width=group_df['tdiff'].dt.total_seconds() / 60, color=colors, edgecolor='black')
    
    # Annotate each bar with the activity name
    for i, (timestamp, dinoFunName, tdiff) in enumerate(zip(group_df['timestamp'], group_df['dinoFunName'], group_df['tdiff'])):
        end_time = (timestamp + tdiff).strftime('%I:%M %p') if not pd.isnull(tdiff) else ''
        ax.text(tdiff.total_seconds() / 60, i, f"{dinoFunName} ({end_time})", va='center', ha='left', fontsize=8)
    
    # Formatting the timeline
    ax.set_yticks(y_pos)
    ax.set_yticklabels(group_df['timestamp'].dt.strftime('%I:%M %p'))
    ax.invert_yaxis()  # labels read top-to-bottom
    
    ax.set_xlabel("Time spent (minutes)")
    ax.set_title(f"Timeline of Activities for Group {group_id}")
    plt.tight_layout()
    
    # Save the plot as a PNG file
    #plt.savefig(save_path)
    plt.show()

# Example usage
example_group_id = 1  # Replace with the desired GroupId
#plot_vertical_timeline(example_group_id, save_path='group1_timeline.png')

# Close the connection
#conn.close()
