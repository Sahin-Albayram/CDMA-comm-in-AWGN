import numpy as np
import matplotlib.pyplot as plt
import random 

def encoder_CDMA(input_bit_sequence, user_code):
    pass

def apply_channel(enc_chips_sequences,noise_stdev):
    pass

def decoder_CDMA(received_bit_sequence, user_code):
    pass

def eval_BER(input_bit_sequence,received_bit_sequence):
    pass




def main():
    MSG_LEN = 10**6
    codes = {"scenario-1":{1:[1,1,1,1],2:[1,-1,1,-1],3:[1,-1,-1,1]},"scenario-2":{1:[1,1,1,1,1,1,1,1],2:[1,1,-1,-1,1,1,-1,-1],3:[1,-1,-1,1,1,-1,-1,1]}}
    st_devs = [0.001,0.005, 0.01, 0.05, 0.1, 0.5, 1]
    msg = []
     # Generating random signal
    for i in range(3):
        s = random.getrandbits(MSG_LEN)
        inp_bit_sq = format(s, '0b')
        msg.append(inp_bit_sq)


    encoded_msgs = [] 
    
    decoded_msgs = []
    for scenario in range(1,3): # loop for each scenario
        for node in range(3): # loop for each node
            encoded_msgs.append(encoder_CDMA(msg[node],codes[f"scenario-{scenario}"][node])) # this holds encoded messages of nodes, its shape (1,3)
        
        received_msgs = apply_channel(encoded_msgs,st_devs) # this holds messages after superposing and adding noise, since there is 7 different noise value its shape (7,3)
        for noise in range(7):
            temp =[]
            for node in range(3):
                temp.append(decoder_CDMA(received_msgs[noise][node],codes[f"scenario-{scenario}"][node]))




if __name__ == "__main__":
    main()