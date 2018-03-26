import sys, csv, re
import random, numpy
from sklearn.metrics import f1_score
random.seed(20161011)
def equal_list(a, b):
	mark = True
	for i in range(len(a)):
		if a[i] != b[i]:
			mark = False 
			break 
	return mark 
	
def transform_labels(labels, max_num):
	gen_labels = [0]*max_num
	for label in labels:
		gen_labels[label] = 1 
	return gen_labels
	
def extract_match(a, b):
	cnt = 0.0 
	for i in range(len(a)):
		a_row = a[i]
		b_row = b[i]
		i_ = equal_list(a_row, b_row)
		cnt += int(i_)
	return cnt/len(a)
	
def return_labels(a):
	b = []
	for i in range(len(a)):
		if a[i] == 1:
			b.append(i) 
	return b 
	
def example_based(aa, bb): # a: ground truth, and b for predicted
	accs = 0.0 
	precs, recalls, f1s = 0.0, 0.0, 0.0
	for i in range(len(aa)):
		a = aa[i]
		b = bb[i]
		#print b
		a_labels = set(return_labels(a))
		b_labels = set(return_labels(b))
		# print b_labels
		acc = len(a_labels & b_labels) / max(1, len(a_labels | b_labels))
		accs += acc
		prec = len(a_labels & b_labels) / max(1, len(b_labels))
		recall = len(a_labels & b_labels) / max(1, len(a_labels))
		f1 = 2*len(a_labels & b_labels)/(len(a_labels) + len(b_labels))
		precs += prec 
		recalls += recall
		f1s += f1 
	return accs/len(aa), precs/len(aa), recalls/len(aa), f1s/len(aa)

def label_based(aa, bb, max_num):
	macro_f1s, micro_f1s = 0.0, 0.0 
	aa = numpy.array(aa)
	bb = numpy.array(bb)
	micro_num, micro_deno = 0.0, 0.0 
	
	for i in range(max_num):
		ai = aa[:, i]
		bi = bb[:, i]
		f1, numerator, denominator = 0.0, 0.0, 0.0 
		for j in range(len(ai)):
			yir = ai[j]
			zir = bi[j]
			numerator += 2*yir*zir 
			denominator += (yir + zir)
			micro_num += 2*yir*zir 
			micro_deno += (yir + zir)
			
		if denominator > 0:
			f1 = numerator / denominator
		else:
			f1 = 0.0 
		macro_f1s += f1 
	macro_f1s = macro_f1s/max_num
	
	return macro_f1s, micro_num/micro_deno
		
def one_error(aa, bb): # random select one as the top ranked 
	o_error = 0.0
	
	for i in range(len(aa)):
		a = aa[i]
		b = bb[i]
		a_labels = return_labels(a)
		b_labels = return_labels(b)
		random.shuffle(b_labels)
		# print b_labels
		if len(b_labels) > 0:
			select = b_labels[0]
			if select not in a_labels:
				o_error += 1.0 
		else:
			o_error += 1.0 
	return o_error/len(aa)
				


with open(sys.argv[1], 'r') as f:
	lines = list(csv.reader(f))

preds = []
trues = []
max_num = 14 

major_labels = {}

for line in lines[1:]:
	rev, label = line[0], line[1]
	if len(label) > 0:
		labels_ = label.split(',')
		labels_ = [int(v) for v in labels_]
		labels = transform_labels(labels_, max_num)
		for i in range(len(labels)):
			if i not in major_labels:
				major_labels[i] = {0:0, 1:0}
			major_labels[i][labels[i]] += 1 
		class_ = random.randint(0, max_num-1)
		pred = [0]*max_num
		pred[class_] = 1 
		# pred = [random.randint(0, 1) for i in range(max_num)]
		preds.append(pred)
		trues.append(labels)
major = []

# print major_labels

for i in range(max_num):
	cnt0, cnt1 = major_labels[i][0], major_labels[i][1]
	# print cnt0
	if cnt0 > cnt1:
		major.append(0)
	elif cnt1 > cnt0:
		major.append(1)
	else:
		major.append(random.randint(0,1))
	
major = [0]*max_num
major[5] = 1 

majors = [] 
for i in range(len(preds)):
	majors.append(major)

# extract match 
print '[result for random guess]'
print 'exact match = ' + str(extract_match(trues, preds))
eacc, eprec, erecall, ef1 = example_based(trues, preds)
print 'example based accuracy = ' + str(eacc)
print 'example based precision = ' + str(eprec)
print 'example based recall = ' + str(erecall)
print 'example based f1 score = ' + str(ef1)
macro_f1s, micro_f1s = label_based(trues, preds, max_num)
print 'label based macro f1 = ' + str(macro_f1s)
print 'label based micro f1 = ' + str(micro_f1s)
print 'ranking one error = ' + str(one_error(trues, preds))

print 'result for majority voting'
print majors[0]
print 'exact match = ' + str(extract_match(trues, majors))
eacc, eprec, erecall, ef1 = example_based(trues, majors)
print 'example based accuracy = ' + str(eacc)
print 'example based precision = ' + str(eprec)
print 'example based recall = ' + str(erecall)
print 'example based f1 score = ' + str(ef1)
macro_f1s, micro_f1s = label_based(trues, majors, max_num)
print 'label based macro f1 = ' + str(macro_f1s)
print 'label based micro f1 = ' + str(micro_f1s)
print 'ranking one error = ' + str(one_error(trues, majors))

		
		