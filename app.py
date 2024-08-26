import streamlit as st
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


##Load the LSTM Model -
model = load_model('next_word_lstm.h5')

#Load the Tokenizer
with open('tokenizer.pickle','rb') as handle:
    tokenizer = pickle.load(handle)

def predict_next_word(model,tokenizer,text,max_len_seq):
    token_list = tokenizer.texts_to_sequences([text])[0]
    if len(token_list) >= max_len_seq:
        token_list = token_list[-(max_len_seq-1):] #Ensure the seq length matches the max seq lenght
    token_list = pad_sequences([token_list], maxlen=max_len_seq-1,padding='pre')
    predicted = model.predict(token_list,verbose=0)
    predicted_word_index = np.argmax(predicted, axis=1)
    for word,index in tokenizer.word_index.items():
        if index == predicted_word_index:
            return word
    return None

#STreamLit App

st.title("Next Word Prediction...")
input_text = st.text_input("Enter the sequence of words",'Hello how are you...')
if st.button("Predict Next Word"):
    max_len_seq = model.input_shape[1] + 1
    next_word = predict_next_word(model, tokenizer,input_text,max_len_seq)
    st.write(f'Next Word: {next_word}')