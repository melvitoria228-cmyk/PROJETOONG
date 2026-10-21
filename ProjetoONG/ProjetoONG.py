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
XANO_ADOCAO_LIST_URL = os.getenv("XANO_ADOCAO_LIST_URL")
XANO_ACOMPANHAMENTO_LIST_URL = os.getenv("XANO_ACOMPANHAMENTO_LIST_URL")
XANO_ACOMPANHAMENTO_DETAIL_URL = os.getenv("XANO_ACOMPANHAMENTO_DETAIL_URL")


class LoginState(rx.State):
    email: str = ""
    senha: str = ""
    token: str = ""
    tipo_usuario: str = ""
    tela_atual: str = "inicio"

    adocoes: list[dict[str, str]] = []
    carregando_adocoes: bool = False
    erro_adocoes: str = ""

    nome_usuario: str = ""
    acompanhamentos: list[dict[str, str]] = []
    carregando_acompanhamentos: bool = False
    erro_acompanhamentos: str = ""

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
    async def carregar_adocoes(self):
        if not self.token:
            self.erro_adocoes = "Faça login para consultar suas adoções."
            return

        if not XANO_ADOCAO_LIST_URL:
            self.erro_adocoes = "A URL de consulta não está configurada."
            return

        self.carregando_adocoes = True
        self.erro_adocoes = ""

        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta = await cliente.get(
                    XANO_ADOCAO_LIST_URL,
                    headers={
                        "Authorization": f"Bearer {self.token}"
                    },
                )

            if resposta.status_code != 200:
                self.erro_adocoes = (
                    "Não foi possível consultar suas adoções."
                )
                return

            dados = resposta.json()

            if isinstance(dados, dict):
                dados = dados.get("items", [])

            if not isinstance(dados, list):
                self.erro_adocoes = (
                    "O servidor retornou dados em formato inesperado."
                )
                return

            self.adocoes = [
                {
                    "id": str(item.get("id", "")),
                    "data_solicitacao": str(
                        item.get("data_solicitacao", "")
                    ),
                    "status_processo": str(
                        item.get("status_processo", "")
                    ),
                    "animal_id": str(item.get("animal_id", "")),
                }
                for item in dados
                if isinstance(item, dict)
            ]

        except httpx.RequestError:
            self.erro_adocoes = (
                "Falha de conexão ao consultar suas adoções."
            )
        except ValueError:
            self.erro_adocoes = (
                "O servidor retornou uma resposta inválida."
            )
        finally:
            self.carregando_adocoes = False



    @rx.event
    async def carregar_acompanhamentos(self):
        if not self.token:
            self.erro_acompanhamentos = "Faça login para consultar o acompanhamento."
            return

        if not XANO_ACOMPANHAMENTO_LIST_URL:
            self.erro_acompanhamentos = "A URL de consulta de acompanhamento não está configurada."
            return

        self.carregando_acompanhamentos = True
        self.erro_acompanhamentos = ""

        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta = await cliente.get(
                    XANO_ACOMPANHAMENTO_LIST_URL,
                    headers={"Authorization": f"Bearer {self.token}"},
                )

            if resposta.status_code != 200:
                self.erro_acompanhamentos = "Não foi possível consultar o acompanhamento pós-adoção."
                return

            dados = resposta.json()

            if isinstance(dados, dict):
                dados = dados.get("items", [])

            if not isinstance(dados, list):
                self.erro_acompanhamentos = "Dados retornados em formato não suportado."
                return

            self.acompanhamentos = [
                {
                    "id": str(item.get("id", "")),
                    "processo_adocao_id": str(item.get("processo_adocao_id", "")),
                    "data_visita": str(item.get("data_visita", item.get("created_at", ""))),
                    "observacao": str(item.get("relatorio_observacao") or "Sem observações cadastradas."),
                }
                for item in dados
                if isinstance(item, dict)
            ]

        except httpx.RequestError:
            self.erro_acompanhamentos = "Falha de conexão ao consultar acompanhamentos."
        except ValueError:
            self.erro_acompanhamentos = "Resposta inválida do servidor."
        finally:
            self.carregando_acompanhamentos = False



    @rx.event
    def avisar_recuperacao_visual(self):
        return rx.toast(
            "Nenhuma solicitação foi enviada. A integração ainda não está implementada."
        )

    @rx.event
    def avisar_alteracao_visual(self):
        return rx.toast(
            "Nenhuma senha foi alterada. A integração ainda não está implementada."
        )

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
                    try:
                        erro_login = resposta.json()
                    except ValueError:
                        erro_login = {}

                    if (
                        isinstance(erro_login, dict)
                        and erro_login.get("message") == "Invalid Credentials."
                    ):
                        return rx.toast("E-mail ou senha inválidos.")

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


