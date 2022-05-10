# from transformers import BertForQuestionAnswering
# from spacy.matcher import PhraseMatcher
# from transformers import BertTokenizer
# from math import ceil
# import spacy
# import torch
#
#
# nlp = spacy.load('en_core_web_sm')
# model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
# tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
#
#
# def get_berts_ans(question, answer_text, display=False):
#     """
#     Takes a `question` string and an `answer_text` string (which contains the
#     answer), and identifies the words within the `answer_text` that are the
#     answer. Prints them out.
#     """
#     # ======== Tokenize ========
#     # Apply the tokenizer to the input text, treating them as a text-pair.
#     input_ids = tokenizer.encode(question, answer_text)
#
#     # Report how long the input sequence is.
#     print('Query has {:,} tokens.\n'.format(len(input_ids))) if display else None
#
#     # ======== Set Segment IDs ========
#     # Search the input_ids for the first instance of the `[SEP]` token.
#     sep_index = input_ids.index(tokenizer.sep_token_id)
#
#     # The number of segment A tokens includes the [SEP] token istelf.
#     num_seg_a = sep_index + 1
#
#     # The remainder are segment B.
#     num_seg_b = len(input_ids) - num_seg_a
#
#     # Construct the list of 0s and 1s.
#     segment_ids = [0]*num_seg_a + [1]*num_seg_b
#
#     # There should be a segment_id for every input token.
#     assert len(segment_ids) == len(input_ids)
#
#     # ======== Evaluate ========
#     # Run our example through the model.
#     outputs = model(torch.tensor([input_ids]), # The tokens representing our input text.
#                     token_type_ids=torch.tensor([segment_ids]), # The segment IDs to differentiate question from answer_text
#                     return_dict=True)
#
#     start_scores = outputs.start_logits
#     end_scores = outputs.end_logits
#
#     # ======== Reconstruct Answer ========
#     # Find the tokens with the highest `start` and `end` scores.
#     answer_start = torch.argmax(start_scores)
#     answer_end = torch.argmax(end_scores)
#
#     # Get the string versions of the input tokens.
#     tokens = tokenizer.convert_ids_to_tokens(input_ids)
#
#     # Start with the first token.
#     answer = tokens[answer_start]
#
#     # Select the remaining answer tokens and join them with whitespace.
#     for i in range(answer_start + 1, answer_end + 1):
#         # If it's a subword token, then recombine it with the previous token.
#         if tokens[i][0:2] == '##':
#             answer += tokens[i][2:]
#         # Otherwise, add a space then the token.
#         else:
#             answer += ' ' + tokens[i]
#     return answer
#
#
# def remove_punc(word):
#     # Removes all punctuation from a string word
#     for c in '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~''':
#         word = word.replace(c, "")
#     return word  # Returns a string
#
#
# def create_stop_words(nlp):
#     # Calls stop words from nlp Spacy
#     stop_words = nlp.Defaults.stop_words
#
#     # Include stop qords found in questions, they are not keywords
#     stop_words.add("why")
#     stop_words.add("who")
#     stop_words.add("what")
#     stop_words.add("when")
#     stop_words.add("where")
#
#     return stop_words # Returns a set
#
#
# def get_keywords(question, keywords):
#     # Any keywords passed as arguments to this function ARE NOT DROPPED OR REPLACED
#
#     # Calls set of stop words from Spacy, including common question words
#     stop_words = create_stop_words(nlp)
#
#     # Iterate over all words in the question
#     for word in question.lower().split(' '):
#         # Remove punctuation from words
#         word = remove_punc(word)
#         # Search for all common stop words in question and excludes them
#         if word not in stop_words and word not in keywords:
#             keywords.append(word)
#     return keywords  # Returns a list
#
#
# def gen_phrase_Matcher(keywords, nlp):
#
#     # Instantiate phrase matcher object from Spacy using Spacy vocabulary field
#     phrase_matcher = PhraseMatcher(nlp.vocab)
#
#     # Create a pattern using keywords from question
#     patterns = [nlp(word) for word in keywords]
#
#     # Add pattern to 'empty' phrase matcher object
#     phrase_matcher.add('_', None, *patterns)
#
#     return phrase_matcher # Returns a phrase matcher object, see Spacy documentation
#
#
# def combine_phrases(matched_phrases, doc):
#     par_len = 0
#     minitext = ''
#
#     for match_id, start, end in matched_phrases:
#         # Iterate through sentences that contain phrases using document indices
#         sentence = doc[start:end].sent.text
#         # Exclude any duplicate sentences, often occur from a sentence containing two or more pattern words
#         if sentence not in minitext:
#             # Add sentence to minitext
#             minitext = minitext + sentence + ' '
#             # Increase paragraph length by 1 for every sentence
#             par_len = par_len + 1
#     # Returns intiger and string text
#     return par_len, minitext[1:]
#
#
# def gen_minitext(text, question, nlp, keywords):
#     # Create document object from string text
#     doc = nlp(text)
#     # Get keywords, excluding stop words, from question
#     keywords = get_keywords(question, keywords)
#     # Generate phrase matcher object using keywords
#     phrase_matcher = gen_phrase_Matcher(keywords, nlp)
#     # Scan document object for any keywords
#     matched_phrases = phrase_matcher(doc)
#     # Combine all sentences found with keyword into minitext containing relevant sentences
#     par_len, minitext = combine_phrases(matched_phrases, doc)
#     # Returns list, integer and string text
#     return keywords, par_len, minitext
#
#
# def get_sentence_list(text, nlp):
#
#     # Create document object from string text
#     doc = nlp(text)
#     sentence_list = []
#
#     # Create array of sentences from the text
#     for sent in doc.sents:
#         sentence = sent.text.strip()
#         sentence_list.append(sentence) if sentence != '' else None
#
#     # Returns integer and list
#     return len(sentence_list), sentence_list
#
#
# def cosine_score(text_A, text_B, nlp):
#     # Create document objects from two texts
#     doc_A, doc_B = nlp(text_A), nlp(text_B)
#     # Calculate the cosine similarity score between documents
#     score = doc_A.similarity(doc_B)
#     # Return score in percent form to nearest hundreth
#     return round(score*100, 2)
#
#
# def sort_tuple_list(array, index=0):
#     # Sort a list of tuples based on first value of tuple, greatest to least
#     return sorted(array, key=lambda tup: -1*tup[index]) # Returns list of tuples
#
#
# def gen_answer_list(text, question, nlp, par_len=9, keywords=None):
#     # Replace text and paragrah length if argument keywords contains words or empty string
#     if keywords:
#         keywords, par_len, text = gen_minitext(text, question, nlp, keywords)
#     # Create empty list of answers
#     answer_list = []
#
#     # Get list of sentences from text and number of sentences
#     num_sent, sentence_list = get_sentence_list(text, nlp)
#
#     # Calculate the number of assumed paragraphs from the number of sentences and average length of a paragraph
#     num_par = ceil(num_sent/par_len)
#
#     # Iterate for the number of paragraphs that are assumed
#     for i in range(num_par):
#         # Index the sentences that are assumed in each paragraph, the same number of sentences each
#         sub_sentence_list = sentence_list[par_len * i: par_len * (i+1)]
#
#         # Condition to determine if indexed sentences exist
#         if len(sub_sentence_list) > 0:
#             # Join indexed sentences into sudo-paragraph
#             paragraph = ' '.join(sub_sentence_list)
#             # Task BERT with answering question from text in the paragraph, may return CLS, SEP or empty space if failed
#             answer = get_berts_ans(question, paragraph)
#
#             # CLS and SEP are special tokens in the BERT architecture, if they are returned in answer they are assumed
#             # to be failed answers (errors)
#             if ("[CLS]" not in answer) and ("[SEP]" not in answer) and (answer):
#
#                 # Determine cosine score of question and answer
#                 score = cosine_score(question, answer, nlp)
#
#                 # Append score and answer as tuple in list of answers
#                 answer_list.append( (score, answer) )
#
#     # IMPORTANT: Cosine score does not quantify validity of score! It quantifies how similar
#     # the answer is to the question!
#
#     # Sort list of answers by cosine score, greatest to least
#     answer_list = sort_tuple_list(answer_list, index=0)
#     # If keywords are not empty, return the list of answers with the keywords used
#     if keywords:
#         return keywords, answer_list
#     # Returns list of tuples
#     return answer_list
#
#
# def print_answers(answer_list, limit = 10):
#     # Print the top ten scored answers in the list
#     for i, answer in enumerate(answer_list):
#         if i == limit:
#             break
#         print(answer)
#
#
# def grade_response(response, answer_list, nlp, limit=10):
#     grade = 0
#     total = 0
#     for i, answer in enumerate(answer_list):
#         if i == limit:
#             break
#         answer_score = answer_list[i][0]
#         response_score = cosine_score(response, answer_list[i][1], nlp)
#         grade += response_score*answer_score
#         total += answer_score
#     if (grade/total)/100 >= 0.5:
#         return "pass"
#     else:
#         return "fail"
