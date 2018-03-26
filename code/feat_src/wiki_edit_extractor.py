from mwapi import Session
from revscoring.extractors import api
from revscoring.features import temporal, wikitext, wikibase 
from revscoring.datasources import revision_oriented as ro
from datasources.diff import (operations_return, relocation_segments_context, added_segments_context, operations_context, removed_segments_context, operations_with_context)

from revscoring.languages import english

from wiki_edit_util import *
from gensim.models import word2vec 

model = word2vec.Word2Vec.load_word2vec_format('./wiki_revision_trained_embedding.bin', binary=True)

# revision_id = 687120365

session = Session("https://en.wikipedia.org/w/api.php", user_agent="test")
api_extractor = api.Extractor(session)

MAX_NUM = 14
features = [	
		# *** user
		## ro.revision.user.id, # id = 0 for ip
		## ro.revision.user.info.groups,
		## ro.revision.user.registeration,
		## ro.revision.user.gender,
		# *** revision - overall 
		## ro.revision.byte_len,
		## ro.revision.comment,
		## ro.revision.minor,
		## ro.revision.timestamp,
		### ro.revision.text,
		# page 
		# ro.revision.page.id,
		ro.revision.page.namespace.id,	
		ro.revision.minor,
		ro.revision.byte_len, 
		
		## char features
		wikitext.revision.diff.uppercase_words_added,
		wikitext.revision.diff.chars_added,
		wikitext.revision.diff.chars_removed,
		wikitext.revision.diff.numeric_chars_added,
		wikitext.revision.diff.numeric_chars_removed,
		wikitext.revision.diff.whitespace_chars_added,
		wikitext.revision.diff.whitespace_chars_removed,
		wikitext.revision.diff.markup_chars_added,
		wikitext.revision.diff.markup_chars_removed,
		wikitext.revision.diff.cjk_chars_added,
		wikitext.revision.diff.cjk_chars_removed,
		wikitext.revision.diff.entity_chars_added,
		wikitext.revision.diff.entity_chars_removed,
		wikitext.revision.diff.url_chars_added,
		wikitext.revision.diff.url_chars_removed,
		wikitext.revision.diff.word_chars_added,
		wikitext.revision.diff.word_chars_removed,
		wikitext.revision.diff.uppercase_words_added,
		wikitext.revision.diff.uppercase_words_removed,
		wikitext.revision.diff.punctuation_chars_added,
		wikitext.revision.diff.punctuation_chars_removed,
		## token features
		wikitext.revision.diff.token_delta_sum,
		wikitext.revision.diff.token_delta_increase,
		wikitext.revision.diff.token_delta_decrease,
		wikitext.revision.diff.token_prop_delta_sum,
		wikitext.revision.diff.token_prop_delta_increase,
		wikitext.revision.diff.token_prop_delta_decrease,
		wikitext.revision.diff.number_delta_sum,
		wikitext.revision.diff.number_delta_increase,
		wikitext.revision.diff.number_delta_decrease,
		wikitext.revision.diff.number_prop_delta_sum,
		wikitext.revision.diff.number_prop_delta_increase,
		wikitext.revision.diff.number_prop_delta_decrease,
		wikitext.revision.diff.whitespace_delta_sum,
		wikitext.revision.diff.whitespace_delta_increase,
		wikitext.revision.diff.whitespace_delta_decrease,
		wikitext.revision.diff.whitespace_prop_delta_sum,
		wikitext.revision.diff.whitespace_prop_delta_increase,
		wikitext.revision.diff.whitespace_prop_delta_decrease,
		wikitext.revision.diff.markup_delta_sum,
		wikitext.revision.diff.markup_delta_increase,
		wikitext.revision.diff.markup_delta_decrease,
		wikitext.revision.diff.markup_prop_delta_sum,
		wikitext.revision.diff.markup_prop_delta_increase,
		wikitext.revision.diff.markup_prop_delta_decrease,
		wikitext.revision.diff.cjk_delta_sum,
		wikitext.revision.diff.cjk_delta_increase,
		wikitext.revision.diff.cjk_delta_decrease,
		wikitext.revision.diff.cjk_prop_delta_sum,
		wikitext.revision.diff.cjk_prop_delta_increase,
		wikitext.revision.diff.cjk_prop_delta_decrease,
		wikitext.revision.diff.entity_delta_sum,
		wikitext.revision.diff.entity_delta_increase,
		wikitext.revision.diff.entity_delta_decrease,
		wikitext.revision.diff.entity_prop_delta_sum,
		wikitext.revision.diff.entity_prop_delta_increase,
		wikitext.revision.diff.entity_prop_delta_decrease,
		wikitext.revision.diff.url_delta_sum,
		wikitext.revision.diff.url_delta_increase,
		wikitext.revision.diff.url_delta_decrease,
		wikitext.revision.diff.url_prop_delta_sum,
		wikitext.revision.diff.url_prop_delta_increase,
		wikitext.revision.diff.url_prop_delta_decrease,
		wikitext.revision.diff.word_delta_sum,
		wikitext.revision.diff.word_delta_increase,
		wikitext.revision.diff.word_delta_decrease,
		wikitext.revision.diff.word_prop_delta_sum,
		wikitext.revision.diff.word_prop_delta_increase,
		wikitext.revision.diff.word_prop_delta_decrease,
		wikitext.revision.diff.uppercase_word_delta_sum,
		wikitext.revision.diff.uppercase_word_delta_increase,
		wikitext.revision.diff.uppercase_word_delta_decrease,
		wikitext.revision.diff.uppercase_word_prop_delta_sum,
		wikitext.revision.diff.uppercase_word_prop_delta_increase,
		wikitext.revision.diff.uppercase_word_prop_delta_decrease,
		wikitext.revision.diff.punctuation_delta_sum,
		wikitext.revision.diff.punctuation_delta_increase,
		wikitext.revision.diff.punctuation_delta_decrease,
		wikitext.revision.diff.punctuation_prop_delta_sum,
		wikitext.revision.diff.punctuation_prop_delta_increase,
		wikitext.revision.diff.punctuation_prop_delta_decrease,
		wikitext.revision.diff.break_delta_sum,
		wikitext.revision.diff.break_delta_increase,
		wikitext.revision.diff.break_delta_decrease,
		wikitext.revision.diff.break_prop_delta_sum,
		wikitext.revision.diff.break_prop_delta_increase,
		wikitext.revision.diff.break_prop_delta_decrease,
		## token edit features
		wikitext.revision.diff.segments_added,
		wikitext.revision.diff.segments_removed,
		wikitext.revision.diff.tokens_added,
		wikitext.revision.diff.tokens_removed,
		wikitext.revision.diff.numbers_added,
		wikitext.revision.diff.numbers_removed,
		wikitext.revision.diff.markups_added,
		wikitext.revision.diff.markups_removed,
		wikitext.revision.diff.whitespaces_added,
		wikitext.revision.diff.whitespaces_removed,
		wikitext.revision.diff.cjks_added,
		wikitext.revision.diff.cjks_removed,
		wikitext.revision.diff.entities_added,
		wikitext.revision.diff.entities_removed,
		wikitext.revision.diff.urls_added,
		wikitext.revision.diff.urls_removed,
		wikitext.revision.diff.words_added,
		wikitext.revision.diff.words_removed,
		wikitext.revision.diff.uppercase_words_added,
		wikitext.revision.diff.uppercase_words_removed,
		wikitext.revision.diff.punctuations_added,
		wikitext.revision.diff.punctuations_removed,
		wikitext.revision.diff.breaks_added,
		wikitext.revision.diff.breaks_removed,
		wikitext.revision.diff.longest_token_added,
		wikitext.revision.diff.longest_uppercase_word_added,
		
		# *** language features 
		# *** stop word features 
		english.stopwords.revision.diff.stopwords_added,
		english.stopwords.revision.diff.stopwords_removed,
		english.stopwords.revision.diff.non_stopwords_added,
		english.stopwords.revision.diff.non_stopwords_removed,
		english.stopwords.revision.diff.stopword_delta_sum,
		english.stopwords.revision.diff.stopword_delta_increase,
		english.stopwords.revision.diff.stopword_delta_decrease,
		english.stopwords.revision.diff.non_stopword_delta_sum,
		english.stopwords.revision.diff.non_stopword_delta_increase,
		english.stopwords.revision.diff.non_stopword_delta_decrease,
		english.stopwords.revision.diff.stopword_prop_delta_sum,
		english.stopwords.revision.diff.stopword_prop_delta_increase,
		english.stopwords.revision.diff.stopword_prop_delta_decrease,
		english.stopwords.revision.diff.non_stopword_prop_delta_sum,
		english.stopwords.revision.diff.non_stopword_prop_delta_increase,
		english.stopwords.revision.diff.non_stopword_prop_delta_decrease,
		
		# *** stemmed features 
		english.stemmed.revision.diff.stem_delta_sum,
		english.stemmed.revision.diff.stem_delta_increase,
		english.stemmed.revision.diff.stem_delta_decrease,
		english.stemmed.revision.diff.stem_prop_delta_sum,
		english.stemmed.revision.diff.stem_prop_delta_increase,
		english.stemmed.revision.diff.stem_prop_delta_decrease,
		
		# *** badwords 
		english.badwords.revision.diff.matches_added,
		english.badwords.revision.diff.matches_removed,
		english.badwords.revision.diff.match_delta_sum,
		english.badwords.revision.diff.match_delta_increase,
		english.badwords.revision.diff.match_delta_decrease,
		english.badwords.revision.diff.match_prop_delta_sum,
		english.badwords.revision.diff.match_prop_delta_increase,
		english.badwords.revision.diff.match_prop_delta_decrease,
		
		# *** informals
		english.informals.revision.diff.matches_added,
		english.informals.revision.diff.matches_removed,
		english.informals.revision.diff.match_delta_sum,
		english.informals.revision.diff.match_delta_increase,
		english.informals.revision.diff.match_delta_decrease,
		english.informals.revision.diff.match_prop_delta_sum,
		english.informals.revision.diff.match_prop_delta_increase,
		english.informals.revision.diff.match_prop_delta_decrease
	   ]

