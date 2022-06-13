import os, threading, sys, ctypes, random, string, math, requests, json, numpy
from rich import print
from rich.console import Console
from os import system
from time import sleep
from datetime import datetime
c = Console()
system('mode con: cols=100 lines=45')
system(command='cls' if os.name == 'nt' else 'clear')
banner = """[red]
 ▄▄▄       ███▄    █  ▄▄▄       ██▀███   ▄████▄   ██░ ██▓██   ██▓
▒████▄     ██ ▀█   █ ▒████▄    ▓██ ▒ ██▒▒██▀ ▀█  ▓██░ ██▒▒██  ██▒
▒██  ▀█▄  ▓██  ▀█ ██▒▒██  ▀█▄  ▓██ ░▄█ ▒▒▓█    ▄ ▒██▀▀██░ ▒██ ██░
░██▄▄▄▄██ ▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██▀▀█▄  ▒▓▓▄ ▄██▒░▓█ ░██  ░ ▐██▓░
 ▓█   ▓██▒▒██░   ▓██░ ▓█   ▓██▒░██▓ ▒██▒▒ ▓███▀ ░░▓█▒░██▓ ░ ██▒▓░
 ▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ░▒ ▒  ░ ▒ ░░▒░▒  ██▒▒▒
  ▒   ▒▒ ░░ ░░   ░ ▒░  ▒   ▒▒ ░  ░▒ ░ ▒░  ░  ▒    ▒ ░▒░ ░▓██ ░▒░
  ░   ▒      ░   ░ ░   ░   ▒     ░░   ░ ░         ░  ░░ ░▒ ▒ ░░
      ░  ░         ░       ░  ░   ░     ░ ░       ░  ░  ░░ ░
                                        ░                ░ ░[/red]
"""
c.print(banner, justify="center")


class Settings:
    try: # loading settings from config.json
        ctypes.windll.kernel32.SetConsoleTitleW("Anarchy wallet cracker | Loading")
        with open('config.json') as f:
            data = json.load(f)
        wallet_address = data['wallet address']
        if str(wallet_address).startswith('1') or str(wallet_address).startswith('3') or str(wallet_address).startswith('bc1q') or str(wallet_address).startswith('bc1p'): # check if address is valid
            resp = requests.get(f"https://www.blockchain.com/btc/address/{wallet_address}")
            if resp.status_code == 200:
                print(F"[+][green] Loaded wallet address: {wallet_address}[/green]")
            elif resp.status_code == 404:
                print(F"[-][red] Wallet address is invalid - {wallet_address}.")
                input("Press enter to exit.")
                sys.exit(1)
            else:
                print(f"[-][red] Failed to check wallet validity. Error code: {resp.status_code}[/red]")
                input("Press enter to exit.")
                sys.exit(1)
        else:
            print(F"[-][red] Wallet address is invalid - {wallet_address}.")
            input("Press enter to exit.")
            sys.exit(1)
        currency = data['currency']
        if str(currency).upper() == 'USD' or str(currency).upper() == 'GBP' or str(currency).upper() == 'EUR':
            print(f"[+][green] Loaded currency: {currency}[/green]")
        else:
            print(F"[-][red] Currency is invalid - {currency}.\nCurrently only euros (eur), dollars (usd) and pounds (gbp) are supported.")
            input("Press enter to exit.")
            sys.exit(1)
        logging = bool(data['logging'])
        print(f"[+][green] Loaded logging: {logging}[/green]")
        print(f"[+][green] Loaded GUI[/green]")
        for i in range(3):
            print(f"[+][green] Going to menu in {3-i} seconds[/green]", end="\r")
            sleep(1)
        system('cls' if os.name == 'nt' else 'clear')
    except FileNotFoundError:
        print("[!] Config file not found. Please create a config.json file.")
        sleep(3)
        sys.exit(1)

