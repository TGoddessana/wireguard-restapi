import subprocess
import os
import sys


def init_letsencrypt(
    email,
    domain,
    rsa_key_size=4096,
    staging=1,  # 0 for production, 1 for staging
):
    domain = domain
    rsa_key_size = rsa_key_size
    data_path = "./compose-data/certbot"
    email = email
    staging = staging

    if os.path.isdir(data_path):
        decision = input(
            f"Existing data found for {domain}. Continue and replace existing certificate? (y/N) "
        )
        if decision.lower() != "y":
            sys.exit(0)

    if not os.path.exists(
        f"{data_path}/conf/options-ssl-nginx.conf"
    ) or not os.path.exists(f"{data_path}/conf/ssl-dhparams.pem"):
        print("### Downloading recommended TLS parameters ...")
        os.makedirs(f"{data_path}/conf", exist_ok=True)
        subprocess.run(
            [
                "curl",
                "-s",
                "https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf",
                "-o",
                f"{data_path}/conf/options-ssl-nginx.conf",
            ],
            check=True,
        )
        subprocess.run(
            [
                "curl",
                "-s",
                "https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem",
                "-o",
                f"{data_path}/conf/ssl-dhparams.pem",
            ],
            check=True,
        )
        print()

    print(f"### Creating dummy certificate for {domain} ...")
    path = f"/etc/letsencrypt/live/{domain}"
    os.makedirs(f"{data_path}/conf/live/{domain}", exist_ok=True)
    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "--entrypoint",
            f"openssl req -x509 -nodes -newkey rsa:{rsa_key_size} -days 1 -keyout '{path}/privkey.pem' -out '{path}/fullchain.pem' -subj '/CN=localhost'",
            "certbot",
        ],
        check=True,
    )
    print()

    print("### Starting nginx ...")
    subprocess.run(
        ["docker", "compose", "up", "--force-recreate", "-d", "nginx"], check=True
    )
    print()

    print(f"### Deleting dummy certificate for {domain} ...")
    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "--entrypoint",
            f"rm -Rf /etc/letsencrypt/live/{domain} && rm -Rf /etc/letsencrypt/archive/{domain} && rm -Rf /etc/letsencrypt/renewal/{domain}.conf",
            "certbot",
        ],
        check=True,
    )
    print()

    print(f"### Requesting Let's Encrypt certificate for {domain} ...")
    domain_args = " ".join([f"-d {d}" for d in [domain]])
    email_arg = f"--email {email}" if email else "--register-unsafely-without-email"
    staging_arg = "--staging" if staging != 0 else ""

    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            "--entrypoint",
            f"certbot certonly --webroot -w /var/www/certbot {staging_arg} {email_arg} {domain_args} --rsa-key-size {rsa_key_size} --agree-tos --force-renewal",
            "certbot",
        ],
        check=True,
    )
    print()

    print("### Reloading nginx ...")
    subprocess.run(
        ["docker", "compose", "exec", "nginx", "nginx", "-s", "reload"], check=True
    )
