
import reflex as rx

from ProjetoONG.state.doacoes_state import DoacoesState
from ProjetoONG.modulos_administracao.menu_administrativo import (
    sidebar_administracao,
)


# ============================================================
# PALETA VISUAL
# ============================================================

COR_PRINCIPAL = "#58392B"
COR_PRINCIPAL_HOVER = "#422A1F"
COR_TITULO = "#2D1F18"
COR_TEXTO = "#52433D"
COR_TEXTO_CLARO = "#66534A"
COR_FUNDO = "#F8F3EC"
COR_CARTAO = "#FFFFFF"
COR_DESTAQUE = "#FFF8F0"
COR_SUCESSO = "#059669"
COR_AVISO = "#D97706"

BORDA = "1px solid #EDE5DC"
SOMBRA_SUAVE = "0 2px 8px rgba(45, 31, 24, 0.04)"


# ============================================================
# COMPONENTES DE APOIO
# ============================================================

def titulo_secao(titulo: str, descricao: str = ""):
    return rx.vstack(
        rx.heading(
            titulo,
            size="5",
            color=COR_TITULO,
            font_weight="700",
        ),
        rx.text(
            descricao,
            color=COR_TEXTO_CLARO,
            font_size="16px",
        ),
        align="start",
        spacing="1",
        width="100%",
    )


def campo_formulario(
    rotulo: str,
    valor,
    setter,
    placeholder: str = "",
):
    return rx.vstack(
        rx.text(
            rotulo,
            color=COR_TEXTO,
            font_size="16px",
            font_weight="600",
        ),
        rx.input(
            value=valor,
            on_change=setter,
            placeholder=placeholder,
            width="100%",
            size="3",
            border_radius="9px",
        ),
        align="start",
        spacing="1",
        width="100%",
    )


def cartao_metrica(titulo: str, valor, icone: str):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    titulo,
                    color=COR_TEXTO_CLARO,
                    font_size="16px",
                    font_weight="500",
                ),
                rx.spacer(),
                rx.icon(
                    icone,
                    color=COR_PRINCIPAL,
                    size=19,
                ),
                width="100%",
                align="center",
            ),
            rx.heading(
                valor,
                size="6",
                color=COR_TITULO,
            ),
            align="start",
            spacing="2",
            width="100%",
        ),
        background=COR_CARTAO,
        border=BORDA,
        border_radius="12px",
        padding="16px",
        box_shadow=SOMBRA_SUAVE,
        width="100%",
    )


def botao_aba(texto: str, identificador: str):
    return rx.button(
        texto,
        on_click=lambda: DoacoesState.selecionar_aba(identificador),
        background=rx.cond(
            DoacoesState.aba_ativa == identificador,
            COR_PRINCIPAL,
            COR_CARTAO,
        ),
        color=rx.cond(
            DoacoesState.aba_ativa == identificador,
            "#FFFFFF",
            COR_TEXTO,
        ),
        border=rx.cond(
            DoacoesState.aba_ativa == identificador,
            f"1px solid {COR_PRINCIPAL}",
            BORDA,
        ),
        border_radius="9px",
        size="3",
        _hover={
            "background": COR_PRINCIPAL_HOVER,
            "color": "#FFFFFF",
        },
    )


# ============================================================
# ABA: DOADORES
# ============================================================

def formulario_doador():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("user-plus", color=COR_PRINCIPAL, size=20),
                rx.heading(
                    "Cadastrar doador",
                    size="4",
                    color=COR_TITULO,
                ),
                align="center",
                spacing="2",
            ),

            campo_formulario(
                "Nome",
                DoacoesState.nome_doador,
                DoacoesState.set_nome_doador,
                "Nome completo ou nome da organização",
            ),

            campo_formulario(
                "CPF",
                DoacoesState.cpf_doador,
                DoacoesState.set_cpf_doador,
                "000.000.000-00",
            ),

            campo_formulario(
                "Telefone",
                DoacoesState.telefone_doador,
                DoacoesState.set_telefone_doador,
                "(00) 00000-0000",
            ),

            campo_formulario(
                "E-mail",
                DoacoesState.email_doador,
                DoacoesState.set_email_doador,
                "email@exemplo.com",
            ),

            rx.button(
                rx.icon("plus", size=16),
                "Cadastrar doador",
                on_click=DoacoesState.cadastrar_doador,
                background=COR_PRINCIPAL,
                color="#FFFFFF",
                width="100%",
                _hover={"background": COR_PRINCIPAL_HOVER},
            ),

            rx.text(
                DoacoesState.mensagem,
                color=COR_SUCESSO,
                font_size="16px",
            ),

            align="start",
            spacing="3",
            width="100%",
        ),
        background=COR_CARTAO,
        border=BORDA,
        border_radius="14px",
        padding="18px",
        width="100%",
        box_shadow=SOMBRA_SUAVE,
    )


