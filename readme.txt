* ./feat_src/
	- wiki_edit_extractor.py
	- wiki_edit_main.py
	- wiki_edit_util.py

	To make features, please run:
		python ./feat_src/wiki_edit_main.py edit_intention_dataset.csv
	This will generate an arff file "edit_intention_dataset.feats.arff". 
* ./pred_src/
	To run the classifier, please run:
		python ./pred_src/wiki_model.py edit_intention_dataset.feats.arff test_file_to_be_predicted.arff

* edit_intention_dataset.csv

	The format of this dataset is:
		<revision id>\t<labels>

	To retrive the content of each revision, please use: https://en.wikipedia.org/wiki/WP:Labels?diff=<replace_with_revision_id>
	The labels (numbers) are seperated by comma, if there are multiple. The mapping from number to label can be found below:
		{	
			'counter-vandalism':0, 
			'fact-update': 1, 
			'refactoring':2, 
			'copy-editing':3, 
			'other':4, 
			'wikification':5, 
			'vandalism':6, 
			'simplification':7, 
			'elaboration':8, 
			'verifiability':9, 
			'process':10, 
			'clarification':11,
			'disambiguation':12, 
			'point-of-view':13
		}
