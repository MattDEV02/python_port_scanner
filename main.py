import socket
from datetime import datetime
from os import system
from pyfiglet import figlet_format
from webbrowser import open as broswer_open


def is_ipv4_address(address="127.0.0.1"):
   address = str(address)
   try:
      socket.inet_pton(socket.AF_INET, address)
      try:
         socket.inet_aton(address)
      except socket.error:
         return False
      return address.count('.') == 3
   except (socket.error, AttributeError, TypeError):
      return False


def port_print(port=1):
   port = int(port)
   print(f"Scanning port: {port}", end='')
   print('\r', end='')


DATE_TIME_FORMAT = str("%d/%m/%Y %H:%M:%S")
FIRST_PORT = 1
LAST_PORT = 65535


def main():
   print(('\n' * 3) + figlet_format("PORT SCANNER"))
   hostname = input("\nInsert an hostname or ip-address: ")
   if hostname is None or len(hostname) == 0 or hostname == "0.0.0.0":
      hostname = "localhost"
   ip = str("")
   try:
      ip = socket.gethostbyname(hostname)
      if is_ipv4_address(hostname):
         hostname = socket.gethostbyaddr(ip)[0]
   except (socket.gaierror, socket.herror, socket.error):
      print(f"\nHostname \"{hostname}\" Could Not Be Resolved !!!")
      exit()
   print('\n' + ("-" * 99))
   print(f"Scanning target: hostname = {hostname} ; ip-address = {ip}")
   start_scanning_date = datetime.now()
   print(f"Scanning started at: {start_scanning_date.strftime(DATE_TIME_FORMAT)}")
   print("-" * 99 + '\n')
   port = opened_ports = int(0)
   try:
      for port in range(FIRST_PORT, LAST_PORT):
         port_print(port)
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         socket.setdefaulttimeout(1)
         if s.connect_ex((ip, port)) == 0:
            port_scanning_date = datetime.now()
            port_scanning_time = port_scanning_date - start_scanning_date
            print(f"{opened_ports + 1} ) Port {ip}:{port} is open ({port_scanning_date.strftime(DATE_TIME_FORMAT)} ==> {str(port_scanning_time).split('.', 1)[0]})")
            opened_ports += 1
            if port == 22:
               system(f"start ssh {ip}")
            elif port == 80:
               broswer_open(f"http://{hostname}/")
            elif port == 443:
               broswer_open(f"https://{hostname}/")
         s.close()
   except KeyboardInterrupt:
      print(('\n' * 2) + "Exiting Program !!!")
   except (socket.gaierror, socket.herror, socket.error):
      print(('\n' * 2) + f"Hostname \"{hostname}\" Could Not Be Resolved !!!")
   finish_scanning_date = datetime.now()
   finish_scanning_time = finish_scanning_date - start_scanning_date
   media_port_secs = round(port / finish_scanning_time.seconds, 5)
   print(f"\nScanning terminated at: {finish_scanning_date.strftime(DATE_TIME_FORMAT)} ; total time: {str(finish_scanning_time).split('.', 1)[0]} ; last port scanned: {port} ; opened ports: {opened_ports} ; {media_port_secs} ports at sec.")


if __name__ == "__main__":
   main()
