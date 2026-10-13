import os
import httpx
import reflex as rx
from dotenv import load_dotenv
from ProjetoONG.gestao_animal import gestao_animal
load_dotenv()

XANO_LOGIN_URL = os.getenv("XANO_LOGIN_URL")
XANO_ME_URL = os.getenv("XANO_ME_URL")
XANO_ANIMAL_LIST_URL = os.getenv("XANO_ANIMAL_LIST_URL")
XANO_ANIMAL_CREATE_URL = os.getenv("XANO_ANIMAL_CREATE_URL")
XANO_ANIMAL_DETAIL_URL = os.getenv("XANO_ANIMAL_DETAIL_URL")
XANO_ANIMAL_UPDATE_URL = os.getenv("XANO_ANIMAL_UPDATE_URL")
XANO_ANIMAL_DELETE_URL = os.getenv("XANO_ANIMAL_DELETE_URL")


class LoginState(rx.State):
    email: str = ""
    senha: str = ""
    token: str = ""
    tipo_usuario: str = ""
    tela_atual: str = "inicio"

    @rx.event
    def set_tela(self, tela: str):
        self.tela_atual = tela

    @rx.event
    def set_email(self, valor: str):
        self.email = valor

    @rx.event
    def set_senha(self, valor: str):
        self.senha = valor

    @rx.event
    async def validar_login(self):
        if not self.email.strip() or not self.senha:
            return rx.toast("Preencha o e-mail e a senha.")

        if not XANO_LOGIN_URL or not XANO_ME_URL:
            return rx.toast(
                "A conexão com o servidor não está configurada."
            )

        etapa = "login"

        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:

                # 1. Envia as credenciais ao Xano
                resposta = await cliente.post(
                    XANO_LOGIN_URL,
                    json={
                        "email": self.email.strip(),
                        "password": self.senha,
                    },
                )

                if resposta.status_code in (401, 403):
                    return rx.toast("E-mail ou senha inválidos.")

                if resposta.status_code != 200:
                    print(
                        f"Erro no login: HTTP {resposta.status_code}"
                    )
                    return rx.toast(
                        "O servidor não conseguiu realizar o login."
                    )

                try:
                    dados = resposta.json()
                except ValueError:
                    print("O login retornou uma resposta que não é JSON.")
                    return rx.toast("Resposta inválida do servidor.")

                token = dados.get("authToken")

                if not token:
                    print("A resposta do login não contém authToken.")
                    return rx.toast(
                        "O servidor não retornou o token de acesso."
                    )

                # 2. Consulta os dados do usuário autenticado
                etapa = "consulta do usuário"

                resposta_usuario = await cliente.get(
                    XANO_ME_URL,
                    headers={
                        "Authorization": f"Bearer {token}"
                    },
                )

                if resposta_usuario.status_code != 200:
                    print(
                        "Erro em /auth/me: "
                        f"HTTP {resposta_usuario.status_code}"
                    )
                    return rx.toast(
                        "Não foi possível confirmar o usuário autenticado."
                    )

                try:
                    usuario = resposta_usuario.json()
                except ValueError:
                    print(
                        "/auth/me retornou uma resposta que não é JSON."
                    )
                    return rx.toast(
                        "Resposta inválida ao consultar o usuário."
                    )

                tipo_usuario = usuario.get("tipo_usuario")

                if not isinstance(tipo_usuario, str):
                    print("Tipo de usuário ausente ou não reconhecido.")
                    return rx.toast(
                        "Tipo de usuário não reconhecido."
                    )

                tipo_usuario = tipo_usuario.strip().lower()

                if tipo_usuario == "administrador":
                    self.token = token
                    self.tipo_usuario = tipo_usuario
                    return rx.redirect("/administrativo")

                if tipo_usuario == "tutor/adotante":
                    self.token = token
                    self.tipo_usuario = tipo_usuario
                    return rx.redirect("/tutor")

                print("Tipo de usuário ausente ou não reconhecido.")
                return rx.toast(
                    "Tipo de usuário não reconhecido."
                )

        except httpx.RequestError as erro:
            # Não exibe senha, token ou endereço da requisição
            print(
                f"Falha de conexão na etapa '{etapa}': "
                f"{type(erro).__name__}"
            )
            return rx.toast(
                f"Falha de conexão durante {etapa}. "
                "Consulte o terminal para verificar o erro."
            )

    @rx.event
    def sair(self):
        """Limpa os dados locais da sessão e retorna à tela de login."""
        self.token = ""
        self.tipo_usuario = ""
        self.email = ""
        self.senha = ""
        self.tela_atual = "inicio"
        return rx.redirect("/")


