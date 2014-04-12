# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# filters.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge
import os
import sys
import getopt
import weka.core.jvm as jvm
from weka.core.classes import OptionHandler
from weka.core.converters import Loader
from weka.core.converters import Saver
from weka.core.dataset import Instances
from weka.core.dataset import Instance


class Filter(OptionHandler):
    """
    Wrapper class for filters.
    """

    def __init__(self, classname):
        """
        Initializes the specified filter.
        :param classname: the classname of the filter
        """
        jobject = Filter.new_instance(classname)
        self.enforce_type(jobject, "weka.filters.Filter")
        super(Filter, self).__init__(jobject)

    def set_inputformat(self, data):
        """
        Sets the input format.
        :param data: the data to use as input
        """
        return javabridge.call(self.jobject, "setInputFormat", "(Lweka/core/Instances;)Z", data.jobject)

    def input(self, inst):
        """
        Inputs the Instance.
        :param inst: the instance to filter
        """
        return javabridge.call(self.jobject, "input", "(Lweka/core/Instance;)Z", inst.jobject)

    def output(self):
        """
        Outputs the filtered Instance.
        :rtype : an Instance object
        """
        return Instance(javabridge.call(self.jobject, "output", "()Lweka/core/Instance;"))

    def filter(self, data):
        """
        Filters the dataset.
        :param data: the Instances to filter
        :rtype : the filtered Instances object
        """
        return Instances(javabridge.static_call(
            "Lweka/filters/Filter;", "useFilter",
            "(Lweka/core/Instances;Lweka/filters/Filter;)Lweka/core/Instances;",
            data.jobject, self.jobject))


def main(args):
    """
    Runs a filter from the command-line. Calls JVM start/stop automatically.
    Options:
        -j jar1[:jar2...]
        -i input1
        -o output1
        [-r input2]
        [-s output2]
        [-c classindex]
        filter classname
        [filter options]
    """

    usage = "Usage: weka.filters -j jar1[" + os.pathsep + "jar2...] -i input1 -o output1 " \
            + "[-r input2 -s output2] [-c classindex] filterclass [filter options]"
    optlist, args = getopt.getopt(args, "j:i:o:r:s:c:h")
    if len(args) == 0:
        raise Exception("No filter classname provided!\n" + usage)
    for opt in optlist:
        if opt[0] == "-h":
            print(usage)
            return

    jars    = []
    input1  = None
    output1 = None
    input2  = None
    output2 = None
    cls     = "-1"
    for opt in optlist:
        if opt[0] == "-j":
            jars = opt[1].split(os.pathsep)
        elif opt[0] == "-i":
            input1 = opt[1]
        elif opt[0] == "-o":
            output1 = opt[1]
        elif opt[0] == "-r":
            input2 = opt[1]
        elif opt[0] == "-s":
            output2 = opt[1]
        elif opt[0] == "-c":
            cls = opt[1]

    # check parameters
    if input1 is None:
        raise Exception("No input file provided ('-i ...')!")
    if output1 is None:
        raise Exception("No output file provided ('-o ...')!")
    if not input2 is None and output2 is None:
        raise Exception("No 2nd output file provided ('-s ...')!")

    jvm.start(jars)
    try:
        flter = Filter(args[0])
        args = args[1:]
        if len(args) > 0:
            flter.set_options(args)
        loader = Loader("weka.core.converters.ArffLoader")
        in1 = loader.load_file(input1)
        if str(cls) == "first":
            cls = "0"
        if str(cls) == "last":
            cls = str(in1.num_attributes() - 1)
        in1.set_class_index(int(cls))
        flter.set_inputformat(in1)
        out1 = flter.filter(in1)
        saver = Saver("weka.core.converters.ArffSaver")
        saver.save_file(out1, output1)
        if not input2 is None:
            in2 = loader.load_file(input2)
            in2.set_class_index(int(cls))
            out2 = flter.filter(in2)
            saver.save_file(out2, output2)
    except Exception, ex:
        print(ex)
    finally:
        jvm.stop()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception, e:
        print(e)