import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_ip(ip):
    """Attempt to connect to an IP address on HTTP."""
    try:
        response = requests.get(f'http://{ip}', timeout=1)
        if response.status_code == 200:
            return f"{ip}\tHTTP Success\t{response.status_code}"
        else:
            return f"{ip}\tHTTP Fail\t{response.status_code}"
    # except requests.ConnectionError:
        # return f"{ip}\tConnection Error"
    # except requests.Timeout:
        # return f"{ip}\tTimeout"
    except requests.RequestException as e:
        return f"{ip}\tError: {str(e)}"

def output_results(futures):
    for future in as_completed(futures):
        print(future.result())

def main():
    input_ip = input("Enter Router IP (e.g., 192.168.1.1) or press Enter for default: ")
    router_ip = input_ip if input_ip.strip() != "" else "192.168.1.1"
    base_ip = router_ip.rsplit('.', 1)[0]
    ips = [f"{base_ip}.{i}" for i in range(1, 255)]

    print("IP Address\tStatus\tDetail")  # Table header
    print("-------------------------------------------")

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for ip in ips:
            futures.append(executor.submit(scan_ip, ip))
            if len(futures) >= 20:
                output_results(futures)
                futures = []

        if futures:
            output_results(futures)

if __name__ == "__main__":
    main()