def painel_autenticacao(conteudo: rx.Component) -> rx.Component:
    return rx.hstack(
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
        rx.center(
            conteudo,
            width="50%",
            height="100vh",
            background="#FFF7ED",
        ),
        width="100%",
        height="100vh",
        spacing="0",
        align="stretch",
    )

##--- TELA VISUAL 
def recuperar_senha() -> rx.Component:
    return painel_autenticacao(
        rx.vstack(
            rx.heading(
                "Recuperar senha",
                size="6",
                color="#3E4149",
            ),
            rx.text(
                "Informe o e-mail cadastrado na sua conta.",
                size="3",
                color="#5E5A55",
            ),
            rx.input(
                placeholder="E-mail",
                type="email",
                width="100%",
                radius="large",
            ),
            rx.button(
                "Solicitar recuperação",
                on_click=LoginState.avisar_recuperacao_visual,
                width="100%",
                background="#D78A45",
                color="white",
                radius="large",
            ),
            rx.text(
                "Esta tela é apenas visual. Nenhuma solicitação será enviada.",
                size="1",
                color="#766A62",
            ),
            rx.link(
                "Voltar ao login",
                href="/",
                color="#684638",
                size="2",
                align_self="center",
            ),
            spacing="4",
            align="stretch",
            width="80%",
            max_width="400px",
        )
    )


