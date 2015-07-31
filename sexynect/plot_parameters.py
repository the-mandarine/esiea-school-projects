#!/usr/bin/env python2
import struct
import sys
import matplotlib.pyplot as plt

class Image(object):
    def __init__(self, gender, lines, columns, data):
        self.gender = gender
        self.nb_lin = lines
        self.nb_col = columns
        self.data = data

def get_img_getter():
    f = open('data.bin', 'rb')
    
    while True: 
        #headers
        gender = f.read(1).decode()
        if not gender:
            f.close()
            break
        cols = struct.unpack('i', f.read(4))[0]
        lins = struct.unpack('i', f.read(4))[0]
        if cols < 0 or lins < 0:
            continue

        # datas
        data = []
        cur_lin = 0
        for i in range(lins):
            data.append([])
            for j in range(cols):
                cur_block = ord(f.read(1))
                data[cur_lin].append(cur_block)

            cur_lin += 1

        #operations
        img = Image(gender, lins, cols, data)
        yield img

def get_energy(img):
    strength = 0
    for lin in img.data:
        strength += get_line_energy(lin)

    energy = strength / img.nb_lin
    return energy

def get_barycenter(img):
    strength = 0.
    barycenter_x = 0.
    barycenter_y = 0.
    surface = img.nb_lin * img.nb_col
    
    for lin_id in xrange(img.nb_lin):
    	for col_id in xrange(img.nb_col):
            cur_strength = float(img.data[lin_id][col_id])
            strength += cur_strength / float(surface)
            if cur_strength != 0:
                barycenter_y += float(lin_id) / img.nb_lin
                barycenter_x += float(col_id) / img.nb_col
            
                barycenter_x *= float(cur_strength) / float(surface)
                barycenter_y *= float(cur_strength) / float(surface)

    return barycenter_y, barycenter_x

def get_section_ratio(img):
    sec_energies = get_sec_energies(img)
    ratio = float(sec_energies[0]) / float(sec_energies[5])
    return ratio

def get_section_ratio_2(img):
    sec_energies = get_sec_energies(img) 
    ratio = float(sec_energies[1]) / float(sec_energies[4])
    return ratio

def get_sec_energies(img):
    sec_energies = []
    sections = get_img_sections_2(img)
    for sec in sections:
        sec_energy = 0
        for lin in sec:
            sec_energy += get_line_energy(lin)

        sec_energies.append(sec_energy)
    
    return sec_energies

def get_top_points_ratio(img):
    points = get_6_top_points(img)
    ratio = float(points[2]) / float(points[4])
    return ratio

def get_6_top_points(img):
    points = []
    sections = get_img_sections_2(img)
    for sec in sections:
        points.append(get_top_point(sec))
    return points
    
def get_top_point(section):
    top_point_val = -1
    for lin in section:
        for dat in lin:
            if dat > top_point_val:
                top_point_val = dat
    return top_point_val

def get_img_sections_2(img):
    step = img.nb_lin / 6
    secs = []
    for i in range(6):
        section = []
        for j in range(step):
            section.append(img.data[step * i + j])

        secs.append(section)
    
    return secs
        

def get_img_sections(img):
    sections = []
    k = -1
    for i in range(0,img.nb_lin):
        if i%(img.nb_lin/6) == 0:
            k +=1
            sections.append([])
        sections[k].append(img.data[i])
    return  sections

def get_line_energy(line):
    energy = 0
    for pixel in line:
        energy += pixel
    
    energy = float(energy) / len(line)
    return energy

def pixels_on_line(line):
    seuil = 10
    nb_pixel = 0
    for pixel in line:
        if pixel > seuil:
            nb_pixel += 1

    nb_pixel = float(nb_pixel) / len(line)
    return nb_pixel

def get_most_dispatched_energy(img):
    pixels = []
    for line in img.data:
        nb_pixel = pixels_on_line(line)
        pixels.append(nb_pixel)

    max_pixels = max(pixels)
    max_pixels_pos = float(pixels.index(max_pixels)) / img.nb_lin
    return max_pixels_pos
    
def get_max_energy_pos(img):
    energies = []
    for line in img.data:
        energy = get_line_energy(line)
        energies.append(energy)

    max_energy = max(energies)
    max_energy_pos = float(energies.index(max_energy)) / img.nb_lin
    return max_energy_pos
    
def get_legs_height(img):
    #we get the real middle of the image 
    line_to_check = img.nb_lin / 5 * 3
    return 0
    

def get_parameter_1(img):
    #param = get_energy(img)
    #param = get_max_energy(img)
    param = get_section_ratio(img)
    return param

def get_parameter_2(img):
    #bary_y, bary_x = get_barycenter(img)

    #param = bary_y
    param = get_most_dispatched_energy(img)

    return param

def get_parameters(img):
    param1 = get_parameter_1(img)
    param2 = get_parameter_2(img)
    #param1, param2 = get_barycenter(img)

    return param1, param2


def get_graph(pf1, pf2, pm1, pm2):
    plt.plot(pf1, pf2, 'ro', pm1, pm2, 'bo')
    plt.show()
    

def main():
    img_id = 0
    img_getter = get_img_getter()

    params_f1 = []
    params_f2 = []
    params_m1 = []
    params_m2 = []

    sys.stderr.write("== SexyNect gender determination ==\nExecution : ")
    sys.stderr.write("00%")
    for img in img_getter:    
        param1, param2 = get_parameters(img)
        if img.gender == 'f':
            params_f1.append(param1)
            params_f2.append(param2)
        elif img.gender == 'm':
            params_m1.append(param1)
            params_m2.append(param2)

        percent = "\b\b\b%02i%%" % (img_id * 100 / 201)
        sys.stderr.write(percent)
        img_id += 1

    get_graph(params_f1, params_f2, params_m1, params_m2)

if __name__ == '__main__':
    main()

