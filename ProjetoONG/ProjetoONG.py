import os
import httpx
import asyncio
import reflex as rx
from dotenv import load_dotenv
from ProjetoONG.gestao_animal import gestao_animal
load_dotenv()

# URLs de integração com a API do Xano
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
XANO_TUTOR_UPDATE_URL="https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/tutor_adotante"


# ==============================================================================
# ESTADO GLOBAL DA APLICAÇÃO (LOGIN, SESSÃO E REQUISIÇÕES)
# ==============================================================================
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

    # Carrossel da tela de login
    fotos_carrossel: list[str] = [
        "https://images.unsplash.com/photo-1543466835-00a7907e9de1?q=80&w=1000",
        "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?q=80&w=1000",
        "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?q=80&w=1000",
    ]
    indice_foto: int = 0

    # Variáveis de Estado para Edição do Tutor
    tutor_id: str = ""
    novo_nome: str = ""
    novo_cpf: str = ""
    novo_telefone: str = ""
    novo_tipo_residencia: str = ""
    novo_endereco: str = ""
    salvando_dados: bool = False

    @rx.event
    def set_novo_nome(self, valor: str):
        self.novo_nome = valor

    @rx.event
    def set_novo_cpf(self, valor: str):
        self.novo_cpf = valor

    @rx.event
    def set_novo_telefone(self, valor: str):
        self.novo_telefone = valor

    @rx.event
    def set_novo_tipo_residencia(self, valor: str):
        self.novo_tipo_residencia = valor

    @rx.event
    def set_novo_endereco(self, valor: str):
        self.novo_endereco = valor

    @rx.event
    def proxima_foto(self):
        self.indice_foto = (self.indice_foto + 1) % len(self.fotos_carrossel)

    @rx.event
    def foto_anterior(self):
        self.indice_foto = (self.indice_foto - 1) % len(self.fotos_carrossel)

    @rx.event(background=True)
    async def iniciar_carrossel_automatico(self):
        while True:
            await asyncio.sleep(4)
            async with self:
                self.indice_foto = (self.indice_foto + 1) % len(self.fotos_carrossel)

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
                    headers={"Authorization": f"Bearer {self.token}"},
                )

            if resposta.status_code != 200:
                self.erro_adocoes = "Não foi possível consultar suas adoções."
                return

            dados = resposta.json()
            if isinstance(dados, dict):
                dados = dados.get("items", [])

            if not isinstance(dados, list):
                self.erro_adocoes = "O servidor retornou dados em formato inesperado."
                return

            self.adocoes = [
                {
                    "id": str(item.get("id", "")),
                    "data_solicitacao": str(item.get("data_solicitacao", "")),
                    "status_processo": str(item.get("status_processo", "")),
                    "animal_id": str(item.get("animal_id", "")),
                    "nome_animal": str((item.get("_animal") or item.get("animal") or {}).get("nome") or item.get("nome_animal") or ""),
                }
                for item in dados
                if isinstance(item, dict)
            ]

        except httpx.RequestError:
            self.erro_adocoes = "Falha de conexão ao consultar suas adoções."
        except ValueError:
            self.erro_adocoes = "O servidor retornou uma resposta inválida."
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
        return rx.toast("Nenhuma solicitação foi enviada. A integração ainda não está implementada.")

    @rx.event
    def avisar_alteracao_visual(self):
        return rx.toast("Nenhuma senha foi alterada. A integração ainda não está implementada.")

    @rx.event
    async def validar_login(self):
        if not self.email.strip() or not self.senha:
            return rx.toast("Preencha o e-mail e a senha.")

        if not XANO_LOGIN_URL or not XANO_ME_URL:
            return rx.toast("A conexão com o servidor não está configurada.")

        etapa = "login"

        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta = await cliente.post(
                    XANO_LOGIN_URL,
                    json={"email": self.email.strip(), "password": self.senha},
                )

                if resposta.status_code in (401, 403):
                    return rx.toast("E-mail ou senha inválidos.")

                if resposta.status_code != 200:
                    try:
                        erro_login = resposta.json()
                    except ValueError:
                        erro_login = {}

                    if isinstance(erro_login, dict) and erro_login.get("message") == "Invalid Credentials.":
                        return rx.toast("E-mail ou senha inválidos.")

                    return rx.toast("O servidor não conseguiu realizar o login.")

                try:
                    dados = resposta.json()
                except ValueError:
                    return rx.toast("Resposta inválida do servidor.")

                token = dados.get("authToken")
                if not token:
                    return rx.toast("O servidor não retornou o token de acesso.")

                etapa = "consulta do usuário"
                resposta_usuario = await cliente.get(
                    XANO_ME_URL,
                    headers={"Authorization": f"Bearer {token}"},
                )

                if resposta_usuario.status_code != 200:
                    return rx.toast("Não foi possível confirmar o usuário autenticado.")

                try:
                    usuario = resposta_usuario.json()
                    tutor_dados = usuario.get("_tutor_adotante_of_usuario") or {}
                    self.nome_usuario = tutor_dados.get("nome", "")
                    self.tutor_id = str(tutor_dados.get("id", ""))  # <--- Captura o ID da tabela tutor_adotante
                    self.novo_nome = self.nome_usuario  # Inicializa o campo de edição com o nome atual
                    self.novo_cpf = tutor_dados.get("cpf", "")
                    self.novo_telefone = tutor_dados.get("telefone", "")
                    self.novo_tipo_residencia = tutor_dados.get("tipo_residencia", "")
                    self.novo_endereco = tutor_dados.get("endereco", "")
                except ValueError:
                    return rx.toast("Resposta inválida ao consultar o usuário.")

                tipo_usuario = usuario.get("tipo_usuario")
                if not isinstance(tipo_usuario, str):
                    return rx.toast("Tipo de usuário não reconhecido.")

                tipo_usuario = tipo_usuario.strip().lower()

                if tipo_usuario == "administrador":
                    self.token = token
                    self.tipo_usuario = tipo_usuario
                    return rx.redirect("/administrativo")

                if tipo_usuario == "tutor/adotante":
                    self.token = token
                    self.tipo_usuario = tipo_usuario
                    return rx.redirect("/tutor")

                return rx.toast("Tipo de usuário não reconhecido.")

        except httpx.RequestError as erro:
            return rx.toast(f"Falha de conexão durante {etapa}.")

    @rx.event
    def sair(self):
        """Limpa os dados locais da sessão e retorna à tela de login."""
        self.token = ""
        self.tipo_usuario = ""
        self.email = ""
        self.senha = ""
        self.indice_foto = 0
        self.tela_atual = "inicio"
        return rx.redirect("/")

    @rx.event
    async def salvar_dados_tutor(self):
        if not self.token:
            return rx.toast("Sessão expirada. Faça login novamente.")

        if not self.tutor_id:
            return rx.toast("ID do tutor não encontrado para atualização.")

        if not self.novo_nome.strip():
            return rx.toast("O nome não pode ficar em branco.")

        self.salvando_dados = True

        url_base = os.getenv(
            "XANO_TUTOR_UPDATE_URL", 
            "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/tutor_adotante"
        )

        # Trata a URL para garantir a formação correta com o ID (ex: .../tutor_adotante/1)
        if "{tutor_adotante_id}" in url_base:
            url_final = url_base.replace("{tutor_adotante_id}", str(self.tutor_id))
        else:
            url_final = f"{url_base.rstrip('/')}/{self.tutor_id}"

        try:
            corpo = {
                "nome": self.novo_nome.strip(),
                "cpf": self.novo_cpf.strip(),
                "telefone": self.novo_telefone.strip(),
                "tipo_residencia": self.novo_tipo_residencia.strip(),
                "endereco": self.novo_endereco.strip(),
            }

            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta = await cliente.patch(
                    url_final,
                    json=corpo,
                    headers={"Authorization": f"Bearer {self.token}"},
                )

            print(f"--- DIAGNÓSTICO XANO ---")
            print(f"URL Chamada: {url_final}")
            print(f"Status Code: {resposta.status_code}")
            print(f"Resposta Xano: {resposta.text}")
            print(f"------------------------")

            if resposta.status_code in (200, 201):
                self.nome_usuario = self.novo_nome.strip()
                self.salvando_dados = False
                return rx.toast("Dados atualizados com sucesso no Xano!")
            else:
                self.salvando_dados = False
                return rx.toast(f"Não foi possível atualizar os dados ({resposta.status_code}).")

        except httpx.RequestError:
            self.salvando_dados = False
            return rx.toast("Falha de conexão ao salvar alterações.")

