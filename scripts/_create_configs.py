import subprocess

from jinja2 import Environment, FileSystemLoader


def update_nginx_config(domain):
    """
    Update the Nginx configuration file with the domain name.

    see: ./compose-data/nginx/conf.d/default.conf
    """
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("templates/nginx.conf.j2")

    nginx_config = template.render(domain=domain)

    with open("compose-data/nginx/conf.d/default.conf", "w") as f:
        f.write(nginx_config)

    subprocess.run(["docker", "compose", "restart", "nginx"], check=True)


def create_xray_config():
    """
    Create the XRay configuration file with the Vmess clients.

    see: ./compose-data/xray/config/config.json
    """
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("templates/config.json.j2")

    xray_config = template.render()

    with open("compose-data/xray/config/config.json", "w") as f:
        f.write(xray_config)
