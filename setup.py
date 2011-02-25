#!/usr/bin/env python
from distutils.core import setup
import sys

try:
    import Bio
except ImportError:
    sys.exit("Biopython must be installed")

try:
    import matplotlib
except ImportError:
    print "matplotlib is not installed, so you won't be able to use the graphics library"
    #sys.exit("matplotlib is not installed, you won't be able to use the graphics libraries")

setup(
    name='rosettautils',
    version='1.0',
    description='Rosetta analysis tools',
    author='Sam DeLuca',
    author_email='samuel.l.deluca@vanderbilt.edu',
    url='https://github.com/decarboxy/py_protein_utils/',
    packages = ['rosettautil',
                'rosettautil.graphics',
                'rosettautil.protein',
                'rosettautil.rosetta',
                'rosettautil.util'
                ],
    scripts = [
                'scripts/best_models.py',
                'scripts/clustering.py',
                'scripts/pdb_renumber.py',
                'scripts/remove_loop_coords.py',
                'scripts/score_scatter_plot.py',
                'scripts/score_vs_rmsd.py',
                'scripts/sequence_recovery.py',
                'scripts/thread_pdb_from_alignment.py',
                'scripts/top_n_percent.py'
                ]
    )
