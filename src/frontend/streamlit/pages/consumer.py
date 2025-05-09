import streamlit as st

class ConsumerPage:
    def __init__(self):
        self.username = st.session_state.username
        
    def render(self):
        st.title(f"Bem-vindo, {self.username}!")
        st.markdown("---")
        
        # Sidebar com menu de navegação
        with st.sidebar:
            st.markdown("### Menu do Cidadão")
            menu_option = st.radio(
                "Selecione uma opção:",
                ["Dashboard", "Fazer Reclamação", "Minhas Reclamações", "Perfil"]
            )
            
        # Conteúdo principal baseado na opção selecionada
        if menu_option == "Dashboard":
            self.render_dashboard()
        elif menu_option == "Fazer Reclamação":
            self.render_complaint_form()
        elif menu_option == "Minhas Reclamações":
            self.render_my_complaints()
        elif menu_option == "Perfil":
            self.render_profile()
            
    def render_dashboard(self):
        st.header("Dashboard")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Reclamações Ativas", "3")
        with col2:
            st.metric("Reclamações Resolvidas", "12")
        with col3:
            st.metric("Tempo Médio de Resposta", "5 dias")
            
    def render_complaint_form(self):
        st.header("Nova Reclamação")
        with st.form("complaint_form"):
            company = st.text_input("Empresa")
            category = st.selectbox("Categoria", ["Produto", "Serviço", "Atendimento"])
            description = st.text_area("Descrição da Reclamação")
            submit = st.form_submit_button("Enviar")
            
    def render_my_complaints(self):
        st.header("Minhas Reclamações")
        # Aqui você implementará a listagem das reclamações do usuário
        
    def render_profile(self):
        st.header("Meu Perfil")
        # Aqui você implementará a visualização e edição do perfil do usuário 