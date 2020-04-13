
from transformers import pipeline, AutoModel, AutoTokenizer, BertTokenizer, BertForQuestionAnswering
import transformers
import torch
import pandas as pd
import os
DATA_DIRECTORY = "/home/xcs224u_student/notebooks/cs224u/github_repo/data"
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer


# Question answering pipeline, specifying the checkpoint identifier
MODEL_NAME_SQUAD2 = "deepset/bert-base-cased-squad2"
qa_squad2_pipeline = pipeline('question-answering', model=MODEL_NAME_SQUAD2, tokenizer=MODEL_NAME_SQUAD2)


from transformers.data.processors import squad
processor = squad.SquadV2Processor()
dev_squad_2 = processor.get_dev_examples(DATA_DIRECTORY, "squad/dev-v2.0.json")
#squad datasets: https://rajpurkar.github.io/SQuAD-explorer/

import json
def save_evaluation_squad_json(squadExamples, predictions, filename=DATA_DIRECTORY+'/evaluation.json', confidence_tresh=0.5):
    obj = {};
    index =0
    for example in squadExamples:
        if predictions[index]["score"] > confidence_tresh:
            obj[example.qas_id] = predictions[index]["answer"]
        else:
            obj[example.qas_id] = ""
        index += 1;
    with open(filename, 'w') as fout:
        json.dump(obj, fout)


FILENAME = "/squad/evaluation_dev_sq2_squad2_2.json"
if os.path.isfile(DATA_DIRECTORY+FILENAME) == False:
    print("evaluation file doesnt exist, creating it")
    predictions = qa_squad2_pipeline(dev_squad_2);
    save_evaluation_squad_json(dev_squad_2, predictions, DATA_DIRECTORY+FILENAME);
