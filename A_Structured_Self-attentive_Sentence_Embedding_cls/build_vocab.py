import pandas as pd
import gluonnlp as nlp
import itertools
import pickle
from pathlib import Path
from mecab import MeCab

# loading dataset
cwd = Path.cwd()
tr_path = cwd / 'data' / 'train.txt'
tr = pd.read_csv(tr_path, sep='\t').loc[:, ['document', 'label']]

# extracting morph in sentences
tokenizer = MeCab().morphs
list_of_tokens = tr['document'].apply(tokenizer).tolist()

# making the vocab
counter = nlp.data.count_tokens(itertools.chain.from_iterable(list_of_tokens))
vocab = nlp.Vocab(counter=counter, min_freq=10, bos_token=None, eos_token=None)

# connecting SISG embedding with vocab
ptr_embedding = nlp.embedding.create('fasttext', source='wiki.ko')
vocab.set_embedding(ptr_embedding)

# saving vocab
with open('./data/vocab.pkl', mode='wb') as io:
    pickle.dump(vocab, io)