- Health Check Script

health_check.py script reads an input argument to a file path with a list of HTTP endpoints in YAML format, tests the health of the endpoints every 15 seconds, keeps track of the availability percentage of the HTTP domain names being monitored by the program and logs the cumulative availability percentage for each domain to the console after the completion of each 15-second test cycle.
- Table of Contents
- Prerequisites
- Installation
- Input File Format
- Usage
- Output
- Customization
- Prerequisites
1. Python: The script requires Python 3.x. downloaded on the machine 
Requests Library: This script relies on the requests library to make HTTP calls.

2. Installation
Clone or Download this repository to your local machine.
Install the Requests Library: Open a terminal or command prompt, then run:
pip install requests

3. Input File Format
Create an input file that lists all endpoints to be monitored in YAML-like format. Each endpoint should contain the following fields:
name: A name or description of the endpoint
url: The URL to be monitored
method: The HTTP method (e.g., GET, POST)
headers: Optional HTTP headers as key-value pairs
body: Optional request body (for POST requests)
Sample Input File (input_file.yaml):

4. Usage
Save the input file (e.g., input_file.yaml) with above endpoints. You can also add more endpoints if you want to monitor those.
Edit the File Path in the Script: In the Python script, locate the following line and replace "/path/to/file" with the path to your input file.
file_path = "/path/to/your/input_file.yaml file"
Run the Script: Open a terminal or command prompt in the directory containing the script, then run:
python health_check.py
Stopping the Script: To stop the monitoring process, press Ctrl + C in the terminal.

5. Output
The script will continuously monitor each endpoint and print the availability percentage for each domain every 15 seconds. Sample output might look like this:

fetch.com has 67% availability percentage

www.fetchrewards.com has 100% availability percentage

fetch.com has 67% availability percentage

www.fetchrewards.com has 100% availability percentage

...

7. Customization
Timeout: You can adjust the timeout in the check_health function by modifying the timeout parameter:
response = requests.request(method, url, headers=headers, data=body, timeout=0.5)
By default, the script does a health check every 15 seconds. Change the time.sleep(15) line to adjust the interval.

