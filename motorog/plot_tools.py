import matplotlib.pyplot as plt
import indexes 

def plot(y,title='Plot'):
    plt.ion()
    fig = plt.figure ()
    fig.canvas.set_window_title(title)
    ax = fig.add_subplot ('111')
    plt.title(title)
    ax.plot(y, linewidth=3.0)
    return fig, ax

def plot2(x,y,title='Plot'):
    plt.ion()
    fig = plt.figure ()
    fig.canvas.set_window_title(title)
    ax = fig.add_subplot ('111')
    plt.title(title)
    ax.plot(x, y, linewidth=3.0)
    return fig, ax

def plotCoordinate(x,name):
    plot(x[:,indexes.coordinateIndex(name)])
