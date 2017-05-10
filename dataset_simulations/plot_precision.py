"""Calc and store precision and recall

Usage:
  plot_precision.py 
"""

import glob
import json

import matplotlib.pyplot as plt
import os
from docopt import docopt
from cycler import cycler

if __name__ == '__main__':
    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +
                           cycler('linestyle', ['-', '--', ':', '-.' ])))
    arguments = docopt(__doc__)
    graph_data = {}
    legend_names = []
    precision_fig = plt.figure()
    precision_plot = precision_fig.add_subplot(111)
    recall_fig = plt.figure()
    recall_plot = recall_fig.add_subplot(111)
    for filename in glob.glob('*/*/pr_spread*.json'):
        with open(filename) as f:
            pr_spread_json = json.load(f)

        threshold = pr_spread_json['threshold']
        precision = pr_spread_json['precision']['mean']
        recall = pr_spread_json['recall']['mean']
        if threshold < 1:
            legend_name = os.path.join(*filename.split('/')[:2])
            if legend_name not in graph_data:
                legend_names.append(legend_name)
                graph_data[legend_name] = {
                    'x': [],
                    'precision': [],
                    'recall': []
                }
            graph_data[legend_name]['x'].append(threshold)
            graph_data[legend_name]['precision'].append(precision)
            graph_data[legend_name]['recall'].append(recall)

    graph_x = []
    graph_y = []
    for name in legend_names:
        precision_plot.plot(graph_data[name]['x'], graph_data[name]['precision'])
        recall_plot.plot(graph_data[name]['x'], graph_data[name]['recall'])
    # Shrink current axis by 20%
    box = precision_plot.get_position()
    precision_plot.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    precision_plot.legend(legend_names, loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 7})
    box = recall_plot.get_position()
    recall_plot.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    recall_plot.legend(legend_names, loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 7})
    precision_fig.savefig('precision.png', dpi=100)
    recall_fig.savefig('recall.png', dpi=100)
