import requests
import time
from collections import defaultdict


def extract_endpoints(file_path):
    endpoints = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    items = []
    item = []
    first_line = True

    for line in lines:
        if line.startswith("-") and first_line:
            item.append(line)
            first_line = False
        elif line.startswith("-") and not first_line:
            items.append(item)  # Save the previous item
            item = [line]  # Start a new item
        else:
            item.append(line)

    items.append(item)  # Append the last item after loop

    # print(items)
    for item in items:
        endpoint = {}
        endpoint['headers'] = {}
        collecting_headers = False

        for line in item:
            stripped_line = line.lstrip("-").strip()

            if stripped_line.startswith("name:"):
                endpoint['name'] = stripped_line.split(":", 1)[1].strip()
            elif stripped_line.startswith("url:"):
                endpoint['url'] = stripped_line.split(":", 1)[1].strip()
            elif stripped_line.startswith("method:"):
                endpoint['method'] = stripped_line.split(":", 1)[1].strip()
            elif stripped_line.startswith("headers:"):
                collecting_headers = True  # Start collecting headers
            elif collecting_headers:
                if line.startswith("    "):
                    header_line = stripped_line.strip()
                    if ':' in header_line:
                        key, value = map(str.strip, header_line.split(":", 1))
                        # endpoint['headers'].append((key, value))  # Collect header as tuple
                        endpoint['headers'][key] = value
                else:
                    collecting_headers = False  # End of headers section
            elif stripped_line.startswith("body:"):
                endpoint['body'] = stripped_line.split(":", 1)[1].strip()

        # Ensure we add the endpoint to the list if it has both 'name' and 'url'
        if 'name' in endpoint and 'url' in endpoint:
            endpoints.append(endpoint)

    # print(endpoints)
    return endpoints


def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers', {})
    # headers = dict(endpoint.get('headers', []))  # Convert headers from list of tuples to a dictionary
    body = endpoint.get('body', None)

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, data=body, timeout=0.5)
        response_time = (time.time() - start_time) * 1000

        if 200 <= response.status_code < 300 and response_time < 500:
            return 'UP'
        else:
            return 'DOWN'
    except Exception as e:
        print("An error occurred:", str(e))
        return None


def monitor_endpoints(file_path):
    endpoints = extract_endpoints(file_path)
    domain_stats = defaultdict(lambda: {'up': 0, 'total': 0})

    try:
        while True:
            for endpoint in endpoints:
                domain = endpoint['url'].split('//')[1].split('/')[0]
                status = check_health(endpoint)
                domain_stats[domain]['total'] += 1
                if status == 'UP':
                    domain_stats[domain]['up'] += 1

            # print(domain_stats)

            for domain, stats in domain_stats.items():
                availability = round(100 * (stats['up'] / stats['total']))
                print(f"{domain} has {availability}% availability percentage")
            # print("\n")

            time.sleep(15)

    except KeyboardInterrupt:
        print("Monitoring interrupted.")


if __name__ == "__main__":
    file_path = "/path/to/file"  # Update with your file path
    file_path = "input_file.yaml"
    monitor_endpoints(file_path)

