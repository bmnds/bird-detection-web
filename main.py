import streamlit as st
import pandas as pd

def call_backend(image):
    import requests

    url = 'https://bird-detection-api-qc7z4pqwva-uc.a.run.app/predict'
    files = {'image': image}
    
    try:
        response = requests.post(url, files = files)
        j = response.json()
        bird = j["bird"]
        proba = j["probability"]
        predictions = j["predictions"]
        return bird, proba, predictions
    except:
        st.error("Falha na requisição ao serviço")
        return "", 0, {}


st.title("Descubra a espécie do pássaro")      
image = st.file_uploader("Escolha a imagem de um pássaro")

if not image:
    st.error("Primeiro escolha uma imagem de um pássaro")
else:
    bird, proba, predictions = call_backend(image)
    st.image(image, f"{bird} {proba*100:.2f}%", width=244)
    
    st.text("")
    st.text("Confira as demais predições:")
    df = pd.DataFrame.from_dict(predictions, orient="index", columns=["Probabilidade"]) \
        .sort_values("Probabilidade", ascending=False)
    df["Probabilidade"] = df["Probabilidade"]*100
    st.table(df.style.format({'Probabilidade': "{:.2f}%"}))
