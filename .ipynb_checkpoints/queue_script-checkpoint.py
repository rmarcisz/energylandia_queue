import requests
import csv
from datetime import datetime

API_URL = "https://queue-times.com/parks/317/queue_times.json"
CSV_FILE = "energylandia_queues.csv"

def fetch_queue_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def parse_queue_data(data):
    results = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for ride in data.get("rides", []):
        results.append({
            "timestamp": timestamp,
            "ride_name": ride.get("name"),
            "wait_time": ride.get("wait_time"),
            "is_open": ride.get("is_open"),
            "last_updated": ride.get("last_updated")
        })
    return results
    
def save_to_csv(records, filename):
    fieldnames = ["timestamp", "ride_name", "wait_time", "is_open", "last_updated"]

    try:
        with open(filename, 'x', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except FileExistsError:
        pass

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerows(records)

def main():
    try:
        data = fetch_queue_data()
        parsed_data = parse_queue_data(data)
        print(f"✔️ Ilość atrakcji znalezionych: {len(parsed_data)}")
        save_to_csv(parsed_data, CSV_FILE)
        print(f"✔️ Zapisano {len(parsed_data)} rekordów do pliku {CSV_FILE}")
    except Exception as e:
        print(f"❌ Wystąpił błąd: {e}")

if __name__ == "__main__":
    main()