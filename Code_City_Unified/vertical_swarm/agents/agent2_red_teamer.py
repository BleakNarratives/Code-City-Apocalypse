import logging

import socket
import threading
from queue import Queue

# A common list of ports to scan
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]

def port_scan(target, port):
    """
    Scans a single port on the target host.
    Returns True if the port is open, False otherwise.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((target, port))
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    except socket.gaierror:
        # Hostname could not be resolved
        return False

def worker(target, port_queue, open_ports):
    """
    The worker function for the thread pool.
    """
    while not port_queue.empty():
        port = port_queue.get()
        if port_scan(target, port):
            open_ports.append(port)
        port_queue.task_done()

def run_recon_scan(target, ports=COMMON_PORTS, num_threads=10):
    """
    Performs a port scan on the target using multiple threads.
    """
    logging.info(f"--- Running reconnaissance scan on {target} ---")
    
    try:
        target_ip = socket.gethostbyname(target)
        logging.info(f"Resolved {target} to {target_ip}")
    except socket.gaierror:
        logging.info(f"Error: Could not resolve hostname '{target}'. Aborting.")
        return

    open_ports = []
    port_queue = Queue()
    for port in ports:
        port_queue.put(port)
        
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(target_ip, port_queue, open_ports))
        thread.start()
        threads.append(thread)
        
    port_queue.join() # Wait for all ports to be processed
    
    # Wait for all threads to complete
    for t in threads:
        t.join()

    if open_ports:
        logging.info("Open ports found:")
        for port in sorted(open_ports):
            logging.info(f"- Port {port} is open")
    else:
        logging.info("No open ports found among the common ports scanned.")
    logging.info("--- Scan complete ---")

if __name__ == '__main__':
    # We'll scan a known, reliable target for demonstration purposes.
    # localhost is a good candidate as it will have some open ports
    # without scanning the public internet.
    target_host = 'localhost'
    run_recon_scan(target_host)

    # Example of scanning a public domain (will only find common web ports)
    # Be aware of the rules and regulations of scanning public domains.
    # This is for educational purposes only.
    # target_host_public = 'scanme.nmap.org'
    # run_recon_scan(target_host_public)
