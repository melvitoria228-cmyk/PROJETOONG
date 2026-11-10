# ==============================================================================
# IMPORTS E DEPENDÊNCIAS
# ==============================================================================
import re
import requests
import reflex as rx

# Endpoint de alteração de senha no Xano
XANO_CHANGE_PASSWORD_URL = "https://x8ki-letl-twmt.n7.xano.io/api:RNkNxhJn/usuario/alterar-senha"


# ==============================================================================
# ESTADO DA PÁGINA (STATE)
# Gerencia os dados, visibilidade, cálculo de força e validações
# ==============================================================================
class ChangePasswordState(rx.State):
    """Estado responsável pelo gerenciamento dos dados e lógica de validação de senha."""
    # Lê o token salvo no navegador após o login
    auth_token: str = rx.Cookie("", name="auth_token")

    # Variáveis de formulário e visibilidade
    show_password: bool = False
    old_password: str = ""
    new_password: str = ""
    confirm_password: str = ""
    is_loading: bool = False

    def set_new_password(self, value: str):
        """Atualiza a nova senha."""
        self.new_password = value

    def set_confirm_password(self, value: str):
        """Atualiza a confirmação da senha."""
        self.confirm_password = value

    def toggle_show_password(self):
        """Alterna a visibilidade dos campos entre texto plano e senha oculta."""
        self.show_password = not self.show_password

    @rx.var
    def password_strength(self) -> int:
        """Calcula a pontuação da força da nova senha de 0 a 100."""
        pwd = self.new_password
        if not pwd:
            return 0
        score = 0
        if len(pwd) >= 8:
            score += 35
        if re.search(r"[A-Z]", pwd):
            score += 25
        if re.search(r"[0-9]", pwd):
            score += 20
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
            score += 20
        return min(score, 100)

    @rx.var
    def strength_color(self) -> str:
        """Retorna a cor da barra de progresso com base na pontuação de força."""
        s = self.password_strength
        if s < 40:
            return "red"
        if s < 75:
            return "orange"
        return "green"

    @rx.var
    def strength_label(self) -> str:
        """Retorna o texto orientativo referente à força da senha."""
        s = self.password_strength
        if s < 40:
            return "Senha fraca (adicione maiúsculas, números ou símbolos)"
        if s < 75:
            return "Senha média"
        return "Senha forte"

    @rx.var
    def passwords_match(self) -> bool:
        """Valida se o campo de confirmação coincide com a nova senha."""
        if not self.confirm_password:
            return True
        return self.new_password == self.confirm_password

    @rx.var
    def is_submit_disabled(self) -> bool:
        """Bloqueia o botão se a senha for fraca ou os campos não coincidirem."""
        return (
            self.password_strength < 40
            or not self.passwords_match
            or self.new_password == ""
            or self.confirm_password == ""
        )

    def submit_change_password(self):
        """Executa a alteração e exibe o feedback visual."""
        if not self.auth_token:
            yield rx.toast.error("Sessão expirada. Faça login novamente.")
            yield rx.redirect("/login")
            return

        self.is_loading = True
        yield  # Renderiza a mudança visual no botão para o estado de carregamento

        try:
            # PARTE 3: Configuração e envio da requisição PUT para o Xano
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}",
            }

            payload = {
                "new_password": self.new_password,
            }

            response = requests.put(
                XANO_CHANGE_PASSWORD_URL,
                json=payload,
                headers=headers,
                timeout=10,
            )

            self.is_loading = False

            # Tratamento da Resposta do Xano
            if response.status_code == 200:
                self.new_password = ""
                self.confirm_password = ""
                yield rx.toast.success("Senha alterada com sucesso!")
                yield rx.redirect("/")
            else:
                data = response.json()
                msg = data.get("message", "Erro ao alterar a senha no servidor.")
                yield rx.toast.error(f"Erro: {msg}")

        except Exception as e:
            self.is_loading = False
            yield rx.toast.error("Erro de conexão com o servidor.")