# ==============================================================================
# TELA DE LOGIN / INDEX
# ==============================================================================
def index() -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.image(
                src=LoginState.fotos_carrossel[LoginState.indice_foto],
                width="100%", height="100%", object_fit="cover",
                position="absolute", top="0", left="0",
            ),
            rx.box(
                position="absolute", top="0", left="0",
                width="100%", height="100%", background="rgba(0, 0, 0, 0.4)",
            ),
            rx.vstack(
                rx.text("🐾", font_size="3em"),
                rx.heading("Porto Seguro Pet", color="white", size="8"),
                rx.text("Cuidando de vidas, construindo novos começos.", color="white", size="4", text_align="center"),
                align="center", justify="center", height="100%",
                position="relative", z_index="2", padding="20px",
            ),
            position="relative", width=["0%", "0%", "50%"], height="100vh",
            overflow="hidden", display=["none", "none", "block"],
        ),
        rx.center(
            rx.vstack(
                rx.heading("Olá! Que bom ter você aqui!", size="6", color="#3E4149", text_align="center"),
                rx.text("Faça seu login para continuar.", size="3", color="#5E5A55", text_align="center"),
                rx.input(placeholder="E-mail", type="email", on_change=LoginState.set_email, width="50%", radius="large"),
                rx.input(placeholder="Senha", type="password", on_change=LoginState.set_senha, width="50%", radius="large"),
                rx.button("Entrar", on_click=LoginState.validar_login, width="50%", background="#D78A45", color="white", radius="large"),
                spacing="4", align="center", width="80%", max_width="380px", padding="30px",
                background="rgba(255, 247, 237, 0.50)", border_radius="20px", box_shadow="0 8px 30px rgba(0,0,0,0.05)",
            ),
            width=["100%", "100%", "50%"], height="100vh", background_color="#FFF7ED",
            background_image="url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 100 100' fill='%23D78A45' opacity='0.12'%3E%3Cpath d='M30 50c-6 0-10 6-10 12 0 8 10 18 20 18s20-10 20-18c0-6-4-12-10-12s-8 3-10 3-4-3-10-3zm-12-8c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18-12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm24 0c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18 12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8z'/%3E%3C/svg%3E\")",
            background_repeat="repeat",
        ),
        width="100%", height="100vh", spacing="0", padding="0", margin="0",
    )


def painel_autenticacao(conteudo: rx.Component) -> rx.Component:
    return rx.hstack(
        rx.center(
            rx.vstack(
                rx.text("🐾", size="9"),
                rx.heading("Porto Seguro Pet", size="8", color="#3E4149"),
                rx.text("Cuidando de vidas, construindo novos começos.", size="4", color="#3E4149", text_align="center"),
                spacing="4", align="center", max_width="440px", padding="8",
            ),
            width="50%", height="100vh", background="#F4E7D5",
        ),
        rx.center(conteudo, width="50%", height="100vh", background="#FFF7ED"),
        width="100%", height="100vh", spacing="0", align="stretch",
    )


def recuperar_senha() -> rx.Component:
    return painel_autenticacao(
        rx.vstack(
            rx.heading("Recuperar senha", size="6", color="#3E4149"),
            rx.text("Informe o e-mail cadastrado na sua conta.", size="3", color="#5E5A55"),
            rx.input(placeholder="E-mail", type="email", width="100%", radius="large"),
            rx.button("Solicitar recuperação", on_click=LoginState.avisar_recuperacao_visual, width="100%", background="#D78A45", color="white", radius="large"),
            rx.text("Esta tela é apenas visual. Nenhuma solicitação será enviada.", size="1", color="#766A62"),
            rx.link("Voltar ao login", href="/", color="#684638", size="2", align_self="center"),
            spacing="4", align="stretch", width="80%", max_width="400px",
        )
    )


def alterar_senha() -> rx.Component:
    return painel_autenticacao(
        rx.vstack(
            rx.heading("Alterar senha", size="6", color="#3E4149"),
            rx.text("Preencha os campos para alterar sua senha.", size="3", color="#5E5A55"),
            rx.input(placeholder="Senha atual", type="password", width="100%", radius="large"),
            rx.input(placeholder="Nova senha", type="password", width="100%", radius="large"),
            rx.input(placeholder="Confirme a nova senha", type="password", width="100%", radius="large"),
            rx.button("Salvar nova senha", on_click=LoginState.avisar_alteracao_visual, width="100%", background="#D78A45", color="white", radius="large"),
            rx.text("Esta tela é apenas visual. Nenhuma senha será alterada.", size="1", color="#766A62"),
            rx.link("Voltar ao login", href="/", color="#684638", size="2", align_self="center"),
            spacing="4", align="stretch", width="80%", max_width="400px",
        )
    )


