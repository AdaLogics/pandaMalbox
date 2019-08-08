import os
import sys
import time
import subprocess
import argparse
import string
import shutil

# Configs
PANDA_BASE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "panda")
PANDA_x86 = os.path.join(PANDA_BASE, "build", "i386-softmmu", "qemu-system-i386")
IMG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sandbox_base/IE8_win7_disk1.qcow2")

PANDA_flags = [
        "-monitor", "stdio",
        "-show-cursor",
        "-m", "8192",
        "-loadvm", "1",
        IMG_PATH
    ]
TIME_TO_EXECUTE = 20

def log_info(msg):
    print("[+] %s"%(msg))

def log_exit(msg):
    print("[-] %s"%(msg))
    exit(0)

def guest_type(s, p):

    keymap = {
        '-': 'minus',
        '=': 'equal',
        '[': 'bracket_left',
        ']': 'bracket_right',
        ';': 'semicolon',
        '\'': 'apostrophe',
        '\\': 'backslash',
        ',': 'comma',
        '.': 'dot',
        '/': 'slash',
        '*': 'asterisk',
        ' ': 'spc',
        '_': 'shift-minus',
        '+': 'shift-equal',
        '{': 'shift-bracket_left',
        '}': 'shift-bracket_right',
        ':': 'shift-semicolon',
        '"': 'shift-apostrophe',
        '|': 'shift-backslash',
        '<': 'shift-comma',
        '>': 'shift-dot',
        '?': 'shift-slash',
        '\n': 'ret',
    }

    for c in s:
        if c in string.ascii_uppercase:
            key = 'shift-' + c.lower()
        else:
            key = keymap.get(c, c)

        p.stdin.write("sendkey %s\n"%(key))
        time.sleep(.5)

def record_execution(sample, recording_time):
    '''
    
    '''
    log_info("Recording execution %s"%(sample))
    log_info("Recording for %d seconds"%(recording_time))


    # Create new temporary sample
    new_sample = "sample"
    shutil.copy(sample, new_sample)


    # Create an ISO file of the sample file
    cmd = []
    cmd.append("/usr/bin/genisoimage")
    cmd.append("-iso-level")
    cmd.append("4")
    cmd.append("-l")
    cmd.append("-R")
    cmd.append("-J")
    cmd.append("-o")
    cmd.append("sample.iso")
    cmd.append(new_sample)    

    try:
        subprocess.check_call(cmd)
        log_info("Made an iso file for the sample")
    except Exception:
        print(traceback.format_exc())
        print(sys.exc_info()[0])
        log_exit("Could not make any iso file for the sample")

    # Launch PANDA
    cmd = []
    cmd.append(PANDA_x86)
    for flag in PANDA_flags:
        cmd.append(flag)

    panda_stdout_path = "panda.stdout"
    panda_stderr_path = "panda.stderr"
    panda_stdout = open(panda_stdout_path, 'w+')
    panda_stderr = open(panda_stderr_path, 'w+')

    #log_info("Executing command: %s"%(" ".join(cmd)))
    p = subprocess.Popen(cmd,
            stdin = subprocess.PIPE,
            stdout = panda_stdout,
            stderr = panda_stderr)

    p.stdin.write("MARK\n")

    # Check whenever the virtual machine is ready for us to interact with it.
    f_out = open(panda_stdout_path, "r")
    while True:
        content = f_out.read()
        if "MARK" in content:
            log_info("VM started")  
            break
        f_out.seek(0)
        time.sleep(0.5)

    # Sleep for 1 second
    time.sleep(1)

    # Configure QEMU so the sample.iso file is mounted in the cdrom.
    p.stdin.write("change ide1-cd0 sample.iso\n")   

    # Sleep for 3 seconds
    time.sleep(5)

    # Because the cd-rom was mounted, a window in the guest was opened, 
    # close this window now by sending the escape key to the guest.
    p.stdin.write("sendkey esc\n") 
    
    # Write the command in the guest command line interface to 
    # copy the sample in the cd-rom drive onto the guest desktop.
    copy_cmd = " copy D:\\sample C:\\Users\\IEUser\\Desktop\\sample.exe\n"
    guest_type(copy_cmd, p)

    # Sleep for 5 seconds to make sure the guest finished it's tasks. 
    time.sleep(5)

    # Start writing the command that will execute the sample inside
    # the guest machine. Notice that we don't actually execute the command
    # as there is no \n at the end of the line. We do this because we want to
    # start recording the guest execution before the application executes
    start_cmd = "start C:\\Users\\IEUser\\Desktop\\sample.exe"
    guest_type(start_cmd, p)

    # Now begin recording before we launch the above command
    p.stdin.write("begin_record sample\n")
    
    # Now send the final \n that will launch the execution command.
    guest_type("\n", p)     

    log_info("Started recording and executed the sample in the guest machine")


    log_info("Recording for: %d seconds"%(TIME_TO_EXECUTE))
    time.sleep(TIME_TO_EXECUTE)

    # End the record
    p.stdin.write("end_record\n")

    # Exit the VM
    p.stdin.write("q\n")

    log_info("Recording is over, shutting the VM down")
    p.stdin.write("q\n")
    time.sleep(3)

    while True:
        poll = p.poll()
        if poll == None:
            time.sleep(1)
        else:
            log_info("VM is shut down")
            break

    log_info("Finished recording the sample execution")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
            "-sample", 
            help = "The sample to executed",
            required = True)

    parser.add_argument(
            "-time",
            help = "The number of seconds to record an execution",
            type = int,
            default = 25)

    args = parser.parse_args(args = sys.argv[1:])

    record_execution(args.sample, args.time)
