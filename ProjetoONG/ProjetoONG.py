# 1. TOPO DO ARQUIVO: Configuração do caminho + Importações de bibliotecas e páginas
import os
import sys
import httpx
import asyncio
import reflex as rx
from dotenv import load_dotenv
from ProjetoONG.gestao_animal import gestao_animal
from ProjetoONG.alterar_senha import ChangePasswordState, formulario_alterar_senha, alterar_senha_page
from ProjetoONG.modulos_administracao.tela_adocoes import adocoes_page
from ProjetoONG.state.voluntarios_state import VoluntariosState

from ProjetoONG.modulos_administracao.menu_administrativo import (
    sidebar_administracao,
)
from ProjetoONG.modulos_administracao.pos_adocao import pos_adocao
from ProjetoONG.modulos_administracao.tela_atendimento_veterinario import (
    atendimento_veterinario_page,
)
from ProjetoONG.state.lares_temporarios_state import LaresTemporariosState
from ProjetoONG.modulos_administracao.tela_doacoes import doacoes_page
from ProjetoONG.modulos_administracao.tela_voluntarios import voluntarios_page
from ProjetoONG.modulos_administracao.tela_lares_temporarios import (
    lares_temporarios_page,
)
from ProjetoONG.state.doacoes_state import DoacoesState
from ProjetoONG.state.adocoes_state import AdocoesState
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


    # Aba ativa do painel unificado do tutor (apenas UI)
    aba_tutor: str = "adocoes"

    @rx.event
    def set_aba_tutor(self, aba: str):
        self.aba_tutor = aba

    @rx.event
    async def iniciar_painel_tutor(self):
        """Carrega automaticamente adoções e acompanhamentos ao entrar na Área do Tutor."""
        await self.carregar_adocoes()
        await self.carregar_acompanhamentos()

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
                rx.button("Entrar", on_click=LoginState.validar_login, width="50%", background="#A96348", color="white", radius="large"),
               
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


# ==============================================================================
# ÁREA ADMINISTRATIVA 
# ==============================================================================
def item_menu(icone: str, texto: str, tela: str = "") -> rx.Component:
    ativo = LoginState.tela_atual == tela
    return rx.hstack(
       rx.icon(
           icone,
           size=20 if icone == "stethoscope" else 18,
           color=rx.cond(ativo, "#58392B", "#64748B"),
        ),
        rx.text(
            texto,
            size="2",
            weight=rx.cond(ativo, "bold", "medium"),
            color=rx.cond(ativo, "#2D1F18", "#52433D"),
            white_space="nowrap",
        ),
        spacing="3",
        align="center",
        width="100%",
        padding="10px 14px",
        border_radius="10px",
        cursor="pointer",
        background=rx.cond(ativo, "#FFFFFF", "transparent"),
        box_shadow=rx.cond(ativo, "0 1px 3px rgba(0, 0, 0, 0.05)", "none"),
        transition="background 0.15s ease",
        _hover={"background": rx.cond(ativo, "#FFFFFF", "#F5EFE6")},
        on_click=LoginState.set_tela(tela) if tela else None,
    )


def titulo_secao_menu(texto: str) -> rx.Component:
    return rx.text(
        texto,
        size="1",
        weight="bold",
        color="#9E8C82",
        letter_spacing="0.08em",
        padding="10px 8px 2px 8px",
    )


def menu_lateral() -> rx.Component:
    return rx.vstack(
        # Logotipo / Brand
        rx.hstack(
            rx.center(
                rx.icon("paw-print", size=20, color="white"),
                background="#58392B",
                border_radius="10px",
                width="34px",
                height="34px",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text("Porto Seguro Pet", size="3", weight="bold", color="#2D1F18"),
                rx.text("Painel administrativo", size="1", color="#78675E"),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
            padding="4px 4px 14px 4px",
            width="100%",
        ),
        # CATEGORIAS DO MENU
        titulo_secao_menu("PRINCIPAL"),
        item_menu("layout-dashboard", "Início", "inicio"),
           rx.link(
             item_menu("paw-print", "Gestão de Animais"),
             href="/animais",
             underline="none",
             width="100%",
            ),
        item_menu("home", "Lares Temporários"),
        titulo_secao_menu("ATENDIMENTO"),
       rx.link(
           item_menu("heart", "Atendimento Veterinário"),
            href="/atendimento-vet",
            underline="none",
            width="100%",
        ),
        rx.link(
            item_menu("heart", "Adoções"),
            href="/adocoes",
            underline="none",
            width="100%",
        ),
        item_menu("clipboard-check", "Pós-Adoção"),
        titulo_secao_menu("ADMINISTRAÇÃO"),
        item_menu("users", "Voluntários"),
        item_menu("wallet", "Doações"),
        spacing="1",
        align="stretch",
        width="100%",
        height="100vh",
        overflow_y="auto",
        position="sticky",
        top="0",
        padding="16px 12px",
        background="#EFE6DA",
        border_right="1px solid #E2D7C7",
        box_sizing="border-box",
    )

def pagina_gestao_animais() -> rx.Component:
    return rx.box(
        rx.flex(
            # Menu lateral
            rx.box(
                sidebar_administracao(),
                width="260px",
                min_width="260px",
                height="100vh",
                position="sticky",
                top="0",
            ),
            # Conteúdo principal
            rx.box(
                gestao_animal(LoginState.token),
                flex="1",
                padding="24px 32px",
                overflow_y="auto",
                min_width="0",
            ),
            width="100%",
            align="start",
        ),
        background="#F8F3EC",
        min_height="100vh",
        width="100%",
    )


def cartao_boas_vindas(
    icone: str,
    titulo: str,
    texto: str,
    cor_icone: str,
    bg_cartao: str,
    borda_cartao: str,
    borda_hover: str,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.icon(
                icone,
                size=30,
                color=cor_icone,
            ),
            rx.heading(
                titulo,
                size="6",
                color="#2D1F18",
            ),
            rx.text(
                texto,
                font_size="16px",
                color="#52433D",
                line_height="1.7",
            ),
            align="start",
            spacing="3",
            width="100%",
        ),
        background=bg_cartao,
        padding="28px",
        border_radius="18px",
        border=f"1px solid {borda_cartao}",
        width="100%",
        height="100%",
        box_shadow="0 3px 12px rgba(88,57,43,0.06)",
        transition="transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease",
        _hover={
            "transform": "translateY(-4px)",
            "box_shadow": "0 9px 22px rgba(88,57,43,0.13)",
            "border_color": borda_hover,
        },
    )