def cartao_doador(doador: dict):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.center(
                    rx.icon(
                        "user-round",
                        color=COR_PRINCIPAL,
                        size=19,
                    ),
                    background=COR_DESTAQUE,
                    width="38px",
                    height="38px",
                    border_radius="10px",
                ),
                rx.vstack(
                    rx.text(
                        doador["nome"],
                        color=COR_TITULO,
                        font_weight="600",
                    ),
                    rx.text(
                        rx.cond(
                            doador["cpf"] != "",
                            "CPF: " + doador["cpf"],
                            "Pessoa jurídica / sem CPF informado",
                        ),
                        color=COR_TEXTO_CLARO,
                        font_size="14px",
                    ),
                    align="start",
                    spacing="0",
                    flex="1",
                    min_width="0",
                ),
                width="100%",
                align="center",
                spacing="2",
            ),

            rx.divider(color="#EEE5DC"),

            rx.text(
                "Telefone: " + doador["telefone"],
                color=COR_TEXTO,
                font_size="16px",
            ),

            rx.text(
                "E-mail: " + doador["email"],
                color=COR_TEXTO,
                font_size="16px",
            ),

            align="start",
            spacing="2",
            width="100%",
        ),
        background=COR_CARTAO,
        border=BORDA,
        border_radius="11px",
        padding="12px",
        width="100%",
    )


def aba_doadores():
    return rx.vstack(
        titulo_secao(
            "Cadastro de doadores",
            "Cadastre e consulte as pessoas e organizações que contribuem com a ONG.",
        ),

        rx.grid(
            formulario_doador(),

            rx.vstack(
                rx.hstack(
                    rx.heading(
                        "Doadores cadastrados",
                        size="4",
                        color=COR_TITULO,
                    ),
                    rx.spacer(),
                    rx.badge(
                        DoacoesState.quantidade_doadores,
                        color_scheme="brown",
                        variant="soft",
                    ),
                    width="100%",
                    align="center",
                ),

                rx.input(
                    placeholder="Pesquisar por nome ou CPF...",
                    value=DoacoesState.filtro_doador,
                    on_change=DoacoesState.set_filtro_doador,
                    width="100%",
                    size="3",
                    border_radius="9px",
                ),

                rx.foreach(
                    DoacoesState.doadores_filtrados,
                    cartao_doador,
                ),

                rx.cond(
                    DoacoesState.doadores_filtrados.length() == 0,
                    rx.text(
                        "Nenhum doador encontrado.",
                        color=COR_TEXTO_CLARO,
                        font_size="16px",
                    ),
                    rx.box(),
                ),

                background=COR_CARTAO,
                border=BORDA,
                border_radius="14px",
                padding="18px",
                width="100%",
                align="start",
                spacing="3",
            ),

            columns={"initial": "1", "md": "2"},
            spacing="4",
            width="100%",
            align="start",
        ),

        width="100%",
        align="start",
        spacing="4",
    )


# ============================================================
# SELEÇÃO DE DOADOR PARA UMA DOAÇÃO
# ============================================================

def opcao_doador(doador: dict):
    return rx.button(
        rx.hstack(
            rx.text(
                doador["nome"],
                font_size="16px",
            ),
            rx.spacer(),
            rx.cond(
                DoacoesState.doador_selecionado_id == doador["id"],
                rx.icon("check-check", color=COR_SUCESSO, size=17),
                rx.icon("circle", color=COR_TEXTO_CLARO, size=17),
            ),
            width="100%",
            align="center",
        ),
        on_click=lambda: DoacoesState.set_doador_selecionado(
            doador["id"]
        ),
        background=rx.cond(
            DoacoesState.doador_selecionado_id == doador["id"],
            COR_DESTAQUE,
            COR_CARTAO,
        ),
        color=COR_TEXTO,
        border=rx.cond(
            DoacoesState.doador_selecionado_id == doador["id"],
            f"1px solid {COR_PRINCIPAL}",
            BORDA,
        ),
        width="100%",
        justify="start",
        size="2",
    )


