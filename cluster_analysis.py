from util import *


class ClusterAnalysis:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename)
        self.cluster_name = ''
        self.collect_info()

    def collect_info(self):
        cluster_line = self.file.readline()
        self.cluster_name = cluster_line.split(' ', 1)[1].strip()
        print(self.cluster_name)  # cluster name -> sheet name
        line = self.file.readline()
        while line != '':
            if not_empty_line(line):
                if line.startswith('%'):  # sub module
                    substr = line.strip().split(' ', 1)
                    print('fuse name:\t' + substr[0])  # sub module name
                    substr = substr[1].strip('{').split(' -> ')
                    print(substr)  # input & output
                    line = self.file.readline()  # {}
                    while not line.startswith('}'):
                        if not_empty_line(line):
                            # op analysis
                            op = self.op_analysis(line.strip())
                            print('ID: ' + op.ID)
                            print('input: ' + op.inputs)
                            print('output: ' + op.outputs)
                            print('others: ' + op.other)

                        else:
                            pass
                        line = self.file.readline()
                elif line.startswith('ENTRY'):  # main module
                    substr = line.strip().split(' ', 2)
                    print(len(substr))
                    line = self.file.readline()  # {}
                    while not line.startswith('}'):
                        if not_empty_line(line):
                            op = self.op_analysis(line.strip())
                            print('ID: ' + op.ID)
                            print('input: ' + op.inputs)
                            print('output: ' + op.outputs)
                            print('others: ' + op.other)
                        else:
                            pass
                        line = self.file.readline()
                else:
                    pass
            else:
                pass
            line = self.file.readline()

    def op_analysis(self, string):
        """
        op_id, output(dtype, shape), input(dtype, shape, ...), and
        parameter_replication
        kind
        calls
        dimensions
        metadata
        window
        ...
        :return: op object
        """
        op = Op(string)
        return op


    def cluster_name(self):
        # str = self.file.readline()
        # print(str)
        for i in range(3):
            str = self.file.readline()
            if str == '':
                print('end of file!')
            print('line %d', i)
            print(len(str))
        return str


class SubModule:
    def __init__(self):
        self.name = ''


class Op:
    def __init__(self, string):
        self.name = ''
        self.ID = ''
        self.inputs = ''
        self.outputs = ''
        self.metadata = ''
        self.window = ''
        self.other = ''

        substr = string.split(' = ', 1)
        self.ID = substr[0]
        if ',' in substr[1]:
            substr = split_by_comma_space(substr[1])
            [self.outputs, self.inputs] = split_by_space(substr[0])
            self.other = substr[1]
        else:
            [self.outputs, self.inputs] = substr[1].split(' ', 1)
            self.other = 'null'
        if 'metadata' in self.other:
            # metadata get
            pass
        if 'window' in self.other:
            # conv
            pass





if __name__ == '__main__':
    flist = list_all_files('./data')
    for i in range(2):
        cluster = ClusterAnalysis('./data/' + flist[i])
    # cluster.cluster_name()
