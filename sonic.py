# -*- coding: utf-8 -*-

import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import SingleLetterAlphabet
from psonic import *
import RPi.GPIO as GPIO
import sys
import time


aa2scale = {
'W': 48,
'Y': 50,
'R': 52,
'U': 53,
'F': 55,
'H': 57,
'M': 59,
'E': 60,
'K': 62,
'Q': 64,
'D': 65,
'N': 67,
'I': 69,
'L': 71,
'C': 72,
'T': 74,
'V': 76,
'P': 77,
'S': 79,
'A': 81,
'G': 83
}


def sound(aa, orf):
    if aa == '*':
        sample(AMBI_CHOIR)

    scale = aa2scale[aa] if aa in aa2scale else 0

    if orf:
        use_synth(HOOVER)
    else:
        use_synth(BEEP)

    play(scale)
    return



def light():
    GPIO.output(2, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(2, GPIO.LOW)
    time.sleep(0.1)
    return


def readSeq(ntFile):
    for ntRec in SeqIO.parse(ntFile, 'fasta'):
        print('Playing ' + ntRec.id)

        ntSeqStr = str(ntRec.seq)
        while(len(ntSeqStr) % 3 != 0):
            ntSeqStr += 'N'

        ntSeq = Seq(ntSeqStr, SingleLetterAlphabet())
        aaSeq = ntSeq.translate()
        orf = 0
    
        for aa in aaSeq:
            if aa == 'M':
                orf = 1
            elif aa == '*':
                orf = 0

            sound(aa, orf)
            if orf:
                light()
            print(aa, end="")
            sys.stdout.flush()
            sleep(0.3)

        print("")


if __name__ == '__main__':
    par = argparse.ArgumentParser(description = '')
    
    par.add_argument('ntFile', metavar='fasta', type=str,
                     help='Input fasta file')

    args = par.parse_args()

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.OUT)
    readSeq(args.ntFile)
    GPIO.cleanup()
