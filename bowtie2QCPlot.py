def plot_bar(ax, labels, sizes, title, **kwargs):
    '''
    plot bar
    '''
    offset = kwargs.get('offset', 500000)
    color = kwargs.get('color', '#078282')

    total = sum(sizes)
    ax.barh(range(len(labels)), sizes, align='center', color=color)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=5)
    ax.set_xlabel('Reads', fontsize=5)
    ax.set_title(title, fontsize=5)

    for idx, value in enumerate(sizes):
        percentage = (value / total) * 100 if total else 0
        ax.text(value + offset,
                idx,
                f'{percentage:.1f}%',
                va='center',
                fontsize=5)

    ax.set_xlim(1, max(sizes) * 20 if max(sizes) > 0 else 10)
    ax.set_xscale('log')
    ax.tick_params(axis='both', labelsize=5)


def plot_bars_of_bowtie2_log(data, ax):
    '''
    plot bars of a bowtie2 pe log
    '''
    labels_sets = [['0', '1', '>1'], ['1', '0'], ['0', '1', '>1']]

    sizes_sets = [[
        data['concordant_0']['count'], data['concordant_1']['count'],
        data['concordant_more']['count']
    ],
                  [
                      data['discordant_1']['count'],
                      data['concordant_0']['count'] +
                      data['discordant_1']['count']
                  ],
                  [
                      data['mate_0']['count'], data['mate_1']['count'],
                      data['mate_more']['count']
                  ]]

    titles = [
        f'{data["log_file"]}\nConcordant N',
        f'{data["log_file"]}\nConcordant=0`s Breakdown\n(Discordant N)',
        f'{data["log_file"]}\nMate-Level N'
    ]

    colors = ['#078282', '#0ababa', '#c3ffff']
    offsets = [500000, 500000, 100000]

    for i in range(3):
        plot_bar(ax[i],
                 labels_sets[i],
                 sizes_sets[i],
                 titles[i],
                 offset=offsets[i],
                 color=colors[i])
