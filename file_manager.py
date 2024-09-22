import csv
import os
from datetime import datetime

class ScoreManager:
    def __init__(self):
        self.file_name = "scores.csv"
        # Create the CSV file with headers if it doesn't exist
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Game Number", "Moves", "Time Taken", "Date", "Time"])

    def save_score(self, moves, time_taken):
        # Append a new score entry to the CSV file
        with open(self.file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            game_number = sum(1 for _ in open(self.file_name))  # Count existing games
            current_time = datetime.now()
            writer.writerow([game_number, moves, time_taken, current_time.strftime("%Y-%m-%d"), current_time.strftime("%H:%M:%S")])

    def get_scores(self):
        # Read all scores from the CSV file
        with open(self.file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            return list(reader)  # Return all score records
