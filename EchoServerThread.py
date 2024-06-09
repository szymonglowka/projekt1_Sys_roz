import socket
import threading
import fileinput
class EchoServerThread(threading.Thread):
    def __init__(self, client_socket, logins):
        super().__init__()
        self.socket = client_socket
        self.logins = logins

    def run(self):
        thread_name = threading.current_thread().name
        try:
            brinp = self.socket.makefile('r')
            out = self.socket.makefile('w')
            while True:
                line = brinp.readline().strip()
                print(thread_name + "| Line read: " + line)
                self.logins = read_logins_from_file("users.txt")
                if line == "login":
                    print(thread_name + " wants to login.")
                    login_pass = False
                    while not login_pass:
                        out.write("Login and password?\r\n")
                        out.flush()
                        print(thread_name + "| Line sent: " + "Login and password?")
                        line = brinp.readline().strip()
                        print(thread_name + "| Login and pass: " + line)
                        s = line.split()
                        for user in self.logins:
                            if user[0] == s[0] and user[1] == s[1]:
                                login_pass = True
                                login_user = user[0]
                                out.write("Correct login and password\r\n")
                                out.flush()
                                print(thread_name + "| Line sent: " + "Correct login and password")
                                break
                        if login_pass == False:
                            print(thread_name + "| Line sent: Nie poprawne dane logowania")
                            out.write("Nie poprawne dane logowania")
                            out.flush()
                            break
                elif line == "register":
                    print(thread_name + " wants to register.")
                    login_pass = False
                    while not login_pass:
                        out.write("Login Nazwisko(haslo) Pesel numer_konta saldo?\r\n")
                        out.flush()
                        print(thread_name + "| Line sent: " + "Login Nazwisko(haslo) Pesel numer_konta saldo ?")
                        line = brinp.readline().strip()
                        print(thread_name + "| Login Nazwisko(haslo) Pesel numer_konta saldo: " + line)
                        s = line.split()
                        login_pass = True
                        for user in self.logins:
                            login_user = user[0]
                            if user[0] == s[0]:
                                login_pass = False
                                print(thread_name + "| Line sent: " + "Login already in use :(")
                                break
                        if login_pass:
                            new_user = s[:5]
                            self.logins.append(new_user)
                            out.write("User registered \r\n")
                            out.flush()
                            save_logins_to_file("users.txt", self.logins)
                elif line == "list":
                    user_list = " ".join(user[0] for user in self.logins)
                    out.write(user_list + "\r\n")
                    out.flush()
                elif line == "balance":
                    try:
                        login_pass
                    except:
                        login_pass = False
                    if login_pass:
                        for user in self.logins:
                            if user[0] == login_user:
                                print(thread_name + "| Line sent: " + user[4])
                                out.write("Twoje saldo to: " +user[4]+"\r\n")
                                out.flush()
                                break
                    else:
                        out.write("Nie zalogowaes  sie : (\r\n")
                        out.flush()
                elif line == "transfer":
                    try:
                        login_pass
                    except:
                        login_pass = False
                    if login_pass:
                        for user in self.logins:
                            if user[0] == login_user:
                                out.write("Podaj ilosc przelewu:")
                                out.flush()
                                transfer_amount = brinp.readline().strip()
                                print(thread_name + "| Line read: " + transfer_amount)
                                out.write("Podaj usera:")
                                out.flush()
                                transfer_target = brinp.readline().strip()
                                print(thread_name + "| Line read: " + transfer_target)
                                if int(transfer_amount) <= int(user[4]) and int(transfer_amount) > 0:
                                    aktualne_saldo =int(user[4]) - int(transfer_amount)
                                    change_param_in_file("users.txt",user[0],aktualne_saldo)
                                    print(thread_name + "| Line sent: " + str(aktualne_saldo))
                                    out.write("Przelales: "+ str(transfer_amount)+" Zostalo ci:"+ str(aktualne_saldo) + "\r\n")
                                    for user in self.logins:
                                        if user[0] == transfer_target:
                                            aktualne_saldo = int(user[4]) + int(transfer_amount)
                                            change_param_in_file("users.txt", user[0], aktualne_saldo)
                                            print(thread_name + "| Line sent: " + str(aktualne_saldo))
                                            out.write(user[0]+"Otrzymal: " + str(transfer_amount) + "ma teraz:" + str(aktualne_saldo) + "\r\n")
                                            out.flush()
                                            break
                                else:
                                    print(thread_name + "| Line sent: Nie poprawna wartosc lub nie masz wystarczajaco pieniedzy")
                                    out.write("Nie poprawna wartosc lub nie masz wystarczajaco pieniedzy")
                                    out.flush()
                                    break

                    else:
                        out.write("nie zalogowaes  sie : (\r\n")
                        out.flush()
                elif line == "withdraw":
                    try:
                        login_pass
                    except:
                        login_pass = False
                    if login_pass:
                        for user in self.logins:
                            if user[0] == login_user:
                                out.write("Podaj ilosc:")
                                out.flush()
                                line = brinp.readline().strip()
                                print(thread_name + "| Line read: " + line)
                                if int(line) <= int(user[4]) and int(line) > 0:
                                    aktualne_saldo =int(user[4]) - int(line)
                                    change_param_in_file("users.txt",user[0],aktualne_saldo)
                                    print(thread_name + "| Line sent: " + str(aktualne_saldo))
                                    out.write("Wyplaciles: "+ str(line)+" Zostalo ci:"+ str(aktualne_saldo) + "\r\n")
                                    out.flush()
                                    break
                                else:
                                    print(thread_name + "| Line sent: Nie poprawna wartosc lub nie masz wystarczajaco pieniedzy")
                                    out.write("Nie poprawna wartosc lub nie masz wystarczajaco pieniedzy")
                                    out.flush()
                                    break

                    else:
                        out.write("nie zalogowaes  sie : (\r\n")
                        out.flush()
                elif line == "deposit":
                    try:
                        login_pass
                    except:
                        login_pass = False
                    if login_pass:
                        for user in self.logins:
                            if user[0] == login_user:
                                out.write("Podaj ilosc:")
                                out.flush()
                                line = brinp.readline().strip()
                                if line > 0:
                                    print(thread_name + "| Line read: " + line)
                                    aktualne_saldo =int(user[4]) + int(line)
                                    change_param_in_file("users.txt",user[0],aktualne_saldo)
                                    print(thread_name + "| Line sent: " + str(aktualne_saldo))
                                    out.write("Wplaciles: "+ str(line)+" Masz teraz:"+ str(aktualne_saldo) + "\r\n")
                                    out.flush()
                                    break
                                else:
                                    out.write("podales nie poprawna wartosc\r\n")
                                    out.flush()
                    else:
                        out.write("nie zalogowaes  sie : (\r\n")
                        out.flush()
                else:
                    out.write(line + "\r\n")
                    out.flush()
                    print(thread_name + "| Line sent: " + line)

        except Exception as e:
            print(thread_name + "| Input/output error: " + str(e))

        finally:
            self.socket.close()


def read_logins_from_file(file_name):
    logins = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                login, password, nickname,pesel,bank_number = line.strip().split()
                logins.append([login, password, nickname,pesel,bank_number])
    except FileNotFoundError:
        print("Plik nie istnieje. Tworzę nowy plik:", file_name)
        with open(file_name, 'w'):
            pass
    return logins

def save_logins_to_file(file_name, logins):
    with open(file_name, 'w') as file:
        for user in logins:
            file.write(" ".join(user) + "\n")

def change_param_in_file(file_name, login, new_balanace):
    for linia in fileinput.input(file_name, inplace=True):
        param = linia.strip().split()
        if param[0] == login:
            param[4] = str(new_balanace)
            print(" ".join(param))
        else:
            print(linia.strip())

logins_file = "users.txt"

logins = read_logins_from_file(logins_file)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 7005))
server_socket.listen(5)

print("Echo server is listening...")

while True:
    logins = read_logins_from_file(logins_file)
    client_socket, _ = server_socket.accept()
    print("Client connected")
    thread = EchoServerThread(client_socket, logins)
    thread.start()

