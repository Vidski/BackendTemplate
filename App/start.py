import os
import socket
import time
import argparse
from datetime import datetime

"""
This is a workaround python script in order to check if
database port is open, avoiding this way docker-compose
race condition that makes django mysql connection fail.
"""

# Configuration to get arguments by command
parser = argparse.ArgumentParser(description='Check if port is open, avoid\
                                 docker-compose race condition')
parser.add_argument('--waiting-service-name', required=True)
parser.add_argument('--ip', required=True)
parser.add_argument('--port', required=True)
parser.add_argument('--raising-service-name', required=True)
parser.add_argument('--command', required=True)

# Set the arguments
arguments_passed_by_command = parser.parse_args()
waiting_service_name = str(arguments_passed_by_command.waiting_service_name)
port = int(arguments_passed_by_command.port)
ip = str(arguments_passed_by_command.ip)
raising_service_name = str(arguments_passed_by_command.raising_service_name)
command = str(arguments_passed_by_command.command)

# Infinite loop to iterate over the database service dockerized
while True:
    database_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    service_result = database_socket.connect_ex((ip, port))
    if service_result == 0:
        now = datetime.now()
        os.system(f'echo "{now}" [info] The service {waiting_service_name} is now' \
                  f'running and the port is open. Now {raising_service_name} will start!')
        os.system(command)
        break
    now = datetime.now()
    os.system(f'echo "{now}" [info] The port of "{waiting_service_name}" is not'\
                ' open yet. It will be checked again soon!')
    time.sleep(1)