def alterar_senha() -> rx.Component:
    return painel_autenticacao(
        rx.vstack(
            rx.heading(
                "Alterar senha",
                size="6",
                color="#3E4149",
            ),
            rx.text(
                "Preencha os campos para alterar sua senha.",
                size="3",
                color="#5E5A55",
            ),
            rx.input(
                placeholder="Senha atual",
                type="password",
                width="100%",
                radius="large",
            ),
            rx.input(
                placeholder="Nova senha",
                type="password",
                width="100%",
                radius="large",
            ),
            rx.input(
                placeholder="Confirme a nova senha",
                type="password",
                width="100%",
                radius="large",
            ),
            rx.button(
                "Salvar nova senha",
                on_click=LoginState.avisar_alteracao_visual,
                width="100%",
                background="#D78A45",
                color="white",
                radius="large",
            ),
            rx.text(
                "Esta tela é apenas visual. Nenhuma senha será alterada.",
                size="1",
                color="#766A62",
            ),
            rx.link(
                "Voltar ao login",
                href="/",
                color="#684638",
                size="2",
                align_self="center",
            ),
            spacing="4",
            align="stretch",
            width="80%",
            max_width="400px",
        )
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
                    "Sair",
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


def cartao_tutor(
    icone: str,
    titulo: str,
    texto: str,
    rota: str = "",
) -> rx.Component:
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
        on_click=rx.redirect(rota) if rota else None,
        cursor="pointer" if rota else "default",
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
                    background="#684638",
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

            # Cartões de navegação atualizados com as rotas
            rx.grid(
                cartao_tutor(
                    "heart",
                    "Minhas adoções",
                    "Espaço destinado às informações sobre suas adoções.",
                    "/minhas-adocoes",
                ),
                cartao_tutor(
                    "calendar-check",
                    "Acompanhamento",
                    "Espaço destinado ao acompanhamento pós-adoção.",
                    "/acompanhamento",
                ),
                cartao_tutor(
                    "user-round",
                    "Meus dados",
                    "Espaço destinado às informações do tutor.",
                    "/meus-dados",
                ),
                cartao_tutor(
                    "book-open",
                    "Orientações",
                    "Espaço destinado a orientações sobre adoção responsável.",
                    "/orientacoes",
                ),
                columns={"initial": "1", "sm": "2", "lg": "4"},
                spacing="4",
                width="100%",
            ),

            # Mensagem durante o carregamento
            rx.cond(
                LoginState.carregando_adocoes,
                rx.text("Carregando adoções..."),
                rx.fragment(),
            ),

            # Mensagem de erro, caso ocorra
            rx.cond(
                LoginState.erro_adocoes != "",
                rx.text(
                    LoginState.erro_adocoes,
                    color="red",
                ),
                rx.fragment(),
            ),

            # Lista dos processos de adoção
            rx.cond(
                LoginState.adocoes.length() > 0,
                rx.vstack(
                    rx.heading(
                        "Minhas adoções",
                        size="4",
                        color="#3E4149",
                    ),
                    rx.foreach(
                        LoginState.adocoes,
                        lambda adocao: rx.box(
                            rx.vstack(
                                rx.text(
                                    "Processo: ",
                                    adocao["id"],
                                ),
                                rx.text(
                                    "Animal: ",
                                    adocao["animal_id"],
                                ),
                                rx.text(
                                    "Data da solicitação: ",
                                    adocao["data_solicitacao"],
                                ),
                                rx.text(
                                    "Status: ",
                                    adocao["status_processo"],
                                ),
                                align="start",
                                spacing="2",
                            ),
                            padding="16px",
                            background="#FFFFFF",
                            border_radius="12px",
                            width="100%",
                        ),
                    ),
                    width="100%",
                    spacing="3",
                ),
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


def pagina_minhas_adocoes() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(
                    "Minhas adoções",
                    size="7",
                    color="#3E4149",
                ),
                rx.spacer(),
                               rx.link(
                    rx.button(
                        "Voltar",
                        background="#684638",
                        color="#FFFFFF",
                    ),
                    href="/tutor",
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                "Consulte suas solicitações de adoção e acompanhe "
                "o andamento de cada processo.",
                color="#5E5A55",
                size="3",
            ),
            rx.button(
                "Consultar minhas adoções",
                on_click=LoginState.carregar_adocoes,
                background="#D78A45",
                color="#FFFFFF",
                radius="large",
            ),
            rx.cond(
                LoginState.carregando_adocoes,
                rx.text("Carregando adoções..."),
                rx.fragment(),
            ),
            rx.cond(
                LoginState.erro_adocoes != "",
                rx.text(
                    LoginState.erro_adocoes,
                    color="red",
                ),
                rx.fragment(),
            ),
            rx.cond(
                LoginState.adocoes.length() > 0,
                rx.vstack(
                    rx.foreach(
                        LoginState.adocoes,
                        lambda adocao: rx.box(
                            rx.vstack(
                                rx.text(
                                    "Processo: ",
                                    adocao["id"],
                                ),
                                rx.text(
                                    "Animal: ",
                                    adocao["animal_id"],
                                ),
                                rx.text(
                                    "Data da solicitação: ",
                                    adocao["data_solicitacao"],
                                ),
                                rx.hstack(
                                    rx.text(
                                        "Status:",
                                        weight="bold",
                                        color="#3E4149",
                                    ),
                                    rx.badge(
                                        adocao["status_processo"],
                                        color_scheme="orange",
                                    ),
                                    align="center",
                                    spacing="2",
                                ),
                                align="start",
                                spacing="2",
                            ),
                            padding="16px",
                            background="#FFFFFF",
                            border_radius="12px",
                            width="100%",
                        ),
                    ),
                    width="100%",
                    spacing="3",
                ),
                rx.fragment(),
            ),
            align="start",
            spacing="4",
            width="100%",
            max_width="900px",
            margin="0 auto",
            padding="32px",
        ),
        width="100%",
        min_height="100vh",
        background="#FFF7ED",
    )


