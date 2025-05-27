def plot_bar(ax, labels, sizes, title, **kwargs):
    '''
    plot bar
    '''
    color = kwargs.get('color', '#078282')
    ax.barh(range(len(labels)), sizes, align='center', color=color)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=5)
    ax.set_xlabel('Reads', fontsize=5)
    ax.set_title(title, fontsize=5)
    for idx, value in enumerate(sizes):
        ax.text(value + 10, idx, f'{value:.2f}%', va='center', fontsize=5)
    ax.set_xlim(1, 100)
    ax.tick_params(axis='both', labelsize=5)


def plot_bars_of_bowtie2_log(data, ax):
    '''
    plot bars of a bowtie2 pe log
    '''
    labels_sets = [['0', '1', '>1'], ['1', '0'], ['0', '1', '>1']]

    sizes_sets = [[
        data['concordant_0']['percent'], data['concordant_1']['percent'],
        data['concordant_more']['percent']
    ],
                  [
                      data['discordant_1']['percent'],
                      data['concordant_0']['percent'] +
                      data['discordant_1']['percent']
                  ],
                  [
                      data['mate_0']['percent'], data['mate_1']['percent'],
                      data['mate_more']['percent']
                  ]]

    titles = [
        f'{data["log_file"]}\nConcordant N',
        f'{data["log_file"]}\nConcordant=0`s Breakdown\n(Discordant N)',
        f'{data["log_file"]}\nMate-Level N'
    ]

    colors = ['#078282', '#0ababa', '#03fffa']
    offsets = [500000, 500000, 100000]

    for i in range(3):
        plot_bar(ax[i],
                 labels_sets[i],
                 sizes_sets[i],
                 titles[i],
                 offset=offsets[i],
                 color=colors[i])

def plot_overall_plot(data, ax):
    total_reads = [val['total_reads'] for val in data]
    concordant_0 = [val['concordant_0']['count'] for val in data]
    concordant_1 = [val['concordant_1']['count'] for val in data]
    concordant_more = [
        val['concordant_more']['count'] for val in data
    ]

    ax[0].barh(range(len(data)),
               concordant_0,
               align='center',
               color='#078282',
               label='Concordant 0 times')
    ax[0].barh(range(len(data)),
               concordant_1,
               align='center',
               color='#0ababa',
               label='Concordant 1 time')
    ax[0].barh(range(len(data)),
               concordant_more,
               align='center',
               color='#c3ffff',
               label='Concordant >1 times')

    ax[0].set_yticks(range(len(data)))
    ax[0].set_yticklabels([val['log_file'] for val in data],
                          fontsize=5)  # 調整字體大小
    ax[0].set_xlabel('Reads', fontsize=5)
    ax[0].set_title('Overall Concordant Alignment', fontsize=5)
    ax[0].legend(fontsize=5)

    alignment_rates = [val['overall_alignment_rate'] for val in data]
    ax[1].barh(range(len(data)),
               alignment_rates,
               align='center',
               color='#0ababa')
    ax[1].set_yticks(range(len(data)))
    ax[1].set_yticklabels([val['log_file'] for val in data],
                          fontsize=5)  # 調整字體大小
    ax[1].set_xlabel('Alignment Rate (%)', fontsize=5)
    ax[1].set_title('Overall Alignment Rates', fontsize=5)