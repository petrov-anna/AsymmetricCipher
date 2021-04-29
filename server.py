import socket
import pickle


# симметричный шифр
def encrypt(k, m):
    return ''.join(map(chr, [x + k for x in map(ord, m)]))


def decrypt(k, c):
    return ''.join(map(chr, [x - k for x in map(ord, c)]))


def checker(m):
    sp = [1, 3, 6, 5]
    num = 0
    for i in sp:
        if int(m) != i:
            num = num + 1
    if num > 3:
        print('Ключ некорректен')
        conn.send(pickle.dumps('exit'))
        conn.close()
        return False
    return True


HOST = '127.0.0.1'
def_port = 8080

PORT = int(input("Введите порт: "))
if (1023 >= int(PORT)) | (int(PORT) >= 65536):
    print(f'Порт введён неверно, порт по умолчанию - {def_port}')
    PORT = int(def_port)


sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

file = open("textS.txt", 'w')

p, g, b = 7, 5, 3
B = g ** b % p

# запись ключа в файл
file.write(str(B))
file.close()

# считываем данные из файла
keyB = open("textS.txt").read()

if checker(keyB):
    # отправлем открытый ключ клиенту
    conn.send(pickle.dumps((p, g, int(keyB))))

    # получаем открытый ключ клиента
    msgK = conn.recv(1024)
    K = pickle.loads(msgK)[2] ** b % p
    print('Client =', K)

    # расшифровать сообщение клиента
    msgR = conn.recv(1024)
    msgR = decrypt(b, pickle.loads(msgR))
    msgR = decrypt(K, msgR)
    print("Message decrypt =", msgR)

    # отправить сообщение
    msg = encrypt(b, 'Hi!')
    msg = encrypt(K, msg)
    conn.send(pickle.dumps(msg))
    print("Message to send =", msg)

    conn.close()
