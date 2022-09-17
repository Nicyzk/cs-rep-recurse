from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.ticker_stream_part1
import codeitsuisse.routes.ticker_stream_part2
import codeitsuisse.routes.crypto_collapz
import codeitsuisse.routes.stack_pwn_runner