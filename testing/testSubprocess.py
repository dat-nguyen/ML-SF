import subprocess, os

#HOST_LIST   = ['athena', 'artemis', 'aphrodite', 'poseidon', 'hades']
SSH_CMD     = "ssh -t -X "

#################################################################

hosts = ['ares', 'eos', 'eros']
command = [" /home/dat/WORK/glidedock_v2013-refined_1.sh",
           " /home/dat/WORK/glidedock_v2013-refined_2.sh",
           " /home/dat/WORK/glidedock_v2013-refined_3.sh"]
processes = set()
max_processes = 2*len(hosts)

#p1 = subprocess.Popen(ssh + hosts[0] + command[0], shell=True)
#p2 = subprocess.Popen(ssh + hosts[1] + command[1], shell=True)
#p3 = subprocess.Popen(ssh + hosts[2] + command[2], shell=True)
#for proc in [p1, p2, p3]:
#    time.sleep(60)
#    status = proc.poll()
#    if status == None:
#        continue
#    else:
#        print("command failed with status", status)

for name in range(0, len(hosts)):
    processes.add(subprocess.Popen(SSH_CMD + hosts[name] + command[name], shell=True))
    if len(processes) >= max_processes:
        os.wait()
        processes.difference_update(
            [p for p in processes if p.poll() is not None])

##Check if all the child processes were closed
for p in processes:
    if p.poll() is None:
        p.wait()