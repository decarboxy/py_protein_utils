#!/usr/bin/env python
from distutils.core import setup

setup(
    name='proteinutils',
    version='1.0',
    #package_dir = {'':'lib'},
    packages = ['rosettautil',
                'rosettautil.graphics',
                'rosettautil.protein',
                'rosettautil.rosetta'
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
