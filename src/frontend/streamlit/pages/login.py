import streamlit as st

class LoginPage:
    def __init__(self):
        self.user_types = ['cidadao', 'servidor', 'empresa']
        
    def render(self):
        st.title("Bem-vindo ao Consumidor.gov")
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1,2,1])
        
        with col2:
            st.markdown("### Login")
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            user_type = st.selectbox("Tipo de Usuário", self.user_types)
            
            if st.button("Entrar"):
                # Aqui você deve implementar a lógica de autenticação real
                if self.authenticate(username, password, user_type):
                    st.session_state.authenticated = True
                    st.session_state.user_type = user_type
                    st.session_state.username = username
                    st.experimental_rerun()
                else:
                    st.error("Credenciais inválidas!")
                    
    def authenticate(self, username, password, user_type):
        # Implementação temporária para teste
        # Em produção, você deve implementar uma autenticação segura
        if username and password:
            return True
        return False 