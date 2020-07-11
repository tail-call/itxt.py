#!/usr/bin/env python3

import struct
import binascii
import sys

pngMagic = bytearray(b'\x89PNG\x0d\x0a\x1a\x0a')

def arg(i):
    if i >= len(sys.argv):
        return False
    return sys.argv[i]

def die(message, code = -1):
    print('Error: ' + message)
    exit(code)

def usage():
    print('Usage: ' + sys.argv[0] + ' <input png> <input txt>')

def spew(buf):
    sys.stdout.buffer.write(buf)

def checkMagic(file):
    leadingBytes = file.read(len(pngMagic))
    return leadingBytes == pngMagic

def skip_iHDR(file):
    rawLength = file.read(4)
    length = struct.unpack('>L', rawLength)[0]
    rawData = file.read(4 + length + 4)
    spew(rawLength)
    spew(rawData)

def spew_iTXt(buf):
    length = len(buf)
    buf = b'iTXt' + buf
    crc = binascii.crc32(buf)
    spew(struct.pack('>L', length))
    spew(buf)
    spew(struct.pack('>L', crc))

def inject_iTXt(inputFile, textFile):
    checkMagic(inputFile) or die('input file is not a PNG')
    spew(pngMagic)

    skip_iHDR(inputFile)

    text = textFile.read()
    spew_iTXt(text)

    trailer = inputFile.read()
    spew(trailer)

inputFileName = arg(1) or usage() or die('no input file specified')
textFileName = arg(2) or usage() or die('no itxt content file specified')

inputFile = open(inputFileName, mode = 'rb')
textFile = open(textFileName, mode = 'rb')

inject_iTXt(inputFile, textFile)
