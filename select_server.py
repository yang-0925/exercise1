"""
重点代码

要关注的IO:监听套接字  各个客户端的连接套接字
"""
from socket import *
from select import select

sock = socket()
sock.bind(("0.0.0.0",8899))
sock.listen(5)

#设置关注列表
rlist = [sock] #初始只关注监听套接字
wlist = []
xlist = []

#对IO进行关注
while True:
    rs,ws,xs = select(rlist,wlist,xlist)
    for r in rs:
        if r is sock:
            connfd,addr = rs[0].accept()
            print("客户端地址:",addr)
            connfd.setblocking(False)
            # 每连接一个客户端 都将这个客户端套接字加入关注
            rlist.append(connfd)
        else:
            data = r.recv(1024)
            if not data:
                rlist.remove(r) #这个Io不不要监控了
                r.close()
                continue
            print(data.decode())
            r.send(b"OK")










