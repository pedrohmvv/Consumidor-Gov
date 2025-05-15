import streamlit as st
import pandas as pd
import altair as alt

from numpy import nan

from src.backend.database import Database
from src.config import Config
from src.backend.servant import Servant
from src.models.ml.models import ANN

global prod_model
prod_model = ANN()

class ServantPage:
    def __init__(self, session_state):
        self.db = Database()
        self.config = Config()
        self.backend = Servant(session_state)
        self.session_state = session_state
        self.data = self.backend.get_dashboard_data()

    def main(self):
        st.title("Painel do Servidor")
        st.write(f"Bem-vindo(a), {self.session_state.user.name}!")

        with st.spinner("Carregando dados..."):
            self.dashboard()

    def dashboard(self):
        df = self.data

        min_date = df["date_format"].min().date()
        max_date = df["date_format"].max().date()
        months_gap = (max_date - min_date).days // 30
        st.write('---')
        st.subheader(f"Visão Geral das Reclamações - Período: {min_date} a {max_date} ({months_gap} meses)")

        model_metrics = prod_model.get_metrics()
        model_acc = model_metrics['accuracy']
        model_f1 = model_metrics['f1_score']
        model_precision = model_metrics['precision']
        model_recall = model_metrics['recall']

        company_counts = df["company_name"].value_counts()
        valid_companies = company_counts[company_counts >= 20].index
        df_filtered = df[df["company_name"].isin(valid_companies)]

        total = len(df)
        resolved = df[df["status"] == "Resolvido"]
        unresolved = df[df["status"] == "Não Resolvido"]

        mean_resolution_prob_df = (
            df.groupby(["id_company", "company_name"]).agg({
                "prediction": "mean",
                "id_report": "count"
            }).reset_index()
        )
        mean_resolution_prob_df = mean_resolution_prob_df[mean_resolution_prob_df["id_report"] >= 20]

        prop_resolved = len(resolved) / total
        prop_unresolved = len(unresolved) / total

        resolution_rate = prop_resolved * 100
        unresolved_rate = prop_unresolved * 100
        mean_resolution_prob = mean_resolution_prob_df["prediction"].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Reclamações", total)
        col2.metric("✅ Resolvidas", len(resolved))
        col3.metric("❌ Não Resolvidas", len(unresolved))

        col4, col5, col6 = st.columns(3)
        col4.metric("Taxa de Resolução", f"{resolution_rate:.2f}%")
        col5.metric("Taxa de Não-Resolução", f"{unresolved_rate:.2f}%")
        col6.metric("Probabilidade Média de Resolução das Reclamações", f"{mean_resolution_prob*100:.2f}%")

        st.write("---")
        st.subheader("Métricas do Modelo em Produção")
        st.write(f"Modelo: {model_metrics['type']}")

        model_col1, model_col2, model_col3, model_col4 = st.columns(4)
        model_col1.metric("Acurácia", f"{model_acc*100:.2f}%")
        model_col2.metric("F1-Score", f"{model_f1*100:.2f}%")
        model_col3.metric("Precisão", f"{model_precision*100:.2f}%")
        model_col4.metric("Recall", f"{model_recall*100:.2f}%")

        st.write("---")
        st.subheader("Resoluções ao Longo do Tempo")
        df["day"] = df["date_format"].dt.date

        df_by_day = (
            df.groupby(["day", "status"]).size().reset_index(name="count")
        )

        chart = alt.Chart(df_by_day).mark_line(point=True).encode(
            x=alt.X("day:T", title="Dia"),
            y=alt.Y("count:Q", title="Qtd. de Reclamações"),
            color=alt.Color("status:N", title="Status"),
            tooltip=["day:T", "status:N", "count:Q"]
        ).properties(height=400)

        st.altair_chart(chart, use_container_width=True)

        st.write("---")
        st.subheader("Empresas em Destaque")
        col6, col7 = st.columns(2)

        with col6:
            st.markdown("#### Mais Reclamações")
            top_companies = df_filtered["company_name"].value_counts().head(5).reset_index()
            top_companies['Proporção'] = top_companies['count'] / total
            top_companies.columns = ["Empresa", "Qtd", "Proporção"]
            st.dataframe(top_companies, use_container_width=True)

        with col7:
            st.markdown("#### Maior Taxa de Resolução")
            company_resolutions = df_filtered.groupby("company_name").agg({
                'status': ['count', lambda x: (x == "Resolvido").mean()]
            }).reset_index()
            company_resolutions.columns = ["Empresa", "Total de Reclamações", "Taxa de Resolução"]
            top_res = company_resolutions.sort_values("Taxa de Resolução", ascending=False).head(5)
            st.dataframe(top_res, use_container_width=True)

        col8, col9 = st.columns(2)
        with col8:
            st.markdown("#### Menor Taxa de Resolução")
            worst_res = company_resolutions.sort_values("Taxa de Resolução").head(5)
            st.dataframe(worst_res, use_container_width=True)

        st.write("---")
        st.subheader("Avaliações das Reclamações")

        col10, col11, col_12 = st.columns(3)
        df_ratings = df_filtered[df_filtered["rating"] != nan].assign(rating = lambda x: x.rating.astype(int))

        with col10:
            st.markdown("#### Média Geral")
            mean_reports_per_company_df = (
                df.groupby("company_name").agg({
                    "id_report": "count",
                    "rating": "mean"
                }).reset_index()
            )
            mean_reports_per_company_df['count'] = mean_reports_per_company_df['id_report'].astype(int)
            mean_score = mean_reports_per_company_df["rating"].mean()
            mean_reports = mean_reports_per_company_df["count"].mean()
            st.write(f"###### Métricas Gerais")
            st.metric("Nota Média", f"{mean_score:.2f}")
            st.metric("Média de Reclamações por Empresa", f"{mean_reports:.2f}")

        with col11:
            st.markdown("#### Por Status")
            avg_by_status = df.groupby("status").agg({'rating': ['count', 'mean']}).reset_index()
            col11_1, col11_2 = st.columns(2)
            with col11_1:
                st.markdown("###### ✅ Resolvido")
                st.metric("Total de Reclamações", f"{avg_by_status['rating']['count'][0]}")
                st.metric("Média de Avaliação", f"{avg_by_status['rating']['mean'][0]:.2f}")

            with col11_2:
                st.markdown("###### ❌ Não Resolvido")
                st.metric("Total de Reclamações", f"{avg_by_status['rating']['count'][1]}")
                st.metric("Média de Avaliação", f"{avg_by_status['rating']['mean'][1]:.2f}")

        with col_12:
            st.markdown("#### Por Empresa")
            avg_by_company = df_ratings.groupby("company_name").agg({
                'rating': ['count', 'mean']
            }).reset_index()
            avg_by_company.columns = ["Empresa", "Total de Reclamações", "Média de Avaliação"]
            st.dataframe(avg_by_company, use_container_width=True)

        st.write("---")
        st.subheader("Probabilidade de Resolução")

        col12, col13 = st.columns(2)
        with col12:
            st.markdown("#### Empresas com Maior Probabilidade Média")
            high_pred = df_filtered.groupby("company_name").agg({
                'prediction': ['count', 'mean']
            }).reset_index()
            high_pred.columns = ["Empresa", "Total de Reclamações", "Probabilidade Média"]
            high_pred = high_pred.sort_values("Probabilidade Média", ascending=False).head(5)
            st.dataframe(high_pred, use_container_width=True)

        with col13:
            st.markdown("#### Empresas com Menor Probabilidade Média")
            low_pred = df_filtered.groupby("company_name").agg({
                'prediction': ['count', 'mean']
            }).reset_index()
            low_pred.columns = ["Empresa", "Total de Reclamações", "Probabilidade Média"]
            low_pred = low_pred.sort_values("Probabilidade Média").head(5)
            st.dataframe(low_pred, use_container_width=True)

        col14, col15 = st.columns(2)
        with col14:
            st.markdown("#### Reclamações com Maior Probabilidade de Resolução")
            top_res = df_filtered.sort_values("prediction", ascending=False)[["company_name", "prediction", "report"]].head(5)
            st.dataframe(top_res, use_container_width=True)

        with col15:
            st.markdown("#### Reclamações com Menor Probabilidade de Resolução")
            bottom_res = df_filtered.sort_values("prediction")[["company_name", "prediction", "report"]].head(5)
            st.dataframe(bottom_res, use_container_width=True)
