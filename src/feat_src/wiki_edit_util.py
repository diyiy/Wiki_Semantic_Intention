from mwapi import Session
from revscoring.extractors import api
from revscoring.features import temporal, wikitext, wikibase 
from revscoring.datasources import revision_oriented as ro
from datasources.diff import (operations_return, relocation_segments_context, added_segments_context, operations_context, removed_segments_context, operations_with_context)
import datetime, time, re, operator
from mwtypes import Timestamp
import enchant
import enchant
from nltk import PorterStemmer
# from gensim.models import word2vec 

# model = word2vec.Word2Vec.load_word2vec_format('./wiki_revision_trained_embedding.bin', binary=True)

d = enchant.Dict('en_US')

TEMPLATE = ['{{', '}}']

REFERENCE = ['[', ']', '<ref>', '</ref>', 'reference', 'ref']

EXTERNAL = ['http:', 'https:', '//:', '.com']
EXTERNAL_RE = '((http|https)://)'

WIKILINK = ['[[',']]']

FILE = ['file', 'image', 'media']
FILE_RE = '(\[\[[File:|Image:|Media:])'

MARKUP = ['===', '==', '=', '<div', '</div>', '*', '**', '***', '****', '#', '##', '###', '####', '<dl>',
			'<small>', '<sup>', '<sub>', '<span>']

SPAN = 30

def simi_overlap(added_segments, removed_segments, model):
	added = ' '.join(added_segments).lower().split()
	removed = ' '.join(removed_segments).lower().split()
	
	max_simi, min_simi, avg_simi = 0.0, 1.0, 0.0
	simi_cnt = 0.0 
	
	for s in added:
		for t in removed:
			if (s in model) and (t in model):
				simi = model.similarity(s, t)
				max_simi = max(simi, max_simi)
				min_simi = min(simi, min_simi)
				avg_simi += simi 
				simi_cnt += 1 
	return max_simi, min_simi, avg_simi/max(1, simi_cnt)
	
def spell_error(sentence):
	mis_spell = 0.0
	sentence = str(sentence)
	for token in sentence.split():
		if d.check(token) == False:
			mis_spell += 1
	return mis_spell
	
def stem_words(segments):
	tokens = []
	for s in segments:
		ss = s.lower().split()
		tokens.extend(ss)
	ans = set()
	for t in tokens:
		stem_t = PorterStemmer().stem_word(t)
		ans.add(stem_t)
	return ans 
	
def stem_overlap(added_segments, removed_segments):
	added_set = stem_words(added_segments)
	removed_set = stem_words(removed_segments)
	return len(added_set & removed_set)
	
def is_ascii(s):
	return all(ord(c) < 128 for c in s)
	
def remove_nonascii(text):
	return ''.join([i if ord(i) < 128 else ' ' for i in text])

def set_contain_words(sentence, words):
	word_cnt = 0
	tokens = sentence.lower().split(' ')
	for i in range(len(tokens)):
		if tokens[i] in words:
			word_cnt += 1
	return word_cnt

def segment_search(segment, pattern):
	res = 0.0
	for context in segment:
		s_obj = re.search(pattern, context)
		if s_obj:
			res += 1
	return res

def segment_count(segment, wset):
	res = 0.0
	for line in segment:
		res += set_contain_words(line.lower(), set(wset))
	return res

def segment_in(segments, contexts, wset):
	word_segments = 0 
	for segment, context in zip(segments, contexts):
		segment, context = remove_nonascii(segment), remove_nonascii(context)
		pos = context.find(segment)
		text_span = context[max(0, pos - SPAN): pos] + " " + context[pos + len(segment): min(pos + len(segment) + SPAN, len(context))]
		word_segments += set_contain_words(text_span, set(wset))
	return word_segments
	
def gender_type(gender):
	if gender is None: 
		return -1
	if gender.find('unknown') != -1:
		return 0 
	if gender.find('female') != -1:
		return 1 
	if gender.find('male') != -1:
		return 2
		
def reloc_len(texts):
	return len(texts)
	
def is_registered(uid):
	if int(uid) == 0:
		return 0 
	else:
		return 1 
		
def user_history(rev_time, reg_time):# seconds 
	# print(type(rev_time))
	# print(type(reg_time))
	if (rev_time is not None) and (reg_time is not None):
		return rev_time - reg_time 
	else:
		return -1.0 # if registeration time is None

def comment_revert(text):
	wset = set(['revert', 'reverted', 'rvt'])
	return set_contain_words(text.lower(), wset)
	
def comment_length(text):
	return len(text)

def segment_length(segment): # added or removed
	res_len = 0.0
	for s in segment:
		res_len += len(s) 
	return res_len

