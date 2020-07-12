#!/usr/bin/env python3

 #########################################################################
##/                                                                     \##
##  Injects text content into a JPEG or PNG input file as close to       ##
##  beggining of file as possible. Outputs a valid JPEG/PNG file         ##
##  readable by most software to stdout.                                 ##
##                                                                       ##
##  Please note that for JPEG embedded payload shouldn't be larger than  ##
##  65,534 bytes (64kb). For PNG limit is 4,294,967,296 bytes (~4Gb).    ##
##                                                                       ##
##  © 2020 Anton Istomin                                                 ##
##\                                                                     /##
 #########################################################################

import struct
import binascii
import sys

PNG_MAGIC = bytearray(b'\x89PNG\x0d\x0a\x1a\x0a')
JPG_MAGIC = bytearray(b'\xFF\xD8')

EXIT_NOINPUT = 1
EXIT_NOTEXT = 2
EXIT_BADINPUT = 3

def arg(i):
    if i >= len(sys.argv):
        return False
    return sys.argv[i]

def die(message, code = -1):
    print('Error: ' + message, file=sys.stderr)
    exit(code)

def usage():
    print('Usage: ' + sys.argv[0] + ' <input jpeg/png> <input txt>', file=sys.stderr)

def spew(buf):
    sys.stdout.buffer.write(buf)

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

def skip_APP0(file):
    marker = file.read(2)
    rawLength = file.read(2)
    # Length includes length marker
    length = struct.unpack('>H', rawLength)[0] - 2
    print(length, file=sys.stderr)
    rawData = file.read(length)
    spew(marker)
    spew(rawLength)
    spew(rawData)

def spew_COM(buf):
    spew(b'\xFF\xFE')
    length = len(buf) + 2
    spew(struct.pack('>H', length))
    spew(buf)

# Injects iTXt chunk for PNG
def inject_iTXt(inputFile, textFile):
    inputFile.read(len(PNG_MAGIC))
    spew(PNG_MAGIC)

    skip_iHDR(inputFile)

    text = textFile.read()
    spew_iTXt(text)

    trailer = inputFile.read()
    spew(trailer)

# Inject comment section for JPEG
def inject_COM(inputFile, textFile):
    inputFile.read(len(JPG_MAGIC))
    spew(JPG_MAGIC)

    skip_APP0(inputFile)

    text = textFile.read()
    spew_COM(text)

    trailer = inputFile.read()
    spew(trailer)

def matchesMagic(file, magic):
    leadingBytes = file.read(len(magic))
    file.seek(-len(magic), 1)
    return leadingBytes == magic

inputFileName = arg(1) or usage() or die('no input file specified', EXIT_NOINPUT)
textFileName = arg(2) or usage() or die('no itxt content file specified', EXIT_NOTEXT)

inputFile = open(inputFileName, mode='rb')
textFile = open(textFileName, mode='rb')

if matchesMagic(inputFile, PNG_MAGIC):
    inject_iTXt(inputFile, textFile)
elif matchesMagic(inputFile, JPG_MAGIC):
    inject_COM(inputFile, textFile)
else:
    die(inputFileName + ': file not supported', EXIT_BADINPUT)
