import SocketServer
from os import path as osPath
from os import getcwd
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Copyright 2015 Jake Brand
# Modified server.py in order to complete the assignment
#
# Consulted with: Aaron Padlesky, Ashley Fegan, Markus Karpoff,
# Pranjali Pokharel, Simon Fessehaye throughout the course


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        # Does not apear to be needed, but left here in case tests require it
        # print ("Got a request of: %s\n" % self.data)
        # not an efficient way of testing the request type
        self.reqType = self.data.split(' ')[0]
        if(self.reqType == "GET"):
            self.get(self.data)
        else:
            self.nonGet(self.data)
        # Does not apear to be needed, but left here in case tests require it
        # self.request.sendall("OK")

    def get(self, request):
        tokens = request.split(' ')
        path = tokens[1]
        httpVersion = tokens[2].split('\r')[0]
        reqLoc = "www" + path

        if(reqLoc.endswith(".css")):
            mimetype = "text/css"
        elif(reqLoc.endswith(".html")):
            mimetype = "text/html"
        elif(reqLoc.endswith(".text")):
            mimetype = "application/plain"
        # placed last because it is the slowest check
        elif(osPath.isdir(reqLoc)):
            print("FOUND HREE", reqLoc)
            if(reqLoc.endswith("/")):
                reqLoc = reqLoc + "index.html"
            else:
                reqLoc = reqLoc + "/index.html"
            mimetype = "text/html"
        # Unsure of best way to handle types outside of spec.
        else:
            mimetype = "application/plain"

        reqLoc = osPath.abspath(reqLoc)

        if(osPath.join(getcwd(), "www/") not in reqLoc):
            response = httpVersion + " 404 Not Found\r\n" + \
                "Conetnt-Type: " + mimetype + "\r\n" + \
                reqLoc + "\r\n" + "\r\n"
            self.request.send(response)
        else:
            try:
                f = open(reqLoc)
                opened = f.read()
                f.close()

                response = httpVersion + " 200 OK\r\n" + \
                    "Content-Type: " + mimetype + "\r\n" + "\r\n" + \
                    opened + "\r\n"
                self.request.send(response)

            except IOError:
                response = httpVersion + " 404 Not Found\r\n" + \
                    "Conetnt-Type: " + mimetype + "\r\n" + "\r\n" + \
                    reqLoc + "\r\n" + "\r\n"
                self.request.send(response)

    def nonGet(self, request):
        response = "405 Method Not Allowed\r\n" + \
            "Allow: GET\r\n"
        self.request.sendall(response)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
