import asyncio
import datetime
import random
import time
import paramiko

from simple_print import sprint

from database import methods as db_methods


async def check_host_accessibility(host: str, port: int, duration=5, delay=1):
    """
    host : str
        host ip address or hostname
    port : int
        port number
    duration : int, optional
        Total duration in seconds to wait, by default 10
    delay : int, optional
        delay in seconds between each try, by default 2
    """

    date_now = datetime.datetime.now()
    time_now = time.time()
    tmax = time.time() + duration
    while time.time() < tmax:
        try:
            reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=5)
            writer.close()
            await writer.wait_closed()
            response_time = time.time() - time_now
            response_time_ms = (datetime.datetime.now() - date_now).microseconds
            print(response_time_ms)
            if response_time_ms == 0:
                response_time_ms = random.randint(1, 3)
            return True, response_time, response_time_ms
        except:
            if delay:
                await asyncio.sleep(delay)

    response_time = time.time() - time_now
    return False, response_time, 0


async def restore(incoming_data):

    monitor_request_time = datetime.datetime.now().strftime("%H:%M")
    connection_establish, response_time, response_time_ms = await check_host_accessibility(incoming_data["monitor_host"], incoming_data["monitor_port"])

    await db_methods.insert_monitor_activity(incoming_data["monitor_id"], connection_establish, response_time, response_time_ms)
    sprint(f"Monitor {incoming_data['monitor_name']} ID={incoming_data['monitor_id']} HOST={incoming_data['monitor_host']} PORT={incoming_data['monitor_port']}", c="green", s=1, p=1)
    sprint(f"Connection establish={connection_establish} :: response_time={response_time}", c="yellow", s=1, p=1)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="192.168.10.10", username="ubuntu", key_filename="/home/ubuntu/.ssh/mykey.pem")

    stdin, stdout, stderr = ssh.exec_command("lsb_release -a")

    for line in stdout.read().splitlines():
        print(line)

    ssh.close()
