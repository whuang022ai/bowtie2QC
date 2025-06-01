'''
The bowtie2 qc log procress
'''
import re
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from .bowtie2QCPlot import plot_bars_of_bowtie2_log
from .bowtie2QCPlot import plot_overall_plot


def auto_cast(value):
    '''
    cast value to int or float from str
    '''
    return float(value) if '.' in value else int(value)


def parse_bowtie2_log(log_file: str):
    '''
    parse bowtie2 log of Pair-End mapping
    input : bowtie2 log file path
    output : stats kv pairs
    '''
    stats = {
        'total_reads': 0,
        'overall_alignment_rate': 0.0,
        'concordant_0': {},
        'concordant_1': {},
        'concordant_more': {},
        'discordant_1': {},
        'mate_0': {},
        'mate_1': {},
        'mate_more': {},
    }

    patterns = {
        'total_reads': r'(\d+) reads;',
        'concordant_0':
        r'(\d+)\s+\(([\d.]+)%\)\s+aligned concordantly 0 times',
        'concordant_1':
        r'(\d+)\s+\(([\d.]+)%\)\s+aligned concordantly exactly 1 time',
        'concordant_more':
        r'(\d+)\s+\(([\d.]+)%\)\s+aligned concordantly >1 times',
        'discordant_1': r'(\d+)\s+\(([\d.]+)%\)\s+aligned discordantly 1 time',
        'mate_0': r'(\d+)\s+\(([\d.]+)%\)\s+aligned 0 times',
        'mate_1': r'(\d+)\s+\(([\d.]+)%\)\s+aligned exactly 1 time',
        'mate_more': r'(\d+)\s+\(([\d.]+)%\)\s+aligned >1 times',
        'overall_alignment_rate': r'([\d.]+)% overall alignment rate',
    }

    with open(log_file, encoding='utf-8') as file:
        for line in file:
            for key, pattern in patterns.items():
                match = re.search(pattern, line)
                if not match:
                    continue
                groups = match.groups()
                if len(groups) == 1:
                    stats[key] = auto_cast(groups[0])
                elif len(groups) == 2:
                    stats[key] = {
                        'count': auto_cast(groups[0]),
                        'percent': auto_cast(groups[1])
                    }

    stats['log_file'] = log_file
    stats['title_name'] = os.path.basename(log_file).split('.')[0]
    return stats


def procress_logs(log_files: list):
    '''
    procress bowtie logs to combine fig
    '''
    fig, ax = plt.subplots(len(log_files), 3, figsize=(8.27, 11.69))
    for i, log_file in enumerate(log_files):
        data = parse_bowtie2_log(log_file)
        plot_bars_of_bowtie2_log(data, ax[i])
    plt.savefig(f"tmp.png")
    plt.close(fig)


def procress_logs_with_png(log_files: list):
    all_data = collect_bowtie2_log_data(log_files)
    fig = generate_sample_plot(all_data, for_pdf=False)
    fig_overall = generate_overall_plot(all_data, for_pdf=False)

    fig.savefig('page1.png', dpi=300)
    fig_overall.savefig('page2.png', dpi=300)

    plt.close(fig)
    plt.close(fig_overall)


def procress_logs_with_pdf(log_files: list):
    all_data = collect_bowtie2_log_data(log_files)
    fig = generate_sample_plot(all_data, for_pdf=True)
    fig_overall = generate_overall_plot(all_data, for_pdf=True)

    with PdfPages('bowtie2_alignment_results.pdf') as pdf:
        pdf.savefig(fig)
        pdf.savefig(fig_overall)

    plt.close(fig)
    plt.close(fig_overall)


def collect_bowtie2_log_data(log_files: list):
    all_data = []
    for log_file in log_files:
        data = parse_bowtie2_log(log_file)
        flat_data = {
            'title_name': data['title_name'],
            'log_file': data['log_file'],
            'total_reads': data['total_reads'],
            'overall_alignment_rate': data['overall_alignment_rate'],
        }
        for key in [
                'concordant_0', 'concordant_1', 'concordant_more',
                'discordant_1', 'mate_0', 'mate_1', 'mate_more'
        ]:
            flat_data[f'{key}_count'] = data[key]['count']
            flat_data[f'{key}_percent'] = data[key]['percent']
        flat_data["raw_data"] = data
        all_data.append(flat_data)
    return all_data


def generate_sample_plot(all_data, for_pdf=True):
    n = len(all_data)

    if for_pdf:
        fig_size = (8.27, 11.69)  # A4
    else:
        fig_size = (10, 3 * n)

    fig, ax = plt.subplots(n, 3, figsize=fig_size)
    if n == 1:
        ax = [ax]

    for i, item in enumerate(all_data):
        plot_bars_of_bowtie2_log(item['raw_data'], ax[i])

    if for_pdf:
        fig.subplots_adjust(left=0.15,
                            right=0.9,
                            top=0.9,
                            bottom=0.55,
                            hspace=0.6)
    else:
        fig.tight_layout()

    return fig


def generate_overall_plot(all_data, for_pdf=True):
    if for_pdf:
        fig_size = (8.27, 11.69)
    else:
        fig_size = (12, 5)

    fig, ax = plt.subplots(1, 2, figsize=fig_size, sharey=True)

    plot_overall_plot(all_data, ax)

    if for_pdf:
        fig.subplots_adjust(left=0.25,
                            right=0.75,
                            top=0.95,
                            bottom=0.75,
                            hspace=0.15)
    else:
        fig.tight_layout()

    return fig


def procress(log_files: list, output_format: str = 'pdf'):
    assert output_format in ['pdf',
                             'png'], "output_format must be 'pdf' or 'png'"
    if output_format == 'pdf':
        procress_logs_with_pdf(log_files)
    else:
        procress_logs_with_png(log_files)
