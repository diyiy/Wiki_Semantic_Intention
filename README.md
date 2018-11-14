# Identifying Edit Intentions from Revisions in Wikipedia
We develop in collaboration with Wikipedia editors a 13-category taxonomy of the semantic intention behind edits in Wikipedia articles. 
Using labeled article edits, we build a computational classifier of intentions that achieved a micro-averaged F1 score of 0.621.

## Install

```
conda create --name wiki_edit_intention python=3.5 
source activate wiki_edit_intention
pip install mwapi 
pip install revscoring
```

You might also need to install some dependencies (e.g., scipy, numpy and sklearn).

## Run

To make features associated with each revision, please run:

```python ./feat_src/wiki_edit_main.py edit_intention_dataset.csv```

This will generate an arff file "edit_intention_dataset.feats.arff".

To predict the edit intentions for a set of revisions, please run:

```python ./pred_src/wiki_model.py edit_intention_dataset.feats.arff test_file_to_be_predicted.arff```

## Data 

To retrive the content of each revision, please use:

```https://en.wikipedia.org/wiki/WP:Labels?diff=<replace_with_revision_id>```

The mapping from label to edit intention can be found below:

```
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
```

To use our trained word embeddings for Wikipedia article revision, please download it from this link:
[https://goo.gl/An7DZP](wiki_revision_trained_embedding.bin)

## Cite

If you use our tools for your work, please cite the following paper:

* Yang, Diyi, Aaron Halfaker, Robert Kraut, and Eduard Hovy. "Identifying semantic edit intentions from revisions in wikipedia." In Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing, pp. 2000-2010. 2017.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