def selecao_doador():
    return rx.vstack(
        rx.text(
            "Selecione o doador",
            color=COR_TEXTO,
            font_size="16px",
            font_weight="600",
        ),

        rx.foreach(
            DoacoesState.doadores,
            opcao_doador,
        ),

        align="start",
        spacing="2",
        width="100%",
        max_height="180px",
        overflow_y="auto",
    )


# ============================================================
# ABA: DOAÇÕES FINANCEIRAS
# ============================================================

def aba_doacoes_financeiras():
    return rx.vstack(
        titulo_secao(
            "Doações financeiras",
            "Registre os valores recebidos e consulte os respectivos registros.",
        ),

        rx.grid(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            "hand-coins",
                            color=COR_PRINCIPAL,
                            size=20,
                        ),
                        rx.heading(
                            "Registrar doação financeira",
                            size="4",
                            color=COR_TITULO,
                        ),
                        align="center",
                        spacing="2",
                    ),

                    selecao_doador(),

                    campo_formulario(
                        "Valor recebido (R$)",
                        DoacoesState.valor_doacao,
                        DoacoesState.set_valor_doacao,
                        "Ex.: 150,00",
                    ),

                    campo_formulario(
                        "Data do recebimento",
                        DoacoesState.data_doacao,
                        DoacoesState.set_data_doacao,
                        "DD/MM/AAAA",
                    ),

                    rx.button(
                        rx.icon("plus", size=16),
                        "Registrar doação",
                        on_click=DoacoesState.registrar_doacao_financeira,
                        background=COR_PRINCIPAL,
                        color="#FFFFFF",
                        width="100%",
                        _hover={"background": COR_PRINCIPAL_HOVER},
                    ),

                    rx.text(
                        DoacoesState.mensagem,
                        color=COR_SUCESSO,
                        font_size="16px",
                    ),

                    align="start",
                    spacing="3",
                    width="100%",
                ),
                background=COR_CARTAO,
                border=BORDA,
                border_radius="14px",
                padding="18px",
                width="100%",
            ),

            rx.vstack(
                rx.heading(
                    "Registros financeiros",
                    size="4",
                    color=COR_TITULO,
                ),

                rx.foreach(
                    DoacoesState.doacoes_com_doador,
                    item_doacao_financeira,
                ),

                align="start",
                spacing="3",
                background=COR_CARTAO,
                border=BORDA,
                border_radius="14px",
                padding="18px",
                width="100%",
            ),

            columns={"initial": "1", "md": "2"},
            spacing="4",
            width="100%",
            align="start",
        ),

        width="100%",
        spacing="4",
        align="start",
    )


def item_doacao_financeira(doacao: dict):
    return rx.cond(
        doacao["tipo_doacao"] == "Financeira",
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        doacao["nome_doador"],
                        color=COR_TITULO,
                        font_weight="600",
                    ),
                    rx.spacer(),
                    rx.badge(
                        "Financeira",
                        color_scheme="green",
                        variant="soft",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.heading(
                    "R$ " + doacao["valor"],
                    size="5",
                    color=COR_SUCESSO,
                ),
                rx.text(
                    "Recebida em " + doacao["data_doacao"],
                    color=COR_TEXTO_CLARO,
                    font_size="14px",
                ),
                align="start",
                spacing="1",
                width="100%",
            ),
            padding="12px",
            border=BORDA,
            border_radius="10px",
            width="100%",
        ),
        rx.box(),
    )


# ============================================================
# ABA: DOAÇÕES MATERIAIS
# ============================================================

