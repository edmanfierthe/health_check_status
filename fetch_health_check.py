import yaml
import requests
import time
import signal
import sys
from collections import defaultdict

# Dictionary to track the number of UP requests and total requests per domain
availability_tracker = defaultdict(lambda: {"up": 0, "total": 0})

# Function to parse the YAML configuration file
def parse_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to check the health of an endpoint
def check_endpoint(endpoint):
    name = endpoint.get('name')
    url = endpoint.get('url')
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)

    try:
        # Measure the response time
        response = requests.request(method, url, headers=headers, json=body, timeout=2)
        latency = response.elapsed.total_seconds() * 1000  # Convert to milliseconds

        # Determine if the endpoint is UP
        if 200 <= response.status_code < 300 and latency < 500:
            print(f"{name} ({url}) is UP. Response time: {latency:.2f} ms")
            return 'UP'
        else:
            print(f"{name} ({url}) is DOWN. Response time: {latency:.2f} ms, Status code: {response.status_code}")
            return 'DOWN'
    except requests.exceptions.RequestException as e:
        print(f"{name} ({url}) encountered an error: {e}")
        return 'DOWN'

# Function to update availability metrics and log results
def update_availability(endpoint, status):
    url = endpoint.get('url')
    domain = url.split("//")[-1].split("/")[0]

    # Update the tracker for total and UP requests
    availability_tracker[domain]['total'] += 1
    if status == 'UP':
        availability_tracker[domain]['up'] += 1

# Function to log the current availability percentages
def log_availability():
    for domain, metrics in availability_tracker.items():
        up = metrics['up']
        total = metrics['total']
        if total > 0:
            availability_percentage = round((up / total) * 100)
        else:
            availability_percentage = 0
        print(f"{domain} has {availability_percentage}% availability")

# Signal handler for graceful exit
def signal_handler(sig, frame):
    print("\nExiting program.")
    sys.exit(0)

# Main function to run the health check loop
def main(file_path):
    signal.signal(signal.SIGINT, signal_handler)
    endpoints = parse_config(file_path)

    while True:
        for endpoint in endpoints:
            # Ensure the required 'name' field is present
            if 'name' not in endpoint or 'url' not in endpoint:
                print("Error: 'name' and 'url' are required fields in the configuration.")
                continue

            status = check_endpoint(endpoint)
            update_availability(endpoint, status)
        log_availability()
        time.sleep(15)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fetch_health_check.py <config_file_path>")
        sys.exit(1)

    config_file_path = sys.argv[1]
    main(config_file_path)