import logging
from argparse import ArgumentParser
from vilma import VERSION
from vilma.make_ld_schema import main as make_ld_schema
from vilma.make_ld_schema import args as make_ld_schema_args
from vilma.check_ld_schema import main as check_ld_schema
from vilma.check_ld_schema import args as check_ld_schema_args
from vilma.sim import main as sim
from vilma.sim import args as sim_args
from vilma.vi_options import main as fit
from vilma.vi_options import args as fit_args
from numba import gdb

COMMANDS = {
    'make_ld_schema': {'cmd': make_ld_schema, 'parser': make_ld_schema_args},
    'check_ld_schema': {'cmd': check_ld_schema,
                        'parser': check_ld_schema_args},
    'sim': {'cmd': sim, 'parser': sim_args},
    'fit': {'cmd': fit, 'parser': fit_args},
}


#''
parser = ArgumentParser(
    description="""
    vilma v%s uses variational inference to estimate variant
    effect sizes from GWAS summary data while simultaneously
    learning the overall distribution of effects.
    """ % VERSION,
    usage='vilma <command> <options>'
)

subparsers = parser.add_subparsers(title='Commands', dest='command')
for cmd in COMMANDS:
    cmd_parser = COMMANDS[cmd]['parser'](subparsers)
    cmd_parser.add_argument(
        '--logfile',
        required=False,
        type=str,
        default='',
        help='File to store information about the vilma run. To print to '
        'stdout use "-". Defaults to no logging.'
    )
    cmd_parser.add_argument(
        '--verbose',
        dest='verbose',
        action='store_true',
        help='Log all information (as opposed to just warnings)'
    )
args = parser.parse_args(['fit',
                          '--logfile',
                          '-',
	                  '--sumstats', '/home/ni905586/Repos/vilma/example/example_data/example_gwas_sumstats.txt',
	                  '--output', '/home/ni905586/Repos/vilma/example/example_vilma_run',
	                  '--ld-schema', '/home/ni905586/Repos/vilma/example/ld_mat/example_schema.schema',
	                  '--seed','42',
	                  '-K', '81',
	                  '--init-hg', '0.2',
	                  '--samplesizes', '300e3',
                          '--verbose',
	                  '--names', 'ukbb',
	                  '--learn-scaling',
	                  '--extract', '/home/ni905586/Repos/vilma/example/keep_variants.txt'])

func = COMMANDS[args.command]['cmd']
func(args)
