import datetime

def generate_contribution_graph(commit_data):
    # Define emoji intensity levels
    intensity_levels = [
        "❌",  # No commits
        "🤦‍♂️",  # Low intensity (1-4 commits)
        "✅",  # Medium intensity (5-9 commits)
        "💪",  # High intensity (10-19 commits)
        "👑"   # Very high intensity (20+ commits)
    ]

    # Get the current date and the date 30 days ago
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=30)

    # Generate a list of all dates in the past 30 days
    date_list = [(start_date + datetime.timedelta(days=i)) for i in range(31)]

    # Prepare the graph, which will be a list of weeks (each week is a row)
    graph = []
    week_data = []  # List to hold one week's worth of commit history
    month_labels = []  # List to store the month labels
    current_month = start_date.strftime('%b')  # Get the starting month abbreviation
    
    # Loop through each day in the 30-day period
    for i, current_date in enumerate(date_list):
        day_of_week = current_date.weekday()  # Monday is 0, Sunday is 6
        date_str = current_date.isoformat()  # Convert date to ISO format
        month_str = current_date.strftime('%b')  # Get the current month's abbreviation

        # Add the month label when the month changes
        if month_str != current_month:
            month_labels.append(f" {current_month} ")
            current_month = month_str
        else:
            month_labels.append("     ")

        # Determine the intensity level for the current day
        if date_str in commit_data:
            commits = commit_data[date_str]
            if commits == 0:
                level = 0
            elif commits < 5:
                level = 1
            elif commits < 10:
                level = 2
            elif commits < 20:
                level = 3
            else:
                level = 4
            week_data.append(intensity_levels[level])
        else:
            week_data.append(intensity_levels[0])  # No commits on this day

        # If we reach Sunday or the last day in the range, start a new week
        if day_of_week == 6 or i == len(date_list) - 1:
            graph.append(week_data)
            week_data = []  # Reset for the next week

    # Print the graph (rows are weeks, columns are days)
    print("    S  M  T  W  T  F  S")  # Print day labels
    for idx, week in enumerate(graph):
        print(f"{month_labels[idx]} {' '.join(week)}")


