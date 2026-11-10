import reflex as rx

from ProjetoONG.state.voluntarios_state import VoluntariosState
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
        on_click=lambda: VoluntariosState.selecionar_aba(identificador),
        background=rx.cond(
            VoluntariosState.aba_ativa == identificador,
            COR_PRINCIPAL,
            COR_CARTAO,
        ),
        color=rx.cond(
            VoluntariosState.aba_ativa == identificador,
            "#FFFFFF",
            COR_TEXTO,
        ),
        border=rx.cond(
            VoluntariosState.aba_ativa == identificador,
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


def cartao_padrao(conteudo):
    return rx.box(
        conteudo,
        background=COR_CARTAO,
        border=BORDA,
        border_radius="14px",
        padding="18px",
        width="100%",
        box_shadow=SOMBRA_SUAVE,
    )


# ============================================================
# ABA: VOLUNTÁRIOS
# ============================================================

def formulario_voluntario():
    return cartao_padrao(
        rx.vstack(
            rx.hstack(
                rx.icon("user-plus", color=COR_PRINCIPAL, size=20),
                rx.heading(
                    "Cadastrar voluntário",
                    size="4",
                    color=COR_TITULO,
                ),
                align="center",
                spacing="2",
            ),

            campo_formulario(
                "Nome",
                VoluntariosState.nome_voluntario,
                VoluntariosState.set_nome_voluntario,
                "Nome completo",
            ),

            campo_formulario(
                "Telefone",
                VoluntariosState.telefone_voluntario,
                VoluntariosState.set_telefone_voluntario,
                "(00) 00000-0000",
            ),

            campo_formulario(
                "E-mail",
                VoluntariosState.email_voluntario,
                VoluntariosState.set_email_voluntario,
                "email@exemplo.com",
            ),

            rx.vstack(
                rx.text(
                    "Status",
                    color=COR_TEXTO,
                    font_size="16px",
                    font_weight="600",
                ),
                rx.select(
                    ["Ativo", "Inativo"],
                    value=VoluntariosState.status_voluntario,
                    on_change=VoluntariosState.set_status_voluntario,
                    width="100%",
                ),
                align="start",
                spacing="1",
                width="100%",
            ),

            rx.button(
                rx.icon("plus", size=16),
                "Cadastrar voluntário",
                on_click=VoluntariosState.cadastrar_voluntario,
                background=COR_PRINCIPAL,
                color="#FFFFFF",
                width="100%",
                _hover={"background": COR_PRINCIPAL_HOVER},
            ),

            rx.text(
                VoluntariosState.mensagem,
                color=COR_SUCESSO,
                font_size="16px",
            ),

            align="start",
            spacing="3",
            width="100%",
        )
    )


def cartao_voluntario(voluntario: dict):
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
                        voluntario["nome"],
                        color=COR_TITULO,
                        font_weight="600",
                    ),
                    rx.text(
                        voluntario["email"],
                        color=COR_TEXTO_CLARO,
                        font_size="14px",
                    ),
                    align="start",
                    spacing="0",
                    flex="1",
                    min_width="0",
                ),
                rx.badge(
                    voluntario["status"],
                    color_scheme=rx.cond(
                        voluntario["status"] == "Ativo",
                        "green",
                        "gray",
                    ),
                    variant="soft",
                ),
                width="100%",
                align="center",
                spacing="2",
            ),

            rx.divider(color="#EEE5DC"),

            rx.text(
                "Telefone: " + voluntario["telefone"],
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


def aba_voluntarios():
    return rx.vstack(
        titulo_secao(
            "Cadastro de voluntários",
            "Cadastre e consulte as pessoas que colaboram com as atividades da ONG.",
        ),

        rx.grid(
            formulario_voluntario(),

            rx.vstack(
                rx.hstack(
                    rx.heading(
                        "Voluntários cadastrados",
                        size="4",
                        color=COR_TITULO,
                    ),
                    rx.spacer(),
                    rx.badge(
                        VoluntariosState.quantidade_voluntarios,
                        color_scheme="brown",
                        variant="soft",
                    ),
                    width="100%",
                    align="center",
                ),

                rx.input(
                    placeholder="Pesquisar por nome, telefone ou e-mail...",
                    value=VoluntariosState.filtro_voluntario,
                    on_change=VoluntariosState.set_filtro_voluntario,
                    width="100%",
                    size="3",
                    border_radius="9px",
                ),

                rx.foreach(
                    VoluntariosState.voluntarios_filtrados,
                    cartao_voluntario,
                ),

                rx.cond(
                    VoluntariosState.voluntarios_filtrados.length() == 0,
                    rx.text(
                        "Nenhum voluntário encontrado.",
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
# ABA: ATIVIDADES
# ============================================================

def formulario_atividade():
    return cartao_padrao(
        rx.vstack(
            rx.hstack(
                rx.icon("calendar-plus", color=COR_PRINCIPAL, size=20),
                rx.heading(
                    "Cadastrar atividade",
                    size="4",
                    color=COR_TITULO,
                ),
                align="center",
                spacing="2",
            ),

            campo_formulario(
                "Tipo de atividade",
                VoluntariosState.tipo_atividade,
                VoluntariosState.set_tipo_atividade,
                "Ex.: Feira de adoção",
            ),

            campo_formulario(
                "Data da atividade",
                VoluntariosState.data_atividade,
                VoluntariosState.set_data_atividade,
                "DD/MM/AAAA",
            ),

            rx.vstack(
                rx.text(
                    "Descrição",
                    color=COR_TEXTO,
                    font_size="16px",
                    font_weight="600",
                ),
                rx.text_area(
                    value=VoluntariosState.descricao_atividade,
                    on_change=VoluntariosState.set_descricao_atividade,
                    placeholder="Descreva a atividade...",
                    width="100%",
                    min_height="100px",
                ),
                align="start",
                spacing="1",
                width="100%",
            ),

            rx.button(
                rx.icon("plus", size=16),
                "Cadastrar atividade",
                on_click=VoluntariosState.cadastrar_atividade,
                background=COR_PRINCIPAL,
                color="#FFFFFF",
                width="100%",
                _hover={"background": COR_PRINCIPAL_HOVER},
            ),

            rx.text(
                VoluntariosState.mensagem,
                color=COR_SUCESSO,
                font_size="16px",
            ),

            align="start",
            spacing="3",
            width="100%",
        )
    )


def cartao_atividade(atividade: dict):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.center(
                    rx.icon(
                        "calendar-days",
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
                        atividade["tipo_atividade"],
                        color=COR_TITULO,
                        font_weight="600",
                    ),
                    rx.text(
                        atividade["data_atividade"],
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
                rx.cond(
                    atividade["descricao"] != "",
                    atividade["descricao"],
                    "Sem descrição informada.",
                ),
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


def aba_atividades():
    return rx.vstack(
        titulo_secao(
            "Cadastro de atividades",
            "Registre e consulte as atividades realizadas pela ONG.",
        ),

        rx.grid(
            formulario_atividade(),

            rx.vstack(
                rx.hstack(
                    rx.heading(
                        "Atividades cadastradas",
                        size="4",
                        color=COR_TITULO,
                    ),
                    rx.spacer(),
                    rx.badge(
                        VoluntariosState.quantidade_atividades,
                        color_scheme="brown",
                        variant="soft",
                    ),
                    width="100%",
                    align="center",
                ),

                rx.input(
                    placeholder="Pesquisar por tipo de atividade...",
                    value=VoluntariosState.filtro_atividade,
                    on_change=VoluntariosState.set_filtro_atividade,
                    width="100%",
                    size="3",
                    border_radius="9px",
                ),

                rx.foreach(
                    VoluntariosState.atividades_filtradas,
                    cartao_atividade,
                ),

                rx.cond(
                    VoluntariosState.atividades_filtradas.length() == 0,
                    rx.text(
                        "Nenhuma atividade encontrada.",
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
# ABA: PARTICIPAÇÕES E HISTÓRICO
# ============================================================

def opcao_voluntario(voluntario: dict):
    return rx.button(
        rx.hstack(
            rx.text(
                voluntario["nome"],
                font_size="16px",
            ),
            rx.spacer(),
            rx.cond(
                VoluntariosState.voluntario_selecionado_id == voluntario["id"],
                rx.icon("check-check", color=COR_SUCESSO, size=17),
                rx.icon("circle", color=COR_TEXTO_CLARO, size=17),
            ),
            width="100%",
            align="center",
        ),
        on_click=lambda: VoluntariosState.set_voluntario_selecionado_id(
            voluntario["id"]
        ),
        background=rx.cond(
            VoluntariosState.voluntario_selecionado_id == voluntario["id"],
            COR_DESTAQUE,
            COR_CARTAO,
        ),
        color=COR_TEXTO,
        border=rx.cond(
            VoluntariosState.voluntario_selecionado_id == voluntario["id"],
            f"1px solid {COR_PRINCIPAL}",
            BORDA,
        ),
        width="100%",
        justify="start",
        size="2",
    )


def opcao_atividade(atividade: dict):
    return rx.button(
        rx.hstack(
            rx.vstack(
                rx.text(
                    atividade["tipo_atividade"],
                    font_size="16px",
                ),
                rx.text(
                    atividade["data_atividade"],
                    font_size="14px",
                    color=COR_TEXTO_CLARO,
                ),
                align="start",
                spacing="0",
            ),
            rx.spacer(),
            rx.cond(
                VoluntariosState.atividade_selecionada_id == atividade["id"],
                rx.icon("check-check", color=COR_SUCESSO, size=17),
                rx.icon("circle", color=COR_TEXTO_CLARO, size=17),
            ),
            width="100%",
            align="center",
        ),
        on_click=lambda: VoluntariosState.set_atividade_selecionada_id(
            atividade["id"]
        ),
        background=rx.cond(
            VoluntariosState.atividade_selecionada_id == atividade["id"],
            COR_DESTAQUE,
            COR_CARTAO,
        ),
        color=COR_TEXTO,
        border=rx.cond(
            VoluntariosState.atividade_selecionada_id == atividade["id"],
            f"1px solid {COR_PRINCIPAL}",
            BORDA,
        ),
        width="100%",
        justify="start",
        size="2",
    )


def formulario_participacao():
    return cartao_padrao(
        rx.vstack(
            rx.hstack(
                rx.icon("user-round-plus", color=COR_PRINCIPAL, size=20),
                rx.heading(
                    "Registrar participação",
                    size="4",
                    color=COR_TITULO,
                ),
                align="center",
                spacing="2",
            ),

            rx.text(
                "Selecione o voluntário",
                color=COR_TEXTO,
                font_size="16px",
                font_weight="600",
            ),

            rx.vstack(
                rx.foreach(
                    VoluntariosState.voluntarios,
                    opcao_voluntario,
                ),
                width="100%",
                max_height="150px",
                overflow_y="auto",
                spacing="2",
            ),

            rx.divider(color="#EEE5DC"),

            rx.text(
                "Selecione a atividade",
                color=COR_TEXTO,
                font_size="16px",
                font_weight="600",
            ),

            rx.vstack(
                rx.foreach(
                    VoluntariosState.atividades,
                    opcao_atividade,
                ),
                width="100%",
                max_height="150px",
                overflow_y="auto",
                spacing="2",
            ),

            campo_formulario(
                "Função na atividade",
                VoluntariosState.funcao_na_atividade,
                VoluntariosState.set_funcao_na_atividade,
                "Ex.: Organização e recepção",
            ),

            rx.button(
                rx.icon("plus", size=16),
                "Registrar participação",
                on_click=VoluntariosState.associar_voluntario_atividade,
                background=COR_PRINCIPAL,
                color="#FFFFFF",
                width="100%",
                _hover={"background": COR_PRINCIPAL_HOVER},
            ),

            rx.text(
                VoluntariosState.mensagem,
                color=COR_SUCESSO,
                font_size="16px",
            ),

            align="start",
            spacing="3",
            width="100%",
        )
    )


def item_participacao(participacao: dict):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(
                        participacao["nome_voluntario"],
                        color=COR_TITULO,
                        font_weight="600",
                    ),
                    rx.text(
                        participacao["tipo_atividade"],
                        color=COR_TEXTO,
                        font_size="16px",
                    ),
                    align="start",
                    spacing="0",
                ),
                rx.spacer(),
                rx.badge(
                    participacao["data_atividade"],
                    color_scheme="brown",
                    variant="soft",
                ),
                width="100%",
                align="center",
            ),

            rx.cond(
                participacao["funcao_na_atividade"] != "",
                rx.text(
                    "Função: " + participacao["funcao_na_atividade"],
                    color=COR_TEXTO_CLARO,
                    font_size="16px",
                ),
                rx.box(),
            ),

            align="start",
            spacing="2",
            width="100%",
        ),
        background=COR_CARTAO,
        border=BORDA,
        border_radius="10px",
        padding="12px",
        width="100%",
    )


def aba_participacoes():
    return rx.vstack(
        titulo_secao(
            "Participações e histórico",
            "Associe voluntários às atividades e consulte os registros de participação.",
        ),

        rx.grid(
            formulario_participacao(),

            rx.vstack(
                rx.hstack(
                    rx.heading(
                        "Histórico de participações",
                        size="4",
                        color=COR_TITULO,
                    ),
                    rx.spacer(),
                    rx.badge(
                        VoluntariosState.quantidade_participacoes,
                        color_scheme="brown",
                        variant="soft",
                    ),
                    width="100%",
                    align="center",
                ),

                rx.input(
                    placeholder="Pesquisar por voluntário ou atividade...",
                    value=VoluntariosState.filtro_historico,
                    on_change=VoluntariosState.set_filtro_historico,
                    width="100%",
                    size="3",
                    border_radius="9px",
                ),

                rx.foreach(
                    VoluntariosState.historico_filtrado,
                    item_participacao,
                ),

                rx.cond(
                    VoluntariosState.historico_filtrado.length() == 0,
                    rx.text(
                        "Nenhuma participação encontrada.",
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
# PÁGINA PRINCIPAL
# ============================================================

def voluntarios_page():
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
                            "Voluntários",
                            size="7",
                            color=COR_TITULO,
                            font_weight="700",
                        ),
                        rx.text(
                            "Organize os voluntários, as atividades da ONG "
                            "e os registros de participação.",
                            color=COR_TEXTO_CLARO,
                            font_size="18px",
                        ),
                        align="start",
                        spacing="1",
                        width="100%",
                    ),

                    # INDICADORES
                    rx.grid(
                        cartao_metrica(
                            "Voluntários cadastrados",
                            VoluntariosState.quantidade_voluntarios,
                            "users",
                        ),
                        cartao_metrica(
                            "Atividades cadastradas",
                            VoluntariosState.quantidade_atividades,
                            "calendar-days",
                        ),
                        cartao_metrica(
                            "Participações registradas",
                            VoluntariosState.quantidade_participacoes,
                            "handshake",
                        ),
                        columns={
                            "initial": "1",
                            "sm": "2",
                            "lg": "3",
                        },
                        spacing="3",
                        width="100%",
                    ),

                    # ABAS
                    rx.flex(
                        botao_aba("Voluntários", "voluntarios"),
                        botao_aba("Atividades", "atividades"),
                        botao_aba("Participações e histórico", "participacoes"),
                        width="100%",
                        spacing="2",
                        wrap="wrap",
                    ),

                    # CONTEÚDO DAS ABAS
                    rx.cond(
                        VoluntariosState.aba_ativa == "voluntarios",
                        aba_voluntarios(),
                        rx.cond(
                            VoluntariosState.aba_ativa == "atividades",
                            aba_atividades(),
                            aba_participacoes(),
                        ),
                    ),

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
