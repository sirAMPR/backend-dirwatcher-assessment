import signal
import time
import argparse
import sys

exit_flag = False


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name
    logger.warn('Received ' + signal.Signals(sig_num).name)
    exit_flag = True


def create_parser():
    """Creates an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('poll', help='polling interval')
    parser.add_argument('magic_text', help='string to search for')
    parser.add_argument(
        'ext', help='filters what kind of file extension to search within')
    parser.add_argument('directory', help='specify the directory to watch')

    return parser


def main(args):
    parser = create_parser()

    if not args():
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    polling_interval = parsed_args.poll

    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    while not exit_flag:
        try:
            # call my directory watching function
            pass
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            pass

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(polling_interval)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start


if '__name__' == '__main__':
    main(sys.argv[1:])