# ==============================================================================
# ÁREA ADMINISTRATIVA ORIGINAL (INTACTA E PRESERVADA)
# ==============================================================================
def item_menu(icone: str, texto: str, tela: str = "") -> rx.Component:
    ativo = LoginState.tela_atual == tela
    return rx.hstack(
        rx.icon(icone, size=18, color=rx.cond(ativo, "#684638", "#766A62")),
        rx.text(texto, size="2", weight=rx.cond(ativo, "bold", "medium"), color=rx.cond(ativo, "#342D29", "#5E5A55")),
        spacing="3", align="center", width="100%", padding="10px 12px", border_radius="10px",
        cursor="pointer", background=rx.cond(ativo, "#FFFFFF", "transparent"),
        box_shadow=rx.cond(ativo, "0 1px 3px rgba(104, 70, 56, 0.15)", "none"),
        transition="background 0.15s ease", _hover={"background": "rgba(255, 255, 255, 0.65)"},
        on_click=LoginState.set_tela(tela) if tela else None,
    )


def titulo_secao_menu(texto: str) -> rx.Component:
    return rx.text(
        texto, size="1", weight="bold", color="#9A8C82",
        letter_spacing="0.08em", padding="14px 12px 4px 12px",
    )


def menu_lateral() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.center(
                rx.icon("paw-print", size=22, color="white"),
                background="#684638", border_radius="12px", width="42px", height="42px", flex_shrink="0",
            ),
            rx.vstack(
                rx.text("Porto Seguro Pet", size="4", weight="bold", color="#342D29"),
                rx.text("Painel administrativo", size="1", color="#766A62"),
                spacing="0", align="start",
            ),
            spacing="3", align="center", padding="4px 4px 16px 4px", width="100%",
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
        spacing="1", align="stretch", width="280px", min_width="280px",
        height="100vh", padding="24px 16px", background="#F4E7D5",
        border_right="1px solid #EAE1D7", overflow_y="auto",
    )


def area_administrativa() -> rx.Component:
    return rx.hstack(
        menu_lateral(),
        rx.vstack(
            rx.hstack(
                rx.spacer(),
                rx.button("Sair", on_click=LoginState.sair, color="#FFFFFF", background="#684638"),
                width="100%", align="center", padding="20px 24px",
            ),
            rx.box(
                rx.cond(
                    LoginState.tela_atual == "animais",
                    gestao_animal(LoginState.token),
                    rx.vstack(
                        rx.text("Bem-vindo à área administrativa!", size="8", weight="bold", color="#3E4149"),
                        rx.text("Proteção, cuidado e novas oportunidades.", size="4", color="#6D896F"),
                        rx.box(
                            rx.vstack(
                                rx.heading("Quem somos", size="5", color="#3E4149"),
                                rx.text("Somos uma organização dedicada à proteção e ao cuidado dos animais, acompanhando sua trajetória do resgate à adoção responsável.", size="3", color="#5E5A55"),
                                spacing="3", align="start", width="100%",
                            ),
                            background="#FFFFFF", padding="24px", border_radius="16px", width="100%", box_shadow="0 2px 10px rgba(62, 65, 73, 0.08)",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.heading("Nossa missão", size="5", color="#3E4149"),
                                rx.text("Promover o bem-estar animal por meio do resgate, dos cuidados necessários, do acolhimento temporário e da busca por lares responsáveis.", size="3", color="#5E5A55"),
                                spacing="3", align="start", width="100%",
                            ),
                            background="#FFFFFF", padding="24px", border_radius="16px", width="100%", box_shadow="0 2px 10px rgba(62, 65, 73, 0.08)",
                        ),
                        spacing="5", align="center", justify="center", width="100%", max_width="760px", min_height="60vh", margin="0 auto", padding="24px",
                    ),
                ),
                width="100%", flex="1",
            ),
            spacing="0", align="stretch", flex="1", min_width="0", min_height="100vh", background="#FAF6F0",
        ),
    )


# ==============================================================================
# ÁREA DO TUTOR 
# ==============================================================================
def cartao_tutor(icone: str, titulo: str, texto: str, rota: str = "") -> rx.Component:
    return rx.link(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon(tag=icone, size=22, color="#D78A45"),
                        background="#FFF3E0", padding="8px", border_radius="10px",
                    ),
                    rx.icon(tag="arrow-right", size=16, color="#C5C5C5"),
                    justify="between", align="center", width="100%",
                ),
                rx.heading(titulo, size="3", color="#2D3142", weight="bold"),
                rx.text(texto, size="1", color="#7A756E"),
                align="start", spacing="2",
            ),
            padding="16px", background="rgba(255, 255, 255, 0.95)",
            border_radius="16px", border="1px solid rgba(215, 138, 69, 0.2)",
            box_shadow="0 4px 15px rgba(0,0,0,0.03)", cursor="pointer",
            transition="all 0.2s ease",
            _hover={"transform": "translateY(-4px)", "border_color": "#D78A45"},
            height="100%",
        ),
        href=rota, style={"text_decoration": "none", "width": "100%"},
    )