def area_administrativa() -> rx.Component:
    return rx.grid(
        sidebar_administracao(),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.spacer(),
                    rx.button(
                        "Sair",
                        on_click=LoginState.sair,
                        width="auto",
                        height="36px",
                        padding="6px 16px",
                        font_size="13px",
                        background="#A96348",
                        color="#FFFFFF",
                        border_radius="8px",
                        transition="background 0.2s ease",
                        _hover={
                            "background": "#8F503B",
                        },
                    ),
                    width="100%",
                    align="center",
                    justify="end",
                ),
                rx.box(
                    rx.cond(
                        LoginState.tela_atual == "animais",
                        gestao_animal(LoginState.token),
                        rx.vstack(
                            rx.hstack(
                                rx.vstack(
                                    rx.text(
                                        "BEM-VINDO(A) AO PORTO SEGURO PET",
                                        font_size="13px",
                                        font_weight="bold",
                                        color="#A65F43",
                                        letter_spacing="1px",
                                    ),
                                    rx.heading(
                                        "Bem-vindo à área administrativa!",
                                        size="8",
                                        color="#2D1F18",
                                        weight="bold",
                                    ),
                                    rx.text(
                                        "Proteção, cuidado e novas oportunidades.",
                                        font_size="18px",
                                        color="#78675E",
                                    ),
                                    align="start",
                                    spacing="3",
                                    flex="1",
                                ),
                                rx.image(
                                    src="/animais-boas-vindas.gif",
                                    alt="Cachorrinho e gatinho animados",
                                    width="220px",
                                    height="194px",
                                    object_fit="contain",
                                ),
                                align="center",
                                justify="between",
                                spacing="5",
                                width="100%",
                            ),

                            # Linha 1: Quem somos & Nossa missão
                            rx.grid(
                                cartao_boas_vindas(
                                    icone="heart-handshake",
                                    titulo="Quem somos",
                                    texto="Somos uma organização dedicada à proteção e ao cuidado dos animais, acompanhando sua trajetória do resgate à adoção responsável.",
                                    cor_icone="#A65F43",
                                    bg_cartao="#EFE6DA",
                                    borda_cartao="#D6B99A",
                                    borda_hover="#C77D5B",
                                ),
                                cartao_boas_vindas(
                                    icone="paw-print",
                                    titulo="Nossa missão",
                                    texto="Promover o bem-estar animal por meio do resgate, dos cuidados necessários, do acolhimento temporário e da busca por lares responsáveis.",
                                    cor_icone="#737747",
                                    bg_cartao="#E5E6CF",
                                    borda_cartao="#C8CA9D",
                                    borda_hover="#A3A66B",
                                ),
                                columns={"initial": "1", "md": "2"},
                                spacing="4",
                                width="100%",
                            ),

                            # Linha 2: Funcionalidades, Público e Área do Tutor
                            rx.grid(
                                cartao_boas_vindas(
                                    icone="layout-grid",
                                    titulo="Funcionalidades do sistema",
                                    texto="Centraliza a gestão de animais resgatados, lares temporários, atendimentos veterinários, processos de adoção, pós-adoção, voluntários e doações.",
                                    cor_icone="#A65F43",
                                    bg_cartao="#F5E7DF",
                                    borda_cartao="#E3C2B2",
                                    borda_hover="#C77D5B",
                                ),
                                cartao_boas_vindas(
                                    icone="users",
                                    titulo="Nosso público",
                                    texto="Desenvolvido para equipes de ONGs, voluntários, cuidadores de lares temporários, doadores e famílias comprometidas com a guarda responsável.",
                                    cor_icone="#737747",
                                    bg_cartao="#E5E6CF",
                                    borda_cartao="#C8CA9D",
                                    borda_hover="#A3A66B",
                                ),
                                cartao_boas_vindas(
                                    icone="user-check",
                                    titulo="Área do tutor",
                                    texto="O sistema também conta com um portal exclusivo para os adotantes acompanharem cada etapa da adoção e consultarem orientações sobre o pós-adoção.",
                                    cor_icone="#8C6239",
                                    bg_cartao="#EFE6DA",
                                    borda_cartao="#D6B99A",
                                    borda_hover="#C77D5B",
                                ),
                                columns={"initial": "1", "md": "3"},
                                spacing="4",
                                width="100%",
                            ),

                            spacing="6",
                            align="start",
                            width="100%",
                            max_width="1050px",
                            margin="0 auto",
                        ),
                    ),
                    width="100%",
                    flex="1",
                ),
                spacing="0",
                align="stretch",
                width="100%",
            ),
            padding="32px 40px",
            background="#F8F3EC",
            width="100%",
            height="100vh",
            overflow_y="auto",
            box_sizing="border-box",
        ),
        grid_template_columns="260px minmax(0, 1fr)",
        width="100vw",
        height="100vh",
        overflow="hidden",
        box_sizing="border-box",
    )


