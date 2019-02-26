import json
import yaml
import sys
import os
import subprocess
import distutils.sysconfig


def report(data_to_write, rname, rformat):
    if rformat in 'json':
        dump_func = json.dump
    elif rformat == 'yaml':
        dump_func = yaml.dump
    else:
        raise Exception("Only <json> & <yaml> formats supported.")

    data_to_write["current_piplist"] = {
        i[0]: i[1]
        for i in [i.split()
                  for i in data_to_write["current_piplist"][2:]]}

    for k, v in data_to_write.items():
        if type(v) is str:
            print(v.split('\n'))
        else:
            print(k, v)

    with open(f"{rname}.{rformat}", 'w') as outfile:
        dump_func(data_to_write, outfile)


def main():
    pyversion = sys.version_info[0]
    pyalias = subprocess.check_output("which python", shell=True)
    pyall = subprocess.check_output("which python -a", shell=True)
    pyexec = sys.executable
    pypip = subprocess.check_output("which pip", shell=True)
    pypipall = subprocess.check_output("which pip -a", shell=True)
    pythonpath = os.getenv("PYTHONPATH")
    pypiplist = subprocess.check_output("pip list", shell=True)
    site_packages = distutils.sysconfig.get_python_lib()

    pydata = {
        "current_version": pyversion,
        "current_alias": pyalias,
        "all_pythons": pyall,
        "current_executable": pyexec,
        "all_pips": pypipall,
        "current_pip": pypip,
        "pythonpath": pythonpath or "[ WARN ] Not set",
        "current_piplist": pypiplist,
        "current_site_packages": site_packages

    }

    pydata = {k: ([i for i in v if len(i) != 0] if type(v) is list else v)
              for k, v in {k: (v.split('\n') if type(v) is str else v)
                           for k, v in {
                               k: (v.decode('utf-8')
                                   if type(v) is bytes else v)
                               for k, v in pydata.items()}.items()}.items()}

    report(pydata, rname="report#1", rformat="json")


if __name__ == "__main__":
    main()
