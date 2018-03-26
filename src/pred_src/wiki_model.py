import sys, os

def cross_validation(arff_filename, model):
	if model.find('BinaryRelevance') != -1:
		# print '10-cross validation for bianry relevance'
		command = "java -jar BinaryRelevance.jar -arff " + arff_filename + " -xml edit_intention.xml"
		os.system(command)
	elif model.find('RAKEL') != -1:
		# print '10-cross validation for RAKEL'
		command = "java -jar RAKEL.jar -arff " + arff_filename + " -xml edit_intention.xml"
		os.system(command)
	elif model.find('MLKNN') != -1:
		#print '10-cross validation for MLKNN'
		command = "java -jar MLKNN.jar -arff " + arff_filename + " -xml edit_intention.xml"
		os.system(command)
	else:
		print('[Error]: unrecognized model parameter')

def model_prediction(arff_filename, unlabeled_filename):
	predict_filename = unlabeled_filename[:-5] + '.pred.txt'
	predict_command = "java -jar BinaryRelevancePredict.jar -arff " + arff_filename + " -xml edit_intention.xml -unlabeled " + unlabeled_filename + ' -pred ' + predict_filename
	os.system(predict_command)
	
model_prediction(sys.argv[1], sys.argv[2])
	