# ==============================================================================
# PALETA EXCLUSIVA: ÁREA DO TUTOR (TERRACOTA ABERTO + SÁLVIA + SOFT WHITE)
# ==============================================================================
TUTOR_TERRACOTA = "#D9967B"           # Terracota fraco e aberto
TUTOR_TERRACOTA_HOVER = "#C68065"     # Terracota hover
TUTOR_TERRACOTA_SUAVE = "#F6E9E2"     # Fundo suave terracota
TUTOR_TERRACOTA_BORDA = "#E8CFC3"     # Borda sutil terracota

TUTOR_SALVIA = "#7B9076"              # Sálvia principal
TUTOR_SALVIA_ESCURO = "#566952"       # Texto sálvia escuro
TUTOR_SALVIA_SUAVE = "#E7EDE4"        # Fundo suave sálvia
TUTOR_SALVIA_BORDA = "#C9D4C4"        # Borda sutil sálvia

TUTOR_SOFT_WHITE = "#FAF8F5"          # Soft White para cartões
TUTOR_TITULO = "#2C2523"              # Grafite quente
TUTOR_TEXTO = "#574E4A"               # Texto padrão
TUTOR_TEXTO_CLARO = "#7D726D"         # Subtítulos
TUTOR_BORDA = "#E6DDD5"               # Borda neutra sutil

TUTOR_ERRO = "#A64B3A"                # Detalhe discreto para recusa
TUTOR_ERRO_SUAVE = "#F6E4E1"

BG_PATINHAS_TUTOR = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 100 100' fill='%23D9967B' opacity='0.11'%3E%3Cpath d='M30 50c-6 0-10 6-10 12 0 8 10 18 20 18s20-10 20-18c0-6-4-12-10-12s-8 3-10 3-4-3-10-3zm-12-8c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18-12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm24 0c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8zm18 12c3 0 6-4 6-8s-3-8-6-8-6 4-6 8 3 8 6 8z'/%3E%3C/svg%3E\")"


def pill_tutor(texto: str, tipo: str = "terracota") -> rx.Component:
    bg = {
        "terracota": TUTOR_TERRACOTA_SUAVE,
        "salvia": TUTOR_SALVIA_SUAVE,
        "erro": TUTOR_ERRO_SUAVE,
    }.get(tipo, TUTOR_TERRACOTA_SUAVE)
    cor = {
        "terracota": "#9E5E45",
        "salvia": TUTOR_SALVIA_ESCURO,
        "erro": TUTOR_ERRO,
    }.get(tipo, "#9E5E45")
    borda = {
        "terracota": TUTOR_TERRACOTA_BORDA,
        "salvia": TUTOR_SALVIA_BORDA,
        "erro": "#E5B5AE",
    }.get(tipo, TUTOR_TERRACOTA_BORDA)

    return rx.box(
        rx.text(texto, font_size="13.5px", font_weight="600", color=cor, white_space="nowrap"),
        background=bg,
        border=f"1px solid {borda}",
        padding_x="12px",
        padding_y="4px",
        border_radius="999px",
        display="inline-flex",
        align_items="center",
    )


def botao_aba_tutor(icone: str, titulo: str, valor_aba: str) -> rx.Component:
    ativo = LoginState.aba_tutor == valor_aba
    return rx.box(
        rx.hstack(
            rx.icon(
                tag=icone,
                size=18,
                color=rx.cond(ativo, "#FFFFFF", TUTOR_TEXTO_CLARO),
            ),
            rx.text(
                titulo,
                font_size="15.5px",
                font_weight=rx.cond(ativo, "600", "500"),
                color=rx.cond(ativo, "#FFFFFF", TUTOR_TEXTO),
                white_space="nowrap",
            ),
            spacing="2",
            align="center",
        ),
        padding="10px 20px",
        border_radius="999px",
        background=rx.cond(ativo, TUTOR_TERRACOTA, "transparent"),
        cursor="pointer",
        transition="all 0.2s ease",
        on_click=lambda: LoginState.set_aba_tutor(valor_aba),
        _hover={
            "background": rx.cond(ativo, TUTOR_TERRACOTA, TUTOR_TERRACOTA_SUAVE),
        },
    )