text_features = [
		wikitext.revision.diff.datasources.segments_added,
		wikitext.revision.diff.datasources.segments_removed,
		added_segments_context,
		removed_segments_context,
		relocation_segments_context,
		ro.revision.user.id,
		ro.revision.user.info.gender,
		ro.revision.comment,
		ro.revision.timestamp,
		ro.revision.user.info.registration
]

	
def return_construct_feats(feats):
	if len(feats) != 10:
		print('feats not equal 10')
		exit(-1)
	# print(feats)
	segment_added, segment_removed, segment_added_context, segment_removed_context, relocation_text, userid, gender, comment, rev_timestamp, registeration = feats 
	
	return_feats = []
	return_feats.append(spell_error(segment_removed)) # spell error removed 
	return_feats.append(spell_error(segment_added)) # spell error added 
	
	return_feats.append(stem_overlap(segment_added, segment_removed)) # 
	return_feats.extend(simi_overlap(segment_added, segment_removed, model)) # 
	
	return_feats.append(user_history(rev_timestamp, registeration)) # user registeration seconds 
	
	return_feats.append(comment_revert(comment)) # revert features 
	return_feats.append(comment_length(comment)) # comment length 
	return_feats.append(comment_typo(comment)) # comment typo
	
	return_feats.append(reloc_len(relocation_text)) # relocation length 
	return_feats.append(is_registered(userid)) # user id 
	return_feats.append(gender_type(gender)) # gender 
	
	return_feats.append(segment_length(segment_added)) #  segment_added
	return_feats.append(segment_length(segment_removed)) #  segment_removed
	
	return_feats.append(segment_search_external(segment_added)) # external link segment_added
	return_feats.append(segment_search_external(segment_removed))
	
	return_feats.append(segment_search_file(segment_added)) #  file segment_added
	return_feats.append(segment_search_file(segment_removed))
	
	return_feats.append(segment_template(segment_added)) #  emplate segment_added
	return_feats.append(segment_template(segment_removed))
	
	return_feats.append(segment_reference(segment_added)) #  reference segment_added
	return_feats.append(segment_reference(segment_removed))
	
	return_feats.append(segment_internal(segment_added)) #  internal segment_added
	return_feats.append(segment_internal(segment_removed))
	
	return_feats.append(segment_external(segment_added)) #  external segment_added
	return_feats.append(segment_external(segment_removed))
	
	return_feats.append(segment_file(segment_added)) #  file segment_added
	return_feats.append(segment_file(segment_removed))
	
	return_feats.append(segment_markup(segment_added)) #  markup segment_added
	return_feats.append(segment_markup(segment_removed))
	
	return_feats.append(operation_in_template(segment_added, segment_added_context))
	return_feats.append(operation_in_template(segment_removed, segment_removed_context))
	
	return_feats.append(operation_in_reference(segment_added, segment_added_context))
	return_feats.append(operation_in_reference(segment_removed, segment_removed_context))
	
	return_feats.append(operation_in_internal(segment_added, segment_added_context))
	return_feats.append(operation_in_internal(segment_removed, segment_removed_context))
	
	return_feats.append(operation_in_external(segment_added, segment_added_context))
	return_feats.append(operation_in_external(segment_removed, segment_removed_context))
	
	return_feats.append(operation_in_file(segment_added, segment_added_context))
	return_feats.append(operation_in_file(segment_removed, segment_removed_context))
	
	return_feats.append(is_template(segment_added, segment_added_context))
	return_feats.append(is_template(segment_removed, segment_removed_context))
	
	return_feats.append(is_reference(segment_added, segment_added_context))
	return_feats.append(is_reference(segment_removed, segment_removed_context))
	
	return_feats.append(is_internal(segment_added, segment_added_context))
	return_feats.append(is_internal(segment_removed, segment_removed_context))
	
	return_feats.append(is_external(segment_added, segment_added_context))
	return_feats.append(is_external(segment_removed, segment_removed_context))
	
	return_feats.append(is_markup(segment_added, segment_added_context))
	return_feats.append(is_markup(segment_removed, segment_removed_context))
	
	return_feats.append(is_file(segment_added, segment_added_context))
	return_feats.append(is_file(segment_removed, segment_removed_context))
	
	return return_feats
	
