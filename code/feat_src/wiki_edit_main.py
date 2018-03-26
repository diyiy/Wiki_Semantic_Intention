import sys, csv
from wiki_edit_extractor import *
from wiki_edit_util import *
# from skmultilearn.lazy.mlknn import KNearestNeighbours
# from skmultilearn.lazy.brknn import BinaryRelevanceKNN
from sklearn.naive_bayes import GaussianNB
# from skmultilearn.meta.rakeld import RakelD
import numpy as np
import sklearn.metrics
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.cross_validation import cross_val_score
from sklearn import linear_model
from sklearn.svm import LinearSVC
import pickle
import os.path
from sklearn.decomposition import PCA 

csv.field_size_limit(sys.maxsize)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("Usage: <input_annotation_csv>\n")
		exit(-1)	
	
	with open(sys.argv[1], 'r') as f:
		annotate_lines = list(csv.reader(f))
	
	revision_labels = {}
	for line in annotate_lines[1:]:
		rid, label_text = int(line[0]), line[1]
		
		if len(label_text) < 1:
			continue
		labels = [int(v) for v in label_text.split(',')]
		
		if rid not in revision_labels:
			revision_labels[rid] = labels
	
	# construct features 
	#if not os.path.exists('X_5000.pk'):
	X, Y = generate_features(revision_labels)
	# X = np.matrix(X, dtype=np.float64)
		
	# print(len(X[0]))
	# print(Y)
	#	pickle.dump(X, open("X_5000.pk", "wb" ))
	#	pickle.dump(Y, open("Y_5000.pk", "wb" ))
	#else:
	#	X = pickle.load(open('X_5000.pk', 'rb'))
	#	Y = pickle.load(open('Y_5000.pk', 'rb'))
		
	# PCA 
	#pca = PCA(n_components=50)
	#X = pca.fit_transform(X)
	#print(pca.explained_variance_ratio_)
	#print(X.shape)
	transform_to_arff(X, Y, sys.argv[1] + '.1008.arff')
	'''
	lr = OneVsRestClassifier(LinearSVC(random_state=19910820))
	X = np.matrix(X, dtype=np.float64)
	Y = np.array(Y)
	# lr = OneVsRestClassifier(SVC(kernel='linear'))
	lr.fit(X, Y)
	print(lr.score(X, Y))
	accuracy = cross_val_score(lr, X, Y, scoring='accuracy', cv=3)
	print('10 cross validation accuracy = ' + str(sum(accuracy)/len(accuracy)))
	'''