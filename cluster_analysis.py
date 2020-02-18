from util import *
import pandas as pd

header = [
    'ID',
    'op_type',
    'layer',
    'out_type',
    'out_shape',
    'in_type',
    'in_shape',
    'window',
    'calls',
    'FLOPs'
]
empty_line = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']

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
        print('cluster name:\t' + find_between_brackets(self.filename, '/module', 'after') + self.cluster_name)  # cluster name -> sheet name
        line = self.file.readline()
        while line != '':
            if not_empty_line(line):
                if line.startswith('%'):  # sub module
                    substr = line.strip().split(' ', 1)
                    submodule = substr[0]
                    substr = substr[1].strip('{').split(' -> ')
                    record = [submodule, '', '', substr[1], '', substr[0], '', '', '', '']
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
                    record = [module, '', '', substr[1], '', substr[0], '', '', '', '']
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
                        # print('ID: ' + op.ID)
                        # print('input: ' + op.inputs)
                        # print('output: ' + op.outputs)
                        # print('window: ' + op.window)
                        # print('metadata: ' + op.metadata)
                        # print('others: ' + op.other)
                        # print(op.ID)
                        # print(op.layer + " : " + op.type)
                        record = [
                            op.ID,
                            op.type,
                            op.layer,
                            op.out_type,
                            op.out_shape,
                            op.in_type,
                            op.in_shape,
                            op.window,
                            op.calls,
                            op.FLOPs]
                        records.append(record)
                    else:
                        pass
                    line = self.file.readline()
                records.append(empty_line)
            else:
                pass
            line = self.file.readline()

        # print(records)
        dataframe = pd.DataFrame(records, columns=header)
        records.clear()
        sheet = find_between_brackets(self.filename, '/module', 'after') + self.cluster_name
        dataframe.to_excel(excel_writer=writer, sheet_name=sheet)
        writer.save()

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
        self.calls = ''
        self.other = ''
        self.FLOPs = 0
        # metadata : {layer, type}
        self.layer = ''
        self.type = ''
        self.in_type = ''
        self.out_type = ''
        self.in_shape = ''
        self.out_shape = ''

        substr = string.split(' = ', 1)
        self.ID = substr[0]
        # TODO
        substr = split_by_comma_space(substr[1])
        [self.outputs, self.inputs] = split_by_space(substr[0])
        self.get_in_type_shape()
        self.get_out_type_shape()
        for i in range(len(substr)-1):
            self.other += substr[i+1] + ' '
        '''
        if len(substr) > 1:
            self.other = substr[1]
        else:
            self.other = 'null'
        '''
        if 'metadata' in self.other:
            # metadata get
            self.get_metadata(self.other)
        if 'window' in self.other:
            # conv
            self.get_window(self.other)
        if 'calls' in self.other:
            # calls
            self.get_calls(self.other)

    def get_metadata(self, string):
        pos = string.find('metadata')
        # print(find_between_brace(string[pos:])[0])
        self.metadata = find_between_brace(string[pos:])[0]
        self.type = self.get_attr('op_type', self.metadata)
        self.layer = self.get_attr('op_name', self.metadata)

    def get_window(self, string):
        pos = string.find('window')
        self.window = find_between_brace(string[pos:])[0]
        # print(self.ID + ': window -> ' + self.window)

    def get_calls(self, string):
        lpos = string.find('calls')
        rpos = string[lpos:].index(' ') + lpos
        self.calls = find_assignment_rhs(string[lpos:rpos+1])
        # print(self.calls)

    def get_attr(self, key, string):
        if key in string:
            lpos = string.index(key)
            rpos = string[lpos:].index('"', len(key)+2) + lpos
            attr = find_assignment_rhs(string[lpos:rpos+1])
            attr = attr.strip('"')
            return attr
        else:
            return ''

    def get_in_type_shape(self):
        if len(self.inputs) > 0:
            in_args = find_between_brackets(self.inputs, '(', ')')
            arg_list = split_by_comma_space(in_args)
            for arg in arg_list:
                if '[' in arg:
                    type = arg.split('[', 1)[0]
                    shape = find_between_brackets(arg, '[', ']')
                    self.in_type += type + ', '
                    self.in_shape += '[' + shape + ']' + ', '
        else:
            pass

    def get_out_type_shape(self):
        if len(self.outputs) > 0:
            if '(' in self.outputs:
                out_args = find_between_brackets(self.outputs, '(', ')')
            else:
                out_args = self.outputs
            arg_list = split_by_comma_space(out_args)
            for arg in arg_list:
                if '[' in arg:
                    type = arg.split('[', 1)[0]
                    shape = find_between_brackets(arg, '[', ']')
                    self.out_type += type + ', '
                    self.out_shape += '[' + shape + ']' + ', '
        else:
            pass


if __name__ == '__main__':
    flist = list_all_files('./data')
    # print('file num:\t%d', len(flist))
    for f in flist:
        cluster = ClusterAnalysis('./data/' + f)
    # print("Start Saving...")
    # writer.save()
    writer.close()
    print("Mission Complete!")
