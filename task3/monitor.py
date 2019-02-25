import psutil
import datetime
import time
import os
import json
import yaml
import sys


class Monitor:
    def __init__(self, config_file=None, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.name = "Python System Monitor v0.1"
        self._pname = "pysysmon"
        self.interval = None
        self.output = None
        self.output_file = f"/tmp/{self._pname}"
        self.snapshot_counter = 0
        self.snapshot_format = "SNAPSHOT {}: TIMESTAMP: {} {}\n"
        self._read_config(config_file)
        # 0 - stopped; 1 - working
        self._monitor_status = 0
        self._process_id = None
        self._pidfile = f"/run/{self._pname}.pid"
        self._stderr = stderr
        self._stdout = stdout
        self._stdin = stdin

    def _read_config(self, config_file):
        if config_file is not None:
            try:
                with open(config_file, 'r') as infile:
                    mon_cfg = yaml.safe_load(infile)

                    self.interval = mon_cfg['pysysmon_info']['interval']
                    self.output = mon_cfg['pysysmon_info']['output']

                    if self.interval is None:
                        raise Exception(f"{self.name} cant be created with "
                                        f"time interval == <{self.interval}>")

            except Exception as e:
                print(e)
                print(f"Cant read {config_file}")
                exit()

    def status(self):
        x = 'stopped'
        if os.path.isfile(self._pidfile):
            print(f"PID file {self._pidfile} exists;")
            x = 'unknown'

        print(f"{self.name} is "
              f"{'working' if self._monitor_status == 1 else x}")

        return self._monitor_status

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        if self._monitor_status == 0:
            # check if process has been already started
            maybe_pid = self._get_pid_from_pidfile()
            if maybe_pid is not None:
                print(f"{self.name} is running now with PID {maybe_pid}."
                      f"\nIt will be killed and new one will be started.")
                self.stop()

            try:
                pid = os.fork()
                if pid > 0:
                    # exit first parent
                    sys.exit(0)

            except OSError as e:
                sys.stderr.write(f"fork #1 failed: {e.errno} {e.strerror}\n")
                exit(1)

            # decouple from parent environment
            os.chdir("/")
            os.setsid()
            os.umask(0)

            self._process_id = os.getpid()
            print(f"{self.name} started with PID {self._process_id}")

            # # redirect standard file descriptors
            # sys.stdout.flush()
            # sys.stderr.flush()
            # si = file(self._stdin, 'r')
            # so = file(self._stdout, 'a+')
            # se = file(self._stderr, 'a+', 0)
            # os.dup2(si.fileno(), sys.stdin.fileno())
            # os.dup2(so.fileno(), sys.stdout.fileno())
            # os.dup2(se.fileno(), sys.stderr.fileno())

            try:
                # write pidfile
                with open(self._pidfile, "w") as f:
                    f.write(str(self._process_id) + "\n")

                print(f"{self._process_id} written to {self._pidfile} [ OK ]."
                      f" {self.name} started.")

                self._monitor_status = 1

                while 1:
                    self._make_snapshot()
                    time.sleep(self.interval * 60)

            except Exception as e:
                print(f"{self._process_id} can't be written "
                      f"to {self._pidfile} [ FAILED ]")
                print(e)
                exit()

        else:
            pid = self._get_pid_from_pidfile()
            print(f"{self.name} has been already started with PID {pid}")

    def stop(self):
        pid = self._get_pid_from_pidfile()

        if pid is not None:
            curr_process = psutil.Process(pid)
            curr_process_name = curr_process.name()
            print(f"Killing process {curr_process_name} with PID {pid} ... ")
            try:
                curr_process.terminate()
                self._del_pidfile()
                self._monitor_status = 0
                print(" ... [ OK ]")
            except Exception as e:
                print(e)

        else:
            print(f"{self.name} has not already been started.")

    def _get_pid_from_pidfile(self):
        try:
            # read pidfile
            with open(self._pidfile, "r") as f:
                pid = int(f.readline().strip())
                return pid
        except Exception as e:
            print(e)
            return None

    def _del_pidfile(self):
        os.remove(self._pidfile)

    def _make_snapshot(self):
        sinfo = self._collect_system_info()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.snapshot_counter += 1

        if self.output == 'txt':
            # write to txt file
            delim = "\n\t\t\t"
            net_info_string = "".join(f"{delim}\t{k} {v[0].address}" for k, v
                                      in sinfo['net_info'].items())
            system_info_string = f"System data: {sinfo['system_data']};{delim}" \
                f"CPU load: {sinfo['cpu_load']};{delim}" \
                f"Memory usage: {sinfo['memory_usage']};{delim}" \
                f"Virtual memory usage: {sinfo['virtual_memory_usage']};{delim}" \
                f"IO information: {sinfo['io_info']};{delim}" \
                f"Network information: {net_info_string};{delim}"

            data2write = self.snapshot_format.format(
                self.snapshot_counter, current_time, system_info_string)

            self._write_to_txt(data2write)

        elif self.output == 'json':
            # write to json file
            self._write_to_json({
                "snapshot": f"SNAPSHOT {self.snapshot_counter}",
                "current_time": current_time,
                **sinfo,
            })

        else:
            pass

    def _write_to_json(self, data_to_write, write_to_file=None):
        if write_to_file is None:
            write_to_file = self.output_file + f".{self.output}"

        with open(write_to_file, 'a+') as outfile:
            json.dump(data_to_write, outfile)

    def _write_to_txt(self, data_to_write, write_to_file=None):
        if write_to_file is None:
            write_to_file = self.output_file + f".{self.output}"

        with open(write_to_file, 'a+') as outfile:
            outfile.write(data_to_write)

    @staticmethod
    def _collect_system_info():
        sd = os.uname()
        system_data = f"{sd.sysname} {sd.release} {sd.machine}"
        cpu_load = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().used / 1024 / 1024
        virt_memory_usage = psutil.virtual_memory().percent

        io_info = psutil.disk_io_counters()
        io_info = f"Read count: {io_info.read_count}; " \
            f"Write count: {io_info.write_count};" \
            f"Read data: {io_info.read_bytes / 1024 / 1024} MB;" \
            f"Write data: {io_info.write_bytes / 1024 / 1024} MB"

        net_info = psutil.net_if_addrs()

        return {
            "system_data": system_data,
            "cpu_load": cpu_load,
            "memory_usage": memory_usage,
            "virtual_memory_usage": virt_memory_usage,
            "io_info": io_info,
            "net_info": net_info,
        }

    def __repr__(self):
        return self.name + f"\n\tRepeat every <{self.interval}> " \
            f"minutes;\n\tWrite to <{self.output}>"

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'stop':
            monitor = Monitor()
            monitor.stop()
        elif sys.argv[1] == 'status':
            monitor = Monitor()
            monitor.status()
        elif sys.argv[1] == 'restart':
            monitor = Monitor()
            monitor.restart()
        elif sys.argv[1] == 'start':
            print("Python System Monitor v0.1\n"
                  "usage: start config.yaml|stop|restart|status")
        else:
            print(f"Unknown command <{sys.argv[1]}>")
            exit()

    elif len(sys.argv) == 3:
        if sys.argv[1] == 'start':
            monitor = Monitor(sys.argv[2])
            monitor.start()
        else:
            print(f"Unknown command <{sys.argv[1]}>")
            exit()
    else:
        print("Python System Monitor v0.1\n"
              "usage: start config.yaml|stop|restart|status")

    # parser = argparse.ArgumentParser(
    #     description="Python System Monitor v0.1 "
    #                 "usage: start|stop|restart|status")
    # parser.add_argument("--config", "-c", type=str, required=False,
    #                     dest="config",
    #                     help="Path to the config.yaml file")
    # parser.add_argument("start", type=str, help="Starts the monitor",
    #                     const='start', dest='mode')
    # parser.add_argument("stop", type=str, help="Stops the monitor",
    #                     const='stop', dest='mode')
    # parser.add_argument("status", type=str, help="Get the monitor status",
    #                     const='status', dest='mode')
    # parser.add_argument("restart", type=str, const='restart',
    #                     dest='mode',
    #                     help="Restarts the monitor "
    #                          "if it has already been started")
    #
    # args = parser.parse_args()
    # if not args.mode:
    #     parser.error("usage: start|stop|restart|status")
    #
    # if args.mode == "start":
    #     monitor = Monitor(args.config)
    #     monitor.start()
    #
    # elif args.mode == "status":
    #     monitor = Monitor()
    #     monitor.status()
    #
    # elif args.mode == "stop":
    #
    #
    # elif args.mode == "restart":
    #     monitor = Monitor()
    #     monitor.restart()
