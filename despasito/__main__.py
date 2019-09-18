from .main import run
import sys
import os
import argparse
import logging
import logging.handlers

## Define parser functions and arguements
parser = argparse.ArgumentParser(description="DESPASITO: Determining Equilibrium State and Parametrization: Application for SAFT, Intended for Thermodynamic Output.  This is an open-source application for thermodynamic calculations and parameter fitting for the Statistical Associating Fluid Theory (SAFT) EOS and SAFT-𝛾-Mie coarse-grained simulations.")
parser.add_argument("filename", help="Input .json file with calculation instructions and path(s) to equation of state parameters. See documentation for explicit explanation. Compile docs or visit https://despasito.readthedocs.io")
parser.add_argument("-v", "--verbose", action="count", default=0, help="Verbose level, repeat up to three times.")
parser.add_argument("--log", nargs='?', const="despasito.log", help="Output a log file. The default name is despasito.log.")
parser.add_argument("-t", "--threads", type=int, help="Set the number of theads used. This hasn't been implemented yet.",default=1)

## Extract arguements
args = parser.parse_args()

## Handle arguements

# Logging
## Set up logging (refined after argparse)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Set up rotating log files
if args.log:
#    if args.log == "": args.log = "despasito.log"
    log_file_handler = logging.handlers.TimedRotatingFileHandler(args.log, when='M', interval=2)
    log_file_handler.setFormatter( logging.Formatter('%(asctime)s [%(levelname)s](%(name)s:%(funcName)s:%(lineno)d): %(message)s') )
    log_file_handler.setLevel(logging.DEBUG)
    logger.addHandler(log_file_handler)
# Set up logging to console
console_handler = logging.StreamHandler() # sys.stderr
console_handler.setLevel(logging.CRITICAL) # set later by set_log_level_from_verbose() in interactive sessions
console_handler.setFormatter( logging.Formatter('[%(levelname)s](%(name)s): %(message)s') )
logger.addHandler(console_handler)

if args.verbose == 0:
    console_handler.setLevel('ERROR')
elif args.verbose == 1:
    console_handler.setLevel('WARNING')
elif args.verbose == 2:
    console_handler.setLevel('INFO')
elif args.verbose >= 3:
    console_handler.setLevel('DEBUG')

logging.info("Input args: %r", args)

# Threads
# if args.threads != None:
#     threadcount = args.threads
# else:
#     threadcount = 1

# Run program
if args.filename:
    kwargs = {"filename":args.filename}
else:
    kwargs = {}

run(**kwargs)