def area_tutor() -> rx.Component:
    return rx.box(
        rx.vstack(
            # 1. BARRA SUPERIOR (HEADER)
            rx.box(
                rx.hstack(
                    rx.hstack(
                        rx.box(
                            rx.text("🐾", font_size="1.4em"),
                            background="#FFF3E0", padding="8px", border_radius="12px",
                        ),
                        rx.heading("Porto Seguro Pet", size="5", color="#2D3142", weight="bold"),
                        spacing="3", align="center",
                    ),
                   
                   # Status do usuário + Botão "Sair" Animado e Colorido
                    rx.hstack(
                        rx.link(
                            rx.hstack(
                                rx.text("Sair", font_size="1.15em", font_weight="bold"),
                                rx.icon(tag="arrow-right", size=20),
                                spacing="2",
                                align="center",
                            ),
                            on_click=LoginState.sair,
                            color="#8C4A32",
                            transition="all 0.2s ease",
                            cursor="pointer",
                            _hover={
                                "color": "#D78A45",
                                "transform": "translateX(4px)",
                                "text_decoration": "none",
                            },
                        ),
                        spacing="4",
                        align="center",
                    ),
                    justify="between", align="center", max_width="1100px", margin="0 auto", width="100%",
                ),
                width="100%", padding="16px 24px", background="rgba(255, 255, 255, 0.95)",
                backdrop_filter="blur(12px)", border_bottom="1px solid rgba(215, 138, 69, 0.15)",
                position="sticky", top="0", z_index="1000",
            ),

            # 2. BANNER COMPACTO
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.badge("✨ PAINEL DO TUTOR", color_scheme="orange", variant="soft", radius="full", padding_x="12px"),
                        rx.heading("Um novo começo começa com amor.", size="6", color="#2D3142", weight="bold"),
                        rx.text("Confira o status das suas adoções e gerencie suas informações pessoais.", color="#5E5A55", size="2"),
                        align="start", spacing="2",
                    ),
                    rx.text("🐶 🐱", font_size="3em"),
                    justify="between", align="center", width="100%",
                ),
                width="100%", max_width="1100px", margin="0 auto", padding="24px 32px",
                background="linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255, 243, 224, 0.9) 100%)",
                backdrop_filter="blur(8px)", border_radius="24px",
                border="1px solid rgba(215, 138, 69, 0.25)", box_shadow="0 8px 25px -10px rgba(215, 138, 69, 0.12)",
            ),

            # 3. CONTEÚDO PRINCIPAL (ESTRUTURA DE 2 COLUNAS)
            rx.grid(
                # COLUNA ESQUERDA: Meus Dados + 2 Cards
                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.hstack(
                                    rx.icon(tag="user-round", size=20, color="#D78A45"),
                                    rx.heading("Meus Dados", size="4", color="#2D3142"),
                                    spacing="2", align="center",
                                ),
                                rx.link(
                                    rx.button("Editar / Ver mais", variant="soft", color_scheme="orange", size="1", radius="full"),
                                    href="/meus-dados",
                                ),
                                justify="between", align="center", width="100%",
                            ),
                            rx.divider(margin_y="8px"),
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Nome: ", font_weight="bold", size="2", color="#2D3142"),
                                    rx.cond(
                                        LoginState.nome_usuario != "",
                                        rx.text(LoginState.nome_usuario, size="2", color="#5E5A55"),
                                        rx.text("Usuário Tutor", size="2", color="#5E5A55"),
                                    ),
                                ),
                                rx.hstack(
                                    rx.text("E-mail: ", font_weight="bold", size="2", color="#2D3142"),
                                    rx.text(LoginState.email, size="2", color="#5E5A55"),
                                ),
                                rx.hstack(
                                    rx.text("Perfil: ", font_weight="bold", size="2", color="#2D3142"),
                                    rx.badge("Tutor / Adotante", color_scheme="orange"),
                                ),
                                align="start", spacing="2", width="100%",
                            ),
                            align="start", spacing="2", width="100%",
                        ),
                        padding="20px", background="rgba(255, 255, 255, 0.95)",
                        border_radius="20px", border="1px solid rgba(215, 138, 69, 0.2)",
                        box_shadow="0 4px 15px rgba(0,0,0,0.03)", width="100%",
                    ),
                    rx.heading("Serviços e Orientações", size="4", color="#2D3142", margin_top="12px"),
                    rx.grid(
                        cartao_tutor("calendar-check", "Acompanhamento", "Histórico de pós-adoção.", "/acompanhamento"),
                        cartao_tutor("book-open", "Orientações", "Guias para guarda responsável.", "/orientacoes"),
                        columns={"initial": "1", "sm": "2"}, spacing="3", width="100%",
                    ),
                    spacing="4", width="100%",
                ),

                # COLUNA DIREITA: Minhas Adoções com Nome do Animal e Indicador Visual
                rx.vstack(
                    rx.hstack(
                        rx.heading("Minhas Adoções", size="4", color="#2D3142"),
                        rx.button(
                            rx.icon(tag="refresh-cw", size=14),
                            on_click=LoginState.carregar_adocoes,
                            variant="ghost", color="#D78A45", size="1",
                        ),
                        justify="between", align="center", width="100%",
                    ),
                    rx.cond(
                        LoginState.carregando_adocoes,
                        rx.text("Buscando suas adoções no Xano...", color="#7A756E", size="2"),
                        rx.fragment(),
                    ),
                    rx.cond(
                        LoginState.erro_adocoes != "",
                        rx.text(LoginState.erro_adocoes, color="red", size="2"),
                        rx.fragment(),
                    ),
                    rx.cond(
                        LoginState.adocoes.length() > 0,
                        rx.foreach(
                            LoginState.adocoes,
                            lambda adocao: rx.box(
                                rx.vstack(
                                    # Cabeçalho do Card: Ícone + Nome do Animal + ID
                                    rx.vstack(
                                        rx.heading(
                                            rx.cond(
                                                adocao["nome_animal"],
                                                adocao["nome_animal"],
                                                rx.cond(
                                                    adocao["animal_id"],
                                                    "Animal #" + adocao["animal_id"].to_string(),
                                                    "Pet em Processo",
                                                ),
                                            ),
                                            size="3",
                                            color="#2D3142",
                                            weight="bold",
                                        ),
                                        rx.text(
                                            "Processo #" + adocao["id"].to_string() + " | Solicitação: " + adocao["data_solicitacao"],
                                            size="1",
                                            color="#7A756E",
                                        ),
                                        spacing="0",
                                        align="start",
                                    ),
                                    
                                    rx.divider(margin_y="8px", border_color="rgba(215, 138, 69, 0.15)"),

                                    # INDICADOR VISUAL DE PROGRESSO (BARRA COM PASSOS)
                                    rx.box(
                                        rx.hstack(
                                            # Passo 1: Análise
                                            rx.vstack(
                                                rx.box(
                                                    rx.text("1", font_size="0.75em", font_weight="bold", color="white"),
                                                    width="22px", height="22px", border_radius="full",
                                                    background=rx.cond(
                                                        (adocao["status_processo"] == "Em análise") | 
                                                        (adocao["status_processo"] == "Mais informações necessárias") |
                                                        (adocao["status_processo"] == "Aprovada") |
                                                        (adocao["status_processo"] == "Adoção efetivada"),
                                                        "#D78A45", "#E2E8F0"
                                                    ),
                                                    display="flex", align_items="center", justify_content="center",
                                                ),
                                                rx.text("Análise", size="1", color="#7A756E", font_size="0.7em"),
                                                spacing="1", align="center",
                                            ),
                                            rx.box(height="2px", flex="1", background="#E2E8F0", margin_top="-12px"),
                                            
                                            # Passo 2: Decisão
                                            rx.vstack(
                                                rx.box(
                                                    rx.text("2", font_size="0.75em", font_weight="bold", color="white"),
                                                    width="22px", height="22px", border_radius="full",
                                                    background=rx.cond(
                                                        (adocao["status_processo"] == "Aprovada") | 
                                                        (adocao["status_processo"] == "Adoção efetivada"),
                                                        "#D78A45", "#E2E8F0"
                                                    ),
                                                    display="flex", align_items="center", justify_content="center",
                                                ),
                                                rx.text("Aprovação", size="1", color="#7A756E", font_size="0.7em"),
                                                spacing="1", align="center",
                                            ),
                                            rx.box(height="2px", flex="1", background="#E2E8F0", margin_top="-12px"),

                                            # Passo 3: Efetivação
                                            rx.vstack(
                                                rx.box(
                                                    rx.text("3", font_size="0.75em", font_weight="bold", color="white"),
                                                    width="22px", height="22px", border_radius="full",
                                                    background=rx.cond(
                                                        adocao["status_processo"] == "Adoção efetivada",
                                                        "#2E7D32", "#E2E8F0"
                                                    ),
                                                    display="flex", align_items="center", justify_content="center",
                                                ),
                                                rx.text("Concluído", size="1", color="#7A756E", font_size="0.7em"),
                                                spacing="1", align="center",
                                            ),
                                            width="100%", align="center", padding_x="8px",
                                        ),
                                        padding_y="6px", width="100%",
                                    ),

                                    # EXPLICAÇÃO DETALHADA POR ETAPA
                                    rx.match(
                                        adocao["status_processo"],
                                        ("Em análise", rx.box(
                                            rx.text("Etapa 1 de 3 — A sua solicitação foi registrada e está sendo avaliada pela ONG.", size="1", color="#5E5A55"),
                                            rx.text("⏳ Aguardando avaliação de compatibilidade e perfil.", size="1", color="#8C4A32", font_weight="medium"),
                                            padding="10px 14px", background="#FFF3E0", border_radius="10px", width="100%",
                                        )),
                                        ("Mais informações necessárias", rx.box(
                                            rx.text("Etapa de Análise — A ONG necessita de dados adicionais para concluir a avaliação.", size="1", color="#5E5A55"),
                                            rx.text("⚠️ Por favor, verifique o seu e-mail ou entre em contato com a ONG.", size="1", color="#D78A45", font_weight="medium"),
                                            padding="10px 14px", background="#FFF3E0", border_radius="10px", width="100%",
                                        )),
                                        ("Aprovada", rx.box(
                                            rx.text("Etapa 2 de 3 — A sua solicitação foi aprovada!", size="1", color="#2E7D32", font_weight="bold"),
                                            rx.text("🤝 A ONG entrará em contato para combinar os detalhes e a entrega do pet.", size="1", color="#5E5A55"),
                                            padding="10px 14px", background="#E8F5E9", border_radius="10px", width="100%",
                                        )),
                                        ("Adoção efetivada", rx.box(
                                            rx.text("Etapa 3 de 3 — Processo concluído com sucesso! O pet já está no seu novo lar.", size="1", color="#2E7D32", font_weight="bold"),
                                            rx.text("🎉 Adoção efetivada.", size="1", color="#2E7D32"),
                                            padding="10px 14px", background="#E8F5E9", border_radius="10px", width="100%",
                                        )),
                                        ("Não aprovada", rx.box(
                                            rx.text("Solicitação Recusada — As condições não foram consideradas compatíveis para este animal.", size="1", color="#C62828", font_weight="bold"),
                                            rx.text("❌ Processo encerrado.", size="1", color="#C62828"),
                                            padding="10px 14px", background="#FFEBEE", border_radius="10px", width="100%",
                                        )),
                                        rx.box(
                                            rx.text("O seu processo está sendo acompanhado pela equipe responsável.", size="1", color="#5E5A55"),
                                            padding="10px 14px", background="#F5F5F5", border_radius="10px", width="100%",
                                        ),
                                    ),
                                    align="start", spacing="2", width="100%",
                                ),
                                padding="18px", background="rgba(255, 255, 255, 0.95)",
                                border_radius="18px", border="1px solid rgba(215, 138, 69, 0.2)",
                                box_shadow="0 4px 15px rgba(0,0,0,0.03)", width="100%",
                            ),
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("🐶", font_size="2.2em"),
                                rx.text("Nenhuma solicitação em andamento", font_weight="bold", size="3", color="#2D3142"),
                                rx.text("Você ainda não iniciou nenhum processo de adoção.", size="2", color="#7A756E", text_align="center"),
                                align="center", spacing="2",
                            ),
                            padding="32px 20px", background="rgba(255, 255, 255, 0.8)",
                            border_radius="20px", border="1px dashed rgba(215, 138, 69, 0.4)", width="100%",
                        ),
                    ),
                    spacing="3", width="100%",
                ),
                columns={"initial": "1", "lg": "2"}, spacing="6",
                width="100%", max_width="1100px", margin="0 auto", padding_x=["20px", "28px"],
            ),

            rx.text(
                "Porto Seguro Pet — Conectando corações e patas.",
                color="#7A756E", size="1", text_align="center", width="100%", padding_y="24px",
            ),
            spacing="5", width="100%", align="stretch",
        ),
        width="100%", min_height="100vh", background_color="#FFF7ED",
        background_image="url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 100 100' fill='%23D78A45' opacity='0.10'%3E%3Cpath d='M30 50c-6 0-10 6-10 12 0 8 10 18 20 18s20-10 20-18c0-6-4-12-10-12s-8 3-10 3-4-3-10-3zm-12-8c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18-12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm24 0c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18 12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8z'/%3E%3C/svg%3E\")",
        background_repeat="repeat",
    )

