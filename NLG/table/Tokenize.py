from transformers import BartTokenizer
import warnings
import table.IO
import os
import torch
class SrcVocab(object):
    def __init__(self):
        self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        self.added_token = ['{hlist', '{hvalue', '{hcount', '{hgreater', '{hequal', '{hless', '{his', '{hmax', '{hmin', '?x0','?x1','?y0','?y1', 'starts_with']
        self.tokenizer.add_tokens(self.added_token)
        self.pad_id = self.tokenizer.pad_token_id

    def encodeSeqs(self, seqs):
        # for sequence in seqs:
        #     if '[UNK]' in self.tokenizer(text = sequence, is_split_into_words = True):
        #         warnings.warn('[UNK] in target sequence tokenization: You need to add the corresponding items to the vocabulary')
        # token_sequences = [self.tokenizer.tokenize(text = sequence, is_split_into_words = True) for sequence in seqs]
        token_sequences = self.tokenizer(text=seqs, is_split_into_words = True, padding = True, return_token_type_ids = False)
        return token_sequences

    def seq2ID(self, seq):
        return [self.tokenizer.convert_tokens_to_ids(token) for token in seq]

    def decode_token2token(self, idseq):
        # decoded = []
        # for id in idseq:
        #     print(self.tokenizer.convert_ids_to_tokens(id))
        #     decoded.append(self.tokenizer.convert_ids_to_tokens(id))
        # return decoded
        return [self.tokenizer.convert_ids_to_tokens(ids) for ids in idseq]

    def word_piece_index(self, src, seq):
        word_piece = [1 if token.startswith('##') else 0 for token in seq]
        word_piece[0] = 1
        word_piece[-1] = 1
        lenth = sum([1 - index for index in word_piece])
        if lenth != len(src):
            word_piece = []
            # flag = False
            # for token in seq:
            #     if token not in src:
            #         if token == '[CLS]' or token == '[SEP]':
            #             word_piece.append(1)
            #         else:
            #             if not flag:
            #                 word_piece.append(0)
            #                 flag = True
            #             else:
            #                 word_piece.append(1)
            #         #print('token is {}, new word_piece is {}'.format(token,word_piece))
            #     else:
            #         flag = False
            #         word_piece.append(0)
            src_index = 0
            #print('src is {} seq is {}'.format(src, seq))
            for token in seq:
                if src_index >= len(src):
                    word_piece.append(1)
                else:
                    if token == ['CLS'] or token == '[SEP]':
                        word_piece.append(1)
                    else:
                        if token == src[src_index] or src[src_index].startswith(token):
                            word_piece.append(0)
                            src_index += 1
                        else:
                            word_piece.append(1)
            length = sum([1 - index for index in word_piece])
            if length != len(src):
                #print('src is {} \n seq is {} \n word_piece {} \n'.format(src, seq, word_piece))
                return None
        return word_piece
if __name__ == '__main__':
    vocab = SrcVocab()
    # for id, token in vocab.tokenizer.ids_to_tokens.items():
    #     print('id {} token {}'.format(id, token))
    js_list = table.IO.read_txt('data/input/test.txt')
    srcseqs = js_list[0]['src_']
    tgt = ' '.join(js_list[0]['tgt_'])
    print(vocab.pad_id)
    print(srcseqs)
    print(tgt)
    # srcseqs.append('embeddings')
    batch_seqs = vocab.tokenizer(srcseqs)
    batch_tgt = vocab.tokenizer(tgt)
    fuyuan = vocab.tokenizer.convert_ids_to_tokens(batch_seqs['input_ids'])
    fuyuan_tgt = vocab.tokenizer.convert_ids_to_tokens(batch_tgt['input_ids'])
    print(batch_seqs)
    print(fuyuan)
    print(batch_tgt)
    print(fuyuan_tgt)
    # decoded = vocab.decode_token2token(batch_seqs['input_ids'])
    # print(decoded)
    # word_piece_index = vocab.word_piece_index(decoded)
    # print(word_piece_index)
    # print(vocab.tokenizer.vocab_size)
    # id_seq = vocab.seq2ID(srcseqs[0])
    # print('original is {} and converted is {}'.format(srcseqs[0], id_seq))
    # d = vocab.decode_token2token(id_seq)
    # print(d)