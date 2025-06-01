'''
example plot
'''
import os
from bowtie2qc import bowtie2QC

current_path = os.path.abspath(os.getcwd())


def example_pdf():
    bowtie2QC.procress([
        f"{current_path}/examples/example1.log",
        f"{current_path}/examples/example2.log",
        f"{current_path}/examples/example3.log"
    ],output_format='pdf')


if __name__ == '__main__':
    example_pdf()
