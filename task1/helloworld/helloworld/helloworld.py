import os
import time
import pwd


def timer(func):
	def wrapper(*args, **kwargs):
		print("--- Hello world :) ---")
		start_time = time.time()
		func(*args, **kwargs)
		print("--- Done in {} seconds ---".format(round(time.time() - start_time, 4)))

	return wrapper
		
@timer
def get_os_info_say_hello():
	usn = pwd.getpwuid(os.getuid())[0]
	uid = os.getuid()
	pid = os.getpid()
	cwd = os.getcwd()
	unm = os.uname()
	usd = os.times()

	print("Hello {}! \nUID: {} \nPID: {}\nCurrent directory: {} \nSysinfo: {} {}\n".format(usn, uid, pid, cwd, unm, usd))

if __name__ == "__main__":
	get_os_info_say_hello()
