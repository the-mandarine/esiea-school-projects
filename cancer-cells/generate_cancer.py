#!/usr/bin/env python
import sys

def normalize(ivalue, ibaseMin, ibaseMax, idestMin, idestMax):
    value = float(ivalue)
    baseMin = float(ibaseMin)
    baseMax = float(ibaseMax)
    destMin = float(idestMin)
    destMax = float(idestMax)

    return (((value - baseMin)/(baseMax - baseMin)) * (destMax - destMin)) + destMin


def main():
    f = open("cancer.data.raw", 'r')
    raw_data = f.readlines()
    f.close()

    data_per_line = 30 

    final_in = []
    final_out = []
    
    min_data = [float(x) for x in raw_data[0].split(',')[2:]]
    max_data = [float(x) for x in raw_data[0].split(',')[2:]]


    for line in raw_data:
        splitted_line = line.split(',')
        sp_line = splitted_line[2:]
        
        for itemIndex in range(len(sp_line)):
            if float(sp_line[itemIndex]) < float(min_data[itemIndex]):
                min_data[itemIndex] = float(sp_line[itemIndex])
            if float(sp_line[itemIndex]) > float(max_data[itemIndex]):
                max_data[itemIndex] = float(sp_line[itemIndex])



    counter = 0
    for line in raw_data:
        counter += 1
        splitted_line = line.split(',')

        if splitted_line[1] == 'M':
            out = 1
        else:
            out = -1

        sp_line = splitted_line[2:]
        
        inp = []

        for i in range(len(sp_line)):
            x = sp_line[i]
            dmin = min_data[i]
            dmax = max_data[i]

            inp.append(normalize(x, dmin, dmax, -1, 1))
        
        final_in.append(inp)
        final_out.append(out)
        
    assert len(final_in) == len(final_out)


    # affichage sur la sortie standard
    in_per_test = len(final_in[0])
    out_per_test = 1
    nb_test = counter

    print(nb_test, in_per_test, out_per_test)
    
    for k in range(len(final_in)):
        print("%s\n%s" % (" ".join([str(x) for x in final_in[k]]), final_out[k]))

    sys.stderr.write("# Write in test_net.py\n")
    sys.stderr.write("data_mins = %s\n" % str(min_data))
    sys.stderr.write("data_maxs = %s\n" % str(max_data))


if __name__=='__main__':
    main()

