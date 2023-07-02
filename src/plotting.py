import statistics
import matplotlib.pyplot as plt

def plot_fill_between_min_max(values:list, axs:plt.Axes, label:str, c:str=None):
    x = range(len(values))
    y = values
    y1 = min(values)
    y2 = max(values)
    if c is None:
        axs.plot(x, y, '-', label=label)
        axs.fill_between(x, y1, y2, alpha=0.2)
    else:
        axs.plot(x, y, '-', label=label, color=c)
        axs.fill_between(x, y1, y2, alpha=0.2, color=c)

def plot_fill_between_mean_std(values:list, axs:plt.Axes, label:str, c:str=None):
    x = range(len(values))
    y = values
    y1 = min(values)
    y2 = max(values)
    if c is None:
        axs.plot(x, y, '-', label=label)
        axs.fill_between(x, y1, y2, alpha=0.2)
    else:
        axs.plot(x, y, '-', label=label, color=c)
        axs.fill_between(x, y1, y2, alpha=0.2, color=c)

def plot_matrix_fill_between_mean_min_max(values:list[list], axs:plt.Axes, label:str, c:str=None):
    x = range(len(values))
    inner_len = len(values[0])
    y = [sum(inner_values)/inner_len for inner_values in values]
    y1 = [min(inner_values) for inner_values in values]
    y2 = [max(inner_values) for inner_values in values]
    if c is None:
        axs.plot(x, y, '-', label=label)
        axs.fill_between(x, y1, y2, alpha=0.2)
    else:
        axs.plot(x, y, '-', label=label, color=c)
        axs.fill_between(x, y1, y2, alpha=0.2, color=c)

def plot_matrix_fill_between_mean_std(values:list[list], axs:plt.Axes, label:str, c:str=None):
    x = range(len(values))
    inner_len = len(values[0])
    mean_values = [sum(inner_values)/inner_len for inner_values in values]
    stds = [statistics.pstdev(inner_values) for inner_values in values]
    y = mean_values
    y1 = [mean+std for mean, std in zip(mean_values, stds)]
    y2 = [mean-std for mean, std in zip(mean_values, stds)]
    if c is None:
        axs.plot(x, y, '-', label=label)
        axs.fill_between(x, y1, y2, alpha=0.2)
    else:
        axs.plot(x, y, '-', label=label, color=c)
        axs.fill_between(x, y1, y2, alpha=0.2, color=c)