# ==============================================================================
# ABA 1: MINHAS ADOÇÕES
# ==============================================================================
def card_adocao_tutor(adocao) -> rx.Component:
    status = adocao["status_processo"]
    etapa_1_ativa = (
        (status == "Em análise")
        | (status == "Mais informações necessárias")
        | (status == "Aprovada")
        | (status == "Adoção efetivada")
    )
    etapa_2_ativa = (status == "Aprovada") | (status == "Adoção efetivada")
    etapa_3_ativa = status == "Adoção efetivada"

    return rx.box(
        rx.vstack(
            # Topo: Nome do Pet + Pill de Status
            rx.hstack(
                rx.hstack(
                    rx.center(
                        rx.icon("paw-print", size=20, color=TUTOR_TERRACOTA),
                        background=TUTOR_TERRACOTA_SUAVE,
                        border=f"1px solid {TUTOR_TERRACOTA_BORDA}",
                        width="42px",
                        height="42px",
                        border_radius="12px",
                        flex_shrink="0",
                    ),
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
                            size="5",
                            color=TUTOR_TITULO,
                            weight="bold",
                        ),
                        rx.text(
                            "Processo #" + adocao["id"].to_string() + " • Solicitado em " + adocao["data_solicitacao"],
                            size="2",
                            color=TUTOR_TEXTO_CLARO,
                        ),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.spacer(),
                rx.match(
                    status,
                    ("Aprovada", pill_tutor("Aprovada", "salvia")),
                    ("Adoção efetivada", pill_tutor("Adoção efetivada", "salvia")),
                    ("Não aprovada", pill_tutor("Não aprovada", "erro")),
                    ("Mais informações necessárias", pill_tutor("Pendência de info", "terracota")),
                    pill_tutor("Em análise", "terracota"),
                ),
                width="100%",
                align="center",
                wrap="wrap",
                spacing="2",
            ),

            # Linha do Tempo Horizontal Minimalista
            rx.hstack(
                # Passo 1: Análise
                rx.vstack(
                    rx.center(
                        rx.icon("check", size=14, color="white"),
                        width="28px",
                        height="28px",
                        border_radius="full",
                        background=rx.cond(etapa_1_ativa, TUTOR_TERRACOTA, "#DDD6CE"),
                    ),
                    rx.text("Análise", size="2", color=TUTOR_TEXTO, font_weight="500"),
                    spacing="1",
                    align="center",
                ),
                rx.box(
                    height="2px",
                    flex="1",
                    background=rx.cond(etapa_2_ativa, TUTOR_TERRACOTA, TUTOR_BORDA),
                    margin_top="-20px",
                ),
                # Passo 2: Aprovação
                rx.vstack(
                    rx.center(
                        rx.icon("check", size=14, color="white"),
                        width="28px",
                        height="28px",
                        border_radius="full",
                        background=rx.cond(etapa_2_ativa, TUTOR_TERRACOTA, "#DDD6CE"),
                    ),
                    rx.text("Aprovação", size="2", color=TUTOR_TEXTO, font_weight="500"),
                    spacing="1",
                    align="center",
                ),
                rx.box(
                    height="2px",
                    flex="1",
                    background=rx.cond(etapa_3_ativa, TUTOR_SALVIA, TUTOR_BORDA),
                    margin_top="-20px",
                ),
                # Passo 3: Concluído (Sálvia)
                rx.vstack(
                    rx.center(
                        rx.icon("heart", size=14, color="white"),
                        width="28px",
                        height="28px",
                        border_radius="full",
                        background=rx.cond(etapa_3_ativa, TUTOR_SALVIA, "#DDD6CE"),
                    ),
                    rx.text("No Novo Lar", size="2", color=TUTOR_TEXTO, font_weight="500"),
                    spacing="1",
                    align="center",
                ),
                width="100%",
                align="center",
                padding_x="14px",
                padding_y="8px",
            ),

            # Mensagem objetiva da etapa atual
            rx.match(
                status,
                (
                    "Em análise",
                    rx.box(
                        rx.text(
                            "Etapa 1 de 3 — A equipe da ONG está avaliando seu perfil e compatibilidade com o pet.",
                            size="3",
                            color=TUTOR_TEXTO,
                            line_height="1.55",
                        ),
                        padding="12px 16px",
                        background=TUTOR_TERRACOTA_SUAVE,
                        border=f"1px solid {TUTOR_TERRACOTA_BORDA}",
                        border_radius="12px",
                        width="100%",
                    ),
                ),
                (
                    "Mais informações necessárias",
                    rx.box(
                        rx.text(
                            "A ONG precisa de informações adicionais para concluir a análise. Verifique seu e-mail ou mantenha seus dados atualizados na aba Meu Perfil.",
                            size="3",
                            color="#9E5E45",
                            font_weight="500",
                            line_height="1.55",
                        ),
                        padding="12px 16px",
                        background=TUTOR_TERRACOTA_SUAVE,
                        border=f"1px solid {TUTOR_TERRACOTA_BORDA}",
                        border_radius="12px",
                        width="100%",
                    ),
                ),
                (
                    "Aprovada",
                    rx.box(
                        rx.text(
                            "Etapa 2 de 3 — Solicitação aprovada! A ONG entrará em contato para agendar a entrega do pet.",
                            size="3",
                            color=TUTOR_SALVIA_ESCURO,
                            font_weight="600",
                            line_height="1.55",
                        ),
                        padding="12px 16px",
                        background=TUTOR_SALVIA_SUAVE,
                        border=f"1px solid {TUTOR_SALVIA_BORDA}",
                        border_radius="12px",
                        width="100%",
                    ),
                ),
                (
                    "Adoção efetivada",
                    rx.box(
                        rx.text(
                            "Etapa 3 de 3 — Processo concluído com sucesso! Acompanhe as visitas e orientações na aba Pós-Adoção e Guias.",
                            size="3",
                            color=TUTOR_SALVIA_ESCURO,
                            font_weight="600",
                            line_height="1.55",
                        ),
                        padding="12px 16px",
                        background=TUTOR_SALVIA_SUAVE,
                        border=f"1px solid {TUTOR_SALVIA_BORDA}",
                        border_radius="12px",
                        width="100%",
                    ),
                ),
                (
                    "Não aprovada",
                    rx.box(
                        rx.text(
                            "Solicitação encerrada — No momento, o perfil não atendeu aos requisitos específicos deste animal.",
                            size="3",
                            color=TUTOR_ERRO,
                            font_weight="500",
                            line_height="1.55",
                        ),
                        padding="12px 16px",
                        background=TUTOR_ERRO_SUAVE,
                        border="1px solid #E5B5AE",
                        border_radius="12px",
                        width="100%",
                    ),
                ),
                rx.box(
                    rx.text(
                        "Seu processo está em acompanhamento pela equipe da ONG.",
                        size="3",
                        color=TUTOR_TEXTO,
                        line_height="1.55",
                    ),
                    padding="12px 16px",
                    background="#F3EFEA",
                    border_radius="12px",
                    width="100%",
                ),
            ),
            spacing="4",
            align="start",
            width="100%",
        ),
        padding="24px",
        background=TUTOR_SOFT_WHITE,
        border_radius="18px",
        border=f"1px solid {TUTOR_BORDA}",
        box_shadow="0 4px 14px rgba(44, 37, 25, 0.04)",
        width="100%",
    )


