#!/usr/bin/python3

import sys
import Takshi

server = Takshi.Server()
if "-p" in sys.argv:
    server.poll()
else:
    server.listen()
