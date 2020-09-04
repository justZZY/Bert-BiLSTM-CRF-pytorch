# coding=utf-8


# 用于测试自己的训练集
class Config2(object):
    def __init__(self):
        self.label_file = './equip_data/tag.txt'
        self.train_file = './equip_data/train_data.txt'
        self.dev_file = './equip_data/dev_data.txt'
        self.vocab = './data/bert/vocab.txt'
        self.max_length = 300
        self.use_cuda = False
        self.gpu = 0
        self.batch_size = 50
        self.bert_path = './data/bert'
        self.rnn_hidden = 500
        self.bert_embedding = 768
        self.dropout1 = 0.5
        self.dropout_ratio = 0.5
        self.rnn_layer = 2
        self.lr = 0.0001
        self.lr_decay = 0.00001
        self.weight_decay = 0.00005
        self.checkpoint = 'result/'
        self.optim = 'Adam'
        self.load_model = False
        self.load_path = None
        self.base_epoch = 1000

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):

        return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])


if __name__ == '__main__':

    con = Config()
    con.update(gpu=8)
    print(con.gpu)
    print(con)
