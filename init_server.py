import argparse
import os
import shutil
import time
import uuid

from scripts.create_configs import update_nginx_config, create_xray_config
from scripts.docker_compose import start_docker_compose
from scripts.init_letsencrypt import init_letsencrypt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Setup XRay and Nginx with Let's Encrypt"
    )
    parser.add_argument(
        "--domain",
        required=True,
        help="Domain name for the server",
    )
    parser.add_argument(
        "--email",
        required=True,
        help="Email address for Let's Encrypt",
    )
    args = parser.parse_args()

    try:
        domain = args.domain
        email = args.email
        xray_vmess_clients = [
            {
                "id": str(uuid.uuid4()),
                "level": 0,
            },
            {
                "id": str(uuid.uuid4()),
                "level": 0,
            },
        ]

        os.makedirs("compose-data/nginx/conf.d", exist_ok=True)
        os.makedirs("compose-data/xray/config", exist_ok=True)

        start_docker_compose()
        update_nginx_config(domain)
        create_xray_config(xray_vmess_clients)
        init_letsencrypt(email, domain)
    except Exception as e:
        print(e)
        os.system("docker compose down")
        shutil.rmtree("compose-data")
        exit(1)
