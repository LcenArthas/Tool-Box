# ProxyPulse

ProxyPulse is a Python-based tool for testing and diagnosing proxy connections. It provides information about your IP address, location, and tests connection speeds to various websites through your proxy.

## Features

- Detect and display your public IP address when using a proxy
- Show IP geolocation information
- Display HTTP and HTTPS proxy ports
- Test connection speeds to popular websites
- Option to enable or disable proxy usage
- Configurable proxy settings via JSON file

## Requirements

- Python 3.6+
- requests library

## Installation

1. Clone this repository:

```bash
 git clone https://github.com/yourusername/ProxyPulse.git
```

2. Install the required packages:

```bash
pip install requests
```

3. Create a `proxies.json` file in the same directory as the script with your proxy settings:

```json
{
  "HTTP_PROXY": "http://your_http_proxy:port",
  "HTTPS_PROXY": "https://your_https_proxy:port"
}
```

4. Usage

Run the script with or without proxy:

```
python proxypulse.py
```

To specify a different config file:

```
python proxypulse.py --proxy --config other_config.json
```

## Output
The script will output:

Your public IP address
IP geolocation (city and country)
HTTP and HTTPS proxy ports
Connection speeds to various websites


## Note
This tool uses free IP geolocation APIs which may have rate limits. For frequent or high-volume usage, consider using a paid geolocation service.


License
This project is licensed under the MIT License - see the LICENSE file for details.