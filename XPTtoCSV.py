import xport
import math

def XPTtoCSV(filename):
	#given a XPT file, make a CSV file with it's contents
	of = open('DIQ_I.csv', 'w')
	of.write(getHeader("headermap.txt"))
	of.write("\n")
	print "length of data: " + str(len(data[0]))
	ignores = useHeaderFileInfo("headermap.txt")
	
	for line in data:
		output_line = ""
		i = 0
		#filter out some bad data
		for field in line:
			if (math.isnan(field)):
				output_line += "-1,"
			elif field == ignores[i][0] or field == ignores[i][1]:
				output_line += "-1,"
			elif field < 7000 and field > 400:
				output_line += "0.5,"
			else:
				output_line += str(field) + ","
			i+=1
		of.write(output_line)
		of.write("\n")
		
	of.close()

def XPTtoJSON(filename, ignores):
	#given a XPT file, write a JSON file with it's contents
	in_f = open(filename, 'rb')
	rdr = xport.to_columns(in_f) #maps question to values
	out_f = ""
	out_f += "{\n"
	for k in rdr.keys():
		out_f += "\t\"" + k + "\": ["
		out_str = ""
		for val in rdr[k]:
			if math.isnan(val):
				out_str += "-1.0,"
			elif k in ignores.keys():
				found = False
				for ignore_value in ignores[k]:
					if val == ignore_value:
						found = True
						out_str += "-1.0,"
				if not found:
					if val < 7000 and val > 400:
						out_str += "0.5,"
					else:
						out_str += str(val) + ","
			else:
				out_str += str(val) + ","
		out_str = out_str[:-1]
		out_f += out_str + "],\n"
	out_f = out_f[:-2] + "\n}"
	of = open('DIQ_I.json', 'w')
	of.write(out_f)
	of.close()

def removeUselessRows(data):
	#clean out pointless data, if it exists
	newdata = []
	for i in range(0, len(data)):
		newdata.append([])
		for j in range(0, len(data[i])):
			if data[i][j] > 600:
				newdata.append(-1)
			else:
				newdata.append(data[i][j])



def getHeader(filename):
	# read in a mapping of question ID to string, 
	# return csv-separated header line
	in_f = open(filename, 'r').readlines()
	print "length of header: " + str(len(in_f))
	ol = []
	for line in in_f:
		x = line.strip().split()[:-2]
		os = ""
		for word in x:
			os += word
			os += " "
		os = os[:-1]
		ol.append(os)
	totalos = ""
	for field in ol:
		totalos += field + ","
	totalos = totalos[:-1]
	return totalos

def mapignores(filename):
	#create a map of question codes to ignored answers
	in_f = open(filename, 'r').readlines()
	ignores = {}
	for line in in_f:
		x = line.strip().split()
		ignores[x[0]] = []
		if x[-1] == "_":
			ignores[x[0]].append(-1.0)
			ignores[x[0]].append(-1.0)
		else:
			ignores[x[0]].append(float(x[-1]))
			ignores[x[0]].append(float(x[-2]))
	print ignores.keys()
	return ignores

def useHeaderFileInfo(filename):
	in_f = open(filename, 'r').readlines()
	ignores = []
	for line in in_f:
		#last two are things to ignore; first one is the question info
		x = line.strip().split()[-2:]
		if (x[0] == '_'):
			x[0] = -1
		if (x[1] == '_'):
			x[1] = -1
		x[0] = float(x[0])
		x[1] = float(x[1])
		ignores.append(x)
		print x
	return ignores






if __name__ == '__main__':
	ig = mapignores("headermap.txt")
	data = XPTtoJSON("DIQ_I.xpt", ig)


	