def index() -> rx.Component:
    return rx.hstack(
        # Painel visual à esquerda
        rx.center(
            rx.vstack(
                rx.text("🐾", size="9"),
                rx.heading(
                    "Porto Seguro Pet",
                    size="8",
                    color="#3E4149",
                ),
                rx.text(
                    "Cuidando de vidas, construindo novos começos.",
                    size="4",
                    color="#3E4149",
                    text_align="center",
                ),
                spacing="4",
                align="center",
                max_width="440px",
                padding="8",
            ),
            width="50%",
            height="100vh",
            background="#F4E7D5",
        ),

        # Painel de login à direita
        rx.center(
            rx.vstack(
                rx.heading(
                    "Olá! Que bom ter você aqui!",
                    size="6",
                    color="#3E4149",
                ),
                rx.text(
                    "Faça seu login para continuar.",
                    size="3",
                    color="#5E5A55",
                ),
                rx.input(
                    placeholder="E-mail",
                    type="email",
                    on_change=LoginState.set_email,
                    width="60%",
                    radius="large",
                ),
                rx.input(
                    placeholder="Senha",
                    type="password",
                    on_change=LoginState.set_senha,
                    width="60%",
                    radius="large",
                ),

                # Botão Entrar centralizado
                rx.center(
                    rx.button(
                        "Entrar",
                        on_click=LoginState.validar_login,
                        width="80%",
                        background="#D78A45",
                        color="white",
                        radius="large",
                    ),
                    width="60%",
                ),

                spacing="4",
                align="stretch",
                width="80%",
                max_width="400px",
            ),
            width="50%",
            height="100vh",
            background="#FFF7ED",
        ),

        width="100%",
        height="100vh",
        spacing="0",
        align="stretch",
    )


def item_menu(icone: str, texto: str, tela: str = "") -> rx.Component:
    """Item do menu lateral. Sem 'tela', o item ainda não faz nada."""
    ativo = LoginState.tela_atual == tela
    return rx.hstack(
        rx.icon(
            icone,
            size=18,
            color=rx.cond(ativo, "#684638", "#766A62"),
        ),
        rx.text(
            texto,
            size="2",
            weight=rx.cond(ativo, "bold", "medium"),
            color=rx.cond(ativo, "#342D29", "#5E5A55"),
        ),
        spacing="3",
        align="center",
        width="100%",
        padding="10px 12px",
        border_radius="10px",
        cursor="pointer",
        background=rx.cond(ativo, "#FFFFFF", "transparent"),
        box_shadow=rx.cond(ativo, "0 1px 3px rgba(104, 70, 56, 0.15)", "none"),
        transition="background 0.15s ease",
        _hover={"background": "rgba(255, 255, 255, 0.65)"},
        on_click=LoginState.set_tela(tela) if tela else None,
    )


def titulo_secao_menu(texto: str) -> rx.Component:
    return rx.text(
        texto,
        size="1",
        weight="bold",
        color="#9A8C82",
        letter_spacing="0.08em",
        padding="14px 12px 4px 12px",
    )


