import os, argparse, subprocess, time, re 


parser = argparse.ArgumentParser()
parser.add_argument("--router", required=False)
parser.add_argument("--interface", required=False)

args = parser.parse_args()
router = args.router
router_name = args.interface


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





def get_iw_stats(interface):  
    output = subprocess.check_output(["iw", "dev", interface, "link"], text=True)

    signal = r""
    freq = r""
    channel_width_mhz = r""
    rx_bitrate_mbps = r""
    tx_bitrate_mbps = r""
    return output

#main loop
print(get_iw_stats(get_wifi_interface()))


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