def aba_doacoes_materiais():
    return rx.vstack(
        titulo_secao(
            "Doações materiais",
            "Registre os materiais recebidos pela ONG, com sua descrição e data de recebimento.",
        ),

        rx.grid(
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            "package-check",
                            color=COR_PRINCIPAL,
                            size=20,
                        ),
                        rx.heading(
                            "Registrar doação material",
                            size="4",
                            color=COR_TITULO,
                        ),
                        align="center",
                        spacing="2",
                    ),

                    selecao_doador(),

                    rx.vstack(
                        rx.text(
                            "Descrição do material recebido",
                            color=COR_TEXTO,
                            font_size="16px",
                            font_weight="600",
                        ),
                        rx.text_area(
                            value=DoacoesState.descricao_doacao,
                            on_change=DoacoesState.set_descricao_doacao,
                            placeholder="Descreva os materiais recebidos...",
                            width="100%",
                            min_height="100px",
                        ),
                        align="start",
                        spacing="1",
                        width="100%",
                    ),

                    campo_formulario(
                        "Data do recebimento",
                        DoacoesState.data_doacao,
                        DoacoesState.set_data_doacao,
                        "DD/MM/AAAA",
                    ),

                    rx.button(
                        rx.icon("plus", size=16),
                        "Registrar recebimento",
                        on_click=DoacoesState.registrar_doacao_material,
                        background=COR_PRINCIPAL,
                        color="#FFFFFF",
                        width="100%",
                        _hover={"background": COR_PRINCIPAL_HOVER},
                    ),

                    rx.text(
                        DoacoesState.mensagem,
                        color=COR_SUCESSO,
                        font_size="16px",
                    ),

                    align="start",
                    spacing="3",
                    width="100%",
                ),
                background=COR_CARTAO,
                border=BORDA,
                border_radius="14px",
                padding="18px",
                width="100%",
            ),

            rx.vstack(
                rx.heading(
                    "Materiais recebidos",
                    size="4",
                    color=COR_TITULO,
                ),

                rx.foreach(
                    DoacoesState.doacoes_com_doador,
                    item_doacao_material,
                ),

                align="start",
                spacing="3",
                background=COR_CARTAO,
                border=BORDA,
                border_radius="14px",
                padding="18px",
                width="100%",
            ),

            columns={"initial": "1", "md": "2"},
            spacing="4",
            width="100%",
            align="start",
        ),

        width="100%",
        spacing="4",
        align="start",
    )


def item_doacao_material(doacao: dict):
    return rx.cond(
        doacao["tipo_doacao"] == "Material",
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        doacao["nome_doador"],
                        color=COR_TITULO,
                        font_weight="600",
                    ),
                    rx.spacer(),
                    rx.badge(
                        "Material",
                        color_scheme="orange",
                        variant="soft",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.text(
                    doacao["descricao"],
                    color=COR_TEXTO,
                    font_size="16px",
                ),
                rx.text(
                    "Recebida em " + doacao["data_doacao"],
                    color=COR_TEXTO_CLARO,
                    font_size="14px",
                ),
                align="start",
                spacing="1",
                width="100%",
            ),
            padding="12px",
            border=BORDA,
            border_radius="10px",
            width="100%",
        ),
        rx.box(),
    )


# ============================================================
# ABA: HISTÓRICO
# ============================================================

def item_historico(doacao: dict):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        doacao["nome_doador"],
                        color=COR_TITULO,
                        font_weight="600",
                    ),
                    rx.text(
                        doacao["data_doacao"],
                        color=COR_TEXTO_CLARO,
                        font_size="14px",
                    ),
                    align="start",
                    spacing="0",
                ),
                rx.spacer(),
                rx.badge(
                    doacao["tipo_doacao"],
                    color_scheme=rx.cond(
                        doacao["tipo_doacao"] == "Financeira",
                        "green",
                        "orange",
                    ),
                    variant="soft",
                ),
                width="100%",
                align="center",
            ),

            rx.cond(
                doacao["tipo_doacao"] == "Financeira",
                rx.heading(
                    "R$ " + doacao["valor"],
                    size="4",
                    color=COR_SUCESSO,
                ),
                rx.text(
                    doacao["descricao"],
                    color=COR_TEXTO,
                    font_size="16px",
                ),
            ),

            align="start",
            spacing="2",
            width="100%",
        ),
        background=COR_CARTAO,
        border=BORDA,
        border_radius="10px",
        padding="14px",
        width="100%",
    )


def aba_historico():
    return rx.vstack(
        titulo_secao(
            "Histórico de doações",
            "Consulte todos os recebimentos financeiros e materiais registrados.",
        ),

        rx.foreach(
            DoacoesState.doacoes_com_doador,
            item_historico,
        ),

        width="100%",
        align="start",
        spacing="3",
    )


# ============================================================
# RESUMO E ÚLTIMAS DOAÇÕES
# ============================================================

def item_ultima_doacao(doacao: dict):
    return rx.hstack(
        rx.text(
            doacao["data_doacao"],
            color=COR_TEXTO,
            font_size="16px",
            width="100px",
        ),

        rx.badge(
            doacao["tipo_doacao"],
            color_scheme=rx.cond(
                doacao["tipo_doacao"] == "Financeira",
                "green",
                "orange",
            ),
            variant="soft",
        ),

        rx.text(
            doacao["nome_doador"],
            color=COR_TEXTO,
            font_size="16px",
            flex="1",
        ),

        rx.text(
            rx.cond(
                doacao["tipo_doacao"] == "Financeira",
                "R$ " + doacao["valor"],
                doacao["descricao"],
            ),
            color=COR_TEXTO,
            font_size="16px",
            flex="1",
        ),

        width="100%",
        align="center",
        spacing="2",
        padding="10px",
        border_bottom=BORDA,
    )


