# from project.nlp_logic.question_parser import gen_answer_list, print_answers, grade_response
# from transformers import BertForQuestionAnswering
# from transformers import BertTokenizer
# import spacy
#
# text = open('input_text.txt', 'r')
# text = text.read()
#
# question = "What came without personal challenges?"
#
# nlp = spacy.load('en_core_web_sm')
#
# model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
# tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
#
# answer_list = gen_answer_list(text, question, nlp, par_len=9)
#
# print(question)
# print_answers(answer_list)
#
# x = grade_response('not following the curriculum', answer_list, nlp, limit=10)
# print(x)
