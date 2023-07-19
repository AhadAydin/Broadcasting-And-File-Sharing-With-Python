import socket
import os
import json
import threading


import time
import math


FILE_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + "\\filesToShare"
CHUNK_DIRECTORY = FILE_DIRECTORY + "\\fileChunks"
RECV_DIRECTORY = FILE_DIRECTORY + "\\recv"

CHUNKS = "chunks"
REQUESTED_CONTENT = "requested_content"
TIMESTAMPS_FILE_NAME = "timestamps.txt"

TCP_PORT = 5000
UDP_PORT = 5001
SERVER = socket.gethostbyname(socket.gethostname())
TCP_ADDR = (SERVER,TCP_PORT)
UDP_ADDR = (SERVER,UDP_PORT)

chunks_dict = {CHUNKS:[]}
content_dict = {}

waitingForAFile=False
waitingFileName = "n"

udp_send_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
udp_send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp_send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

udp_recv_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udp_recv_sock.bind(("", UDP_PORT))

tcp_recv_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcp_recv_sock.bind(TCP_ADDR)
tcp_recv_sock.listen()


def chunkAnounce():
    while True:
        udp_send_sock.sendto(json.dumps(chunks_dict).encode(),('192.168.2.255',UDP_PORT))
        time.sleep(10)

def contentDiscovery():
    while True:
        recvContent, recvAddr = udp_recv_sock.recvfrom(1024)
        recvContent = json.loads(recvContent.decode())
        for currentContent in recvContent[CHUNKS]:
            if currentContent in content_dict:
                if recvAddr[0] not in content_dict[currentContent] : 
                    content_dict[currentContent].append(recvAddr[0])
            else : 
                content_dict[currentContent] = [recvAddr[0]]
                  
def chunkDownload(contentName):
    if contentName + "_1" in content_dict:
        for i in range(5):
            tcp_req_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            tempContentName = contentName + "_" + str(i+1)
            if tempContentName in content_dict:

                peerAddr = (content_dict[tempContentName][0],TCP_PORT)
                tcp_req_sock.connect(peerAddr)

                currentContentName = contentName + "_" + str(i+1)
                requestMsg = {REQUESTED_CONTENT : currentContentName}
                tcp_req_sock.send(json.dumps(requestMsg).encode())
                tcp_req_sock.close()

                # get content

                global waitingFileName
                global waitingForAFile
                
                waitingFileName=currentContentName
                waitingForAFile=True

                while waitingForAFile==True:
                    pass
                    
                print("[ file download ] downloaded file",waitingFileName)
                if i == 4:
                    combineChunks(contentName)

    else:
        print("couldn't found file ",contentName)

            


def chunkUpload():
    while True:
        recvContent,recvAddr = tcp_recv_sock.accept()

        recvData = recvContent.recv(42000000)

        if is_json(recvData):
            recvData = json.loads(recvData.decode())
            reqFileName = recvData[REQUESTED_CONTENT]
            print("[ file request ] " ,recvAddr[0] , " wants to download your file : ",reqFileName)
            tcp_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            peerAddr = (recvAddr[0],TCP_PORT)

            tcp_sock.connect(peerAddr)


            os.chdir(CHUNK_DIRECTORY)
            chunkName = reqFileName+".txt"
            chunkToSend = open(chunkName,"rb")
            data = chunkToSend.read()

            tcp_sock.sendall(data)

            chunkToSend.close()                    
            
        else:
            os.chdir(RECV_DIRECTORY)
            tempName = waitingFileName + ".txt"
            recvFile = open(tempName,"wb")
            recvFile.write(recvData)
            recvFile.close()

            os.chdir(FILE_DIRECTORY)
            timeStamps = open(TIMESTAMPS_FILE_NAME,"a")
            timeStampString = "[CHUNK NAME]->" + waitingFileName + "  [IP]->" + recvAddr[0] + "  [TIME]->" + time.ctime(time.time()) + "\n"
            timeStamps.write(timeStampString)
            timeStamps.close()

            global waitingForAFile
            waitingForAFile=False

            



def is_json(parJson):
  try:
    json.loads(parJson)
  except ValueError as e:
    return False
  return True

def createChunksDict():

    chunkList = []

    os.chdir(FILE_DIRECTORY)
    for file in os.listdir(os.getcwd()):

        if os.path.isfile(file):
            print(file)
            print(os.path.getsize(file) )
            chunkSize = math.ceil(os.path.getsize(file) / 5)
            print(chunkSize)
            fileRead = open(file,"rb")

            os.chdir(CHUNK_DIRECTORY)

            for i in range(5):
                chunkData = fileRead.read(chunkSize)
                
                fileName = os.path.splitext(file)[0] + "_" + str(i+1)
                chunkList.append(fileName)

                fileName += ".txt"
                fileTemp = open(fileName,"wb")
                fileTemp.write(chunkData)
                fileTemp.close()

            os.chdir(FILE_DIRECTORY)

    chunks_dict[CHUNKS] = chunkList

def combineChunks(contentName):
    os.chdir(RECV_DIRECTORY)
    currentFileName = "recv_"+ contentName + ".png"
    currentFile = open(currentFileName,"wb")
    for i in range(5):
        currentChunkName = contentName + "_" + str(i+1) + ".txt"
        currentChunk = open(currentChunkName,"rb")
        currentFile.write(currentChunk.read())
    currentFile.close()



# MAIN

createChunksDict()

threading.Thread(target=chunkAnounce).start()
threading.Thread(target=contentDiscovery).start()
threading.Thread(target=chunkUpload).start()
command = ''
while command != 'q':
    command = input("Enter a command\n\tc to view contents\n\td to donwnload content\n\tq to quit\n\t")
    if command == 'c':
        print(content_dict)
    elif command == 'd':
        fileName = input("enter file name : ")
        chunkDownload(fileName)
    elif command != 'q':
        print("invalid command")