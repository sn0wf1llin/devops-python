import os
import time
import pwd


def timer(func):
    def wrapper(*args, **kwargs):
        print("--- Hello world :) ---")
        start_time = time.time()
        func(*args, **kwargs)
        sec = round(time.time() - start_time, 4)
        print("--- Done in {} seconds ---".format(sec))

    return wrapper


@timer
def get_os_info_say_hello():
    usn = pwd.getpwuid(os.getuid())[0]
    uid = os.getuid()
    pid = os.getpid()
    cwd = os.getcwd()
    unm = os.uname()
    usd = os.times()

    print("Hello {}! \nUID: {} \n".format(usn, uid))
    print("PID: {}\nCurrent directory: {} \n".format(pid, cwd))
    print("Sysinfo: {} {}\n".format(unm, usd))


if __name__ == "__main__":
    get_os_info_say_hello()
