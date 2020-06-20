from socket import *

s = socket()
s.bind(("0.0.0.0",8008))
s.listen(3)

c,addr = s.accept()
print("连接到:",addr)

data = c.recv(4096) # 接受来自浏览器的http请求
print(data.decode())


response = "HTTP/1.1 200 OK\r\n"
response +="Content-Type: text/html\r\n"
response += "\r\n"
fw = open("python.html")
while True:
    data = fw.read(1024 * 1024)
    if not data:
        break
    response += data

fw.close()
c.send(response.encode())

c.close()
s.close()