# --- OUTRAS SUBPÁGINAS DO TUTOR ---
def pagina_minhas_adocoes() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Minhas adoções", size="7", color="#3E4149"),
                rx.spacer(),
                rx.link(rx.button("Voltar", background="#684638", color="#FFFFFF"), href="/tutor"),
                width="100%", align="center",
            ),
            rx.text("Consulte suas solicitações de adoção e acompanhe cada processo.", color="#5E5A55", size="3"),
            rx.button("Consultar minhas adoções", on_click=LoginState.carregar_adocoes, background="#D78A45", color="#FFFFFF", radius="large"),
            rx.cond(LoginState.carregando_adocoes, rx.text("Carregando adoções..."), rx.fragment()),
            rx.cond(LoginState.erro_adocoes != "", rx.text(LoginState.erro_adocoes, color="red"), rx.fragment()),
            rx.cond(
                LoginState.adocoes.length() > 0,
                rx.vstack(
                    rx.foreach(
                        LoginState.adocoes,
                        lambda adocao: rx.box(
                            rx.vstack(
                                rx.text("Processo: ", adocao["id"]),
                                rx.text("Animal: ", adocao["animal_id"]),
                                rx.text("Data da solicitação: ", adocao["data_solicitacao"]),
                                rx.hstack(
                                    rx.text("Status:", weight="bold", color="#3E4149"),
                                    rx.badge(adocao["status_processo"], color_scheme="orange"),
                                    align="center", spacing="2",
                                ),
                                align="start", spacing="2",
                            ),
                            padding="16px", background="#FFFFFF", border_radius="12px", width="100%",
                        ),
                    ),
                    width="100%", spacing="3",
                ),
                rx.fragment(),
            ),
            align="start", spacing="4", width="100%", max_width="900px", margin="0 auto", padding="32px",
        ),
        width="100%", min_height="100vh", background="#FFF7ED",
    )

