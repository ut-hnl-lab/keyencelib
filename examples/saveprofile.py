from argparse import ArgumentParser
from keyencelib import Profiler


def measure(savedir, n_measure):
    profiler = Profiler(savedir=savedir)
    with profiler.open():
        for n in range(n_measure):
            profiler.get(tag=f'data-{n}')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-s', '--savedir', help='Save directory', default=None)
    parser.add_argument(
        '-n', '--number', help='Number of measurements', default=1)
    args = parser.parse_args()
    measure(args.savedir, int(args.number))
