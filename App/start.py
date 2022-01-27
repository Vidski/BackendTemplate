import os
import socket
import time
import argparse
from datetime import datetime

"""
This is a workaround python script in order to check if
database port is open, avoiding this way docker-compose
race condition that makes django mysql connection fail.

It can be run passing one of these services : Django-app
Celery-Worker or Celery-Beat. Or you can pass custom services
calling it as:

python3 start.py --waiting-service-name database --ip database
--port 3306 --raising-service-name Django-App
--command 'python3 manage.py runserver 0.0.0.0:8000'
"""

def get_command(service):
    if service == 'Django-App':
        command = 'python3 manage.py runserver 0.0.0.0:8000'
    elif service == 'Celery-Worker':
        command = 'celery --app=Worker.worker.app worker --concurrency=1 --hostname=worker@%h --loglevel=INFO'
    elif service == 'Celery-Beat':
        command = 'python3 -m celery --app=Worker.worker.app beat -l debug -f /var/log/App-celery-beat.log --pidfile=/tmp/celery-beat.pid'
    return command

# Configuration to get arguments by command
parser = argparse.ArgumentParser(description='Check if port is open, avoid\
                                 docker-compose race condition')
parser.add_argument('--service', required=False)
parser.add_argument('--waiting-service-name', required=False)
parser.add_argument('--ip', required=False)
parser.add_argument('--port', required=False)
parser.add_argument('--raising-service-name', required=False)
parser.add_argument('--command', required=False)

# Set the arguments
arguments_passed_by_command = parser.parse_args()
service = str(arguments_passed_by_command.service)

if service:
    raising_service_name = service
    waiting_service_name = 'database'
    ip = waiting_service_name
    port = 3306
    command = get_command(service)
else:
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
