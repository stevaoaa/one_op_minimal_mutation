#!/usr/bin/env python
# -*- coding: utf-8 -*-


import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#reference & credits: https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py

if __name__ == "__main__":

    #deletion [SSDL, OODL, VVDL, CCDL]
    minimal_means  = (0.347, 0.392, 0.318, 0.182)
    complete_means = (0.923, 0.950, 0.917, 0.808)

    #union of deletion operators [SODL, SVDL, SCDL, VCDL, SVCDL]
    minimal_means  = (0.460, 0.417, 0.382, 0.353, 0.440)
    complete_means = (0.966, 0.952, 0.939, 0.933, 0.960)

    ind = np.arange(len(minimal_means))  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects2 = ax.bar(ind + width/2, complete_means, width, color = 'firebrick', label='Complete')
    rects1 = ax.bar(ind - width/2, minimal_means, width, color = 'steelblue',label='Minimal')


    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_title('Effectiveness (Mutation Score)')
    ax.set_xticks(ind)
    ax.set_xticklabels(('SSDL', 'OODL', 'VVDL', 'CCDL')) #individual op
    ax.set_xticklabels(('SODL', 'SVDL', 'SCDL', 'VCDL', 'SVCDL')) #union op
    ax.legend()


    def autolabel(rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0, 'right': 1, 'left': -1}

        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(offset[xpos]*3, 3),  # use 3 points offset
                        textcoords="offset points",  # in both directions
                        ha=ha[xpos], va='bottom')


    autolabel(rects1, "left")
    autolabel(rects2, "right")

    fig.tight_layout()

    plt.show()