def menu_lateral() -> rx.Component:
    return rx.vstack(
        # Marca
        rx.hstack(
            rx.center(
                rx.icon("paw-print", size=22, color="white"),
                background="#684638",
                border_radius="12px",
                width="42px",
                height="42px",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text("Porto Seguro Pet", size="4", weight="bold", color="#342D29"),
                rx.text("Painel administrativo", size="1", color="#766A62"),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
            padding="4px 4px 16px 4px",
            width="100%",
        ),

        rx.divider(color_scheme="brown", opacity="0.4"),

        titulo_secao_menu("PRINCIPAL"),
        item_menu("layout-dashboard", "Início", "inicio"),
        item_menu("paw-print", "Gestão de Animais", "animais"),
        item_menu("bed-double", "Lares Temporários"),

        titulo_secao_menu("ATENDIMENTO"),
        item_menu("stethoscope", "Atendimento Veterinário"),
        item_menu("heart-handshake", "Adoções"),
        item_menu("clipboard-check", "Pós-Adoção"),

        titulo_secao_menu("ADMINISTRAÇÃO"),
        item_menu("users", "Voluntários"),
        item_menu("package", "Estoque"),
        item_menu("wallet", "Doações"),

        spacing="1",
        align="stretch",
        width="280px",
        min_width="280px",
        height="100vh",
        padding="24px 16px",
        background="#F4E7D5",
        border_right="1px solid #EAE1D7",
        overflow_y="auto",
    )


def area_administrativa() -> rx.Component:
    return rx.hstack(
        # Menu lateral administrativo
        menu_lateral(),

        # Área principal administrativa
        rx.vstack(
            # Cabeçalho com o botão Sair à direita
            rx.hstack(
                rx.spacer(),
                rx.button(
                    "↩  Sair",
                    on_click=LoginState.sair,
                    color="#FFFFFF",
                    background="#684638",
                ),
                width="100%",
                align="center",
                padding="20px 24px",
            ),

            # Conteúdo central
            rx.box(
                rx.cond(
                    LoginState.tela_atual == "animais",
                    gestao_animal(LoginState.token),

                    
                    rx.vstack(
                        rx.text(
                           "Bem-vindo à área administrativa!",
                           size="8",
                           weight="bold",
                           color="#3E4149",
                        ),


                        rx.text(
                            "Proteção, cuidado e novas oportunidades.",
                            size="4",
                            color="#6D896F",
                        ),

                        rx.box(
                           rx.vstack(
                                rx.heading(
                                    "Quem somos",
                                    size="5",
                                    color="#3E4149",
                               ),


                              rx.text(
                                   "Somos uma organização dedicada à proteção e ao cuidado dos animais, acompanhando sua trajetória do resgate à adoção responsável.",
                                   size="3",
                                   color="#5E5A55",
                                ),
                   
                   
                               spacing="3",
                               align="start",
                               width="100%",
                            ),

                          background="#FFFFFF",
                          padding="24px",
                          border_radius="16px",
                          width="100%",
                          box_shadow="0 2px 10px rgba(62, 65, 73, 0.08)",
                        ),


                        rx.box(
                            rx.vstack(
                                rx.heading(
                                    "Nossa missão",
                                    size="5",
                                    color="#3E4149",
                                ),


                                rx.text(
                                    "Promover o bem-estar animal por meio do resgate, dos cuidados necessários, do acolhimento temporário e da busca por lares responsáveis.",
                                    size="3",
                                    color="#5E5A55",
                                
                                ),
                                spacing="3",
                                align="start",
                                width="100%",
                            ),
                         background="#FFFFFF",
                         padding="24px",
                         border_radius="16px",
                         width="100%",
                         box_shadow="0 2px 10px rgba(62, 65, 73, 0.08)",
                        ),
                        spacing="5",
                        align="center",
                        justify="center",
                        width="100%",
                        max_width="760px",
                        min_height="60vh",
                        margin="0 auto",
                        padding="24px",
                    ),
                ),
                width="100%",
                flex="1",
            ),
            spacing="0",
            align="stretch",
            flex="1",
            min_width="0",
            min_height="100vh",
            background="#FAF6F0",
        ),    
    ),

# Fim da área administrativa


def cartao_tutor(icone: str, titulo: str, texto: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.center(
                rx.icon(
                    icone,
                    size=30,
                    color="#D78A45",
                ),
                width="54px",
                height="54px",
                background="#F4E7D5",
                border_radius="14px",
            ),
            rx.heading(
                titulo,
                size="4",
                color="#3E4149",
            ),
            rx.text(
                texto,
                size="2",
                color="#5E5A55",
            ),
            align="start",
            spacing="3",
            width="100%",
        ),
        width="100%",
        height="100%",
        padding="20px",
        background="#FFFFFF",
        border_radius="16px",
        box_shadow="0 4px 14px rgba(62, 65, 73, 0.08)",
    )


