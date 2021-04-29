import socket
import pickle


# симметричный шифр
def encrypt(k, m):
    return ''.join(map(chr, [x + k for x in map(ord, m)]))


def decrypt(k, c):
    return ''.join(map(chr, [x - k for x in map(ord, c)]))


HOST = '127.0.0.1'
def_port = 8080

PORT = int(input("Введите порт: "))
if (1023 >= int(PORT)) | (int(PORT) >= 65536):
    print(f'Порт введён неверно, порт по умолчанию - {def_port}')
    PORT = int(def_port)

sock = socket.socket()
sock.connect((HOST, PORT))

file = open("textC.txt", 'w')

p, g, a = 7, 5, 3
A = g ** a % p

# запись ключа в файл
file.write(str(A))
file.close()

# считываем данные из файла
keyA = open("textC.txt").read()

# отправляем открытый ключ серверу
sock.send(pickle.dumps((p, g, int(keyA))))  # открытый ключ клиента

# получаем открытый ключ сервера
msgK = sock.recv(1024)
K = pickle.loads(msgK)[2] ** int(a) % p
print('Server =', K)

# отправить сообщение
msg = encrypt(a, 'Hello!')
msg = encrypt(K, msg)
sock.send(pickle.dumps(msg))
print("Message to send =", msg)

# расшифровать сообщение сервера
msgR = sock.recv(1024)
msgR = decrypt(a, pickle.loads(msgR))
msgR = decrypt(K, msgR)
print("Message decrypt =", msgR)

sock.close()