def pagina_acompanhamento() -> rx.Component:
    return rx.box(
        rx.vstack(
            # ==========================================
            # 1. CABEÇALHO DA PÁGINA (COM VOLTAR INTERATIVO)
            # ==========================================
            rx.hstack(
                rx.heading("Acompanhamento Pós-Adoção", size="7", color="#2D3142", weight="bold"),
                rx.spacer(),
                # Botão Voltar Colorido e Interativo
                rx.link(
                    rx.hstack(
                        rx.icon(tag="arrow-left", size=20),
                        rx.text("Voltar", font_size="1.15em", font_weight="bold"),
                        spacing="2",
                        align="center",
                    ),
                    href="/tutor",
                    color="#684638",
                    transition="all 0.2s ease",
                    _hover={
                        "color": "#D78A45",
                        "transform": "translateX(-4px)",
                        "text_decoration": "none",
                    },
                ),
                width="100%",
                align="center",
            ),

            # ==========================================
            # 2. CARD INFORMATIVO "COMO FUNCIONA"
            # ==========================================
            rx.box(
                rx.vstack(
                    rx.badge("COMO FUNCIONA", color_scheme="orange", variant="soft", radius="full", padding_x="12px"),
                    rx.heading(
                        "O que esperar do Acompanhamento Pós-Adoção?",
                        size="5",
                        color="#2D3142",
                        weight="bold",
                    ),
                    rx.text(
                        "O acompanhamento pós-adoção garante que você e seu novo pet tenham uma transição tranquila e segura. Durante este período, você passará pelos seguintes processos:",
                        color="#5E5A55",
                        size="2",
                    ),
                    rx.vstack(
                        rx.text(
                            "• Adaptação Inicial: Acompanhamento da rotina, alimentação e comportamento do animal nos primeiros dias no novo lar.",
                            color="#5E5A55",
                            size="2",
                        ),
                        rx.text(
                            "• Contato e Visitas: Contatos periódicos da equipe para recebimento de fotos, vídeos ou realização de visitas preventivas de rotina.",
                            color="#5E5A55",
                            size="2",
                        ),
                        rx.text(
                            "• Suporte Continuado: Orientação sobre saúde (vacinação, vermifugação e castração) e apoio para eventuais dúvidas de comportamento.",
                            color="#5E5A55",
                            size="2",
                        ),
                        rx.text(
                            "• Conclusão da Adaptação: Finalização do acompanhamento oficial assim que o pet estiver completamente integrado à família.",
                            color="#5E5A55",
                            size="2",
                        ),
                        align="start",
                        spacing="2",
                        padding_left="8px",
                    ),
                    spacing="3",
                    align="start",
                ),
                padding="28px",
                background="rgba(255, 255, 255, 0.95)",
                backdrop_filter="blur(8px)",
                border_radius="20px",
                border_left="6px solid #D78A45",
                border_top="1px solid rgba(215, 138, 69, 0.2)",
                border_right="1px solid rgba(215, 138, 69, 0.2)",
                border_bottom="1px solid rgba(215, 138, 69, 0.2)",
                box_shadow="0 4px 20px rgba(0,0,0,0.03)",
                width="100%",
            ),

            rx.divider(border_color="rgba(215, 138, 69, 0.2)", margin_y="12px"),

            # ==========================================
            # 3. REGISTROS DE ACOMPANHAMENTO
            # ==========================================
            rx.hstack(
                rx.heading("Seus Registros de Acompanhamento", size="5", color="#2D3142", weight="bold"),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon(tag="refresh-cw", size=16),
                        rx.text("Consultar Registros"),
                        spacing="2",
                        align="center",
                    ),
                    on_click=LoginState.carregar_acompanhamentos,
                    background="#D78A45",
                    color="#FFFFFF",
                    radius="full",
                    padding_x="20px",
                    _hover={"background": "#C07838", "transform": "translateY(-1px)"},
                ),
                width="100%",
                align="center",
            ),

            # Feedbacks de carregamento e erro
            rx.cond(
                LoginState.carregando_acompanhamentos,
                rx.text("Carregando acompanhamentos pós-adoção...", color="#7A756E", size="2"),
                rx.fragment(),
            ),
            rx.cond(
                LoginState.erro_acompanhamentos != "",
                rx.text(LoginState.erro_acompanhamentos, color="red", size="2"),
                rx.fragment(),
            ),

            # Lista de Registros
            rx.cond(
                LoginState.acompanhamentos.length() > 0,
                rx.vstack(
                    rx.foreach(
                        LoginState.acompanhamentos,
                        lambda item: rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.badge("Acompanhamento Registrado", color_scheme="orange", variant="soft", radius="full"),
                                    rx.spacer(),
                                    rx.text("Data da Visita: ", item["data_visita"], size="2", color="#7A756E", font_weight="medium"),
                                    width="100%",
                                    align="center",
                                ),
                                rx.hstack(
                                    rx.text("Processo de Adoção nº: ", font_weight="bold", color="#2D3142", size="2"),
                                    rx.text(item["processo_adocao_id"], color="#D78A45", font_weight="bold", size="2"),
                                    spacing="1",
                                ),
                                rx.text("Relatório / Observação:", font_weight="bold", color="#2D3142", size="2"),
                                rx.text(item["observacao"], color="#5E5A55", size="2"),
                                align="start",
                                spacing="2",
                            ),
                            padding="20px",
                            background="rgba(255, 255, 255, 0.95)",
                            border_radius="18px",
                            border="1px solid rgba(215, 138, 69, 0.2)",
                            box_shadow="0 4px 15px rgba(0,0,0,0.03)",
                            width="100%",
                        ),
                    ),
                    width="100%",
                    spacing="3",
                ),
                rx.box(
                    rx.vstack(
                        rx.text("📋", font_size="2em"),
                        rx.text(
                            "Nenhum registro de acompanhamento pós-adoção encontrado até o momento.",
                            color="#7A756E",
                            size="2",
                            font_style="italic",
                            text_align="center",
                        ),
                        align="center",
                        spacing="2",
                    ),
                    padding="28px",
                    background="rgba(255, 255, 255, 0.8)",
                    border_radius="18px",
                    border="1px dashed rgba(215, 138, 69, 0.4)",
                    width="100%",
                ),
            ),
            align="start",
            spacing="5",
            width="100%",
            max_width="1000px",
            margin="0 auto",
            padding=["20px", "32px"],
        ),
        width="100%",
        min_height="100vh",
        background_color="#FFF7ED",
        background_image="url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 100 100' fill='%23D78A45' opacity='0.10'%3E%3Cpath d='M30 50c-6 0-10 6-10 12 0 8 10 18 20 18s20-10 20-18c0-6-4-12-10-12s-8 3-10 3-4-3-10-3zm-12-8c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18-12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm24 0c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18 12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8z'/%3E%3C/svg%3E\")",
        background_repeat="repeat",
    )