def area_tutor() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Cabeçalho superior
            rx.hstack(
                rx.hstack(
                    rx.text(
                        "🐾",
                        size="7",
                    ),
                    rx.heading(
                        "Porto Seguro Pet",
                        size="6",
                        color="#3E4149",
                    ),
                    align="center",
                    spacing="2",
                ),

                rx.spacer(),

                rx.text(
                    "Área do Tutor/Adotante",
                    size="3",
                    weight="bold",
                    color="#3E4149",
                ),

                rx.button(
                    "Sair",
                    on_click=LoginState.sair,
                    background="#D78A45",
                    color="#FFFFFF",
                    radius="large",
                ),

                width="100%",
                align="center",
                padding="20px 5%",
                background="#FFFFFF",
                border="none",
                box_shadow="none",
            ),

            # Área de boas-vindas
            rx.box(
                rx.vstack(
                    rx.text(
                        "SEJA BEM-VINDO(A)!",
                        size="2",
                        weight="bold",
                        color="#D78A45",
                    ),

                    rx.heading(
                        "Um novo começo começa com amor.",
                        size="7",
                        color="#3E4149",
                    ),

                    rx.text(
                        "Cada adoção é um novo começo. "
                        "Obrigado por fazer parte dessa causa!",
                        size="4",
                        color="#5E5A55",
                    ),

                    rx.text(
                        "🐶  🐱  Mais cuidado, carinho e histórias felizes.",
                        size="3",
                        color="#5E5A55",
                    ),

                    align="start",
                    spacing="3",
                    width="100%",
                ),

                width="100%",
                padding="32px",
                background="#F4E7D5",
                border_radius="20px",
            ),

            # Título da seção de cartões
            rx.vstack(
                rx.heading(
                    "Meu espaço",
                    size="6",
                    color="#3E4149",
                ),

                rx.text(
                    "Encontre aqui os espaços de interesse para você.",
                    size="3",
                    color="#5E5A55",
                ),

                align="start",
                spacing="1",
                width="100%",
            ),

            # Cartões informativos
            rx.grid(
                cartao_tutor(
                    "heart",
                    "Minhas adoções",
                    "Espaço destinado às informações sobre suas adoções.",
                ),
                cartao_tutor(
                    "calendar-check",
                    "Acompanhamento",
                    "Espaço destinado ao acompanhamento pós-adoção.",
                ),
                cartao_tutor(
                    "user-round",
                    "Meus dados",
                    "Espaço destinado às informações do tutor.",
                ),
                cartao_tutor(
                    "book-open",
                    "Orientações",
                    "Espaço destinado a orientações sobre adoção responsável.",
                ),

                columns={
                    "initial": "1",
                    "sm": "2",
                    "lg": "4",
                },

                spacing="4",
                width="100%",
            ),

            # Mensagem de adoção responsável
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Adotar é um ato de amor",
                        size="4",
                        color="#3E4149",
                    ),

                    rx.text(
                        "Uma adoção responsável transforma a vida "
                        "do animal e de toda a família.",
                        size="3",
                        color="#5E5A55",
                    ),

                    align="center",
                    spacing="2",
                    width="100%",
                ),

                width="100%",
                padding="24px",
                background="#FFFFFF",
                border_radius="16px",
            ),

            # Rodapé
            rx.text(
                "Juntos por mais histórias de amor. "
                "Porto Seguro Pet — Adoção é um ato de amor.",
                color="#5E5A55",
                size="2",
                text_align="center",
                width="100%",
                padding_top="8px",
                padding_bottom="12px",
            ),

            spacing="5",
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding="24px",
        ),

        width="100%",
        min_height="100vh",
        background="#FFF7ED",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="brown",
    ),
)
app.add_page(index)
app.add_page(
    area_administrativa,
    route="/administrativo",
)
app.add_page(
    area_tutor,
    route="/tutor",
)