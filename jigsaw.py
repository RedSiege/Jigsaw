import random
import sys


def getShellcode(input_file):
    file_shellcode = b''
    try:
        with open(input_file, 'rb') as shellcode_file:
            file_shellcode = shellcode_file.read()
            file_shellcode = file_shellcode.strip()
            binary_code = ''
            sc_array = []

            for byte in file_shellcode:
                binary_code += "\\x" + hex(byte)[2:].zfill(2)

            raw_shellcode = "0" + ",0".join(binary_code.split("\\")[1:])
        for byte in raw_shellcode.split(','):
            sc_array.append(byte)

        return(sc_array)
    
    except FileNotFoundError:
        sys.exit("\n\nThe input file you specified does not exist! Please specify a valid file path.\nExiting...\n")


def generateJigsaw(filename):
    shellcode = getShellcode(filename)
    sc_len = len(shellcode)
    raw_positions = list(range(0,sc_len))
    random.shuffle(raw_positions)

    jigsaw = []
    for position in raw_positions:
        jigsaw.append(shellcode[position])

    jigsaw_array = 'unsigned char jigsaw[XXX] = { '
    jigsaw_array += ', '.join(str(byte) for byte in jigsaw)
    jigsaw_array += ' };'

    position_array = 'int positions[XXX] = { '
    position_array += ', '.join(str(x) for x in raw_positions)
    position_array += ' };'

    code = jigsaw_array + '\n\n'
    code += position_array + '\n\n'
    code += '''
int calc_len = XXX;
unsigned char calc_payload[XXX] = { 0x00 };
int position;

// Reconstruct the payload
for (int idx = 0; idx < sizeof(positions) / sizeof(positions[0]); idx++) {
	position = positions[idx];
	calc_payload[position] = jigsaw[idx];
}
'''
    code = code.replace('XXX', str(sc_len))

    with open('jigsaw.txt', 'w') as outfile:
        outfile.write(code)


if __name__ == "__main__":

        '''
        Purpose: This script takes one argument: the filename of your shellcode in .bin format. 
                         The script reads the binary file in and then generates a C template 
                         in the current directory containing the randomized shellcode, the lookup table, and the decoder.
        Input: 
                filename of your shellcode (.bin formatted files only)

        Output: 
                jigsaw.txt
        '''

        if not len(sys.argv) == 2:
                print("[x] Script requires one argument, the filename of your shellcode .bin file.")
                sys.exit()
        generateJigsaw(sys.argv[1])
        