# ==============================================================================
# COMPONENTES AUXILIARES E INTERFACE (UI)
# ==============================================================================
def password_input_with_toggle(placeholder: str, value: rx.Var, on_change) -> rx.Component:
    """Campo de entrada com botão acoplado para alternar a visibilidade (olho)."""
    return rx.hstack(
        rx.input(
            placeholder=placeholder,
            type=rx.cond(ChangePasswordState.show_password, "text", "password"),
            value=value,
            on_change=on_change,
            width="100%",
        ),
        rx.button(
            rx.cond(
                ChangePasswordState.show_password,
                rx.icon(tag="eye_off", size=18),
                rx.icon(tag="eye", size=18),
            ),
            on_click=ChangePasswordState.toggle_show_password,
            variant="ghost",
            color_scheme="gray",
            type="button",
        ),
        width="100%",
        align="center",
    )


def formulario_alterar_senha() -> rx.Component:
    """Constroi o formulário visual de alteração de senha."""
    return rx.vstack(
        # Cabeçalho do formulário
        rx.hstack(
            rx.box(
                rx.icon(tag="lock", size=24, color="orange"),
                padding="2",
                bg="orange.2",
                border_radius="md",
            ),
            rx.vstack(
                rx.heading("Alterar Senha", size="5", weight="bold"),
                rx.text(
                    "Escolha uma nova senha forte para proteger sua conta",
                    size="2",
                    color="gray",
                ),
                spacing="1",
            ),
            align="center",
            spacing="3",
        ),
        rx.divider(),

        # Bloco: Nova Senha + Medidor de Força
        rx.vstack(
            rx.text("Nova Senha", size="2", weight="bold"),
            password_input_with_toggle(
                "Digite sua nova senha",
                ChangePasswordState.new_password,
                ChangePasswordState.set_new_password,
            ),
            rx.cond(
                ChangePasswordState.new_password != "",
                rx.vstack(
                    rx.progress(
                        value=ChangePasswordState.password_strength,
                        color_scheme=ChangePasswordState.strength_color,
                        width="100%",
                        size="1",
                    ),
                    rx.text(
                        ChangePasswordState.strength_label,
                        size="1",
                        color=f"{ChangePasswordState.strength_color}.9",
                    ),
                    width="100%",
                    spacing="1",
                ),
            ),
            width="100%",
            spacing="2",
        ),

        # Bloco: Confirmar Nova Senha
        rx.vstack(
            rx.text("Confirmar Nova Senha", size="2", weight="bold"),
            password_input_with_toggle(
                "Repita a nova senha",
                ChangePasswordState.confirm_password,
                ChangePasswordState.set_confirm_password,
            ),
            rx.cond(
                ~ChangePasswordState.passwords_match,
                rx.text("As senhas não coincidem", size="1", color="red"),
            ),
            width="100%",
            spacing="2",
        ),

        # Botão Principal de Ação
        rx.button(
            "Atualizar Senha",
            color_scheme="orange",
            width="100%",
            loading=ChangePasswordState.is_loading,
            disabled=ChangePasswordState.is_submit_disabled,
            on_click=ChangePasswordState.submit_change_password,
            margin_top="3",
        ),
        spacing="4",
        width="100%",
        max_width="380px",
    )


# ==============================================================================
# PÁGINA PRINCIPAL
# Envolve o formulário no painel com o botão Sair fixo no topo direito
# ==============================================================================
def alterar_senha_page(painel_autenticacao_func) -> rx.Component:
    """Página completa com o botão Sair padronizado e animado no canto superior direito."""
    return rx.box(
        # Status do usuário + Botão "Sair" Animado e Colorido (Padrão do Sistema)
        rx.box(
            rx.link(
                rx.hstack(
                    rx.text("Sair", font_size="1.15em", font_weight="bold"),
                    rx.icon(tag="arrow-right", size=20),
                    spacing="2",
                    align="center",
                ),
                on_click=rx.redirect("/"),
                color="#8C4A32",
                display="inline-block",  # Permite que a propriedade transform/animação funcione no hover
                transition="all 0.2s ease",
                cursor="pointer",
                _hover={
                    "color": "#D78A45",
                    "transform": "translateX(4px)",
                    "text_decoration": "none",
                },
            ),
            position="absolute",
            top="20px",
            right="20px",
            z_index="1000",
        ),
        # Layout base contendo o formulário
        painel_autenticacao_func(formulario_alterar_senha()),
        width="100%",
        height="100vh",
        position="relative",
    )