def pagina_meus_dados() -> rx.Component:
    return rx.box(
        rx.vstack(
            # ==========================================
            # 1. CABEÇALHO DA PÁGINA (VOLTAR INTERATIVO ANIMADO)
            # ==========================================
            rx.hstack(
                rx.heading("Meus Dados Cadastrais", size="7", color="#2D3142", weight="bold"),
                rx.spacer(),
                rx.link(
                    rx.hstack(
                        rx.icon(tag="arrow-left", size=20),
                        rx.text("Voltar", font_size="1.15em", font_weight="bold"),
                        spacing="2",
                        align="center",
                    ),
                    href="/tutor",
                    color="#684638",
                    transition="all 0.2s ease",
                    cursor="pointer",
                    _hover={
                        "color": "#D78A45",
                        "transform": "translateX(-4px)",
                        "text_decoration": "none",
                    },
                ),
                width="100%",
                align="center",
            ),

            rx.text(
                "Confira e atualize suas informações pessoais registradas no sistema da ONG.",
                color="#5E5A55",
                size="3",
            ),

            # ==========================================
            # 2. CARTÃO DE EDIÇÃO COMPLETO
            # ==========================================
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            rx.icon(tag="user-check", size=24, color="#D78A45"),
                            background="#FFF3E0",
                            padding="10px",
                            border_radius="14px",
                        ),
                        rx.vstack(
                            rx.heading("Editar Informações do Perfil", size="4", color="#2D3142", weight="bold"),
                            rx.text("Mantenha seus dados atualizados para contato da ONG", size="1", color="#7A756E"),
                            spacing="0",
                            align="start",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    
                    rx.divider(margin_y="12px", border_color="rgba(215, 138, 69, 0.15)"),

                    # Formulário de Edição com novos campos
                    rx.vstack(
                        # Nome Completo
                        rx.vstack(
                            rx.text("Nome Completo:", font_weight="bold", color="#2D3142", size="2"),
                            rx.input(
                                placeholder="Digite seu nome completo",
                                default_value=LoginState.novo_nome,
                                on_change=LoginState.set_novo_nome,
                                width="100%",
                                radius="large",
                                background="#FFFFFF",
                                border="1px solid rgba(215, 138, 69, 0.3)",
                            ),
                            align="start",
                            width="100%",
                            spacing="1",
                        ),

                        # CPF e Telefone em linha
                        rx.grid(
                            rx.vstack(
                                rx.text("CPF:", font_weight="bold", color="#2D3142", size="2"),
                                rx.input(
                                    placeholder="000.000.000-00",
                                    default_value=LoginState.novo_cpf,
                                    on_change=LoginState.set_novo_cpf,
                                    width="100%",
                                    radius="large",
                                    background="#FFFFFF",
                                    border="1px solid rgba(215, 138, 69, 0.3)",
                                ),
                                align="start",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Telefone / WhatsApp:", font_weight="bold", color="#2D3142", size="2"),
                                rx.input(
                                    placeholder="(00) 90000-0000",
                                    default_value=LoginState.novo_telefone,
                                    on_change=LoginState.set_novo_telefone,
                                    width="100%",
                                    radius="large",
                                    background="#FFFFFF",
                                    border="1px solid rgba(215, 138, 69, 0.3)",
                                ),
                                align="start",
                                spacing="1",
                            ),
                            columns={"initial": "1", "sm": "2"},
                            spacing="3",
                            width="100%",
                        ),

                        # Tipo de Residência e Endereço
                        rx.grid(
                            rx.vstack(
                                rx.text("Tipo de Residência:", font_weight="bold", color="#2D3142", size="2"),
                                rx.input(
                                    placeholder="Ex: Casa, Apartamento...",
                                    default_value=LoginState.novo_tipo_residencia,
                                    on_change=LoginState.set_novo_tipo_residencia,
                                    width="100%",
                                    radius="large",
                                    background="#FFFFFF",
                                    border="1px solid rgba(215, 138, 69, 0.3)",
                                ),
                                align="start",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Endereço Completo:", font_weight="bold", color="#2D3142", size="2"),
                                rx.input(
                                    placeholder="Rua, Número, Bairro - Cidade/UF",
                                    default_value=LoginState.novo_endereco,
                                    on_change=LoginState.set_novo_endereco,
                                    width="100%",
                                    radius="large",
                                    background="#FFFFFF",
                                    border="1px solid rgba(215, 138, 69, 0.3)",
                                ),
                                align="start",
                                spacing="1",
                            ),
                            columns={"initial": "1", "sm": "2"},
                            spacing="3",
                            width="100%",
                        ),

                        # E-mail (somente leitura)
                        rx.vstack(
                            rx.text("E-mail de Acesso (Não Editável):", font_weight="bold", color="#2D3142", size="2"),
                            rx.input(
                                value=LoginState.email,
                                disabled=True,
                                width="100%",
                                radius="large",
                                background="#F5F5F5",
                                color="#7A756E",
                            ),
                            align="start",
                            width="100%",
                            spacing="1",
                        ),

                        rx.divider(margin_y="8px", border_color="rgba(215, 138, 69, 0.15)"),

                        # Botão Salvar
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="save", size=18),
                                rx.text("Salvar Alterações", font_weight="bold"),
                                spacing="2",
                                align="center",
                            ),
                            on_click=LoginState.salvar_dados_tutor,
                            loading=LoginState.salvando_dados,
                            background="#D78A45",
                            color="white",
                            radius="full",
                            padding_x="24px",
                            padding_y="12px",
                            align_self="end",
                            _hover={"background": "#C07838", "transform": "translateY(-1px)"},
                        ),
                        spacing="4",
                        align="start",
                        width="100%",
                    ),
                    align="start",
                    spacing="3",
                    width="100%",
                ),
                padding="28px",
                background="rgba(255, 255, 255, 0.95)",
                border_radius="20px",
                border="1px solid rgba(215, 138, 69, 0.2)",
                box_shadow="0 4px 15px rgba(0,0,0,0.03)",
                width="100%",
            ),

            align="start",
            spacing="5",
            width="100%",
            max_width="1000px",
            margin="0 auto",
            padding=["20px", "32px"],
        ),
        width="100%",
        min_height="100vh",
        background_color="#FFF7ED",
        background_image="url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 100 100' fill='%23D78A45' opacity='0.10'%3E%3Cpath d='M30 50c-6 0-10 6-10 12 0 8 10 18 20 18s20-10 20-18c0-6-4-12-10-12s-8 3-10 3-4-3-10-3zm-12-8c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18-12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm24 0c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18 12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8z'/%3E%3C/svg%3E\")",
        background_repeat="repeat",
    )