def aba_minhas_adocoes() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Minhas Adoções", size="6", color=TUTOR_TITULO, weight="bold"),
                rx.text("Acompanhe em tempo real o andamento das suas solicitações.", size="3", color=TUTOR_TEXTO_CLARO),
                spacing="1",
                align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon(tag="refresh-cw", size=16),
                    rx.text("Atualizar", font_size="14.5px"),
                    spacing="2",
                    align="center",
                ),
                on_click=LoginState.carregar_adocoes,
                loading=LoginState.carregando_adocoes,
                background=TUTOR_SOFT_WHITE,
                color="#9E5E45",
                border=f"1px solid {TUTOR_TERRACOTA_BORDA}",
                size="3",
                radius="full",
                cursor="pointer",
                _hover={"background": TUTOR_TERRACOTA_SUAVE},
            ),
            width="100%",
            align="center",
        ),
        rx.cond(
            LoginState.erro_adocoes != "",
            rx.text(LoginState.erro_adocoes, color=TUTOR_ERRO, size="3"),
            rx.fragment(),
        ),
        rx.cond(
            LoginState.adocoes.length() > 0,
            rx.vstack(
                rx.foreach(LoginState.adocoes, card_adocao_tutor),
                spacing="4",
                width="100%",
            ),
            rx.box(
                rx.vstack(
                    rx.center(
                        rx.icon("paw-print", size=28, color=TUTOR_TERRACOTA),
                        background=TUTOR_TERRACOTA_SUAVE,
                        width="56px",
                        height="56px",
                        border_radius="16px",
                    ),
                    rx.text("Nenhuma solicitação em andamento", font_weight="bold", size="4", color=TUTOR_TITULO),
                    rx.text(
                        "Assim que você iniciar um processo de adoção com a ONG, cada etapa aparecerá aqui.",
                        size="3",
                        color=TUTOR_TEXTO_CLARO,
                        text_align="center",
                        max_width="480px",
                        line_height="1.55",
                    ),
                    align="center",
                    spacing="2",
                ),
                padding="42px 24px",
                background="rgba(250, 248, 245, 0.9)",
                border_radius="20px",
                border=f"1px dashed {TUTOR_TERRACOTA_BORDA}",
                width="100%",
            ),
        ),
        spacing="4",
        width="100%",
        align="start",
    )


