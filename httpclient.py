#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse, urlencode
def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):

        host, port = "", 80

        url_parse = urlparse(url)
        

        host = url_parse.hostname
        
        try:
            host_ip = socket.gethostbyname( host )
        except socket.gaierror:
            print ('Hostname could not be resolved. Exiting')
            sys.exit()

        #print (f'Ip address of {host} is {host_ip}')
     
        if url_parse.port != None:
            port = url_parse.port

        return host_ip, port

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        data = data.split("\r\n")
        data = data[0].split(" ")
        code = data[1]
        print(int(code))
        return int(code)

    def get_headers(self,data):
        return None

    def get_body(self, data):
        data = data.split("\r\n\r\n",1)
        body = data[-1]
        print(body)
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(7000)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        host, port = self.get_host_port(url)
        parsed = urlparse(url)
        path = parsed.path
        parsed = parsed.hostname
      

        if path == "":
            path = "/"
        else:
            pass
        print(f'this is path: {path}')

        HTTP_version = "HTTP/1.1"
        #Request-line
        request_line = f"GET {path} {HTTP_version}\r\nHost: {parsed}\r\nConnection: close\r\n\r\n "
        print(request_line)
        #construct data
        payload = request_line
     
        #connect to socket 
        self.connect(host, port)

        #send request to server 
        self.sendall(payload)



        #get data
        data = self.recvall(self.socket)

        

        #close connection
        self.close()

   
        


        #get code, headers, and body
        code = self.get_code(data)
        # headers = self.get_headers(data)
        body = self.get_body(data)




        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        host, port = self.get_host_port(url)
        parsed = urlparse(url)
        path = parsed.path
        parsed = parsed.hostname

        if args == None:
            args = ''
       
        args = urlencode(args)
        content_length = len(args)

        if path == "":
             path = "/"
        else:
            pass
        
       
        HTTP_version = "HTTP/1.1"
        # #Request-line
        post_request =  f"POST {path} {HTTP_version}\r\nHost: {parsed}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {content_length}\r\nConnection: close \r\n\r\n{args}\r\n\r\n"

        # #connect to socket 
        self.connect(host, port)

        # #send request to server 
        self.sendall(post_request)

        # #get data
        data = self.recvall(self.socket)

        # #close connection
        self.close()

        # #get code, headers, and body
        code = self.get_code(data)
        # # headers = self.get_headers(data)
        body = self.get_body(data)
       
        #http://127.0.0.1:27627/abcdef/gjkd/dsadas
   
        
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