def generate_features(rev_ids):
	X, Y = [], []
	
	for revision_id, labels in rev_ids.items():
		feats, text_feats = None, None
		
		print(revision_id)
		try:		
			feats, text_feats = [], []
			values = api_extractor.extract(int(revision_id), features)
			zip_feat_values = zip(features, values)
			for f, v in zip_feat_values:
				feats.append(v)
			
			text_values = api_extractor.extract(int(revision_id), text_features)
			zip_text_feat_values = zip(text_features, text_values)
			for f, v in zip_text_feat_values:
				text_feats.append(v)
		except Exception as e:
			continue
			
		
		if (feats is None) or (text_feats is None):
			print('feats or text_feats is None')
			continue
		
		process_text_feats = return_construct_feats(text_feats)
		
		ans_feats = feats + process_text_feats
		ans_feats_values = []
		
		for v in ans_feats:
			if v is None:
				ans_feats_values.append(-1.0)
			else:
				ans_feats_values.append(float(v))
		X.append(ans_feats_values)
		
		y = transform_labels(labels, MAX_NUM)
		Y.append(y)
	return X, Y 

def generate_features_Y(rev_ids):
	Y = []
	
	for revision_id, labels in rev_ids.items():
		'''feats, text_feats = None, None
		
		print(revision_id)
		try:		
			feats, text_feats = [], []
			values = api_extractor.extract(int(revision_id), features)
			zip_feat_values = zip(features, values)
			for f, v in zip_feat_values:
				feats.append(v)
			
			text_values = api_extractor.extract(int(revision_id), text_features)
			zip_text_feat_values = zip(text_features, text_values)
			for f, v in zip_text_feat_values:
				text_feats.append(v)
		except Exception as e:
			continue
			
		
		if (feats is None) or (text_feats is None):
			print('feats or text_feats is None')
			continue
		
		process_text_feats = return_construct_feats(text_feats)
		
		ans_feats = feats + process_text_feats
		ans_feats_values = []
		
		for v in ans_feats:
			if v is None:
				ans_feats_values.append(-1.0)
			else:
				ans_feats_values.append(float(v))
		X.append(ans_feats_values)
		'''
		y = transform_labels(labels, MAX_NUM)
		Y.append(y)
	return Y 

