import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import itertools

def graph_BloxPot(graphTitle, data, randomDists, xLabel, yLabel):

    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.canvas.set_window_title(graphTitle)
    plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)

    # Hide these grid behind plot objects
    ax1.set_axisbelow(True)
    #ax1.set_title('Comparison of IID Bootstrap Resampling Across Five Distributions')
    ax1.set_xlabel(xLabel)
    ax1.set_ylabel(yLabel)

    # Now fill the boxes with desired colors
    boxColors = ['royalblue'] #'darkkhaki', 
    numBoxes = 4
    medians = list(range(numBoxes))
    #boxCoords = [[]]
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        boxCoords = list(zip(boxX, boxY))
        # Alternate between Dark Khaki and Royal Blue
        
        #k = i % 2
        #facecolor=boxColors[k]
        
        #boxPolygon = Polygon(boxCoords[i], facecolor='royalblue')
        boxPolygon = Polygon(boxCoords, facecolor='royalblue')
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            plt.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        plt.plot([np.average(med.get_xdata())], [np.average(data[i])],
                 color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    #ax1.set_xlim(0.5, numBoxes + 0.5)
    ax1.set_xlim(0.4, numBoxes + 0.4)
    top = max(list(itertools.chain.from_iterable(data)))
    bottom = min(list(itertools.chain.from_iterable(data)))
    ax1.set_ylim(bottom, top)
    xtickNames = plt.setp(ax1, xticklabels=randomDists)
    plt.setp(xtickNames, rotation=45, fontsize=8)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes) + 1
    upperLabels = [str(np.round(s, 2)) for s in medians]
    weights = ['bold', 'semibold']
    for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
        k = tick % 2
        ax1.text(pos[tick], top + (top * 0.01), upperLabels[tick],
                 horizontalalignment='center', size='small', weight=weights[k],
                 color='black')

    plt.show()

if __name__ == '__main__':

    #Independent Variables
    operators = ['SSDL', 'OODL', 'VVDL', 'CCDL']
    xLabel = 'Deletion operators'

    #MPTitle
    yLabel = 'Mutation Score' #Rate of Occurrence of Anomaly

    ssdl = [0.326087, 0.20000010000000001, 0.6, 0.42000010000000004, 0.1571427, 0.31875, 0.43333320000000003, 0.2634918, 0.2833331, 0.24, 0.32999999999999996, 0.36, 0.4857142, 0.1999999, 0.46666660000000004, 0.44285699999999995, 0.44285699999999995, 0.4846153, 0.43333320000000003, 0.38, 0.2999997, 0.3, 0.3772725, 0.45, 0.3428569, 0.36, 0.29999980000000004, 0.3125, 0.24722209999999997, 0.2, 0.3514287225, 0.3, 0.20714280000000002, 0.2428569, 0.1999998, 0.4000001, 0.25, 0.8714287000000001]

    oodl = [0.3913044 ,0.1941179 ,0.3125 ,0.23666649999999997 ,0.1999999 ,0.38125 ,0.3999998 ,0.3444441 ,0.3333332 ,0.33999999999999997 ,0.41 ,0.45999999999999996 ,0.7714288 ,0.2866668 ,0.29999980000000004 ,0.657143 ,0.4571428 ,0.6076927000000001 ,0.43333320000000003 ,0.8 ,0.5190479 ,0.27999999999999997 ,0.2818181 ,0.5833334 ,0.3999998 ,0.36 ,0.1999998375 ,0.31666669999999997 ,0.3625 ,0.2457143275 ,0.4 ,0.2571429 ,0.571429 ,0.1999998 ,0.431579 ,0.25 ,0.6714289]

    vvdl = [0.1956523, 0.17647079999999998, 0.3, 0.1966667, 0.1999999, 0.19375, 0.2999997, 0.222222, 0.3333332308, 0.32999999999999996, 0.27999999999999997, 0.5285716, 0.1733333, 0.29999980000000004, 0.657143, 0.3999997, 0.4230766, 0.43333320000000003, 0.54, 0.2333331, 0.27999999999999997, 0.24090910000000001, 0.5333334, 0.3714283, 0.36, 0.1999998, 0.2625, 0.2472222, 0.25, 0.1257143275, 0.38, 0.2428571, 0.428571, 0.1999998, 0.24736829999999999, 0.25, 0.6571431999999999]

    ccdl = [0.0739132, 0.052941499999999996, 0.2, 0.12666660000000002, 0.0999999, 0.23125, 0.1999998, 0.1873014, 0.2833331192, 0.37, 0.38, 0.2142855, 0.2400001, 0.0, 0.22857120000000003, 0.3428569, 0.2615382, 0.333333, 0.38, 0.2333331, 0.0, 0.1136366, 0.3499999, 0.07142849999999999, 0.16, 0.1999998125, 0.10833319999999999, 0.1125, 0.13999999999999999, 0.0, 0.26, 0.10714300000000002, 0.0, 0.1999998, 0.1263158, 0.25, 0.042857099999999995]

    data = [ssdl, oodl, vvdl, ccdl] 

    graph_BloxPot(operators, data, operators, xLabel, yLabel)   

    # version on R
    # SSDL <- c(1,2,3,4,5,6) #points
    # DF <- data.frame(SSDL, OODL, VVDL, CCDL)
    # boxplot(DF, col=c("#B0E0E6", "#FFE4E1", "#CD5454", "#A8A8A8"), ylim = c(0, 1), ylab = 'Mutation Score', xlab = 'Deletion operators')