def pagina_orientacoes() -> rx.Component:
    return rx.box(
        rx.vstack(
            # ==========================================
            # 1. CABEÇALHO DA PÁGINA (VOLTAR INTERATIVO)
            # ==========================================
            rx.hstack(
                rx.heading("Orientações ao Tutor", size="7", color="#2D3142", weight="bold"),
                rx.spacer(),
                # Botão Voltar Colorido com Animação
                rx.link(
                    rx.hstack(
                        rx.icon(tag="arrow-left", size=20),
                        rx.text("Voltar", font_size="1.15em", font_weight="bold"),
                        spacing="2",
                        align="center",
                    ),
                    href="/tutor",
                    color="#684638",
                    transition="all 0.2s ease",
                    _hover={
                        "color": "#D78A45",
                        "transform": "translateX(-4px)",
                        "text_decoration": "none",
                    },
                ),
                width="100%",
                align="center",
            ),

            rx.text(
                "Guia prático com dicas fundamentais para garantir a saúde, a adaptação e o bem-estar do seu novo pet.",
                color="#5E5A55",
                size="3",
            ),

            # ==========================================
            # 2. CARDS DE ORIENTAÇÕES E DICAS
            # ==========================================
            rx.vstack(
                # Card 1: Adaptação
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.box(
                                rx.text("🏠", font_size="1.4em"),
                                background="#FFF3E0",
                                padding="8px",
                                border_radius="12px",
                            ),
                            rx.heading("Adaptação nos Primeiros Dias", size="4", color="#2D3142", weight="bold"),
                            spacing="3",
                            align="center",
                        ),
                        rx.text(
                            "Proporcione um ambiente calmo, seguro e restrito nos primeiros dias. Deixe o pet explorar o espaço no tempo dele, garantindo água fresca, alimentação adequada e um local aquecido para descansar.",
                            color="#5E5A55",
                            size="2",
                        ),
                        align="start",
                        spacing="3",
                    ),
                    padding="24px",
                    background="rgba(255, 255, 255, 0.95)",
                    border_radius="18px",
                    border="1px solid rgba(215, 138, 69, 0.2)",
                    box_shadow="0 4px 15px rgba(0,0,0,0.03)",
                    width="100%",
                ),

                # Card 2: Saúde e Vacinação
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.box(
                                rx.text("💉", font_size="1.4em"),
                                background="#FFF3E0",
                                padding="8px",
                                border_radius="12px",
                            ),
                            rx.heading("Saúde, Vacinação e Cuidados", size="4", color="#2D3142", weight="bold"),
                            spacing="3",
                            align="center",
                        ),
                        rx.text(
                            "Mantenha a carteira de vacinação, a desvermifugação e o controle de pulgas/carrapatos rigorosamente em dia. Agende uma consulta veterinária de rotina para acompanhamento preventivo.",
                            color="#5E5A55",
                            size="2",
                        ),
                        align="start",
                        spacing="3",
                    ),
                    padding="24px",
                    background="rgba(255, 255, 255, 0.95)",
                    border_radius="18px",
                    border="1px solid rgba(215, 138, 69, 0.2)",
                    box_shadow="0 4px 15px rgba(0,0,0,0.03)",
                    width="100%",
                ),

                # Card 3: Segurança e Guarda Responsável
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.box(
                                rx.text("🛡️", font_size="1.4em"),
                                background="#FFF3E0",
                                padding="8px",
                                border_radius="12px",
                            ),
                            rx.heading("Segurança e Ambiente Protegido", size="4", color="#2D3142", weight="bold"),
                            spacing="3",
                            align="center",
                        ),
                        rx.text(
                            "Certifique-se de que janelas possuem redes de proteção (para gatos) e muros/portões não possuem rotas de fuga (para cães). Mantenha identificação na coleira com seu telefone de contato.",
                            color="#5E5A55",
                            size="2",
                        ),
                        align="start",
                        spacing="3",
                    ),
                    padding="24px",
                    background="rgba(255, 255, 255, 0.95)",
                    border_radius="18px",
                    border="1px solid rgba(215, 138, 69, 0.2)",
                    box_shadow="0 4px 15px rgba(0,0,0,0.03)",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            align="start",
            spacing="5",
            width="100%",
            max_width="1000px",
            margin="0 auto",
            padding=["20px", "32px"],
        ),
        width="100%",
        min_height="100vh",
        background_color="#FFF7ED",
        background_image="url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 100 100' fill='%23D78A45' opacity='0.10'%3E%3Cpath d='M30 50c-6 0-10 6-10 12 0 8 10 18 20 18s20-10 20-18c0-6-4-12-10-12s-8 3-10 3-4-3-10-3zm-12-8c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18-12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm24 0c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18 12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8z'/%3E%3C/svg%3E\")",
        background_repeat="repeat",
    )


# ==============================================================================
# CONFIGURAÇÃO DAS ROTAS DO APP
# ==============================================================================
app = rx.App()

app.add_page(index, route="/", on_load=LoginState.iniciar_carrossel_automatico)
app.add_page(recuperar_senha, route="/recuperar-senha")
app.add_page(alterar_senha, route="/alterar-senha")
app.add_page(area_administrativa, route="/administrativo")

app.add_page(area_tutor, route="/tutor", on_load=LoginState.carregar_adocoes)
app.add_page(pagina_minhas_adocoes, route="/minhas-adocoes")
app.add_page(pagina_acompanhamento, route="/acompanhamento")
app.add_page(pagina_meus_dados, route="/meus-dados")
app.add_page(pagina_orientacoes, route="/orientacoes")