from util import *
import pandas as pd

header = [
    'ID',
    'output',
    'input',
    'window',
    'metadata',
    'FLOPs'
]
empty_line = ['-', '-', '-', '-', '-', '-']

records = []
writer = pd.ExcelWriter('xla_hlo_dump.xlsx')

class ClusterAnalysis:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename)
        self.cluster_name = ''
        self.collect_info()

    def collect_info(self):
        cluster_line = self.file.readline()
        self.cluster_name = cluster_line.split(' ', 1)[1].strip()
        # print(self.cluster_name)  # cluster name -> sheet name
        line = self.file.readline()
        while line != '':
            if not_empty_line(line):
                if line.startswith('%'):  # sub module
                    substr = line.strip().split(' ', 1)
                    submodule = substr[0]
                    substr = substr[1].strip('{').split(' -> ')
                    record = [submodule, substr[1], substr[0], '', '', '']
                    records.append(record)
                    # print(substr)  # input & output
                    # line = self.file.readline()  # {}
                    # while not line.startswith('}'):
                        # if not_empty_line(line):
                            # op analysis
                            # op = self.op_analysis(line.strip())
                            # print('ID: ' + op.ID)
                            # print('input: ' + op.inputs)
                            # print('output: ' + op.outputs)
                            # print('window: ' + op.window)
                            # print('metadata: ' + op.metadata)
                            # print('others: ' + op.other)
                        # else:
                            # pass
                        # line = self.file.readline()
                elif line.startswith('ENTRY'):  # main module
                    substr = line.strip().split(' ', 2)
                    module = substr[1]
                    substr = substr[2].strip('{').split(' -> ')
                    record = [module, substr[1], substr[0], '', '', '']
                    records.append(record)
                    # print('ENTRY name: \t' + substr[1]) # ENTRY (main module) name
                    # line = self.file.readline()  # {}
                    # while not line.startswith('}'):
                        # if not_empty_line(line):
                            # op = self.op_analysis(line.strip())
                            # print('ID: ' + op.ID)
                            # print('input: ' + op.inputs)
                            # print('output: ' + op.outputs)
                            # print('window: ' + op.window)
                            # print('metadata: ' + op.metadata)
                            # print('others: ' + op.other)
                        # else:
                            # pass
                        # line = self.file.readline()
                else:
                    pass

                line = self.file.readline()  # {}
                while not line.startswith('}'):
                    if not_empty_line(line):
                        # op analysis
                        op = self.op_analysis(line.strip())
                        print('ID: ' + op.ID)
                        print('input: ' + op.inputs)
                        print('output: ' + op.outputs)
                        print('window: ' + op.window)
                        print('metadata: ' + op.metadata)
                        print('others: ' + op.other)
                        record = [op.ID, op.outputs, op.inputs, op.window, op.metadata, op.FLOPs]
                        records.append(record)
                    else:
                        pass
                    line = self.file.readline()
                records.append(empty_line)
            else:
                pass
            line = self.file.readline()
        dataframe = pd.DataFrame(records, columns=header)
        dataframe.to_excel(excel_writer=writer, sheet_name=self.cluster_name)

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
        self.FLOPs = 0

        substr = string.split(' = ', 1)
        self.ID = substr[0]
        # TODO
        substr = split_by_comma_space(substr[1])
        [self.outputs, self.inputs] = split_by_space(substr[0])
        if len(substr) > 1:
            self.other = substr[1]
        else:
            self.other = 'null'
        '''
        if '),' in substr[1]:  # maybe problems
            substr = split_by_comma_space(substr[1])
            [self.outputs, self.inputs] = split_by_space(substr[0])
            self.other = substr[1]
        else:
            [self.outputs, self.inputs] = substr[1].split(' ', 1)
            self.other = 'null'
        '''
        if 'metadata' in self.other:
            # metadata get
            self.get_metadata(self.other)
        if 'window' in self.other:
            # conv
            self.get_window(self.other)

    def get_metadata(self, string):
        pos = string.find('metadata')
        # print(find_between_brace(string[pos:])[0])
        self.metadata = find_between_brace(string[pos:])[0]

    def get_window(self, string):
        pos = string.find('window')
        self.window = find_between_brace(string[pos:])[0]
        # print(self.ID + ': window -> ' + self.window)


if __name__ == '__main__':
    flist = list_all_files('./data')
    for f in flist:
        cluster = ClusterAnalysis('./data/' + f)
    writer.save()
    writer.close()
