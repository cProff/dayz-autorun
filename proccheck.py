import subprocess
CREATE_NO_WINDOW = 0x08000000


def process_exists(process_name):
    # use buildin check_output right away
    output = subprocess.run(
        'TASKLIST /FI "IMAGENAME eq %s"' % process_name,
        stdout=subprocess.PIPE, stdin=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        creationflags=CREATE_NO_WINDOW)
    # check in last line for process name
    last_line = output.stdout.decode("cp1251").strip().split('\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())


if __name__ == "__main__":
    print(process_exists('ModernWarfare.exe'))