class BackgroundTasks:
    btc_price = 0
    total_tried = 0
    total_success = 0
    total_made = 0
    def FetchPrice():
        while True:
            try:
                response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
                data = response.json()
                BackgroundTasks.btc_price = float(str(data['bpi'][f'{str(Settings.currency).upper()}']['rate']).replace(',', ''))
                BackgroundTasks.Log(f"Reloaded BTC price :: {BackgroundTasks.btc_price} {str(Settings.currency).upper()}") # auomatically reloads price every 60 seconds
                sleep(60)
            except KeyError:
                BackgroundTasks.Log("[!] Error: Currency not found in API.")
                print(f"'{Settings.currency}' not found in API.\nCurrently only euros (eur), dollars (usd) and pounds (gbp) are supported.")
                input("Press enter to exit.")
                sys.exit(1)
        
    def Log(message):
        if Settings.logging == True: # write to log file if logging is enabled with timestamp
            with open('log.txt', 'a', encoding="utf-8") as f:
                now = datetime.now()
                f.write(f'[{now.strftime("%H:%M:%S")}] - {message}\n')
        else:
            return


    def StartTasks(): # start background tasks
        t = threading.Thread(target=BackgroundTasks.FetchPrice)
        t.start()


def crack():
    before = datetime.now()
    while True: # the "crack" function
        ctypes.windll.kernel32.SetConsoleTitleW(f"Anarchy wallet cracker | {BackgroundTasks.total_tried} tries | {BackgroundTasks.total_success} successes | made {str(BackgroundTasks.total_made)[:5]} BTC")
        a = ("".join(random.choices(string.ascii_lowercase + string.digits + string.ascii_uppercase, k = 33)))
        addr = f'1{a}'
        chance = random.randint(1, 69420)
        if chance == 69 or chance == 420:
            hold = float((random.randint(1, random.randint(1, 9999))) / 100000+ numpy.random.uniform() / random.randint(1, 1000)) / random.randint(1, 10)
            if hold < 5:
                b = BackgroundTasks.btc_price
                amount = hold * float(b)
                print(f"[+] [green]{addr} :: ₿{str(hold)[:5]}")
                sleep(0.537)
                print(f"[+] [green]Transferring {str(amount)[:5]} {str(Settings.currency).upper()} to {Settings.wallet_address}...", end="\r")
                sleep(1.537)
                print(f"[+] [green]Transferred {str(amount)[:5]} {str(Settings.currency).upper()} to {Settings.wallet_address}[/green]")
                sleep(1.784)
                BackgroundTasks.total_tried += 1
                BackgroundTasks.total_success += 1
                BackgroundTasks.total_made += hold
                BackgroundTasks.Log(f"[+] {addr} :: {str(hold)[:5]} ₿ :: {str(amount)[:5]} {str(Settings.currency).upper()}")
            else:
                pass
        else:
            print(f"[-] trying :: {addr} - 0.0000₿", end="\r") # print the address being "cracked"
            BackgroundTasks.total_tried += 1


def main():
    ctypes.windll.kernel32.SetConsoleTitleW("Anarchy wallet cracker | Menu") # main menu function
    menu = f"""[red]
 ▄▄▄       ███▄    █  ▄▄▄       ██▀███   ▄████▄   ██░ ██▓██   ██▓
▒████▄     ██ ▀█   █ ▒████▄    ▓██ ▒ ██▒▒██▀ ▀█  ▓██░ ██▒▒██  ██▒
▒██  ▀█▄  ▓██  ▀█ ██▒▒██  ▀█▄  ▓██ ░▄█ ▒▒▓█    ▄ ▒██▀▀██░ ▒██ ██░
░██▄▄▄▄██ ▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██▀▀█▄  ▒▓▓▄ ▄██▒░▓█ ░██  ░ ▐██▓░
 ▓█   ▓██▒▒██░   ▓██░ ▓█   ▓██▒░██▓ ▒██▒▒ ▓███▀ ░░▓█▒░██▓ ░ ██▒▓░
 ▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ░▒ ▒  ░ ▒ ░░▒░▒  ██▒▒▒
  ▒   ▒▒ ░░ ░░   ░ ▒░  ▒   ▒▒ ░  ░▒ ░ ▒░  ░  ▒    ▒ ░▒░ ░▓██ ░▒░
  ░   ▒      ░   ░ ░   ░   ▒     ░░   ░ ░         ░  ░░ ░▒ ▒ ░░
      ░  ░         ░       ░  ░   ░     ░ ░       ░  ░  ░░ ░
                                        ░                ░ ░[/red]
[green]Welcome {os.getlogin()}[/green]
[green]Anarchy wallet cracker v1.0.0[/green]
{'━' * int(os.get_terminal_size()[0]-1)}
"""
    c.print(menu, justify='center')
    BackgroundTasks.StartTasks()
    print("[+] Background tasks started.")
    input(f"[~] Press enter to start cracking.")
    crack()


main()