def pagina_acompanhamento() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Cabeçalho da Página
            rx.hstack(
                rx.heading("Acompanhamento Pós-Adoção", size="7", color="#3E4149"),
                rx.spacer(),
                rx.link(
                    rx.button("Voltar", background="#684638", color="#FFFFFF"),
                    href="/tutor",
                ),
                width="100%",
                align="center",
            ),

            # Explicação Simples e Direta dos Processos
            rx.box(
                rx.vstack(
                    rx.badge("Como Funciona", bg="#D78A45", color="white", radius="full"),
                    rx.heading(
                        "O que esperar do Acompanhamento Pós-Adoção?",
                        size="5",
                        color="#3E4149",
                    ),
                    rx.text(
                        "O acompanhamento pós-adoção garante que você e seu novo pet tenham uma transição tranquila e segura. Durante este período, você passará pelos seguintes processos:",
                        color="#5E5A55",
                        size="3",
                    ),
                    rx.vstack(
                        rx.text(
                            "• Adaptação Inicial: Acompanhamento da rotina, alimentação e comportamento do animal nos primeiros dias no novo lar.",
                            color="#5E5A55",
                        ),
                        rx.text(
                            "• Contato e Visitas: Contatos periódicos da equipe para recebimento de fotos, vídeos ou realização de visitas preventivas de rotina.",
                            color="#5E5A55",
                        ),
                        rx.text(
                            "• Suporte Continuado: Orientação sobre saúde (vacinação, vermifugação e castração) e apoio para eventuais dúvidas de comportamento.",
                            color="#5E5A55",
                        ),
                        rx.text(
                            "• Conclusão da Adaptação: Finalização do acompanhamento oficial assim que o pet estiver completamente integrado à família.",
                            color="#5E5A55",
                        ),
                        align="start",
                        spacing="2",
                        padding_left="8px",
                    ),
                    spacing="3",
                    align="start",
                ),
                padding="24px",
                background="#F4E7D5",
                border_radius="16px",
                border_left="6px solid #D78A45",
                width="100%",
            ),

            rx.divider(border_color="#D78A45", opacity="0.3", margin_y="8px"),

            # Botão e Lista de Registros
            rx.hstack(
                rx.heading("Seus Registros de Acompanhamento", size="5", color="#3E4149"),
                rx.spacer(),
                rx.button(
                    "Consultar Acompanhamento",
                    on_click=LoginState.carregar_acompanhamentos,
                    background="#D78A45",
                    color="#FFFFFF",
                    radius="large",
                ),
                width="100%",
                align="center",
            ),

            rx.cond(
                LoginState.carregando_acompanhamentos,
                rx.text("Carregando acompanhamentos..."),
                rx.fragment(),
            ),
            rx.cond(
                LoginState.erro_acompanhamentos != "",
                rx.text(LoginState.erro_acompanhamentos, color="red"),
                rx.fragment(),
            ),
            rx.cond(
                LoginState.acompanhamentos.length() > 0,
                rx.vstack(
                    rx.foreach(
                        LoginState.acompanhamentos,
                        lambda item: rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.badge("Acompanhamento Pós-Adoção", color_scheme="orange"),
                                    rx.spacer(),
                                    rx.text("Data: ", item["data_visita"], size="2", color="#766A62"),
                                    width="100%",
                                    align="center",
                                ),
                                rx.text("Processo de Adoção vinculante nº: ", item["processo_adocao_id"], color="#3E4149"),
                                rx.text("Relatório / Observação: ", item["observacao"], color="#5E5A55"),
                                align="start",
                                spacing="2",
                            ),
                            padding="16px",
                            background="#FFFFFF",
                            border_radius="12px",
                            width="100%",
                            box_shadow="0 2px 8px rgba(62, 65, 73, 0.05)",
                        ),
                    ),
                    width="100%",
                    spacing="3",
                ),
                rx.box(
                    rx.text(
                        "Nenhum registro de acompanhamento pós-adoção encontrado até o momento.",
                        color="#5E5A55",
                        font_style="italic",
                    ),
                    padding="16px",
                    background="#FFFFFF",
                    border_radius="12px",
                    width="100%",
                ),
            ),
            align="start",
            spacing="4",
            width="100%",
            max_width="900px",
            margin="0 auto",
            padding="32px",
        ),
        width="100%",
        min_height="100vh",
        background="#FFF7ED",
    )