def comment_typo(text):
	wset = set(['typo', 'grammar', 'format', 'formatting', 'error', 'cleanup'
				'spelling', 'misspell', 'correction', 'copy', 'editor'])
	return set_contain_words(text.lower(), wset)

def segment_search_external(segment):
	return segment_search(segment, EXTERNAL_RE)

def segment_search_file(segment):
	return segment_search(segment, FILE_RE)

def segment_template(line):
	return segment_count(line, TEMPLATE)

def segment_reference(line):
	return segment_count(line, REFERENCE)

def segment_internal(line):
	return segment_count(line, WIKILINK)

def segment_external(line):
	return segment_count(line, EXTERNAL)

def segment_file(line):
	return segment_count(line, FILE)

def segment_markup(line):
	return segment_count(line, MARKUP)

def operation_in_template(segments, contexts):
	res = 0
	for segment, context in zip(segments, contexts):
		segment, context = remove_nonascii(segment), remove_nonascii(context)
		
		new_segment = re.escape(segment)
		pattern = '(\{\{\w*' + new_segment + '\w*\}\})'
		search_res = re.search(pattern, context)
		if search_res:
			res += 1
	return res

def operation_in_reference(segments, contexts):
	res = 0
	for segment, context in zip(segments, contexts):
		segment, context = remove_nonascii(segment), remove_nonascii(context)
		new_segment = re.escape(segment)
		pattern = '(ref\w*' + new_segment + '\w*\/ref)'
		search_res = re.search(pattern, context)
		if search_res:
			res += 1
	return res 

def operation_in_internal(segments, contexts):

	res = 0
	for segment, context in zip(segments, contexts):
		segment, context = remove_nonascii(segment), remove_nonascii(context)
		new_segment = re.escape(segment)
		pattern = '(\[\[\w*' + new_segment + '\w*\]\])'
		search_res = re.search(pattern, context)
		if search_res:
			res += 1
	return res 	

def operation_in_external(segments, contexts):
	res = 0 
	for segment, context in zip(segments, contexts):
		segment, context = remove_nonascii(segment), remove_nonascii(context)

		new_segment = re.escape(segment)

		pattern_t = '(\[[https:|http:]?\/\/:\w*' + new_segment + '\w*\])'
		search_res = re.search(pattern_t, context)
		if search_res:
			res += 1
	return res 
	
def operation_in_file(segments, contexts):
	res = 0 
	for segment, context in zip(segments, contexts):
		segment, context = remove_nonascii(segment), remove_nonascii(context)
		new_segment = re.escape(segment)
		pattern_t = '(\[\[[File:|Image:|Media:]\w*' + new_segment + '\w*\]\])'
		search_res = re.search(pattern_t, context)
		if search_res:
			res += 1
	return res

def is_template(segments, contexts):
	return segment_in(segments, contexts, TEMPLATE)
def is_reference(segments, contexts):
	return segment_in(segments, contexts, REFERENCE)
def is_internal(segments, contexts):
	return segment_in(segments, contexts, WIKILINK)
def is_external(segments, contexts):
	return segment_in(segments, contexts, EXTERNAL)
def is_markup(segments, contexts):
	return segment_in(segments, contexts, MARKUP)
def is_file(segments, contexts):
	return segment_in(segments, contexts, FILE)
	
def transform_labels(labels, max_num):
	gen_labels = [0]*max_num
	for label in labels:
		gen_labels[label] = 1 
	return gen_labels
	
def transform_to_arff(X, Y, filename):
	X = list(X)
	Y = list(Y)
	class_names = {'counter-vandalism':0, 'fact-update': 1, 'refactoring':2, 'copy-editing':3, 'other':4, 'wikification':5, 'vandalism':6, 'simplification':7, 'elaboration':8, 'verifiability':9, 'process':10, 'clarification':11,
					'disambiguation':12, 'point-of-view':13}
	
	feature_len = len(X[0])
	
	output = ''
	output += '@relation edit_itention\n'
	output += '\n'
	
	for i in range(feature_len):
		output += '@attribute feats_' + str(i) + ' numeric\n'
	
	class_names = sorted(class_names.items(), key=operator.itemgetter(1))
	for name, ids in class_names:
		output += '@attribute ' + name + ' {0,1}\n'
	output += '\n'
	
	output += '@data\n'
	
	for i in range(len(X)):
		x = list(X[i])
		y = list(Y[i])
		feat = x + y 
		feat_str = ','.join(map(str,feat))
		output += feat_str + '\n'
	f = open(filename, 'w') 
	f.write(output)
	f.close()
	
	