# * ESPRESSO SBI Pt-level output
# * Process neuroimaging reports to classify a patient's SBI and WMD status
# * @author Sunyang Fu
 
import csv
import sys
import re
import os
import string
import glob

def rad_parser(line):
	line = str(line.encode('utf-8'))
	line = line.replace('[', '')
	line = line.replace(']', '')
	line = line.replace('\'', '')
	line = line.replace('}', '')
	# line = line.replace('', '')
	line = line[121:]
	line = line.split('\par')
	line_str = ''
	for m in line:
		line_str += m + '\n' 
	line = line_str
	return line

def read_txt(indir):
	f = open(indir,'r')
	txt = f.read()
	f.close()
	l = txt.split('\n')
	return l	

def read_file_list(indir, deli):
	opt_notes = []
	with open(indir, 'rU') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=deli)
		for row in spamreader:
			opt_notes += [row]
	return opt_notes

def apply_exclusion_wmd(sent):
	elist = read_txt('SBI/regexp/resources_regexp_reWMDCXEXL.txt')
	for k in elist:
		k = ' '+k+' '
		sent = ' '+sent.lower().replace('.', ' ')
		if k in sent:
			return True
	return False

def apply_positive_screen(sent):
	elist = read_txt('SBI/regexp/resources_regexp_reSBIAlone.txt')
	for k in elist:
		k = ' '+k+' '
		sent = ' '+sent.lower().replace('.', ' ')
		if k in sent:
			return True
	return False	

def apply_negative_screen(sent):
	elist = read_txt('SBI/regexp/resources_regexp_reSBICXEXL.txt')
	for k in elist:
		k = ' '+k+' '
		sent = ' '+sent.lower().replace('.', ' ')
		if k in sent:
			return False
	return True

def get_remove(l, deli):
	r = {}
	for d in l:
		fname = d.split(deli)[-1]
		SBI_STATUS, WMD_STATUS, WMD_GD = '','',''
		ann_list = read_file_list(d,'\t')
		for row in ann_list:
			key = fname+row[-2]
			norm = row[9]
			if 'REMOVE' in norm:
				r[key] = 1
	return r
		
def run_eval_sbi(indir, outdir, sys):
	if sys == '0':
		deli = '/'
	else:
		deli = '\\'
	dir_list = indir+deli+'*.ann'
	l = glob.glob(dir_list)
	output = []
	rm = get_remove(l, deli)

	with open(outdir+deli+'patient_level.csv', 'w') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter='|')
		for d in l:
			fname = d.split(deli)[-1]
			SBI_STATUS, WMD_STATUS, WMD_GD = '','',''
			SBI_STATUS_LIST = []
			ann_list = read_file_list(d,'\t')
			for row in ann_list:
				rm_term = fname+row[-2]
				certainty = row[6]
				status = row[7]
				exp = row[8]
				norm = row[9]
				sent = row[-1].lower()
				key = fname+row[-2]
				double_eval = False
				indeterminate_status = False
				# if ('Negation' not in certainty) and 'Present' in status and 'Patient' in exp:
				# 	if'INF_INDETERMINATE' in norm:
				# 		SBI_STATUS_LIST += ['SBI_INDETERMINATE']
				# 		indeterminate_status = True
				# if ('Possible' in certainty) and 'Present' in status and 'Patient' in exp:
				# 	if ('NONACUTE' in norm or 'INF_GENERAL' in norm or 'ACUTE' in norm):
				# 		SBI_STATUS_LIST += ['SBI_INDETERMINATE']
				# 		indeterminate_status = True
				# if ('Hypothetical' in certainty) and 'Present' in status and 'Patient' in exp:
				# 	if ('NONACUTE' in norm or 'INF_GENERAL' in norm or 'ACUTE' in norm):
				# 		SBI_STATUS_LIST += ['SBI_INDETERMINATE']
				# 		indeterminate_status = True
				if indeterminate_status:
					ps = apply_positive_screen(sent)
					if ps:
						SBI_STATUS_LIST += ['SBI_FOUND']
				if ('Positive' in certainty):
					if ('NONACUTE' in norm or 'INF_GENERAL' in norm or 'ACUTE' in norm):
						ns = apply_negative_screen(sent)
						if ns:
							SBI_STATUS_LIST += ['SBI_FOUND']
						# else:
						# 	SBI_STATUS_LIST += ['SBI_INDETERMINATE']
				if ('Negated' not in certainty):							
					if 'WMD_WHITE' in norm or 'WMD_LEUK' in norm or 'WMD' in norm or 'WMD_SV' in norm:
						exl = apply_exclusion_wmd(sent)
						if not exl and rm_term not in rm:
							WMD_STATUS = 'WMD_FOUND'
			if 'SBI_FOUND' in SBI_STATUS_LIST:
				SBI_STATUS = 'SBI_FOUND'
			# elif 'SBI_INDETERMINATE' in SBI_STATUS_LIST:
			# 	SBI_STATUS = 'SBI_INDETERMINATE'
			for row in ann_list:
				if WMD_STATUS == 'WMD_FOUND':
					if 'SEVERE' in norm:
						WMD_GD = 'SEVERE'
					if 'MODERATE' in norm:
						WMD_GD = 'MODERATE'
					if 'MILD' in norm:
						WMD_GD = 'MILD'
			spamwriter.writerow([fname, SBI_STATUS, WMD_STATUS, WMD_GD])

def main():
	args = sys.argv[1:]
	run_eval_sbi(args[0], args[1], args[2])

if __name__== "__main__":
	main()





