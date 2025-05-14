import streamlit as st
from numpy import nan
from src.backend.database import Database
from src.backend.consumer import Consumer

class ConsumerPage:
    def __init__(self, session_state):
        self.db = Database()
        self.session_state = session_state
        self.backend = None
        self.data = None

    def main(self):
        st.title("Área do Consumidor")
        st.write(f"Bem-vindo, {self.session_state.user.name}!")

        if "backend_loaded" not in self.session_state:
            self.session_state.backend_loaded = False

        if not self.session_state.backend_loaded:
            with st.spinner("Carregando recursos de IA..."):
                self.backend = Consumer(self.session_state)
                self.data = self.backend.get_dashboard_data()
                self.session_state.backend = self.backend
                self.session_state.backend_loaded = True
            st.success("Modelos carregados com sucesso!")
            st.rerun()
        else:
            self.backend = self.session_state.backend
            self.data = self.backend.get_dashboard_data()

            col1, col2 = st.columns([1.3, 1.7])

            with col1:
                st.subheader("Nova Reclamação")
                self.complaint_form()

            with col2:
                st.subheader("Suas Reclamações")
                self.complaints_sidebar()
            st.write('##')
            st.write('---')
            st.subheader("Dashboard")
            self.dashboard()

    def complaint_form(self):
        st.write("Preencha o formulário abaixo para criar uma nova reclamação.")
        with st.form("complaint_form"):
            text = st.text_input("Escreva sua queixa.", key="text")
            company = st.selectbox("Selecione a empresa responsável.", self.backend.get_companies())
            state = st.selectbox("Selecione seu Estado.", self.backend.get_states())
            submit_button = st.form_submit_button("Enviar Reclamação")

            if submit_button:
                report = self.backend.create_report(text=text, company=company, state=state)
                self.backend.insert_report(report)
                st.success("Reclamação enviada com sucesso!")
                st.write('##')
                with st.spinner("Calculando a probabilidade de resolução..."):
                    prediction = self.backend.predict_report(report)
                    probability = prediction['prediction'][0][0]
                    probability_resolvida = probability
                    probability_nao_resolvida = 1 - probability

                    color = 'green' if probability_resolvida >= 0.5 else 'red'

                    st.write(f"<span style='color: {color};'>Probabilidade da sua reclamação ser resolvida: {probability_resolvida*100:.2f}%</span>", unsafe_allow_html=True)
                    st.write(f"<span style='color: gray;'>Probabilidade da sua reclamação NÃO ser resolvida: {probability_nao_resolvida*100:.2f}%</span>", unsafe_allow_html=True)
                st.rerun()

    def complaints_sidebar(self):
        # Aplica o estilo CSS para rolagem
        st.write('Aqui suas reclamações aparecem de forma ordenada pela probabilidade de não-resolução.')
        df = self.data
        if df.empty:
            st.info("Você ainda não enviou nenhuma reclamação.")
            return

        with st.container():
            for index, row in df.iterrows():
                report_id = row['id_report']
                prediction = row['prediction']
                report_truncated = row['report'][:50]
                non_resolution_prob = row['non_resolution_prob']
                company_name = self.backend.get_company_name(row['id_company'])

                with st.expander(f"{company_name} - {row['date']} - {report_truncated}... - (Prob: {prediction:.2%})"):
                    st.write(f"Probabilidade de resolução: {prediction:.2%}")
                    st.write(f"Probabilidade de não resolução: {non_resolution_prob:.2%}")
                    st.write(f"Estado: {row['state']}")
                    st.write(f"Resposta da empresa: {row['company_response']}")
                    st.write(f"Data da resposta: {row['response_date']}")
                    st.write(f"Avaliação: {row['rating_score']}")
                    st.write(f"Comentário: {row['consumer_written_evaluation']}")
                    st.write(f"Resolvido: {row['status']}")

                    if row['company_response'] != '<não respondido pela empresa>':
                        with st.form(f"report_actualization_{report_id}"):
                            rating = st.selectbox("Avaliação", [1, 2, 3, 4, 5], key=f"rating_{report_id}")
                            evaluation = st.text_area("Deixe Comentário", key=f"eval_{report_id}")
                            resolved = st.selectbox("Não resolvido", ['Resolvido', 'Não resolvido'], key=f"resolved_{report_id}")
                            submit_button = st.form_submit_button("Atualizar Reclamação")

                            if submit_button:
                                self.backend.update_report_evaluation(report_id, rating, evaluation, resolved)
                                st.success("Reclamação atualizada com sucesso!")
                                st.rerun()
                    else:
                        st.write("A empresa ainda não respondeu a esta reclamação.")

    def dashboard(self):
        df = self.data
                
        if df.empty:
            st.info("Você ainda não possui nenhuma reclamação.")
            return

        # 1st line: Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Reclamações enviadas", len(df))
        with col2:
            resolved = df[df["status"] == "Resolvido"].shape[0]
            unresolved = df[df["status"] == "Não Resolvido"].shape[0]
            sub_col1, sub_col2 = st.columns(2)
            sub_col1.metric(label="Qtd. Resolvidas", value=resolved)
            sub_col2.metric(label="Qtd. Não Resolvidas", value=unresolved)
        with col3:
            avg_rating_serie = df[df["rating_score"] != '<não há comentários do consumidor>']["rating_score"]
            extracted_rates = avg_rating_serie.str.extract('(\d+)').astype(float)
            if extracted_rates.empty:
                st.metric("Média de Avaliação", "<small>Nenhuma avaliação registrada ainda.</small>", unsafe_allow_html=True)
            else:
                st.metric("Média de Avaliação", f"{avg_rating_serie.mean():.2f}" if not df.empty else "N/A")

        st.markdown("---")
        # 2nd line: Companies with most complaints
        col4, col5 = st.columns(2)
        with col4:
            st.write("### Empresas com mais reclamações")
            st.bar_chart(df["company_name"].value_counts())

        with col5:
            st.write("### Reclamações Resolvidas vs Não Resolvidas")
            st.bar_chart(df["status"].value_counts())

        st.markdown("---")
        # 3rd line: Reclamações with highest and lowest resolution probability
        col6, col7 = st.columns(2)
        with col6:
            st.write("### Reclamação com <span style='color: green;'>**MAIOR**</span> chance de resolução", unsafe_allow_html=True)
            st.write(df.loc[df["prediction"].idxmax()])

        with col7:
            st.write("### Reclamação com <span style='color: red;'>**MENOR**</span> chance de resolução", unsafe_allow_html=True)
            st.write(df.loc[df["prediction"].idxmin()])

        st.markdown("---")
        # 4th line: Companies with best and worst ratings
        df_with_rating = df[df['rating_score'] != '<não há comentários do consumidor>']
        if not df_with_rating.empty:
            df_with_rating["rating_score"] = df_with_rating["rating_score"].astype(float)
            df_rating_mean = df_with_rating.groupby("company_name")["rating_score"].mean().sort_values()

            st.write("### Empresas por Média de Avaliação")
            col8, col9 = st.columns(2)
            with col8:
                st.write("#### 🔻 Piores Avaliações")
                st.dataframe(df_rating_mean.head())

            with col9:
                st.write("#### 🔺 Melhores Avaliações")
                st.dataframe(df_rating_mean.tail())
        else:
            st.info("Nenhuma avaliação registrada ainda.")