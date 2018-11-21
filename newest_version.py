# -*- coding: utf-8 -*-  #für Umlaute etc
import random
from Bio import SeqIO
import argparse
import pybedtools





def find_number(sequence_length, min_distance, already_selected, right_base): #Find a Number, check if same/flanking
    selected_number = None
    while selected_number is None:
        candidate = random.randint(0, sequence_length-1)
        candidate_ok = True
        if right_base[candidate] == "N":
            candidate_ok = False
        else:
            for number in already_selected:
                distance = abs(candidate - number) #abs = Betrag
                if distance < min_distance:
                    candidate_ok = False

        if candidate_ok:
            selected_number = candidate

    return selected_number


def find_all_locations(sequence, n, min_distance): #How many insertions do you want to make? Range(n) = insertion_numbers
    result = []
    for i in range(n):
        new_number = find_number(len(sequence), min_distance, result, sequence)
        print(id, new_number, new_number+201, sep='\t', file=bed_file) #seperated by a tab
        result.append(new_number)

    #bed_file.close()
    #bed_file_sorted = pybedtools.BedTool("unsorted_bed_file.bed")
    #bed_file_sorted = bed_file_sorted.sort()
    #new_file = open("bed_file_sorted.bed", "w")

    #print(bed_file_sorted, file=new_file)


       # result.append(new_number)
    #subprocess("bedtools")
    #bedtools sort bed_file
    result.sort() #Sort because later insertion_size has to be appended to the sequence, only possible when next number is bigger


    return result




def insert_TE(sequence, insertion, insertion_base): #Insert one TE_sequence
    insertion = insertion.upper() #To avoid agaatc
    #insertion = insertion.replace('\n', "")
    sequence_split1 = sequence[:insertion_base]
    sequence_split2 = sequence[insertion_base:]
    new_string = sequence_split1 + insertion + sequence_split2
    return new_string

def insert_all_TEs(sequence, insertion, n, min_distance):
    sequence = sequence.upper() #to avoid aAAcCCTnNnnN
#    sequence = sequence.replace("\n", "")
    new_insert_locations = find_all_locations(sequence, n, min_distance)
    #print(new_insert_locations, file= bed_file)
    #print(new_insert_locations)


    offset = 0  # because previous insertions make the whole sequence longer
    new_sequence = sequence
    #print(new_sequence) #need this if first sequence should be printed
    for number in new_insert_locations:
        new_sequence = insert_TE(new_sequence, insertion, number + offset)
        offset += len(insertion) #to provide new sequece_length
        #print(new_sequence) #need this if all steps of sequences with new insertions should be printed
    return new_sequence





if __name__ == '__main__':


    parser = argparse.ArgumentParser(description="Arguments for the program")
    parser.add_argument('seq_file', metavar='sequence', type=argparse.FileType('r'), nargs="?",
                        # fragezeichen = es gibt nur ein einziges argument
                        help='The sequence in Fasta Format')
    parser.add_argument('--d', metavar="min_distance", type=int, nargs="?", default=100,
                        help="The distance between to insertions in bp. Default = 100bp")
    parser.add_argument("--n", metavar="number", type=int, nargs="?", help="Number of TE insertions, Default = 10",
                        default=10)
    parser.add_argument("ins_file", metavar="insertion", type=argparse.FileType('r'), nargs="?",
                        help="Insertion sequence")
    parser.add_argument("out_file", metavar="Output_file", nargs="?", help = 'The output file name', default = "Sequence_with_insertions.fa" )
    parser.add_argument("ID", metavar="ID", nargs="?", help = 'The ID file name')
    args = parser.parse_args()
    #sequence = args.seq_file
    #min_distance = args.d
    #insertion = args.ins_file
    #number = args.n
    # return(sequence, min_distance, number, insertion)

    #open_sequence = open("short_scaffold1")
    #new_file = open("new_sequence", "w")
    #open_insertion = open("SINEC1_Ame_sequence.fa")
    insertion = SeqIO.read(args.ins_file, "fasta")
    sequence = SeqIO.read(args.seq_file, "fasta")
    id = sequence.id #to insert the right id into the insertions.bed file
    #print(id) just to see if id is right
    n = args.n
    min_distance = args.d
    # print(args.seq_file)
    bed_file = open(args.ID+".insertions.bed", "w")

    Final_sequence = insert_all_TEs(sequence, insertion, n, min_distance)
    SeqIO.write(Final_sequence, args.out_file+".fa", "fasta")

    





