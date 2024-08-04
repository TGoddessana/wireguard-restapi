import argparse
import os
import shutil

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
    parser.add_argument(
        "--letsencrypt-staging",
        required=False,
        type=int,
        default=1,
        help="Staging environment for Let's Encrypt, 1 for staging, 0 for production",
    )
    args = parser.parse_args()

    try:
        domain = args.domain
        email = args.email
        staging = args.letsencrypt_staging
        xray_vmess_clients = []

        os.makedirs("compose-data/nginx/conf.d", exist_ok=True)
        os.makedirs("compose-data/xray/config", exist_ok=True)

        start_docker_compose()
        update_nginx_config(domain=domain)
        create_xray_config(xray_vmess_clients=xray_vmess_clients)
        init_letsencrypt(email=email, domain=domain, staging=staging)
    except Exception as e:
        print(f"Error: {e}")
        print("### Shutting down docker-compose ...")
        os.system("docker system prune -a --volumes")
        shutil.rmtree("compose-data")
        exit(1)
