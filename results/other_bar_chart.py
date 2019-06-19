#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":  

    #chose the target
    print("1 - Phase One Data")
    print("2 - Best results (Phase two)")
    condition = input("Informe the target data: ")

    if condition == 2:
        target = "analyzes/best_all_data.csv"
    else:
        target = "analyzes/phase_one_data.csv"

    # Prepare Data
    df_raw = pd.read_csv(target)
    df = df_raw[['n_tc', 'ms' ,'op']].groupby('op').apply(lambda x: x.mean())
    df.sort_values('n_tc', inplace=True)
    df.reset_index(inplace=True)

    # Draw plot
    import matplotlib.patches as patches

    fig, ax = plt.subplots(figsize=(16,10), facecolor='white', dpi= 80)
    ax.vlines(x=df.index, ymin=0, ymax=df.n_tc, color='cornflowerblue', alpha=0.7, linewidth=20)

    # Annotate Text
    for i, i_ms in enumerate(df.ms):
        ax.text(i, df.n_tc[i] + 2 , 'ms = {}'.format(round(i_ms, 3)), horizontalalignment='center')
    #i_ms + 25.5

    # Title, Label, Ticks and Ylim
    #ax.set_title('Bar Chart for Highway Mileage', fontdict={'size':22})
    ax.set(xlabel= 'Operators', ylabel='Number of test cases', ylim=(0, 450))
    plt.xticks(df.index, df.op.str.upper(), rotation=60, horizontalalignment='right', fontsize=12)

    # Add patches to color the X axis labels
    p1 = patches.Rectangle((.57, -0.005), width=.33, height=.13, alpha=.1, facecolor='green', transform=fig.transFigure)
    p2 = patches.Rectangle((.124, -0.005), width=.446, height=.13, alpha=.1, facecolor='red', transform=fig.transFigure)
    ax.add_artist(p1)
    ax.add_artist(p2)
    plt.show()