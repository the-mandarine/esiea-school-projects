#!/usr/bin/env python2

from pyfann import libfann
from argparse import ArgumentParser

class Configuration(ArgumentParser):
    def __init__(self):
        ArgumentParser.__init__(self)
        self.add_argument("testfile")
        self.add_argument("netfile")

def rnd(value):
    "Chooses : M, F, ? according to the seuil"
    print value
    ret = "?"
    if value < -0.15:
        ret = "M"
    elif value > 0.15:
        ret = "F"
    else:
        ret = "?"
    
    return ret

def main():
    config = Configuration().parse_args()
    network = libfann.neural_net()
    network.create_from_file(config.netfile)

    f = open(config.testfile, 'r')
    full_file = f.read().split("\n")[1:-1]
    f.close()

    assert len(full_file) % 2 == 0
    
    true_f = 0
    true_m = 0
    notsure_f = 0
    notsure_m = 0
    false_f = 0
    false_m = 0
    wtf_res = 0

    for i in range(len(full_file) / 2):
        in_index = i * 2
        out_index = in_index + 1
        ins = full_file[in_index]
        outs = full_file[out_index]

        inp = [float(x) for x in ins.split()]
        real_out = rnd(float(outs))
        net_out = rnd(network.run(inp)[0])

        print "In : %s\nOut : %s\nRealOut : %s\n" % (ins, net_out, real_out)
        if real_out == net_out:
            if real_out == 'F':
                true_f += 1
            elif real_out == 'M':
                true_m += 1
        elif net_out == '?':
            if real_out == 'F':
                notsure_f += 1
            elif real_out == 'M':
                notsure_m += 1
        elif real_out == 'F':
            false_m += 1
        elif real_out == 'M':
            false_f += 1

    
    print "- %i OK" % (true_f + true_m)
    print "- %i NotSure" % (notsure_f + notsure_m)
    print "- %i Wrong" % (false_f + false_m)

if __name__=='__main__':
    main()
