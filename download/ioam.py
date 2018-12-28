import os
import sys
import pykd

STANDARD_ACCESS_MASKS = {
    0x00010000 : "DELETE",
    0x00020000 : "READ_CONTROL",
    0x00040000 : "WRITE_DAC",
    0x00080000 : "WRITE_OWNER",
    0x00100000 : "SYNCHRONIZE",
}

FILE_ACCESS_MASKS = {
    0x0001 : "FILE_READ_DATA",
    0x0002 : "FILE_WRITE_DATA",
    0x0004 : "FILE_APPEND_DATA",
    0x0008 : "FILE_READ_EA",
    0x0010 : "FILE_WRITE_EA",
    0x0020 : "FILE_EXECUTE",
    0x0080 : "FILE_READ_ATTRIBUTES",
    0x0100 : "FILE_WRITE_ATTRIBUTES",
}

def print_file_access_masks(masks):
    "Print access masks for file object as string"
    if 0 == masks:
        return "0"

    ret_val = list()

    for current_mask in STANDARD_ACCESS_MASKS:
        if current_mask & masks:
            ret_val.append( STANDARD_ACCESS_MASKS[current_mask] )
            masks = masks & (~current_mask)

    for current_mask in FILE_ACCESS_MASKS:
        if current_mask & masks:
            ret_val.append( FILE_ACCESS_MASKS[current_mask] )
            masks = masks & (~current_mask)

    if masks:
        raise RuntimeError( "Unknown access mask: {}".format("|".join(ret_val + ["0x{:x}".format(masks), ])) )

    return " | ".join(ret_val)

def generate_enum_map(info_class):
    result = dict()
    for i in info_class.fields()[:-1]: # skip MaximumInformation
        result[getattr(info_class, i[0])] = i[0]
    return result

def generate_mask_map(access_addr, length_addr, count):
    access = pykd.loadDWords(access_addr, count)
    length = pykd.loadBytes(length_addr, count)

    result = dict()
    for i in range(count):
        if length[i] != 0:
            result[i] = access[i]

    return result

class Masks:
    def __init__(self, nt):
        self.values = dict()
        self.enums = dict()

        info_class = nt.type("_FILE_INFORMATION_CLASS")
        self.enums["FILE_INFORMATION_CLASS"] = generate_enum_map(info_class)

        self.values["NtQueryInformationFile"] = generate_mask_map( nt.IopQueryOperationAccess,
                                                                   nt.IopQueryOperationLength,
                                                                   info_class.FileMaximumInformation )


        self.values["NtSetInformationFile"] = generate_mask_map( nt.IopSetOperationAccess,
                                                                 nt.IopSetOperationLength,
                                                                 info_class.FileMaximumInformation )


        info_class = nt.type("_FSINFOCLASS")
        self.enums["FSINFOCLASS"] = generate_enum_map(info_class)

        self.values["NtQueryVolumeInformationFile"] = generate_mask_map( nt.IopQueryFsOperationAccess,
                                                                         nt.IopQueryFsOperationLength,
                                                                         info_class.FileFsMaximumInformation )

        self.values["NtSetVolumeInformationFile"] = generate_mask_map( nt.IopSetFsOperationAccess,
                                                                       nt.IopSetFsOperationLength,
                                                                       info_class.FileFsMaximumInformation )

        self.version = nt.getVersion()

def print_table(collected, function_name, enum_name):
    print( "<br />" )
    print( "<table border=\"1\">" )

    versions = ["<td>{}</td>".format(".".join(["{}".format(n) for n in x.version])) for x in collected]

    print( "<tr>" )
    print( "<td><b>{}</b></td>".format(function_name) )
    print( "\r\n".join(versions) )
    print( "<td></td>")
    print( "</tr>" )

    values = list()
    for x in collected:
        values += [ i for i in x.values[function_name] ]

    for i in sorted( set(values) ):
        print( "<tr>" )

        names = set([ x.enums[enum_name][i] for x in collected if i in x.enums[enum_name] ])
        print( "<td>{} /* = {} */</td>".format(" / ".join(names), i) )

        

        prev = None
        for x in collected:
            am = ""
            if i in x.values[function_name]:
                am = print_file_access_masks(x.values[function_name][i])
            elif i < max([ j for j in x.values[function_name] ]):
                am = "<img src=\"../images/deny_rd_cr.png\" alt=\"X\" />"

            color = ""
            if not prev is None:
                if prev != am:
                    color = "green" if not prev else "red"

            prev = am

            if color:
                am = "<font color=\"{}\">{}</font>".format(color, am)

            print( "<td>{}</td>".format(am) )

        print( "<td>{}</td>".format(" / ".join(names)) )

        print( "</tr>" )

    print( "<tr>" )
    print( "<td></td>")
    print( "\r\n".join(versions) )
    print( "<td></td>")
    print( "</tr>" )

    print( "</table>" )

def collect(fs_path):
    collected = list()

    if not os.path.isfile(fs_path):
        for name in os.listdir(fs_path):
            full_name = os.path.join(fs_path, name)
            if not os.path.isfile(full_name):
                collected += collect(full_name)
            elif name.lower() == "ntoskrnl.exe":
                collected += collect(full_name)
    else:
        sys.stderr.write( "Processing: {} ... ".format(fs_path) )

        dump = pykd.loadDump(fs_path)

        nt = pykd.module( os.path.splitext(os.path.basename(fs_path))[0] )
        collected.append( Masks(nt) )

        pykd.closeDump(dump)

        sys.stderr.write( "done\r\n" )

    return collected

def main(fs_path):
    collected = sorted(collect(fs_path), key=lambda x: x.version[2])

    print( "<html>" )
    print( "<body>" )

    print_table( collected, "NtQueryInformationFile", "FILE_INFORMATION_CLASS" )
    print_table( collected, "NtSetInformationFile", "FILE_INFORMATION_CLASS" )

    print_table( collected, "NtQueryVolumeInformationFile", "FSINFOCLASS" )
    print_table( collected, "NtSetVolumeInformationFile", "FSINFOCLASS" )

    print( "</body>" )
    print( "</html>" )

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main( sys.argv[1] )
    else:
        if len(sys.argv) != 1:
            sys.stderr.write( "Invalid command line\r\n" )
        sys.stderr.write( "Usage: {} <dir_path>\r\n".format(sys.argv[0]) )
