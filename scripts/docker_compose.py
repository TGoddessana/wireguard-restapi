import subprocess
import time


def start_docker_compose():
    """
    Start docker-compose and wait for 10 seconds.
    """
    print("### Starting docker-compose ...")
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    print("### docker-compose started, waiting for 10 seconds ...")
    time.sleep(10)
