import os, subprocess, time, re, statistics, psutil
import numpy as np

interface = None
gateway = None


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

def get_default_gateway():
    output = subprocess.check_output(["ip", "route"], text=True)

    match = re.search(r"default via (\S+)", output)
    
    if match:
        return match.group(1)
    else:
        return None



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

    return signal_match, freq_match, channel_width_match, rx_bitrate_match, tx_bitrate_match



def get_ping_stats(gateway, test_time):
    output = subprocess.check_output(["ping","-i", "0.5", "-w", str(test_time), gateway], text=True)

    ping_list = re.findall(r"time=(\S+)", output)
    pckt_loss = re.search(r"(\d+)% packet loss", output)

    ping_list = [float(x) for x in ping_list]
    
    ping_avg = statistics.mean(ping_list)
    ping_std = statistics.stdev(ping_list)
    ping_p95 = np.percentile(ping_list, 95)

    return ping_avg, ping_std, ping_p95


def get_cpu_stats(test_time):
    cpu_usage = psutil.cpu_percent(interval=test_time)

    return(cpu_usage)


def run_speed_test():
    pass

def create_dataset_row():
    pass


#main loop
while interface == None or gateway == None:
    interface = get_wifi_interface()
    gateway = get_default_gateway()

while True:
    #measurements concurrent

    #run_speed_test

    #finish measurements

    #add datasetrow & save

    for i in range(5):
        stats = get_iw_stats(interface)

        time.sleep(0.5)


    #calc averages/sum
    #add to dataset
    print()





#USE ip route 

#averages over 5 seconds

#rssi_dbm
#frequency_mhz
    #channel_width_mhz
#rx_bitrate_mbps
#tx_bitrate_mbps
#ping_ms
    #jitter_ms
    #packet_loss_pct
#cpu_usage_pct
#download_mbps
#upload_mbps
