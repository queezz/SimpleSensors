import matplotlib.pylab as plt
import numpy as np
import datetime
import os
from pandas import read_csv
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters

def ticks_visual(ax,**kwarg):
    '''
    makes auto minor and major ticks for matplotlib figure
    makes minor and major ticks thicker and longer
    '''
    which = kwarg.get('which','both')
    from matplotlib.ticker import AutoMinorLocator
    if which == 'both' or which == 'x':
        ax.xaxis.set_minor_locator(AutoMinorLocator())
    if which == 'both' or which == 'y':
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    l1 = kwarg.get('l1',7)
    l2 = kwarg.get('l2',4)
    w1 = kwarg.get('w1',1.)
    w2 = kwarg.get('w2',.8)
    ax.xaxis.set_tick_params(width= w1,length = l1,which = 'major')
    ax.xaxis.set_tick_params(width= w2,length = l2,which = 'minor')
    ax.yaxis.set_tick_params(width= w1,length = l1,which = 'major')
    ax.yaxis.set_tick_params(width= w2,length = l2,which = 'minor')
    return

def grid_visual(ax, alpha = [.1,.3]):
    '''
    Sets grid on and adjusts the grid style.
    '''
    ax.grid(which = 'minor',linestyle='-', alpha = alpha[0])
    ax.grid(which = 'major',linestyle='-', alpha = alpha[1])
    return

def gritix(**kws):
    '''
    Automatically apply ticks_visual and grid_visual to the
    currently active pylab axes.
    '''
    import matplotlib.pylab as plt
    
    ticks_visual(plt.gca())
    grid_visual(plt.gca())
    return


def main():
    register_matplotlib_converters()

    lst = sorted([i for i in os.listdir('.') if '.txt' in i and '2020' in i])
    fname = lst[-1]
    data = read_csv(fname,na_values=['nan',' nan'])
    lbls = data.keys()

    t = [datetime.datetime.strptime(i, '%Y/%m/%d %H:%M:%S') for i in data['time']]

    nms = ['$T_1\ ^{\circ}$C','Humidity %','$T_2\ ^{\circ}$C']
    for j,i in enumerate(lbls[1:]):
        plt.plot(t,data[i],'-',label=nms[j])
        
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gca().set_ylim(0,80)
    
    ticks_visual(plt.gca())
    grid_visual(plt.gca())
    plt.savefig(
        os.path.join(
            os.path.expanduser('~'),
            'Desktop',
            fname[:-3]+'png',
       ),
       dpi=300,
       bbox_inches='tight',
    )

    #plt.show()
    
    
main()
