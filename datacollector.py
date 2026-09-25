import os, subprocess, time, re, statistics, psutil, csv
import numpy as np
from concurrent.futures import ThreadPoolExecutor

MEASUREMENT_TIME = 30 # in seconds
CSV_FILE = "wifi_dataset.csv"
CSV_COLUMNS = [
    "rssi_dbm",
    "frequency_mhz",
    "channel_width_mhz",
    "rx_bitrate_mbps",
    "tx_bitrate_mbps",
    "ping_ms",
    "ping_p95_ms",
    "ping_std",
    "jitter_ms",
    "packet_loss_pct",
    "cpu_usage_pct",
    "download_mbps",
    "upload_mbps"
]



interface = None
gateway = None


#fetches the wifi interface through iw dev (unstable)
def get_wifi_interface():
    output  = subprocess.check_output(["iw", "dev"], text=True)
    
    interfaces  = re.findall(r"Interface (\S+)", output)

    for interface in interfaces:
        try:
            link = subprocess.check_output(["iw", "dev", interface, "link"], text=True)

            if "Connected to" in link:
                return interface
        
        except subprocess.CalledProcessError:
            pass

    return None

#fetches gateway through ip route
def get_default_gateway():
    output = subprocess.check_output(["ip", "route"], text=True)

    match = re.search(r"default via (\S+)", output)
    
    if match:
        return match.group(1)
    else:
        return None


#uses iw dev to parse network details (unstable)
def get_iw_stats(interface):  
    output = subprocess.check_output(["iw", "dev", interface, "link"], text=True)

    signal_pattern = r"signal:\s*(-?\d+)"
    freq_pattern = r"freq:\s*([\d.]+)"
    channel_width_mhz_pattern = r"(\d+)MHz"
    rx_bitrate_mbps_pattern = r"rx bitrate:\s*([\d.]+)"
    tx_bitrate_mbps_pattern = r"tx bitrate:\s*([\d.]+)"

    signal_match = re.search(signal_pattern, output)
    freq_match = re.search(freq_pattern, output)
    channel_width_match = re.search(channel_width_mhz_pattern, output)
    rx_bitrate_match = re.search(rx_bitrate_mbps_pattern, output)
    tx_bitrate_match = re.search(tx_bitrate_mbps_pattern, output)

    return {
        "rssi_dbm": float(signal_match.group(1)),
        "frequency_mhz": float(freq_match.group(1)),
        "channel_width_mhz": float(channel_width_match.group(1)),
        "rx_bitrate_mbps": float(rx_bitrate_match.group(1)),
        "tx_bitrate_mbps": float(tx_bitrate_match.group(1))
    }

#gets ping statistics and parses
def get_ping_stats(gateway, test_time):
    output = subprocess.check_output(["ping","-i", "0.5", "-w", str(test_time), gateway], text=True)

    ping_list = re.findall(r"time=(\S+)", output)
    pckt_loss = re.search(r"(\d+)% packet loss", output)

    ping_list = [float(x) for x in ping_list]
    
    ping_avg = statistics.mean(ping_list)
    ping_std = statistics.stdev(ping_list)
    ping_p95 = float(np.percentile(ping_list, 95))
    
    packet_loss_pct = float(pckt_loss.group(1))

    differences = []
    for i in range(1, len(ping_list)):
        differences.append(abs(ping_list[i] - ping_list[i - 1]))
    jitter_ms = statistics.mean(differences)


    return {
       "ping_ms": ping_avg,
        "ping_std": ping_std,
       "ping_p95_ms": ping_p95,
        "jitter_ms": jitter_ms,
       "packet_loss_pct": packet_loss_pct
    } 

#uses psutil to access cpu usage %
def get_cpu_stats(test_time):
    cpu_usage = psutil.cpu_percent(interval=test_time)
    return(cpu_usage)

#enables timing of get_iw_stats
def collect_wifi_samples(interface, duration):
    samples = []

    start = time.time()

    while time.time() - start < duration:
        sample = get_iw_stats(interface)
        samples.append(sample)

        time.sleep(0.5)
    return samples



def run_speed_test():
    output = subprocess.check_output(["speedtest"], text=True)

    download_pattern = r"Download: (\S+)"
    upload_pattern = r"Upload: (\S+)"

    download_mbps = re.search(download_pattern, output)
    upload_mbps = re.search(upload_pattern, output)

    return {
        "download_mbps": float(download_mbps.group(1)),
        "upload_mbps": float(upload_mbps.group(1))
    }

def save_row(row):
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

#main loop

interface = get_wifi_interface()
gateway = get_default_gateway()

if interface is None:
    raise RuntimeError("No WiFi interface found")
if gateway is None:
    raise RuntimeError("No default gateway found")


while True:


    with ThreadPoolExecutor(max_workers=4) as executor:
        wifi_future = executor.submit(collect_wifi_samples, interface, MEASUREMENT_TIME)
        
        ping_future = executor.submit(get_ping_stats, gateway, MEASUREMENT_TIME)

        cpu_future = executor.submit(get_cpu_stats, MEASUREMENT_TIME)
        
        speed_future = executor.submit(run_speed_test)
        
        

        wifi_samples = wifi_future.result()
        ping_stats = ping_future.result()
        cpu_usage = cpu_future.result()
        speed_stats = speed_future.result()


        #aggregate samples
        
        rssi_avg = statistics.mean(sample["rssi_dbm"] for sample in wifi_samples)
        frequency_avg = statistics.mean(sample["frequency_mhz"] for sample in wifi_samples)
        channel_width_avg = statistics.mean(sample["channel_width_mhz"] for sample in wifi_samples)
        rx_bitrate_avg = statistics.mean(sample["rx_bitrate_mbps"] for sample in wifi_samples)
        tx_bitrate_avg = statistics.mean(sample["tx_bitrate_mbps"] for sample in wifi_samples)



        row = {
            "rssi_dbm": rssi_avg,
            "frequency_mhz": frequency_avg,
            "channel_width_mhz": channel_width_avg,
            "rx_bitrate_mbps": rx_bitrate_avg,
            "tx_bitrate_mbps": tx_bitrate_avg,

            "ping_ms": ping_stats["ping_ms"],
            "ping_p95_ms": ping_stats["ping_p95_ms"],
            "ping_std": ping_stats["ping_std"],
            "jitter_ms": ping_stats["jitter_ms"],
            "packet_loss_pct": ping_stats["packet_loss_pct"],

            "cpu_usage_pct": cpu_usage,

            "download_mbps": speed_stats["download_mbps"],
            "upload_mbps": speed_stats["upload_mbps"]
        }

        save_row(row)