def pagina_meus_dados() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Meus Dados", size="7", color="#3E4149"),
                rx.spacer(),
                rx.link(
                    rx.button("Voltar", background="#684638", color="#FFFFFF"),
                    href="/tutor",
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                "Confira suas informações cadastradas no sistema.",
                color="#5E5A55",
                size="3",
            ),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.text("Nome / Identificação: ", weight="bold", color="#3E4149"),
                        rx.text(LoginState.nome_usuario, color="#5E5A55"),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("E-mail de Cadastro: ", weight="bold", color="#3E4149"),
                        rx.text(LoginState.email, color="#5E5A55"),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.text("Perfil de Acesso: ", weight="bold", color="#3E4149"),
                        rx.badge("Tutor / Adotante", color_scheme="orange"),
                        spacing="2",
                    ),
                    align="start",
                    spacing="3",
                    width="100%",
                ),
                padding="24px",
                background="#FFFFFF",
                border_radius="16px",
                width="100%",
                box_shadow="0 2px 8px rgba(62, 65, 73, 0.05)",
            ),
            align="start",
            spacing="4",
            width="100%",
            max_width="900px",
            margin="0 auto",
            padding="32px",
        ),
        width="100%",
        min_height="100vh",
        background="#FFF7ED",
    )


def pagina_orientacoes() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Orientações ao Tutor", size="7", color="#3E4149"),
                rx.spacer(),
                rx.link(
                    rx.button("Voltar", background="#684638", color="#FFFFFF"),
                    href="/tutor",
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                "Dicas e orientações fundamentais para garantir a saúde e a felicidade do seu pet.",
                color="#5E5A55",
                size="3",
            ),
            rx.vstack(
                rx.box(
                    rx.vstack(
                        rx.heading("🏠 Adaptação nos primeiros dias", size="4", color="#3E4149"),
                        rx.text(
                            "Proporcione um ambiente calmo e seguro. Deixe o pet explorar a casa no próprio tempo dele.",
                            color="#5E5A55",
                            size="2",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    padding="20px",
                    background="#FFFFFF",
                    border_radius="12px",
                    width="100%",
                    box_shadow="0 2px 8px rgba(62, 65, 73, 0.05)",
                ),
                rx.box(
                    rx.vstack(
                        rx.heading("💉 Saúde e Vacinação", size="4", color="#3E4149"),
                        rx.text(
                            "Mantenha a carteira de vacinação e a desvermifugação atualizadas de acordo com a orientação veterinária.",
                            color="#5E5A55",
                            size="2",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    padding="20px",
                    background="#FFFFFF",
                    border_radius="12px",
                    width="100%",
                    box_shadow="0 2px 8px rgba(62, 65, 73, 0.05)",
                ),
                rx.box(
                    rx.vstack(
                        rx.heading("📋 Acompanhamento Pós-Adoção", size="4", color="#3E4149"),
                        rx.text(
                            "A equipe da ONG poderá realizar contatos periódicos para saber como o animal está se adaptando à nova família.",
                            color="#5E5A55",
                            size="2",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    padding="20px",
                    background="#FFFFFF",
                    border_radius="12px",
                    width="100%",
                    box_shadow="0 2px 8px rgba(62, 65, 73, 0.05)",
                ),
                spacing="3",
                width="100%",
            ),
            align="start",
            spacing="4",
            width="100%",
            max_width="900px",
            margin="0 auto",
            padding="32px",
        ),
        width="100%",
        min_height="100vh",
        background="#FFF7ED",
    )



app = rx.App()
app.add_page(index)
app.add_page(
    recuperar_senha,
    route="/recuperar-senha",
)
app.add_page(
    alterar_senha,
    route="/alterar-senha",
)
app.add_page(
    area_administrativa,
    route="/administrativo",
)
app.add_page(
    area_tutor,
    route="/tutor",
)

app.add_page(
    pagina_minhas_adocoes,
    route="/minhas-adocoes",
)

app.add_page(
    pagina_acompanhamento, 
    route="/acompanhamento"
)
app.add_page(
    pagina_meus_dados, 
    route="/meus-dados"
)
app.add_page(
    pagina_orientacoes, 
    route="/orientacoes"
)