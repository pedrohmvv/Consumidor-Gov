import streamlit as st

class ServantPage:
    def __init__(self):
        self.username = st.session_state.username
        
    def render(self):
        st.title(f"Painel do Servidor - {self.username}")
        st.markdown("---")
        
        # Sidebar com menu de navegação
        with st.sidebar:
            st.markdown("### Menu do Servidor")
            menu_option = st.radio(
                "Selecione uma opção:",
                ["Dashboard", "Gerenciar Reclamações", "Relatórios", "Perfil"]
            )
            
        # Conteúdo principal baseado na opção selecionada
        if menu_option == "Dashboard":
            self.render_dashboard()
        elif menu_option == "Gerenciar Reclamações":
            self.render_complaints_management()
        elif menu_option == "Relatórios":
            self.render_reports()
        elif menu_option == "Perfil":
            self.render_profile()
            
    def render_dashboard(self):
        st.header("Dashboard do Servidor")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Reclamações Pendentes", "25")
        with col2:
            st.metric("Reclamações em Análise", "15")
        with col3:
            st.metric("Reclamações Resolvidas Hoje", "8")
            
    def render_complaints_management(self):
        st.header("Gerenciamento de Reclamações")
        tab1, tab2, tab3 = st.tabs(["Pendentes", "Em Análise", "Resolvidas"])
        
        with tab1:
            st.subheader("Reclamações Pendentes")
            # Implementar listagem de reclamações pendentes
            
        with tab2:
            st.subheader("Reclamações em Análise")
            # Implementar listagem de reclamações em análise
            
        with tab3:
            st.subheader("Reclamações Resolvidas")
            # Implementar listagem de reclamações resolvidas
            
    def render_reports(self):
        st.header("Relatórios")
        report_type = st.selectbox(
            "Tipo de Relatório",
            ["Reclamações por Categoria", "Tempo Médio de Resposta", "Satisfação do Usuário"]
        )
        
        if st.button("Gerar Relatório"):
            st.info("Funcionalidade em desenvolvimento")
            
    def render_profile(self):
        st.header("Perfil do Servidor")
        # Implementar visualização e edição do perfil do servidor 