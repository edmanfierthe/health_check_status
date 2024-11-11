Here is the fixed and complete README.md file, preserving the Markdown format you requested:

# Fetch Health Check

This program monitors the health of a list of HTTP endpoints and logs the availability percentage of each domain over time. It reads a configuration file in YAML format, sends HTTP requests to each endpoint every 15 seconds, and prints the availability status to the console.

## Features

- Monitors multiple HTTP endpoints.
- Checks the health of endpoints based on response status and latency.
- Logs the availability percentage of each domain.
- Supports both GET and POST requests with custom headers and body.

## Prerequisites

Before running the program, ensure you have the following:

1. **Python 3.6 or later** installed. You can download it [here](https://www.python.org/downloads/).
2. The following Python packages:
   - `requests`
   - `PyYAML`

To install the required packages, run:

```pip install requests pyyaml```

## Getting Started

1. Clone the Repository

- git clone [<repository_url>](https://github.com/edmanfierthe/health_check_status)
- cd health_check_status

2. Create a YAML Configuration File

The program requires a YAML file with a list of HTTP endpoints to monitor. Here is an example configuration file named `config.yaml`:

Here is the configuration for the synthetic monitor request:

```yaml
- name: fetch index page
  url: https://fetch.com/
  method: GET
  headers:
    user-agent: fetch-synthetic-monitor
- body: '{"foo":"bar"}'
  headers:
    content-type: application/json
    user-agent: fetch-synthetic-monitor
  method: POST
  name: fetch some fake post endpoint
  url: https://fetch.com/some/post/endpoint

- name: fetch rewards index page
  url: https://www.fetchrewards.com/
```

3. Running the Program

To start monitoring, run the program with the configuration file as an argument:

```python fetch_health_check.py config.yaml```

4. Stopping the Program

The program runs continuously until you manually stop it. To stop the program, press:

```Ctrl + C```

5. Understanding the Output

The program prints the health status of each endpoint and logs the availability percentage of each domain. Example output:

fetch index page (https://fetch.com/) is UP. Response time: 120.00 ms
fetch careers page (https://fetch.com/careers) is DOWN. Response time: 600.00 ms, Status code: 200
fetch post endpoint (https://fetch.com/some/post/endpoint) is DOWN. Response time: 50.00 ms, Status code: 500
fetch rewards index page (https://www.fetchrewards.com/) is UP. Response time: 90.00 ms
fetch.com has 50% availability
www.fetchrewards.com has 100% availability

Explanation

	•	UP: The endpoint responded with a status code in the range 200-299 and had a latency less than 500 milliseconds.
	•	DOWN: The endpoint either had a status code outside the 200-299 range or had a latency of 500 milliseconds or more.
	•	availability: The percentage of successful (UP) requests for each domain.