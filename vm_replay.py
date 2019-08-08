import os
import sys
import subprocess
import argparse
import time

# Configs
PANDA_BASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "panda")
PANDA_x86 = os.path.join(PANDA_BASE, "build", "i386-softmmu", "qemu-system-i386")
IMG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sandbox_base/IE8_win7_disk1.qcow2")

PANDA_flags = [
        "-monitor", "stdio",
        "-show-cursor",
        "-m", "8192",
    ]

# The PADNA plugins we would like to use
PANDA_plugins = [
        "-panda osi -os windows-32-7 -panda win7x86intro -panda osi_test"
    ]

def log_info(msg):
    print("[+] %s"%(msg))

def log_exit(msg):
    print("[-] %s"%(msg))
    exit(0)

def replay_recording(snapshot_name):
    '''
    Replays a recording
    '''
    
    log_info("Replaying %s"%(snapshot_name))

    # Launch PANDA
    cmd = []
    cmd.append(PANDA_x86)
    cmd.append("-replay")
    cmd.append(snapshot_name)
    
    for flag in PANDA_flags:
        cmd.append(flag)

    for plugin_cmdline in PANDA_plugins:
        cmd.append(plugin_cmdline)

    # Output files
    panda_stdout_path = "replay_panda.stdout"
    panda_stderr_path = "replay_panda.stderr"
    panda_stdout = open(panda_stdout_path, 'w+')
    panda_stderr = open(panda_stderr_path, 'w+')

    log_info("Launching replay %s"%(" ".join(cmd)))
    try:
        p = subprocess.Popen(
                " ".join(cmd),
                shell=True,
                stdout = panda_stdout,
                stderr = panda_stderr,
                preexec_fn = os.setsid)
    except:
        log_exit("Could not complete replay")

    log_info("Replay launched")

    while True:
        poll = p.poll()
        if poll == None:
            time.sleep(1)
        else:
            log_info("Replaying finished")
            break

    log_info("Analysis process finished, exiting")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
            "-recording", 
            help = "The name of the snapshot to replay",
            required = True)

    args = parser.parse_args(args = sys.argv[1:])
    replay_recording(args.recording)
