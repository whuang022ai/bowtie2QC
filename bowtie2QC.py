import re


def auto_cast(value):
    '''
    cast value to int or float from str
    '''
    return float(value) if '.' in value else int(value)


def parse_bowtie2_log(log_file):
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
    return stats


data = parse_bowtie2_log("test.log")
print(data)
