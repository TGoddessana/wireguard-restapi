import subprocess


def start_docker_compose():
    """
    Start docker-compose in detached mode.
    """
    print("### Starting docker-compose ...")
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
