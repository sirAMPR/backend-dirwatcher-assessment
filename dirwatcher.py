import signal
import time
import argparse
import sys
import os

exit_flag = False
file_dictionary = {}


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name
    # logger.warn('Received ' + signal.Signals(sig_num).name)
    # exit_flag = True


def scan_single_file(file, magic_text):
    with open(file) as f:
        file_length = len(f.readlines())
        # TODO check for magic text
        # TODO add file to dictionary and last line read


def detect_added_files(file):
    pass


def detect_removed_files(directory):
    pass


def watch_directory(directory, magic_text, extension):
    # check if dictionary is empty
    if not file_dictionary:
        for file in os.listdir(directory):
            if file.endswith(extension):
                scan_single_file(file, magic_text)


def create_parser():
    """Creates an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--poll', help='polling interval')
    parser.add_argument('magic_text', help='string to search for')
    parser.add_argument(
        'ext', help='filters what kind of file extension to search within')
    parser.add_argument('directory', help='specify the directory to watch')
    return parser


def main(args):
    parser = create_parser()
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    polling_interval = parsed_args.poll if parsed_args.poll else 1

    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    while not exit_flag:
        try:
            # call my directory watching function
            watch_directory(parsed_args.directory,
                            parsed_args.magic_text, parsed_args.ext)
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            pass

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(polling_interval)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start


if __name__ == '__main__':
    main(sys.argv[1:])
