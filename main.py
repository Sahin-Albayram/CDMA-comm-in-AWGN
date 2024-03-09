import numpy as np
import random 
import pandas as pd

MSG_LEN = 10**6

def encoder_CDMA(input_bit_sequence, user_code):

    digit_list = [1 if int(digit)== 1 else -1 for digit in input_bit_sequence] # Changes 0's as -1 
    encode = np.array(digit_list)
    code = np.array(user_code)
    signal = np.empty([len(code)*len(encode)])

    for e_idx,e in enumerate(encode):
        for c_idx,c in enumerate(code):
            signal[e_idx*len(code)+c_idx] = e*c # Spreading operation

    return signal

def apply_channel(enc_chips_sequences,noise_stdevs):
    signals = []
    superposed_signal = np.sum(enc_chips_sequences, axis=0) # summing each signal 
    for stdev in noise_stdevs:
        noise = np.random.normal(0,stdev,len(superposed_signal)) #creating noise 
        signals.append(np.sum([superposed_signal,noise],axis = 0)) # Adding noise to signal and append the signals list
    
    return signals

def decoder_CDMA(received_bit_sequence, user_code):
    decode = np.array(received_bit_sequence).reshape(-1,len(np.array(user_code))) * user_code # Dividing segment and multiply with code 
    decode = np.sum(decode, axis=1) # summing numbers of each segment
    data = np.where(decode>0,1,np.where(decode<=0,0,0)) # 1 if bigger than zero, 0 if less or equal to zero 
    return data


def eval_BER(input_bit_sequence,received_bit_sequence):
    res = []
    
    for i in range(7):
        res_row = []
        for j in range(3):
            count = 0
            inp = input_bit_sequence[j]   
            out = received_bit_sequence[i][j]
            for j in range(len(inp)):
                if int(inp[j]) != out[j] :  #Comparing each bit
                    count += 1 #error counter incerement
            res_row.append(count/MSG_LEN) 
        res.append(res_row)
    
    res_arr = np.array(res).T
    df = pd.DataFrame(res_arr,columns=['0.001','0.005', '0.01', '0.05', '0.1', '0.5', '1']) #Dataframe of results
    return df

def random_bit_generator(length): #Random bit generator
    X = ""
    for i in range(length):
        num = random.randint(0, 1)
        X += str(num)
    return X


def main():
    
    codes = {"scenario-1":{1:[1,1,1,1],2:[1,-1,1,-1],3:[1,-1,-1,1]},"scenario-2":{1:[1,1,1,1,1,1,1,1],2:[1,1,-1,-1,1,1,-1,-1],3:[1,-1,-1,1,1,-1,-1,1]}}
    st_devs = [0.001,0.005, 0.01, 0.05, 0.1, 0.5, 1]
    msg = []
     # Generating random signal
    for i in range(3):
        msg.append(random_bit_generator(MSG_LEN)) #Creating messages of each node 


    
    for scenario in range(1,3): # loop for each scenario
        encoded_msgs = [] 
        decoded_msgs = []
        for node in range(1,4): # loop for each node
            encoded_msgs.append(encoder_CDMA(msg[node-1],codes[f"scenario-{scenario}"][node]).tolist()) # this holds encoded messages of nodes, its shape (1,3)
        
        received_msgs = apply_channel(encoded_msgs,st_devs) # this holds messages after superposing and adding noise, since there is 7 different noise value its shape (7,1)
        for noise in range(7):
            temp =[]
            for node in range(3):
                temp.append(decoder_CDMA(received_msgs[noise],codes[f"scenario-{scenario}"][node+1])) # this holds received messages from different nodes for specific noise std value
                                                                                                        # so its shape is (1,3)
            decoded_msgs.append(temp) # packed format of received messages, shape (7,3)
        results = eval_BER(msg,decoded_msgs) # #Evaluation
        results.to_csv(f"scenario_{scenario}.csv")




if __name__ == "__main__":
    main()