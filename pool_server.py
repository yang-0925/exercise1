"""
ＩＯ多路复用　ｐｏｌｌ方法完成ＩO并发
"""

from socket import *
from select import *

#　创建好监听套接字
sockfd = socket()
sockfd.bind(("0.0.0.0",8000))
sockfd.listen(5)

# IO多路复用配合网络时一般为非阻塞网络模型
sockfd.setblocking(False)

p = poll() #　创建ｐｏｌｌ对象

# 建立查找字典 {fileno:sockfd}
map = dict({})

# 设置关注的ＩＯ 读事件
p.register(sockfd,POLLIN)
map[sockfd.fileno()] = sockfd

# 循环监控，等待IO事件发生
while True:
    events = p.poll()
    # 循环遍历events 分情况讨论处理 events-->[(fileno,event),()]
    for fd,event in events:
        # fd-->就绪IO文件描述符  event --》就绪IO就绪了什么事件
        if fd == sockfd.fileno():
            connfd, addr = map[fd].accept()
            print("Connect from ", addr)
            connfd.setblocking(False)
            p.register(connfd,POLLIN) # 添加新的监控
            map[connfd.fileno()] = connfd # 查找字典时刻与监听的IO保持一致
        else:
            data = map[fd].recv(1024)
            if not data:
                # 客户端退出处理
                p.unregister(fd)  # 不需要监控这个IO
                map[fd].close()
                del map[fd]  # 从字典中删除
                continue
            print(data.decode())
            map[fd].send(b'OK')

