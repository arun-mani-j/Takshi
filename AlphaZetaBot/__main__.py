#!/usr/bin/python3

import sys
import AlphaZetaBot

server = AlphaZetaBot.Server()
if "-p" in sys.argv:
    server.poll()
else:
    server.run()
