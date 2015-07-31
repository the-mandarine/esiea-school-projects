#!/usr/bin/env python2

from pyfann import libfann
from random import shuffle
from json import dumps as json_dumps
from os import makedirs
from os.path import exists

def new_net():
    conn_rate = 3
    learn_rate = 0.2
    num_in = 6
    num_hid = 8
    num_out = 1

    network = libfann.neural_net()
    network.create_sparse_array(conn_rate,
                    (num_in, num_hid, num_out))
    
    network.set_learning_rate(learn_rate)
    network.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)
    network.set_activation_function_hidden(libfann.SIGMOID_SYMMETRIC_STEPWISE)
    
    return network


def get_training_data(data_file):
    data = libfann.training_data()
    data.read_train_from_file(data_file)
    return data


def normalize(ivalue, ibaseMin, ibaseMax, idestMin, idestMax):
    value = float(ivalue)
    baseMin = float(ibaseMin)
    baseMax = float(ibaseMax)
    destMin = float(idestMin)
    destMax = float(idestMax)

    return (((value - baseMin)/(baseMax - baseMin)) * (destMax - destMin)) + destMin


def rnd(val):
    """Define the seuil of the function
    > 0 -> 1
    < 0 -> -1"""
    if val > 0 : 
        return 1
    else:
        return -1

def file_to_data(filename):
    """Returns a list of examples"""
    f = open(filename, 'r')
    nb_examples, nb_in, nb_out = [int(x) for x in f.readline().split()]
    data_in = []
    data_out = []
    for i in xrange(nb_examples):
        data_in.append([float(x) for x in f.readline().split()])
        data_out.append(int(f.readline()))

    f.close()

    return data_in, data_out

def shuffle_data(data_in, data_out):
    data_list = []
    for i in xrange(len(data_in)):
        data_list.append((data_in[i], data_out[i]))

    shuffle(data_list)

    new_data_in = []
    new_data_out = []
    
    for cur_in, cur_out in data_list:
        new_data_in.append(cur_in)
        new_data_out.append(cur_out)
    
    return new_data_in, new_data_out

def get_learn_test_valid(data_in, data_out):
    """Returns a 3 elements tuple containing : 
    - Learning datas (80%)
    - Test datas (10%)
    - Validation data (10%)"""
    
    learn_in = [] 
    learn_out = []
    test_in = []
    test_out = []
    valid_in = []
    valid_out = [] 

    s_data_in, s_data_out = shuffle_data(data_in, data_out)
    perdix_learn = 5
    perdix_test = 2
    perdix_validate = 2

    second_seuil = perdix_learn + perdix_test

    assert perdix_learn + perdix_test + perdix_validate == 9

    cur_i_p = 0
    cur_i_n = 0
    for i in xrange(len(data_in)):
        if data_out[i] == 1:
            if cur_i_p <= perdix_learn:
                learn_in.append(data_in[i])
                learn_out.append(data_out[i])
            elif cur_i_p > perdix_learn and cur_i_p <= second_seuil:
                test_in.append(data_in[i])
                test_out.append(data_out[i])
            elif cur_i_p > second_seuil:
                valid_in.append(data_in[i])
                valid_out.append(data_out[i])
            else:
                print "WTFFFFFF"

            cur_i_p = (cur_i_p + 1 ) % 10

        elif data_out[i] == -1:
            if cur_i_n <= perdix_learn:
                learn_in.append(data_in[i])
                learn_out.append(data_out[i])
            elif cur_i_n > perdix_learn and cur_i_n <= second_seuil:
                test_in.append(data_in[i])
                test_out.append(data_out[i])
            elif cur_i_n > second_seuil:
                valid_in.append(data_in[i])
                valid_out.append(data_out[i])

            cur_i_n = (cur_i_n + 1 ) % 10

    return learn_in, learn_out, test_in, test_out, valid_in, valid_out

def data_to_file(filename, data_in, data_out):
    """Generates a fann file with good datas in it"""
    assert(len(data_in) == len(data_out))
    nb_ex = len(data_in)
    nb_in = len(data_in[0])
    nb_out = 1 

    f = open(filename, 'w')
    f.write("%i %i %i\n" % (nb_ex, nb_in, nb_out))

    for i in xrange(nb_ex):
        f.write("%s\n" % (" ".join([str(x) for x in data_in[i]])))
        f.write("%s\n" % (str(data_out[i])))

    f.close()


def net_error(test_data, net):
    test_in, test_out = test_data

    fp = 0
    fn = 0
    tp = 0
    tn = 0

    for index in xrange(len(test_in)):
        curIn = test_in[index]
        expectedOut = test_out[index]

        actualOut = net.run(curIn)[0]
        
        if rnd(actualOut) == -1 and expectedOut == -1:
            tn += 1
        if rnd(actualOut) == -1 and expectedOut == 1:
            fn += 1
        if rnd(actualOut) == 1 and expectedOut == -1:
            fp += 1
        if rnd(actualOut) == 1 and expectedOut == 1:
            tp += 1
    
    error = float(fp + fn) / float(tp + tn + fp + fn) 
    #print "Examples : %i" % (index)
    #print "True Positive : %f" % (float(tp) / float(index)) 
    #print "False Positive : %f" % (float(fp) / float(index))
    #print "True Negative : %f" % (float(tn) / float(index))
    #print "False Negative : %f" % (float(fn) / float(index))

    return error
    

def main():

    all_data_in, all_data_out = file_to_data("gender_full.data")

    learn_in, learn_out, test_in, test_out, valid_in, valid_out = get_learn_test_valid(all_data_in, all_data_out)
    data_to_file("gender_learn.data", learn_in, learn_out)
    data_to_file("gender_test.data", test_in, test_out)
    data_to_file("gender_valid.data", valid_in, valid_out)

    nb_examples = len(all_data_in)

    #network = libfann.neural_net()
    #network.create_from_file("cancer.net")
    #network = train_my_net("cancer_learn.data")
    test_data = file_to_data("gender_test.data")

    network = new_net()
    learning_rate = 0.5
    network.set_learning_rate(learning_rate)
    
    net_id = 0;
    if not exists("networks"):
        makedirs("networks");
    net_index = {}
    learn_data = get_training_data("gender_learn.data")
    min_err = 1.
    while net_id < 100000:
        network.train_epoch(learn_data);
        if net_id % 10 == 0:
            cur_net_err = net_error(test_data, network)
            if cur_net_err < min_err:
                learning_rate -= learning_rate / 20
                network.set_learning_rate(learning_rate)
                print learning_rate 
                min_err = cur_net_err
                min_net = net_id
                
            net_file_name = "networks/net_%03i.net" % (net_id)
            network.save(net_file_name)
            net_index[net_file_name] = cur_net_err
        net_id += 1

    f = open("networks/errors.json", 'w')
    f.write(json_dumps(net_index, indent=2, sort_keys=True))
    f.close()

    print "Minimum error is around net_%i - Error = %f" % (min_net, min_err)

if __name__ == '__main__':
    main()

