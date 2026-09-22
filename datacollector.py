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

    output = r""


    return output


def get_values(output, name):
    #pattern = 
    match = re.search(pattern, output)

    if match:
        return int(match.group(1))
    return None

print(get_wifi_stats("wlp2s0"))




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
