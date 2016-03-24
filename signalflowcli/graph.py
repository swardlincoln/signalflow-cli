#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 SignalFx, Inc. All Rights Reserved.

from __future__ import print_function

import argparse
import matplotlib.pyplot as plt
import pandas
import six
import StringIO
import sys
import tslib

from .tzaction import TimezoneAction


def render(csv, tz):
    """Render the given CSV data as simple graph.

    :param csv: A block of CSV data, either as a string, a StringIO instance,
        or a generator of lines of CSV text data.
    :param tz: The display timezone for the time axis.
    """
    if isinstance(csv, six.string_types):
        buf = StringIO.StringIO(csv)
    if isinstance(csv, StringIO.StringIO):
        buf = csv
    if callable(getattr(csv, 'read')):
        buf = csv
    else:
        buf = StringIO.StringIO()
        for line in csv:
            print(line, file=buf)
        buf.seek(0)

    df = pandas.read_csv(buf, index_col=0,
                         parse_dates=True,
                         date_parser=tslib.parse_input)
    df = df.set_index(df.index.tz_convert(tz))

    print('Computation complete; got {0} datapoints for {1} from {2} to {3}'
          .format(len(df), df.index[-1] - df.index[0],
                  df.index[0], df.index[-1]))

    plt.style.use('ggplot')
    df.plot()
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description='Simple CSV data plotting utility')
    parser.add_argument('input', nargs='?', type=file, default=sys.stdin,
                        help='read data from file (use \'-\' for stdin)')
    TimezoneAction.add_to_parser(parser)
    options = parser.parse_args()
    render(options.input, options.timezone)
    return 0