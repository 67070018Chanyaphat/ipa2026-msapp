from netmiko import ConnectHandler
import os
import ntc_templates


def get_interfaces(ip, username, password):
    os.environ["NET_TEXTFSM"] = os.path.join(
        os.path.dirname(ntc_templates.__file__), "templates"
    )
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
    }
    with ConnectHandler(**device) as conn:
        conn.enable()
        result = conn.send_command("show ip int br", use_textfsm=True)
    return result
