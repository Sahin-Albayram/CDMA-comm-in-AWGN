

import random
import numpy as np






def encoder_CDMA(input_bit_sequence, user_code):

    digit_list = [1 if int(digit)== 1 else -1 for digit in input_bit_sequence]
    encode = np.array(digit_list)
    code = np.array(user_code)
    signal = np.empty([len(code)*len(encode)])

    for e_idx,e in enumerate(encode):
        for c_idx,c in enumerate(code):
            signal[e_idx*len(code)+c_idx] = e*c

    return signal
def decoder_CDMA(received_bit_sequence, user_code):
    decode = np.array(received_bit_sequence).reshape(-1,len(np.array(user_code))) * user_code
    decode = np.sum(decode, axis=1)
    data = np.where(decode>0,1,np.where(decode<0,0,0))
    return data

print(decoder_CDMA([0,-2,-2,0,2,0,2,0],[1,1]))
# s = random.getrandbits(10)
# inp_bit_sq = format(s, '0b')
# enc_chips_sequences = [[0, 1], [0, 5]]

# digit_list = [1 if int(digit)== 1 else -1 for digit in inp_bit_sq]
# print(digit_list)

# codes = {"scenario-1":{1:[1,1,1,1],2:[1,-1,1,-1],3:[1,-1,-1,1]},"scenario-2":{1:[1,1,1,1,1,1,1,1],2:[1,1,-1,-1,1,1,-1,-1],3:[1,-1,-1,1,1,-1,-1,1]}}
# print(codes["scenario-1"][1])
# print(encoder_CDMA("0011",[1,1]))