# ==============================================================================
# ABA 2: PÓS-ADOÇÃO E GUIAS (HISTÓRICO XANO + CARTÕES DE GUIA)
# ==============================================================================
def card_guia_tutor(icone: str, titulo: str, texto: str, salvia: bool = False) -> rx.Component:
    cor_icone = TUTOR_SALVIA_ESCURO if salvia else TUTOR_TERRACOTA
    bg_icone = TUTOR_SALVIA_SUAVE if salvia else TUTOR_TERRACOTA_SUAVE
    borda_icone = TUTOR_SALVIA_BORDA if salvia else TUTOR_TERRACOTA_BORDA

    return rx.box(
        rx.hstack(
            rx.center(
                rx.icon(icone, size=20, color=cor_icone),
                background=bg_icone,
                border=f"1px solid {borda_icone}",
                width="40px",
                height="40px",
                border_radius="11px",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(titulo, font_weight="700", color=TUTOR_TITULO, size="3"),
                rx.text(texto, size="3", color=TUTOR_TEXTO, line_height="1.6"),
                spacing="1",
                align="start",
                flex="1",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="18px 20px",
        background=TUTOR_SOFT_WHITE,
        border_radius="16px",
        border=f"1px solid {TUTOR_BORDA}",
        box_shadow="0 3px 10px rgba(44, 37, 25, 0.03)",
        width="100%",
    )


def aba_pos_adocao_guias() -> rx.Component:
    return rx.grid(
        # Coluna Esquerda: Registros de Acompanhamento (Xano)
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("Acompanhamento Pós-Adoção", size="5", color=TUTOR_TITULO, weight="bold"),
                    rx.text("Visitas e relatórios registrados pela equipe.", size="3", color=TUTOR_TEXTO_CLARO),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon(tag="refresh-cw", size=16),
                    on_click=LoginState.carregar_acompanhamentos,
                    loading=LoginState.carregando_acompanhamentos,
                    background=TUTOR_SOFT_WHITE,
                    color=TUTOR_SALVIA_ESCURO,
                    border=f"1px solid {TUTOR_SALVIA_BORDA}",
                    size="2",
                    radius="full",
                    cursor="pointer",
                    _hover={"background": TUTOR_SALVIA_SUAVE},
                ),
                width="100%",
                align="center",
            ),

            rx.cond(
                LoginState.erro_acompanhamentos != "",
                rx.text(LoginState.erro_acompanhamentos, color=TUTOR_ERRO, size="3"),
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
                                    pill_tutor("Visita Registrada", "salvia"),
                                    rx.spacer(),
                                    rx.text(item["data_visita"], size="2", color=TUTOR_TEXTO_CLARO, font_weight="600"),
                                    width="100%",
                                    align="center",
                                ),
                                rx.text(
                                    "Processo #" + item["processo_adocao_id"],
                                    size="3",
                                    font_weight="bold",
                                    color=TUTOR_TITULO,
                                ),
                                rx.text(item["observacao"], size="3", color=TUTOR_TEXTO, line_height="1.6"),
                                align="start",
                                spacing="2",
                            ),
                            padding="20px",
                            background=TUTOR_SOFT_WHITE,
                            border_radius="16px",
                            border=f"1px solid {TUTOR_BORDA}",
                            box_shadow="0 4px 12px rgba(44, 37, 25, 0.03)",
                            width="100%",
                        ),
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.box(
                    rx.vstack(
                        rx.center(
                            rx.icon("calendar-check", size=24, color=TUTOR_SALVIA_ESCURO),
                            background=TUTOR_SALVIA_SUAVE,
                            width="48px",
                            height="48px",
                            border_radius="13px",
                        ),
                        rx.text("Nenhum registro pós-adoção ainda", font_weight="600", size="3", color=TUTOR_TITULO),
                        rx.text(
                            "Após a efetivação da adoção, os relatórios de acompanhamento aparecerão aqui.",
                            size="2",
                            color=TUTOR_TEXTO_CLARO,
                            text_align="center",
                            line_height="1.5",
                        ),
                        align="center",
                        spacing="2",
                    ),
                    padding="32px 22px",
                    background="rgba(250, 248, 245, 0.9)",
                    border_radius="18px",
                    border=f"1px dashed {TUTOR_SALVIA_BORDA}",
                    width="100%",
                ),
            ),
            spacing="4",
            width="100%",
            align="start",
        ),

        # Coluna Direita: Guia de Guarda Responsável
        rx.vstack(
            rx.vstack(
                rx.heading("Guia de Guarda Responsável", size="5", color=TUTOR_TITULO, weight="bold"),
                rx.text("Dicas rápidas para adaptação, saúde e segurança.", size="3", color=TUTOR_TEXTO_CLARO),
                spacing="1",
                align="start",
            ),
            rx.vstack(
                card_guia_tutor(
                    "home",
                    "Adaptação nos primeiros dias",
                    "Proporcione um cantinho calmo e seguro nos primeiros dias. Respeite o tempo de exploração do pet, mantendo água fresca, alimentação regular e rotina tranquila.",
                    salvia=False,
                ),
                card_guia_tutor(
                    "stethoscope",
                    "Saúde, vacinação e prevenção",
                    "Mantenha vacinas, vermífugos e controle antipulgas em dia. Consultas veterinárias periódicas garantem longevidade e bem-estar.",
                    salvia=True,
                ),
                card_guia_tutor(
                    "shield-check",
                    "Segurança e ambiente protegido",
                    "Instale telas de proteção em janelas e sacadas (essencial para gatos) e verifique portões e muros para evitar fugas. Use sempre coleira com plaquinha de identificação.",
                    salvia=False,
                ),
                card_guia_tutor(
                    "heart-handshake",
                    "Como funciona o pós-adoção da ONG",
                    "Nossa equipe acompanha os primeiros meses por meio de contatos e visitas preventivas para apoiar a adaptação do pet e esclarecer dúvidas.",
                    salvia=True,
                ),
                spacing="3",
                width="100%",
            ),
            spacing="4",
            width="100%",
            align="start",
        ),
        columns={"initial": "1", "lg": "2"},
        spacing="6",
        width="100%",
        align="start",
    )


