import subprocess
from colors import green_print_color, magenta_print_color, reset_print_color, red_print_color, blue_print_color, p_red, \
    p_blue, p_green
import signal
import sys


def show_ports_with_node_app():
    while True:
        try:
            output = subprocess.check_output(['lsof', '-i', '-P', '-n'], universal_newlines=True)
            output = subprocess.check_output(['grep', 'LISTEN'], input=output, universal_newlines=True)
            user_input = input(
                f"{blue_print_color}Port for what app do you want attach? For example: java, node ({magenta_print_color}by "
                f"default: Node{blue_print_color}): {reset_print_color}")\
                .lower()

            it_is_empty_input = user_input == ''
            it_is_custom_app = user_input != '' and 1 < len(user_input) < 50

            if it_is_empty_input:
                output = subprocess.check_output(['grep', 'node'], input=output, universal_newlines=True)
            if it_is_custom_app:
                output = subprocess.check_output(['grep', user_input], input=output, universal_newlines=True)
            output = subprocess.check_output(['awk', '{print $1, $9}'], input=output, universal_newlines=True)
            output = subprocess.check_output(['awk', '-F', ':', '{print $2}'], input=output, universal_newlines=True)

            ports = list(filter(lambda port: len(port), output.split('\n')))

            string_part = f" which executing via {magenta_print_color}Node.js{blue_print_color}" \
                if it_is_empty_input \
                else f" which executing via {magenta_print_color}{user_input.capitalize()}{blue_print_color}" \
                if it_is_custom_app \
                else ""

            p_blue(f"All Listening ports{string_part}:")
            p_green(list(map(int, ports)))
            return ports
        except Exception:
            if isinstance(Exception, KeyboardInterrupt):
                exit(0)
            p_red('Something wrong. Try again')
            continue


def examine_port_from_user_input(ports: list):
    while True:
        port = input(f"{blue_print_color}Write preferred port from list: {reset_print_color}")

        if port not in ports:
            p_red("Not in the list!")
            print(f"{blue_print_color}Available ports: {green_print_color}{list(map(int, ports))}{reset_print_color}")
            continue
        break
    return port


def signal_handler(process):
    # bound process
    def handler(sig, frame):
        print(f'{blue_print_color}Subprocess terminating')
        process.kill()
        print(f'{green_print_color}Subprocess terminated')
        sys.exit(0)

    return handler


def start_ng_server():
    ports = show_ports_with_node_app()
    port = examine_port_from_user_input(ports)

    process = subprocess.Popen([f"./ngrok http {port}"], shell=True, stdin=subprocess.PIPE)

    signal.signal(signal.SIGINT, signal_handler(process))

    process.wait()


if __name__ == "__main__":
    start_ng_server()
