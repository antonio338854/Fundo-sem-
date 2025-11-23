import streamlit as st
from rembg import remove
from PIL import Image
import io

# --- Configuração da Página ---
st.set_page_config(page_title="Mágico dos Stickers", page_icon="✂️", layout="centered")

# CSS para deixar profissional no celular
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        border-radius: 12px;
        background-color: #7B1FA2; 
        color: white;
        font-weight: bold;
    }
    h1 {color: #4A148C;}
    </style>
    """, unsafe_allow_html=True)

st.title("✂️ Removedor de Fundo PRO")
st.write("Vovô diz: Transforme fotos em PNG transparente (Stickers) em 1 clique!")

# --- Menu Lateral (Sidebar) ---
with st.sidebar:
    st.header("Configurações")
    st.info("Este app usa Inteligência Artificial para detectar o objeto principal e apagar o resto.")
    st.write("Dica: Funciona melhor com fotos bem iluminadas!")

# --- Área de Upload ---
arquivo = st.file_uploader("Escolha sua foto (Pessoa, Animal ou Objeto)", type=['jpg', 'jpeg', 'png', 'webp'])

if arquivo is not None:
    # Ler a imagem original
    image = Image.open(arquivo)
    
    # Criar colunas para Antes e Depois
    st.markdown("---")
    st.subheader("🖼️ Visualização")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Original", use_column_width=True)
    
    # Botão de Ação
    if st.button("✨ Remover Fundo Agora"):
        with st.spinner('A IA está recortando... (pode levar uns segundinhos)'):
            try:
                # 1. Converter imagem para bytes
                buf = io.BytesIO()
                image.save(buf, format='PNG')
                byte_img = buf.getvalue()
                
                # 2. A MÁGICA (Chama a biblioteca rembg)
                # Na primeira vez demora um pouco pois baixa o modelo da IA
                resultado_bytes = remove(byte_img)
                
                # 3. Converter bytes de volta para Imagem para mostrar na tela
                img_sem_fundo = Image.open(io.BytesIO(resultado_bytes))
                
                # Mostrar o resultado
                with col2:
                    st.image(img_sem_fundo, caption="Sem Fundo", use_column_width=True)
                
                st.success("Recorte concluído com sucesso! 🎯")
                
                # Preparar Download
                buf_saida = io.BytesIO()
                img_sem_fundo.save(buf_saida, format='PNG')
                
                st.download_button(
                    label="📥 Baixar PNG Transparente",
                    data=buf_saida.getvalue(),
                    file_name="sticker_do_vovo.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.error(f"Ops! Aconteceu um erro: {e}")
                
else:
    st.info("☝️ Faça o upload de uma foto para começar a mágica.")

st.markdown("---")
st.caption("Desenvolvido com 💜 por Vovô Python Expert. Grátis e Ilimitado.")