# ==============================================================================
# ABA 3: MEU PERFIL (DADOS CADASTRAIS + ALTERAR SENHA)
# ==============================================================================
def aba_meu_perfil() -> rx.Component:
    return rx.grid(
        # Cartão de Dados Cadastrais (Conectado ao Xano PATCH)
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.center(
                        rx.icon(tag="user-check", size=22, color=TUTOR_TERRACOTA),
                        background=TUTOR_TERRACOTA_SUAVE,
                        width="42px",
                        height="42px",
                        border_radius="12px",
                    ),
                    rx.vstack(
                        rx.heading("Dados Cadastrais", size="5", color=TUTOR_TITULO, weight="bold"),
                        rx.text("Informações utilizadas nos processos de adoção", size="2", color=TUTOR_TEXTO_CLARO),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.divider(margin_y="8px", border_color=TUTOR_BORDA),

                rx.vstack(
                    rx.vstack(
                        rx.text("Nome Completo:", font_weight="600", color=TUTOR_TITULO, size="3"),
                        rx.input(
                            placeholder="Digite seu nome completo",
                            value=LoginState.novo_nome,
                            on_change=LoginState.set_novo_nome,
                            width="100%",
                            size="3",
                            radius="large",
                            background="#FFFFFF",
                            border=f"1px solid {TUTOR_TERRACOTA_BORDA}",
                        ),
                        align="start",
                        width="100%",
                        spacing="1",
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.text("CPF:", font_weight="600", color=TUTOR_TITULO, size="3"),
                            rx.input(
                                placeholder="000.000.000-00",
                                value=LoginState.novo_cpf,
                                on_change=LoginState.set_novo_cpf,
                                width="100%",
                                size="3",
                                radius="large",
                                background="#FFFFFF",
                                border=f"1px solid {TUTOR_TERRACOTA_BORDA}",
                            ),
                            align="start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Telefone / WhatsApp:", font_weight="600", color=TUTOR_TITULO, size="3"),
                            rx.input(
                                placeholder="(00) 90000-0000",
                                value=LoginState.novo_telefone,
                                on_change=LoginState.set_novo_telefone,
                                width="100%",
                                size="3",
                                radius="large",
                                background="#FFFFFF",
                                border=f"1px solid {TUTOR_TERRACOTA_BORDA}",
                            ),
                            align="start",
                            spacing="1",
                        ),
                        columns={"initial": "1", "sm": "2"},
                        spacing="3",
                        width="100%",
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.text("Tipo de Residência:", font_weight="600", color=TUTOR_TITULO, size="3"),
                            rx.input(
                                placeholder="Casa, Apartamento...",
                                value=LoginState.novo_tipo_residencia,
                                on_change=LoginState.set_novo_tipo_residencia,
                                width="100%",
                                size="3",
                                radius="large",
                                background="#FFFFFF",
                                border=f"1px solid {TUTOR_TERRACOTA_BORDA}",
                            ),
                            align="start",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Endereço:", font_weight="600", color=TUTOR_TITULO, size="3"),
                            rx.input(
                                placeholder="Rua, Número, Bairro - Cidade/UF",
                                value=LoginState.novo_endereco,
                                on_change=LoginState.set_novo_endereco,
                                width="100%",
                                size="3",
                                radius="large",
                                background="#FFFFFF",
                                border=f"1px solid {TUTOR_TERRACOTA_BORDA}",
                            ),
                            align="start",
                            spacing="1",
                        ),
                        columns={"initial": "1", "sm": "2"},
                        spacing="3",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("E-mail de Acesso:", font_weight="600", color=TUTOR_TITULO, size="3"),
                        rx.input(
                            value=LoginState.email,
                            disabled=True,
                            width="100%",
                            size="3",
                            radius="large",
                            background="#F2EDE7",
                            color=TUTOR_TEXTO_CLARO,
                        ),
                        align="start",
                        width="100%",
                        spacing="1",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="save", size=17),
                            rx.text("Salvar Alterações", font_weight="600", font_size="15px"),
                            spacing="2",
                            align="center",
                        ),
                        on_click=LoginState.salvar_dados_tutor,
                        loading=LoginState.salvando_dados,
                        background=TUTOR_SALVIA,
                        color="white",
                        size="3",
                        radius="full",
                        padding_x="24px",
                        margin_top="6px",
                        align_self="end",
                        cursor="pointer",
                        _hover={"background": TUTOR_SALVIA_ESCURO},
                    ),
                    spacing="3",
                    width="100%",
                ),
                spacing="3",
                width="100%",
                align="start",
            ),
            padding="26px",
            background=TUTOR_SOFT_WHITE,
            border_radius="20px",
            border=f"1px solid {TUTOR_BORDA}",
            box_shadow="0 4px 15px rgba(44, 37, 25, 0.04)",
            width="100%",
        ),

        # Cartão de Segurança / Alteração de Senha
        rx.box(
            formulario_alterar_senha(),
            padding="26px",
            background=TUTOR_SOFT_WHITE,
            border_radius="20px",
            border=f"1px solid {TUTOR_BORDA}",
            box_shadow="0 4px 15px rgba(44, 37, 25, 0.04)",
            width="100%",
        ),
        columns={"initial": "1", "lg": "2"},
        spacing="6",
        width="100%",
        align="start",
    )


