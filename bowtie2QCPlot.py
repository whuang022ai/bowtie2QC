
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
        ax.text(value + offset, idx, f'{percentage:.1f}%', va='center', fontsize=5)

    ax.set_xlim(1, max(sizes) * 20 if max(sizes) > 0 else 10)
    ax.set_xscale('log')
    ax.tick_params(axis='both', labelsize=5)