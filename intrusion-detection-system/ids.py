import socket
import struct
import time
import os
from collections import defaultdict

SYN_THRESHOLD = 5
CHECK_INTERVAL = 5
LOG_FILE = "syn_flood_log.txt"

syn_counter = defaultdict(int)

def capture_packets():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    sock.bind(("0.0.0.0", 0))
    while True:
        packet, _ = sock.recvfrom(65565)
        ip_header = packet[:20]
        iph = struct.unpack("!BBHHHBBH4s4s", ip_header)
        protocol = iph[6]

        if protocol == 6:
            tcp_header = packet[20:40]
            tcph = struct.unpack("!HHLLBBHHH", tcp_header)
            syn_flag = (tcph[5] >> 1) & 1
            src_ip = socket.inet_ntoa(iph[8])

            if syn_flag == 1:
                syn_counter[src_ip] += 1

def detect_syn_flood():
    while True:
        time.sleep(CHECK_INTERVAL)

        for ip, count in list(syn_counter.items()):
            if count > SYN_THRESHOLD:
                log_and_block_ip(ip)
                del syn_counter[ip]

def log_and_block_ip(ip):
    with open(LOG_FILE, "a") as log:
        log.write(f"{time.ctime()} - SYN flood DETECTADO do IP {ip}. Bloqueando.\n")

    os.system(f"iptables -A INPUT -s {ip} -j DROP")
    print(f"IP Bloqueado: {ip}")

if __name__ == "__main__":
    from threading import Thread
    Thread(target=capture_packets).start()
    detect_syn_flood()
