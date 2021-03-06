import os, json
from .general_utils import get_logger
from .data_utils import get_trimmed_glove_vectors, load_vocab, \
        get_processing_word, get_indicators
path = '/nlp/data/romap/naacl-pattern/lstm/joint/model_5/'
#path = '/Users/romapatel/Desktop/naacl-pattern/lstm/single/model_5/part/'

class Config():
    def __init__(self, load=True):
        """Initialize hyperparameters and load vocabs

        Args:
            load_embeddings: (bool) if True, load embeddings into
                np array, else None

        """
        # directory for training outputs
        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)

        # create instance of logger
        self.logger = get_logger(self.path_log)

        # load if requested (default)
        if load:
            self.load()


    def load(self):
        """Loads vocabulary, processing functions and embeddings

        Supposes that build_data.py has been run successfully and that
        the corresponding files have been created (vocab and trimmed GloVe
        vectors)

        """
        #indicator dictionary in json file:
        f = open(path + 'data/indicator_map.json', 'r')
        for line in f: d = json.loads(line)
        
        # 1. vocabulary
        self.vocab_inds = d
        self.vocab_words = load_vocab(self.filename_words)
        self.vocab_tags  = load_vocab(self.filename_tags)
        self.vocab_chars = load_vocab(self.filename_chars)


        
        self.nwords     = len(self.vocab_words)
        self.nchars     = len(self.vocab_chars)
        self.ntags      = len(self.vocab_tags)
        self.ninds      = 8

        # 2. get processing functions that map str -> id
        self.processing_word = get_processing_word(self.vocab_words,
                self.vocab_chars, lowercase=True, chars=self.use_chars)
        self.processing_tag  = get_processing_word(self.vocab_tags,
                lowercase=False, allow_unk=False)

        # 3. get pre-trained embeddings
        self.embeddings = (get_trimmed_glove_vectors(self.filename_trimmed)
                if self.use_pretrained else None)

        self.indicator_embeddings = (get_indicators(self.filename_ind)
                if self.use_pretrained else None)

        print self.embeddings.shape
        print self.indicator_embeddings.shape

    # general config
    dir_output = path + "results/test/"
    dir_model  = dir_output + "model.weights/"
    path_log   = dir_output + "log.txt"

    # embeddings
    dim_word = 200
    dim_char = 100
    dim_ind = 3

    # glove files
    filename_glove = path + "data/glove.6B/glove.6B.{}d.txt".format(dim_word)
    #change to PubMed
    filename_glove = "/nlp/data/romap/naacl-pattern/w2v/PubMed-w2v.txt"

    # trimmed embeddings (created from glove_filename with build_data.py)
    filename_trimmed = path + "data/glove.6B.{}d.trimmed.npz".format(dim_word)
    use_pretrained = True


    filename_ind = path + "/data/indicators.json"

    # dataset
    filename_dev = path + "data/dev.txt"
    filename_test = path + "data/gold.txt"
    filename_train = path + "data/train.txt"

    #filename_dev = filename_test = filename_train = "data/test.txt" # test

    max_iter = None # if not None, max number of examples in Dataset

    # vocab (created from dataset with build_data.py)
    filename_words = path + "data/words.txt"
    filename_tags = path + "data/tags.txt"
    filename_chars = path + "data/chars.txt"

    # training
    train_embeddings = False
    nepochs          = 15
    dropout          = 0.5
    batch_size       = 20
    lr_method        = "adam"
    lr               = 0.001
    lr_decay         = 0.9
    clip             = -1 # if negative, no clipping
    nepoch_no_imprv  = 3

    # model hyperparameters
    hidden_size_char = 100 # lstm on chars
    hidden_size_lstm = 200 # lstm on word embeddings


    # NOTE: if both chars and crf, only 1.6x slower on GPU
    use_crf = True # if crf, training is 1.7x slower on CPU
    use_chars = True # if char embedding, training is 3.5x slower on CPU
    use_indicators = True
