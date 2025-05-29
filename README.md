[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# bowtie2QC

A Python bowtie2 QC plotter

### Bowtie2 Mapping Log PE QC Plot
![image](https://github.com/user-attachments/assets/fd1b697a-a9fa-4494-9569-8f83d38fd376)

### Bowtie2 Mapping Overall Plot

![image](https://github.com/user-attachments/assets/d759103d-3963-4645-ad92-b784865a0c8a)



# Getting Started

## Install from pip

```
pip install bowtie2qc
```
see also [https://pypi.org/project/bowtie2qc/](https://pypi.org/project/bowtie2qc/)

# Usage

run ./examples/bowtie2QCExample.py with

./run_examples.sh

bowtie2QCExample.py:

```
import os
from bowtie2qc import bowtie2QC

current_path = os.path.abspath(os.getcwd())


def example_pdf():
    bowtie2QC.procress_logs_with_pdf([
        f"{current_path}/examples/example1.log",
        f"{current_path}/examples/example2.log",
        f"{current_path}/examples/example3.log"
    ])


if __name__ == '__main__':
    example_pdf()

```
