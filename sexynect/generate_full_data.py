#!/usr/bin/env python2
import struct
import sys
from plot_parameters import * 

def main():
    img_id = 0
    img_getter = get_img_getter()

    sys.stderr.write("== SexyNect generating data ==\nExecution : ")
    sys.stderr.write("00%")
    img_count = 0
    data_output = ""
    for img in img_getter:
        if img.gender == 'f':
            gender = "1"
        elif img.gender == 'm':
            gender = "-1"
        else:
            gender = "0"

        nb_in = 6
        # Calculate parameters
        barycenter_y, barycenter_x = get_barycenter(img)
        most_dispatched = get_most_dispatched_energy(img)
        max_energy_pos = get_max_energy_pos(img)
        section_ratio = get_section_ratio(img)
        section_ratio_2 = get_section_ratio_2(img)
        
        img_output  = str(barycenter_x) + " "
        img_output += str(barycenter_y) + " "
        img_output += str(most_dispatched) + " "
        img_output += str(max_energy_pos) + " "
        img_output += str(section_ratio) + " "
        img_output += str(section_ratio_2) + " "
        img_output += "\n"
        img_output += gender + "\n"
        data_output += img_output

        percent = "\b\b\b%02i%%" % (img_count * 100 / 201)
        sys.stderr.write(percent)
        
        img_count += 1

    data_file = open("gender_full.data", 'w')
    data_file.write("%i %i %i\n" % (img_count, nb_in, 1))
    data_file.write(data_output)
    data_file.close()

if __name__ == '__main__':
    main()