# ==============================================================================
# PÁGINA PRINCIPAL DA ÁREA DO TUTOR
# ==============================================================================
def area_tutor() -> rx.Component:
    return rx.box(
        rx.vstack(
            # 1. HEADER COMPACTO COM NAVEGAÇÃO INTEGRADA
            rx.box(
                rx.hstack(
                    rx.hstack(
                        rx.center(
                            rx.icon("paw-print", size=22, color=TUTOR_TERRACOTA),
                            background=TUTOR_TERRACOTA_SUAVE,
                            border=f"1px solid {TUTOR_TERRACOTA_BORDA}",
                            width="40px",
                            height="40px",
                            border_radius="12px",
                        ),
                        rx.heading("Porto Seguro Pet", size="6", color=TUTOR_TITULO, weight="bold"),
                        spacing="3",
                        align="center",
                    ),
                    rx.spacer(),
                    rx.hstack(
                        pill_tutor("Tutor / Adotante", "salvia"),
                        rx.link(
                            rx.hstack(
                                rx.text("Sair", font_size="15.5px", font_weight="600"),
                                rx.icon(tag="log-out", size=18),
                                spacing="2",
                                align="center",
                            ),
                            on_click=LoginState.sair,
                            color="#8C5843",
                            padding="8px 14px",
                            border_radius="10px",
                            transition="all 0.2s ease",
                            cursor="pointer",
                            _hover={
                                "background": TUTOR_TERRACOTA_SUAVE,
                                "color": TUTOR_TITULO,
                                "text_decoration": "none",
                            },
                        ),
                        spacing="3",
                        align="center",
                    ),
                    max_width="1080px",
                    margin="0 auto",
                    width="100%",
                    align="center",
                ),
                width="100%",
                padding="14px 24px",
                background="rgba(250, 248, 245, 0.94)",
                backdrop_filter="blur(10px)",
                border_bottom=f"1px solid {TUTOR_BORDA}",
                position="sticky",
                top="0",
                z_index="1000",
            ),

            # 2. CONTAINER CENTRAL ENXUTO
            rx.vstack(
                # Saudação + Contadores Rápidos + Barra de Abas
                rx.box(
                    rx.vstack(
                        rx.flex(
                            rx.vstack(
                                rx.heading(
                                    "Olá, ",
                                    rx.cond(
                                        LoginState.nome_usuario != "",
                                        LoginState.nome_usuario,
                                        "Tutor(a)",
                                    ),
                                    "!",
                                    size="7",
                                    color=TUTOR_TITULO,
                                    weight="bold",
                                ),
                                rx.text(
                                    "Um novo começo começa com amor. Gerencie suas adoções e seu perfil em um só lugar.",
                                    size="3",
                                    color=TUTOR_TEXTO_CLARO,
                                ),
                                align="start",
                                spacing="1",
                            ),
                            rx.spacer(),
                            rx.hstack(
                                rx.box(
                                    rx.text(
                                        LoginState.adocoes.length().to_string(),
                                        " adoção(ões)",
                                        font_size="13.5px",
                                        font_weight="600",
                                        color="#9E5E45",
                                    ),
                                    background=TUTOR_TERRACOTA_SUAVE,
                                    border=f"1px solid {TUTOR_TERRACOTA_BORDA}",
                                    padding="6px 14px",
                                    border_radius="999px",
                                ),
                                rx.box(
                                    rx.text(
                                        LoginState.acompanhamentos.length().to_string(),
                                        " visita(s)",
                                        font_size="13.5px",
                                        font_weight="600",
                                        color=TUTOR_SALVIA_ESCURO,
                                    ),
                                    background=TUTOR_SALVIA_SUAVE,
                                    border=f"1px solid {TUTOR_SALVIA_BORDA}",
                                    padding="6px 14px",
                                    border_radius="999px",
                                ),
                                spacing="2",
                                align="center",
                            ),
                            width="100%",
                            align="center",
                            wrap="wrap",
                            gap="12px",
                        ),

                        rx.divider(border_color=TUTOR_BORDA),

                        # Barra de Navegação por Abas
                        rx.hstack(
                            botao_aba_tutor("heart-handshake", "Minhas Adoções", "adocoes"),
                            botao_aba_tutor("calendar-check", "Pós-Adoção e Guias", "acompanhamento"),
                            botao_aba_tutor("user-round", "Meu Perfil", "perfil"),
                            spacing="2",
                            wrap="wrap",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    padding="24px 28px",
                    background=TUTOR_SOFT_WHITE,
                    border_radius="22px",
                    border=f"1px solid {TUTOR_BORDA}",
                    box_shadow="0 6px 20px rgba(44, 37, 25, 0.04)",
                    width="100%",
                ),

                # Conteúdo Dinâmico da Aba Selecionada
                rx.match(
                    LoginState.aba_tutor,
                    ("adocoes", aba_minhas_adocoes()),
                    ("acompanhamento", aba_pos_adocao_guias()),
                    ("perfil", aba_meu_perfil()),
                    aba_minhas_adocoes(),
                ),

                rx.text(
                    "Porto Seguro Pet — Conectando corações e patas.",
                    color=TUTOR_TEXTO_CLARO,
                    size="2",
                    text_align="center",
                    width="100%",
                    padding_top="14px",
                ),
                spacing="5",
                width="100%",
                max_width="1080px",
                margin="0 auto",
                padding=["18px", "26px"],
            ),
            spacing="0",
            width="100%",
            align="stretch",
        ),
        width="100%",
        min_height="100vh",
        background_color="#FFF7ED",
        background_image=BG_PATINHAS_TUTOR,
        background_repeat="repeat",
    )


# Subpáginas de compatibilidade
def pagina_minhas_adocoes() -> rx.Component:
    return area_tutor()


def pagina_acompanhamento() -> rx.Component:
    return area_tutor()


def pagina_meus_dados() -> rx.Component:
    return area_tutor()


def pagina_orientacoes() -> rx.Component:
    return area_tutor()


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
app.add_page(area_administrativa, route="/administrativo")
app.add_page(
    pagina_gestao_animais,
    route="/animais",
    title="Gestão de Animais | Porto Seguro Pet",
)
app.add_page(area_tutor, route="/tutor", on_load=LoginState.iniciar_painel_tutor)
app.add_page(
    pagina_acompanhamento,
    route="/acompanhamento",
    on_load=[LoginState.set_aba_tutor("acompanhamento"), LoginState.iniciar_painel_tutor],
)
app.add_page(
    pagina_meus_dados,
    route="/meus-dados",
    on_load=[LoginState.set_aba_tutor("perfil"), LoginState.iniciar_painel_tutor],
)
app.add_page(
    pagina_orientacoes,
    route="/orientacoes",
    on_load=[LoginState.set_aba_tutor("acompanhamento"), LoginState.iniciar_painel_tutor],
)
app.add_page(pagina_minhas_adocoes, route="/minhas-adocoes")


app.add_page(
    lambda: alterar_senha_page(painel_autenticacao), 
    route="/alterar-senha"
)

app.add_page(
    adocoes_page,
    route="/adocoes",
    title="Adoções | Porto Seguro Pet",
    on_load=AdocoesState.on_load,
)
app.add_page(pos_adocao, route="/pos-adocao", title="Pós-Adoção | Porto Seguro Pet")

app.add_page(
    atendimento_veterinario_page,
    route="/atendimento-vet",
    title="Atendimento Veterinário | Porto Seguro Pet",
)

app.add_page(
    lares_temporarios_page,
    route="/lares-temporarios",
    title="Lares Temporários | Porto Seguro Pet",
    on_load=LaresTemporariosState.on_load,
)

app.add_page(
    doacoes_page,
    route="/doacoes",
    title="Doações | Porto Seguro Pet",
    on_load=DoacoesState.carregar_doadores,
)

app.add_page(
    voluntarios_page,
    route="/voluntarios",
    title="Voluntários | Porto Seguro Pet",
    on_load=VoluntariosState.carregar_dados,
)