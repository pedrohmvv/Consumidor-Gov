import streamlit as st
from os import path
from src.config import Config
from src.models.ml.models import ANN

class Project:
    """Project section class"""

    def __init__(self, session_state): 
        self.config = Config()
        self.session_state = session_state
        self.model_metrics = ANN().get_metrics()

    def main(self):
        
        self.project()

    def project(self):
        """Project section generator function
           return: None
        """
        # Set the project section style
        #st.markdown(self.config.project_style, unsafe_allow_html=True)

        # Section title
        st.markdown(
            """
            <style>
                header {
                    text-align: center;
                }
                div[data-testid="column"] {
                    text-align: center;
                    justify-content: center;
                }
                [data-testid="column"] [data-testid=stImage] {
                    text-align: center;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-left: auto;
                    margin-right: auto;
                    width: 100%;
                }
                .container1 {
                    border: 2px solid #3498db;
                    border-radius: 8px;
                    padding: 10px;
                    margin-bottom: 20px;
                }
                .container2 {
                    border: 2px solid #a60d4e;
                    border-radius: 8px;
                    padding: 10px;
                    margin-bottom: 20px;
                }
                .git:hover {
                    border: 1px solid white;
                    border-radius: 30px;
                    box-shadow: 0 0 2px rgba(255,255,255, 0.6);
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<h1 style='text-align: center;'>Sobre</h1>", unsafe_allow_html=True)

        # jump line 
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        O projeto faz parte da disciplina de Aprendizagem Supervisionada do curso de Ciência de Dados para Negócios (UFPB). O objetivo é desenvolver uma solução real e inovadora de Machine Learning, testando diferentes modelos supervisionados.  
        
        Neste projeto, o desafio foi calcular a **probabilidade de uma reclamação feita no site [Consumidor.gov](https://www.consumidor.gov.br/) ser resolvida ou não** e **ranqueá-las por urgência**, oferecendo prioridade de atendimento baseada nessa probabilidade.
        """, unsafe_allow_html=True)
        st.markdown("---")

        # Leaders containers        
        blank1, c1, c3, c2, blank2 = st.columns([2,2,2,2,2], gap="small")
        leaders_columns_list = [c1, c2]
        with c3:
            st.title("Autor")
            st.markdown(f"""
                        <table>
                          <tr>
                            <td align="center">
                              <a href="https://github.com/pedrohmvv">
                                <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/139015105?v=4" width="100px;" alt=""/>
                                <br />
                                <sub><span style="color: black;"><b>Pedro Henrique</b></span></sub>
                              </a>
                              <br />
                              <a href="https://github.com/pedrohmvv" target="_blank">
                                <img src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" alt="LinkedIn" style="padding-top: 10px;">
                              </a>
                            </td>
                          </tr>
                        </table>"""
            , unsafe_allow_html=True)

        st.markdown("---")

        # Project section content
        st.header("Informações")
        st.markdown("""
                    **Coleta e Modelagem de Dados:**  
                    - Fonte: Site [Consumidor.gov](https://www.consumidor.gov.br/)  
                    - Coleta: API pública que retorna o conteúdo HTML das reclamações.  
                    - Extração: Utilização do **BeautifulSoup** para extrair as seguintes informações:  
                        - `company_name`
                        - `status`
                        - `date`
                        - `report`
                        - `company_response`
                        - `response_date`
                        - `rating_score`
                        - `consumer_written_evaluation`
                    - Tratamento: Limpeza e modelagem dos dados, com pré-processamento textual.

                    **Modelos Testados:**  
                    - Regressão Logística 
                    - Rede Neural com Tensorflow

                    **Resultado:**  

                    O modelo com melhor desempenho foi a **Rede Neural**, considerado o modelo base para o sistema.
                    """, unsafe_allow_html=True)
        
        st.subheader("Métricas do Modelo")
        # streamlit metrics
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Acurácia".center(20), value=f"{self.model_metrics['accuracy']:.2f}")
            st.metric(label="Precisão".center(20), value=f"{self.model_metrics['precision']:.2f}")
        with col2:
            st.metric(label="Recall".center(20), value=f"{self.model_metrics['recall']:.2f}")
            st.metric(label="F1-Score".center(20), value=f"{self.model_metrics['f1_score']:.2f}")
        st.markdown("---")
        
        # Project section links
        st.header("Links Importantes")
        st.markdown("<br>", unsafe_allow_html=True)
        c8, c9, c10, c11 = st.columns([2,2,2,2], gap="small")

        c9.markdown(
            f"""
                    <table>
                        <tr>
                        <td align="center">
                            <a href="https://github.com/pedrohmvv/Consumidor-Gov">
                            <img style="border-radius: 50%;" src="data:image/png;base64,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" width="100px;" alt=""/>
                            <br />
                            <sub><span style="color: black;"><b>Repositório do Projeto</b></span></sub>
                            </a>
                            <br />
                            <a href="https://github.com/pedrohmvv/Consumidor-Gov" target="_blank">
                            <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" style="padding-top: 10px;">
                            </a>
                        </td>
                        </tr>
                    </table>
            """, unsafe_allow_html=True)
        c10.markdown(
            f"""
                    <table>
                        <tr>
                        <td align="center">
                            <a href="">
                            <img style="border-radius: 50%;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAK0AAACUCAMAAADWBFkUAAAAYFBMVEUAAAD///8NDQ2Kiopubm67u7sWFhbIyMjOzs75+fl9fX2VlZXb29v19fVqamp3d3fCwsLp6ekuLi5kZGSqqqpVVVU4ODgcHBwiIiJCQkKenp7V1dW1tbVLS0teXl7v7+/csGgNAAAFI0lEQVR4nO2b6ZqqMAyGkXFDwW1GxAW9/7s8OhSFtvkS5ljKzNPv1yw2vNQ2Sds0iqPfozgKtK4UaN0p0LpToHWnQOtOgdadAq07BVp3CrTuFGjdKdC6U6B1p79EO12NGV27PrBkDH7+nPaYjTgV3WAPM8be9ue0xY2lPXWj3SeMvc3PaaNPlnZ76ER7YsylEIebZcs3dy7TtRv87hztdMLRnvMOsCtsa7LDzVkPFqcc7roDLTa24bypwN9uGdp0Kob9hD7mi20voN1zjkHuc7+QmRP/1pJY9sFMjbMU9ogGgmS2iiIv53b2QtoPYGMpMSDLExjHAD36S9M5aSH5EFmQ0YLnPLSVdW7+3+8rzMFK7HpkEeJCG1i8lTa6Qt9zE0UIYEA2EOT57Rh2ruRpaI69mxZnDInAABr7b6fN4dDlH7dGY+nttAfoxnCm9xCMY2+nxdlYws3qHKYbPdNymWm0hq37ph3B5R+XyfVOO4Gtj7hx77QjaIhp3D8t6lw8x3zQ3sCiiluMuqJNaCdPr1SKGdPWFW32RS580iPVVm1LzMmNGmd9uz53/z5VHFuSg8kdLb0nQK5+q38ncf99u4joNfDK3lTlipfIBy2dqKb2pip7K7307ZF2ntatBbXnkcZTH7RgxT63tVRzaxH5oaU7N7OM3LL69H1h7IcWrF4tEWJR/ecemD3RFiRtYkSIaeWfk7U32mhD4hpbC2X194e78EW7pztXb6fm2NIjLTia0R+sMpnII220JndJt+3wq7zdxCvtQZjbqDlWxWRvtCC/njUP/MYqjuV+acEidtwwrzxz5Sk80tK5TSP85lXXqg1ej7QFveR5LdDUK6mTCY+0aOQ+G6k3Wvmn3dO5TVl/RP1em/BIK8htVICuo7FXWnp3f1t1rsoVR3VXe6UFu93V6Vcdx+ro5peW3oq7PQB36m2eLfzSgiPxR4S4Vj+mzwMfz7RXunOj5xy7vEz4pd3RI3cdxdUPjdWEZ1oYIVQca+wx+KYtyJGbjZX7aqyCfdOCrYW0ytezxumJd9qYpFVqriq90+JDu3vXNo96/NPmuIxl1lyl+adlOrdVgDIA2hU6bb61ijIHQAv2bZpxbCi0qNqvXRMyBFqw+tWKaQdBS5e9aiWOg6CNqc7dlpqJIdCSWwsX3cQgaImSm2ysmxgELZHbGOdRPdKqoGV02EO59cDPKKTskVZtwNnLfaxbC8aneqStB6e1ZtGWOJrVFT3S1hPfXrNoOR03zyV7pH1mhtbzRjNCpGYpSG+0zVslthoPs47FAtAXbdF8jrUQeaFl5bYK4r5o2yl3Yqtl1iLEzPKRnmgXunVLeZJW+mcrrKBp31nbLJpC7ZIQ68UruiiWv5ghpi0tOdbFbNbKbawXAujt6ZusTl5Au7P2iBkkWvV0tko2UOU+ujFFm2JaYt1lDrXGppieK95V4Fq9TILL01J7R4kRqxrHJua9qJgtLCQKnjrRGu7gKbO07vktpGZ05u5DigYDR4suDpz1G5zHOkIYU7zAl1GUbMloF9odvK1lZFmKKdPWY+1QSCvhBgNDy3SJ7qdUVYpxhYsuD2jLmupLaWO0DfPdGVrEVMV02gA8sJcVX8JBDdLSM6yWvgb/HuZaaQ04nLAIhglIy1+P1btx9/jOtcCBL0PqgjEY0u5PS066q7qafys3c7nOMBv7S3f8h6ZA606B1p0CrTsFWncKtO4UaN0p0LpToHWnQOtOgdadAq07BVp3CrTu9Mto/wF/DEJJNjPsBQAAAABJRU5ErkJggg==" width="100px;" alt=""/>
                            <br />
                            <sub><span style="color: black;"><b>Artigo do Projeto</b></span></sub>
                            </a>
                            <br />
                            <a href="" target="_blank">
                            <img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium" style="padding-top: 10px;">
                            </a>
                        </td>
                        </tr>
                    </table>
            """, unsafe_allow_html=True)


        st.markdown("---")
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("Voltar"):
                self.session_state.pagina = 'login'
                st.rerun()
