import json
from pathlib import Path
import collections 

class BioAsqToSquad2(object):

    def __init__(self, input_file, output_file):

        self.input_file = input_file
        self.output_file = output_file
        self.counters = collections.Counter(beginEndDiff=0,answerTitle=0,instanceCount=0)

        with open(self.input_file, "r") as reader:

            # deserialize into python object aka decoding
            self.input_data = json.load(reader)["questions"]
            
            #print(input_data[b)
    def transform_json(self):

        json_data = {} 

        # bioasq 8 contains all question in previous version + new questions + some questions that were removed
        json_data['version'] = 'BioASQ8b'

        # initialize list of question context pair
        json_data['data'] = [] 

        # iterate over the input data
        #total_instances = 0

        for bioasq_question_snippets in self.input_data:
            
            squad_data_instance = {}
            #print(bioasq_question_snippets['type'])
            squad_data_instance['title'] = bioasq_question_snippets['type']  # todo later combine all list , factpod , yesno paragraphs
            squad_data_instance['paragraphs'] = [] 
            
            #squad_qasi_list = []

            # todo fix this by using print format
            bioasq_question_id = bioasq_question_snippets['id'] # + "001"
            #print(bioasq_question_id)
            
            
            #squad_qasi_dict['question'] = bioasq_question_snippets['body']
            bioasq_question = bioasq_question_snippets['body']
            count_entry_per_bioasq_question = 0 

            # we generate one entry per snippet 
            for bioasq_snippet in  bioasq_question_snippets['snippets']:

                count_entry_per_bioasq_question += 1 
                squad_paragraph_dict = {}
                squad_paragraph_dict['qas'] = [] 
                squad_qasi_dict = {}
                
                # one qas will map to one context ( unlike squad where mul qas per context )
                squad_qasi_dict['answers'] = []
                # squad_answers_list = []
                squad_answer_dict = {}

                # todo use python parse lib to extract abstract from document
                document = bioasq_snippet['document']
               

                bioasq_text = bioasq_snippet['text']
                bioasq_answer_start = bioasq_snippet['offsetInBeginSection']
                bioasq_begin_section = bioasq_snippet['beginSection']
                bioasq_end_section = bioasq_snippet['endSection']
                squad_answer_dict['text'] = bioasq_text
                squad_answer_dict['answer_start'] = bioasq_answer_start


                # use this to check that abstract offsets align with the text provided
                #bioasq_answer_end = bioasq_snippet['offsetInEndSection']
                
                if bioasq_begin_section != bioasq_end_section:
                    self.counters.update({'beginEndDiff':1})
                    print(' begin and end section not the same: ', self.counters, bioasq_begin_section, bioasq_end_section )
                elif bioasq_begin_section != "abstract":
                    self.counters.update({'answerTitle':1})
                    print(' begin section is not abstract: ', self.counters )
                    print('It is:', bioasq_begin_section)

                    if bioasq_begin_section != "title":
                        print("Yikes ths is not a title either !!!!!!! ")

                    # move to next snippet as we only add entries that are abstracts
                    print("skipping ", str(bioasq_question_id) + "_" + str(count_entry_per_bioasq_question))

                    continue
                else:
                    squad_qasi_dict['question'] = bioasq_question
                    squad_qasi_dict['id'] = str(bioasq_question_id) + "_" + str(count_entry_per_bioasq_question)

                    # add answer dict to list 
                    squad_qasi_dict['answers'].append(squad_answer_dict)
                    squad_qasi_dict['is_impossible'] = False
                    
                squad_paragraph_dict['qas'].append(squad_qasi_dict)
                squad_paragraph_dict['context'] = document
                squad_data_instance['paragraphs'].append(squad_paragraph_dict)
                self.counters.update({'instanceCount':1})

            json_data['data'].append(squad_data_instance) 
        #print(json.dumps(json_data, indent=4))

        # for one question we will produce several context and answers like in squad 
        with open(self.output_file, 'w', encoding='utf-8') as writer:
            json.dump(json_data, writer ,sort_keys=False, ensure_ascii= False)

            
           



if __name__ == '__main__':
    #print("hello")
    base_path = Path(__file__).parent
    in_file_path = (base_path / "./bioasq/BioASQ-test8b/BioASQ-task8bPhaseB-testset1.json").resolve()
    out_file_path = (base_path/ "./bioasq/BioASQ-test8b/BioASQ-task8bPhaseB-testset1_squad_format.json").resolve()
    cbs = BioAsqToSquad2(in_file_path,out_file_path)
    cbs.transform_json()
    #print(cbs.input_data[0]['body'])



