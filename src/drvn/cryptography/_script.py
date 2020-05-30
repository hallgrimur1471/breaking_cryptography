import logging
import argparse

import drvn.cryptography.example_module
import drvn.cryptography._logging as drvn_logger


def main():
    args = _parse_arguments()

    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    drvn_logger.configure(log_level)

    logging.info(drvn.cryptography.example_module.example_public_function())


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.description = ""
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enables printing of debug statements",
    )
    arguments = parser.parse_args()
    return arguments