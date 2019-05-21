#!/usr/bin/python3

import sys,argparse
import json

unknown_char = '_'

def search_hex(hex_input):
	# print(hex(int(hex_input,16)))
	# print("0x" + file[0:int(len(hex_input)/2)].hex())
	for i in range(len(file)-1):
		a = "0x" + file[i:i+int(len(hex_input)/2)].hex()
		b = "0x{:0{w}x}".format(int(hex_input,16),w=len(hex_input))
		#print(a + " - " + b)
		if(a == b):
			print(hex(i+offset)+":\t"+file[i:i+int(len(hex_input)/2)].hex())
			
def search_single_pattern(str_input):
	if len(str_input)>1:
		diff_str = [0];
		list_search_results = [];
		b_str = bytearray(str_input,'ASCII')
		for i in range(len(b_str)-1):
			diff_str.append(b_str[i+1]-b_str[i])
		for i in range(len(file)-1):
			if((file[i+1]-file[i])==diff_str[1]):
				comp_str = file[i:i+len(diff_str)]
				if(diff_str[1:] == [comp_str[i+1]-comp_str[i] for i in range(len(comp_str)-1)]):
					list_search_results.append((hex(i+offset),comp_str.hex()))
					#print(hex(i+offset) + ":\t" + comp_str.hex())
		for n in list_search_results:
			print(n[0] + ":\t" + n[1])

		return list_search_results;

def search_pattern_method(*strings):
	
	list_results = [];
	dict_text = dict();
	for string in strings[0]:
		print("Searching for " + string + "...")
		results = search_single_pattern(string);
		if(len(results)>0):
			# res = input("Do you want to add it to a dictionary? [y/N] ")
			res = input("Do you want to create a dictionary from this? [y/N] ")
			if(res == 'y'):
				diff = int.from_bytes(string[0].encode(),byteorder='big')-int.from_bytes(' '.encode(),byteorder='big')
				for i in range(128-32):
					#print(str(i+32) + " " + bytes([i+32]).decode() + ": " + bytes([int(results[0][1][0:2],16)+i-diff]).hex())
					dict_text[bytes([int(results[0][1][0:2],16)+i-diff]).hex()] = bytes([i+32]).decode()
				# res = 0;
				# if(len(results)>1):
					# for n in results:
						# print("[" + str(results.index(n)) + "] "+ n[0] + ":\t" + n[1])
					# res = input('Select the result number to be the base of the dictionary: ')
					
				# for s in range(len(string)):
					# dict_text[results[int(res)][1][2*s:2*(s+1)]] = string[s];

	print(dict_text)
	res = input("Introduce the name of the dictionary file: ")
	with open(res,"w") as df:
		json.dump(dict_text,df);

def read_method(dictionary_file):
	n_lines = int(len(file)/16)
	word_group = args.word;
	c_line = 0
	
	for j in range(n_lines):
		string = hex(c_line*16+offset) +":\t"
		for i in range(c_line*16,(c_line+1)*16,word_group):
			string += file[i:i+word_group].hex()+" "
		string += ' | '
		if dictionary_file is None:
			for i in range(c_line*16,(c_line+1)*16,word_group):
				substr = '';
				for j in range(word_group):
					try:
						if file[i+j] > 32:
							substr += bytes([file[i+j]]).decode('UTF')
						else:
							substr += " "
					except ValueError:
						substr += unknown_char
				string += substr + " "
		else:
			dictionary = dict();
			with open(dictionary_file,"r") as df:
				dictionary = json.load(df);
			for i in range(c_line*16,(c_line+1)*16,word_group):
				substr = '';
				for j in range(word_group):
					if bytes([file[i+j]]).hex() in dictionary :
						substr += dictionary[bytes([file[i+j]]).hex()]
					else:
						substr += '_'
				string += substr + " "
		
		print(string)
		c_line+=1
	# else:
		# print("Using dictionary... ")
		# dictionary = dict();
		# with open(dictionary_file,"r") as df:
			# dictionary = json.load(df);
			# print(dictionary)
		# for j in range(n_lines):
			# string = hex(c_line*16+offset) +":\t"
			# for i in range(c_line*16,(c_line+1)*16,word_group):
				# substr = ""
				# data_chk = file[i:i+word_group].hex()
				# for j in range(word_group):
					# if data_chk[2*j:2*(j+1)] in dictionary:
						# substr += dictionary[data_chk[2*j:2*(j+1)]] + " "
					# else:
						# substr += data_chk[2*j:2*(j+1)]
				# string += substr+" "
			# print(string)
			# c_line+=1
			
parser = argparse.ArgumentParser(description='This is an utility to process some GameBoy Pokemon cartridges')

parser.add_argument('filename', type=str, help='filename of the gameboy file to use. Usually .gb or .gbc')
parser.add_argument('-ds', '--diff-search', action='store', default=argparse.SUPPRESS, nargs='+', help='search differentially for a pattern in the game')
parser.add_argument('-s', '--search', action='store', type=str, default=argparse.SUPPRESS, nargs='+', help='search hex data in game')
parser.add_argument('-b', '--block', action='store', type=int, default=None, help='set the size of the block to analize (Default: whole file)')
parser.add_argument('-o', '--offset', action='store', type=str, default='0', help='set the offset to start reading the file (Default: 0)')
parser.add_argument('-w', '--word', action='store', choices=[1,2,4,8,16], type=int, default=2, help='set byte word size in the printout (Default: 2)')
parser.add_argument('-d', '--dictionary', action='store', type=str, default=None, help='filename of the dictionary to use')

args = parser.parse_args()

filename = args.filename;
blocksize = args.block;
offset = int(args.offset,16);
file = None;

with open(filename,"rb") as f:
	f.seek(offset);
	file = f.read(blocksize);
	
if 'diff_search' in args:
	search_pattern_method(args.diff_search)
elif 'search' in args:
	search_hex(args.search[0])
else:
	read_method(args.dictionary)