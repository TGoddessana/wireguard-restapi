import subprocess


def start_docker_compose():
    """
    Start docker-compose in detached mode.
    """
    print("### Starting docker-compose ...")
    subprocess.run(["docker", "compose", "up", "-d"], check=True)


def clean_docker_images():
    """
    Clean up all the docker images.
    """
    print("### Cleaning up docker images ...")
    subprocess.run(["docker", "system", "prune", "-a", "--volumes"], check=True)
