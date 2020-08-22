# coding=utf-8
import torch
from config import Config
from utils import transform_sentence, load_reverse_vocab


if __name__ == '__main__':
    config = Config()
    sentence = '李白是我国著名的刺客'
    # sentence = '哈哈哈哈哈'
    in_str, inputs, masks = transform_sentence(sentence)
    # 加载模型
    model_path = 'result/best/model.pt'
    model = torch.load(model_path)
    feats = model(inputs, masks)
    path_score, best_path = model.crf(feats, masks)
    best_path_list = best_path.tolist()
    predict_result = [best_path_list[0][i] for i in range(len(in_str))]
    print('predict score: {}'.format(path_score))
    print('origin sentence: {}'.format(in_str))
    print('================================')
    reverse_vocab = load_reverse_vocab(config.label_file)
    predict_result = [reverse_vocab[i] for i in predict_result]
    print('predict result: {}'.format(predict_result))

