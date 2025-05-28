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
        f'{data["title_name"]}\nConcordant N',
        f'{data["title_name"]}\nConcordant=0`s Breakdown\n(Discordant N)',
        f'{data["title_name"]}\nMate-Level N'
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

def get_dynamic_fontsize(num_items, axis_size, min_size=3, max_size=10, scale=0.6):
    size = axis_size / num_items * scale
    return max(min(size, max_size), min_size)

def plot_overall_plot(data, ax):
    total_reads = [val['total_reads'] for val in data]
    alignment_rates = [val['overall_alignment_rate'] for val in data]
    labels = [val['title_name'] for val in data]
    num_items = len(data)

    fig = ax[0].get_figure()
    fig.canvas.draw()

    bbox_y = ax[0].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    height_px = bbox_y.height * fig.dpi
    y_fontsize = get_dynamic_fontsize(num_items, height_px, max_size=5, scale=0.15)

    bbox_x = ax[0].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width_px = bbox_x.width * fig.dpi
    x_fontsize = get_dynamic_fontsize(num_items, width_px, min_size=3, max_size=5, scale=0.15)

    ax[0].barh(range(num_items), total_reads, align='center', color='#078282', label='Total Reads')
    ax[0].set_yticks(range(num_items))
    ax[0].set_yticklabels(labels, fontsize=y_fontsize)
    ax[0].set_xlabel('Reads', fontsize=x_fontsize)
    ax[0].tick_params(axis='x', labelsize=x_fontsize)
    ax[0].set_title('Overall Reads', fontsize=x_fontsize)
    ax[0].legend(fontsize=x_fontsize)

    for i, val in enumerate(total_reads):
        ax[0].text(val + max(total_reads) * 0.01, i, f'{val:,}', 
                   va='center', ha='left', fontsize=x_fontsize, color='black')
    ax[1].barh(range(num_items), alignment_rates, align='center', color='#0ababa')
    ax[1].set_xlabel('Alignment Rate (%)', fontsize=x_fontsize)
    ax[1].tick_params(axis='x', labelsize=x_fontsize)
    ax[1].set_title('Overall Alignment Rates', fontsize=x_fontsize)
    ax[1].tick_params(axis='y', left=False, labelleft=False)

    for i, val in enumerate(alignment_rates):
        ax[1].text(val + max(alignment_rates) * 0.01, i, f'{val:.2f}%', 
                   va='center', ha='left', fontsize=x_fontsize, color='black')
