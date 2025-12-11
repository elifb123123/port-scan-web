from flask import Flask, request, render_template
import socket
from concurrent.futures import ThreadPoolExecutor




# Tek port kontrol
def check_single_port(ip, port):
    s = socket.socket()
    s.settimeout(0.2)
    try:
        s.connect((ip, port))
        return port
    except:
        return None
    finally:
        s.close()

# Çoklu port kontrol (multi-thread)
def check_ports(ip, port_str):
    port_str = str(port_str).strip()

    #cache_key = (ip, port_str)
    #if cache_key in port_cache:
     #   return port_cache[cache_key]

    if port_str.lower() == "all":
        ports = [80, 443, 25, 110, 143, 3389, 22, 21]  # yaygın portlar
    elif "-" in port_str:
        try:
            start, end = map(int, port_str.split("-"))
            ports = list(range(start, min(end + 1, start + 50)))
        except:
            return "Geçersiz"
    elif "," in port_str:
        try:
            ports = [int(p.strip()) for p in port_str.split(",")[:10]]
        except:
            return "Geçersiz"
    else:
        try:
            ports = [int(port_str)]
        except:
            return "Geçersiz"

    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda p: check_single_port(ip, p), ports)
        open_ports = [str(p) for p in results if p]

    result_str = ", ".join(open_ports) if open_ports else "Kapalı"
    #port_cache[cache_key] = result_str
    return result_str



