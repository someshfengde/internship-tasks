import time
import paramiko


from paramiko import SSHClient

# Connect
client = SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('172.31.254.217', username='root', password='openwifi')
list1=['ls -s /tmp', 'cd /tmp' , 'wget https://ucentral-ap-firmware.s3.amazonaws.com/20220202-indio_um-305ac-v2.4.1-6d9d4ab-upgrade.bin']
for i in list1:

    # Run a command (execute PHP interpreter)
    stdin, stdout, stderr = client.exec_command(i,timeout=None)
    #time.sleep(5)
    #print(type(stdin))  # <class 'paramiko.channel.ChannelStdinFile'>
    #print(type(stdout))  # <class 'paramiko.channel.ChannelFile'>
    #print(type(stderr))  # <class 'paramiko.channel.ChannelStderrFile'>

    # Optionally, send data via STDIN, and shutdown when done
    #stdin.write('echo "Hello!" > testfile.log;')
    #stdin.channel.shutdown_write()

    # Print output of command. Will wait for command to finish.
    print(f'STDOUT: {stdout.read().decode("utf8")}')
    print(f'STDERR: {stderr.read().decode("utf8")}')

    # Get return code from command (0 is default for success)
    a=stdout.channel.recv_exit_status()

    if a==0:
        print(f'command successful {i}')
    else:
        print('command not successful')
    if i=='wget https://ucentral-ap-firmware.s3.amazonaws.com/20220202-indio_um-305ac-v2.4.1-6d9d4ab-upgrade.bin':
        time.sleep(5)
    else:
        time.sleep(2)
    # Because they are file objects, they need to be closed
    stdin.close()
    stdout.close()
    stderr.close()
    #time.sleep(120)
   #if i=='wget https://ucentral-ap-firmware.s3.amazonaws.com/20220202-indio_um-305ac-v2.4.1-6d9d4ab-upgrade.bin':
    #print('downloading completed')
    #else:
        #continue


time.sleep(60)# Close the client itself
client.close()