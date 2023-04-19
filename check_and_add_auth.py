import os
from subprocess import check_output
from os import path
from colors import green_print_color, magenta_print_color, reset_print_color, red_print_color, blue_print_color, p_red, \
    p_blue, p_green

ngrok_config_path = path.expanduser("~/.config/ngrok/ngrok.yml")


def write_new_token():
    while True:
        p_blue(
            f"Please paste new auth token key ({magenta_print_color}example: "
            f"2Odk5oa5eTEUVxfURcsdDYE43QD_83yPFkssd3rq8PVxddfYS{blue_print_color}):")
        auth_token = input()

        if len(auth_token) < 20:
            continue
        else:
            try:
                output = check_output(["./ngrok", "config", "add-authtoken", auth_token]).decode('utf-8')
                if 'Authtoken saved to configuration' in output:
                    p_green("Saved new new auth token key")
                    break
            except Exception:
                if isinstance(Exception, KeyboardInterrupt):
                    exit(0)
                p_red(f"Cannot perform: [{magenta_print_color}./ngrok config add-authtoken{red_print_color}] command")
                continue

        break


def read_config(new):
    config = open(ngrok_config_path, 'r')
    lines = config.readlines()

    part = " new " if new else " "
    info = f"Your{part}key: [{magenta_print_color}...{lines[1][-10:-1]}{green_print_color}] in path: [{magenta_print_color}{ngrok_config_path}{reset_print_color}]"

    p_green(info)


def check_token():
    try:
        read_config(new=False)
    except FileNotFoundError:
        p_red(f"Cannot found file by path: [{magenta_print_color}{ngrok_config_path}{red_print_color}]")
        write_new_token()
        read_config(new=True)


if __name__ == "__main__":
    check_token()