def secao_resumo_doacoes():
    return rx.grid(
        # RESUMO DE DOAÇÕES
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon(
                        "chart-no-axes-column-increasing",
                        color=COR_PRINCIPAL,
                    ),
                    rx.heading(
                        "Resumo de Doações",
                        size="4",
                        color=COR_TITULO,
                    ),
                    align="center",
                    spacing="2",
                ),

                rx.grid(
                    cartao_metrica(
                        "Total financeiro recebido",
                        "R$ " + DoacoesState.total_doacoes_financeiras.to_string(),
                        "heart",
                    ),

                    cartao_metrica(
                        "Doações registradas",
                        DoacoesState.quantidade_doacoes,
                        "handshake",
                    ),

                    cartao_metrica(
                        "Doadores cadastrados",
                        DoacoesState.quantidade_doadores,
                        "users",
                    ),

                    columns={
                        "initial": "1",
                        "sm": "3",
                    },
                    spacing="2",
                    width="100%",
                ),

                width="100%",
                align="start",
                spacing="3",
            ),

            background=COR_DESTAQUE,
            border=BORDA,
            border_radius="14px",
            padding="16px",
            width="100%",
        ),

        # ÚLTIMAS DOAÇÕES
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon(
                        "clock",
                        color=COR_PRINCIPAL,
                    ),

                    rx.heading(
                        "Últimas Doações",
                        size="4",
                        color=COR_TITULO,
                    ),

                    rx.spacer(),

                    rx.button(
                        "Ver todas",
                        on_click=lambda: DoacoesState.selecionar_aba(
                            "historico"
                        ),
                        size="2",
                        variant="soft",
                        color_scheme="brown",
                    ),

                    width="100%",
                    align="center",
                ),

                rx.foreach(
                    DoacoesState.doacoes_com_doador,
                    item_ultima_doacao,
                ),

                width="100%",
                align="start",
                spacing="2",
            ),

            background=COR_CARTAO,
            border=BORDA,
            border_radius="14px",
            padding="16px",
            width="100%",
        ),

        columns={
            "initial": "1",
            "lg": "2",
        },
        spacing="3",
        width="100%",
        align="start",
    )


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

def doacoes_page():
    return rx.box(
        rx.hstack(
            # MENU ADMINISTRATIVO
            rx.box(
                sidebar_administracao(),
                width="250px",
                min_width="250px",
                height="100vh",
                position="sticky",
                top="0",
            ),

            # CONTEÚDO PRINCIPAL
            rx.box(
                rx.vstack(
                    # CABEÇALHO
                    rx.vstack(
                        rx.heading(
                            "Doações",
                            size="7",
                            color=COR_TITULO,
                            font_weight="700",
                        ),

                        rx.text(
                            "Gerencie os doadores e organize os registros "
                            "de doações recebidas pela ONG.",
                            color=COR_TEXTO_CLARO,
                            font_size="18px",
                        ),

                        align="start",
                        spacing="1",
                        width="100%",
                    ),

                    # ABAS
                    rx.flex(
                        botao_aba("Doadores", "doadores"),
                        botao_aba("Doações Financeiras", "financeiras"),
                        botao_aba("Doações Materiais", "materiais"),
                        botao_aba("Histórico", "historico"),
                        width="100%",
                        spacing="2",
                        wrap="wrap",
                    ),

                    # CONTEÚDO DAS ABAS
                    rx.cond(
                        DoacoesState.aba_ativa == "doadores",
                        aba_doadores(),

                        rx.cond(
                            DoacoesState.aba_ativa == "financeiras",
                            aba_doacoes_financeiras(),

                            rx.cond(
                                DoacoesState.aba_ativa == "materiais",
                                aba_doacoes_materiais(),
                                aba_historico(),
                            ),
                        ),
                    ),

                    # RESUMO E ÚLTIMAS DOAÇÕES NA PARTE INFERIOR
                    secao_resumo_doacoes(),

                    align="start",
                    spacing="5",
                    width="100%",
                ),

                padding="28px",
                width="100%",
                min_height="100vh",
                background=COR_FUNDO,
                flex="1",
            ),

            width="100%",
            align="start",
            spacing="0",
        ),

        width="100%",
        min_height="100vh",
        background=COR_FUNDO,
    )
