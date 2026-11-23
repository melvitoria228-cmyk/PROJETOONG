import reflex as rx

from ProjetoONG.state.voluntarios_state import VoluntariosState
from ProjetoONG.modulos_administracao.menu_administrativo import (
    sidebar_administracao,
)


# ============================================================
# PALETA VISUAL OFICIAL (PORTO SEGURO PET)
# ============================================================

COR_PRINCIPAL = "#C77D5B"          # Terracota
COR_PRINCIPAL_HOVER = "#B26B4B"    # Terracota hover
COR_PRINCIPAL_SUAVE = "#F3E5DE"    # Terracota claro (fundo de card/ícone)

COR_OLIVA = "#A3A66B"              # Verde oliva
COR_OLIVA_SUAVE = "#E7EAD6"        # Verde oliva claro (fundo de card/badge)
COR_OLIVA_TEXTO = "#5A5E36"        # Verde oliva escuro (texto de badge)

COR_AREIA = "#EFE6DA"              # Areia
COR_CARAMELO = "#D6B99A"           # Caramelo

COR_TITULO = "#2C2523"             # Grafite quente
COR_TEXTO = "#4F4643"              # Texto padrão
COR_TEXTO_CLARO = "#756A66"        # Subtítulos e descrições
COR_FUNDO = "#F8F3EC"              # Bege claro (fundo da página)
COR_CARTAO = "#FFFFFF"             # Branco (cards de conteúdo)
COR_DESTAQUE = "#F7EFEA"           # Destaque sutil terracota

COR_SUCESSO = "#6D7A3E"            # Oliva de confirmação
COR_AVISO = "#C77D5B"              # Terracota de destaque

BORDA = "1px solid #E5DDD3"
SOMBRA_SUAVE = "0 2px 8px rgba(44, 37, 35, 0.04)"


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
            font_size="15px",
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
            font_size="15px",
            font_weight="600",
        ),
        rx.input(
            value=valor,
            on_change=setter,
            placeholder=placeholder,
            width="100%",
            size="3",
            border_radius="9px",
            background=COR_CARTAO,
        ),
        align="start",
        spacing="1",
        width="100%",
    )


def indicador_compacto(
    titulo: str,
    valor,
    icone: str,
    fundo: str = COR_PRINCIPAL_SUAVE,
    borda_cor: str = "#E6CFC3",
    cor_icone: str = COR_PRINCIPAL,
    cor_valor: str = COR_TITULO,
):
    return rx.box(
        rx.hstack(
            rx.center(
                rx.icon(
                    icone,
                    color=cor_icone,
                    size=17,
                ),
                background=COR_CARTAO,
                border=f"1px solid {borda_cor}",
                width="34px",
                height="34px",
                border_radius="9px",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(
                    titulo,
                    color=COR_TEXTO_CLARO,
                    font_size="12px",
                    font_weight="600",
                    line_height="1.1",
                ),
                rx.text(
                    valor,
                    color=cor_valor,
                    font_size="19px",
                    font_weight="700",
                    line_height="1.2",
                ),
                align="start",
                spacing="0",
            ),
            align="center",
            spacing="3",
            width="100%",
        ),
        background=fundo,
        border=f"1px solid {borda_cor}",
        border_radius="11px",
        padding="10px 14px",
        width="100%",
    )


def botao_aba(texto: str, identificador: str):
    ativo = VoluntariosState.aba_ativa == identificador
    return rx.button(
        texto,
        on_click=lambda: VoluntariosState.selecionar_aba(identificador),
        background=rx.cond(ativo, COR_PRINCIPAL, COR_CARTAO),
        color=rx.cond(ativo, "#FFFFFF", COR_TEXTO),
        border=rx.cond(ativo, f"1px solid {COR_PRINCIPAL}", BORDA),
        border_radius="10px",
        font_weight="600",
        size="3",
        cursor="pointer",
        _hover={
            "background": rx.cond(ativo, COR_PRINCIPAL_HOVER, COR_AREIA),
            "color": rx.cond(ativo, "#FFFFFF", COR_TITULO),
        },
    )


def cartao_padrao(conteudo):
    return rx.box(
        conteudo,
        background=COR_CARTAO,
        border=BORDA,
        border_radius="14px",
        padding="20px",
        width="100%",
        box_shadow=SOMBRA_SUAVE,
    )


def badge_terracota(texto):
    return rx.box(
        rx.text(
            texto,
            color=COR_PRINCIPAL,
            font_size="13px",
            font_weight="600",
        ),
        background=COR_PRINCIPAL_SUAVE,
        padding_x="10px",
        padding_y="3px",
        border_radius="8px",
    )


def badge_status_voluntario(status):
    ativo = status == "Ativo"
    return rx.box(
        rx.text(
            status,
            color=rx.cond(ativo, COR_OLIVA_TEXTO, COR_TEXTO_CLARO),
            font_size="12px",
            font_weight="600",
        ),
        background=rx.cond(ativo, COR_OLIVA_SUAVE, COR_AREIA),
        padding_x="10px",
        padding_y="3px",
        border_radius="8px",
    )


# ============================================================
# ABA: VOLUNTÁRIOS
# ============================================================

def formulario_voluntario():
    return cartao_padrao(
        rx.vstack(
            rx.hstack(
                rx.center(
                    rx.icon("user-plus", color=COR_PRINCIPAL, size=18),
                    background=COR_PRINCIPAL_SUAVE,
                    width="34px",
                    height="34px",
                    border_radius="9px",
                ),
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
                    font_size="15px",
                    font_weight="600",
                ),
                rx.select(
                    ["Ativo", "Inativo"],
                    value=VoluntariosState.status_voluntario,
                    on_change=VoluntariosState.set_status_voluntario,
                    width="100%",
                    size="3",
                ),
                align="start",
                spacing="1",
                width="100%",
            ),

            rx.button(
                rx.icon("plus", size=17),
                "Cadastrar voluntário",
                on_click=VoluntariosState.cadastrar_voluntario,
                background=COR_PRINCIPAL,
                color="#FFFFFF",
                font_weight="600",
                size="3",
                border_radius="10px",
                height="36px",
                width="100%",
                cursor="pointer",
                _hover={"background": COR_PRINCIPAL_HOVER},
            ),

            rx.cond(
                VoluntariosState.mensagem != "",
                rx.text(
                    VoluntariosState.mensagem,
                    color=COR_SUCESSO,
                    font_size="14px",
                    font_weight="500",
                ),
                rx.box(),
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
                    background=COR_PRINCIPAL_SUAVE,
                    border="1px solid #E6CFC3",
                    width="40px",
                    height="40px",
                    border_radius="10px",
                ),
                rx.vstack(
                    rx.text(
                        voluntario["nome"],
                        color=COR_TITULO,
                        font_weight="700",
                        font_size="16px",
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
                badge_status_voluntario(voluntario["status"]),
                width="100%",
                align="center",
                spacing="3",
            ),

            rx.divider(color="#EDE5DC"),

            rx.hstack(
                rx.icon("phone", size=15, color=COR_TEXTO_CLARO),
                rx.text(
                    voluntario["telefone"],
                    color=COR_TEXTO,
                    font_size="15px",
                ),
                align="center",
                spacing="2",
            ),

            align="start",
            spacing="2",
            width="100%",
        ),
        background=COR_CARTAO,
        border=BORDA,
        border_radius="12px",
        padding="14px",
        box_shadow=SOMBRA_SUAVE,
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
                    badge_terracota(VoluntariosState.quantidade_voluntarios),
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
                        font_size="15px",
                    ),
                    rx.box(),
                ),

                background=COR_CARTAO,
                border=BORDA,
                border_radius="14px",
                padding="20px",
                box_shadow=SOMBRA_SUAVE,
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
                rx.center(
                    rx.icon("calendar-plus", color=COR_PRINCIPAL, size=18),
                    background=COR_PRINCIPAL_SUAVE,
                    width="34px",
                    height="34px",
                    border_radius="9px",
                ),
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
                    font_size="15px",
                    font_weight="600",
                ),
                rx.text_area(
                    value=VoluntariosState.descricao_atividade,
                    on_change=VoluntariosState.set_descricao_atividade,
                    placeholder="Descreva a atividade...",
                    width="100%",
                    min_height="100px",
                    border_radius="9px",
                ),
                align="start",
                spacing="1",
                width="100%",
            ),

            rx.button(
                rx.icon("plus", size=17),
                "Cadastrar atividade",
                on_click=VoluntariosState.cadastrar_atividade,
                background=COR_PRINCIPAL,
                color="#FFFFFF",
                font_weight="600",
                size="3",
                border_radius="10px",
                height="44px",
                width="100%",
                cursor="pointer",
                _hover={"background": COR_PRINCIPAL_HOVER},
            ),

            rx.cond(
                VoluntariosState.mensagem != "",
                rx.text(
                    VoluntariosState.mensagem,
                    color=COR_SUCESSO,
                    font_size="14px",
                    font_weight="500",
                ),
                rx.box(),
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
                        color=COR_OLIVA_TEXTO,
                        size=19,
                    ),
                    background=COR_OLIVA_SUAVE,
                    border="1px solid #D3D8BA",
                    width="40px",
                    height="40px",
                    border_radius="10px",
                ),
                rx.vstack(
                    rx.text(
                        atividade["tipo_atividade"],
                        color=COR_TITULO,
                        font_weight="700",
                        font_size="16px",
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
                spacing="3",
            ),

            rx.divider(color="#EDE5DC"),

            rx.text(
                rx.cond(
                    atividade["descricao"] != "",
                    atividade["descricao"],
                    "Sem descrição informada.",
                ),
                color=COR_TEXTO,
                font_size="15px",
            ),

            align="start",
            spacing="2",
            width="100%",
        ),
        background=COR_CARTAO,
        border=BORDA,
        border_radius="12px",
        padding="14px",
        box_shadow=SOMBRA_SUAVE,
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
                    badge_terracota(VoluntariosState.quantidade_atividades),
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
                        font_size="15px",
                    ),
                    rx.box(),
                ),

                background=COR_CARTAO,
                border=BORDA,
                border_radius="14px",
                padding="20px",
                box_shadow=SOMBRA_SUAVE,
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
    selecionado = VoluntariosState.voluntario_selecionado_id == voluntario["id"]
    return rx.button(
        rx.hstack(
            rx.text(
                voluntario["nome"],
                font_size="15px",
                font_weight=rx.cond(selecionado, "600", "500"),
                text_align="left",
            ),
            rx.spacer(),
            rx.cond(
                selecionado,
                rx.icon("circle-check", color=COR_PRINCIPAL, size=18),
                rx.icon("circle", color=COR_TEXTO_CLARO, size=18),
            ),
            width="100%",
            align="center",
            spacing="3",
        ),
        on_click=lambda: VoluntariosState.set_voluntario_selecionado_id(
            voluntario["id"]
        ),
        background=rx.cond(selecionado, COR_PRINCIPAL_SUAVE, COR_CARTAO),
        color=COR_TITULO,
        border=rx.cond(selecionado, f"1.5px solid {COR_PRINCIPAL}", BORDA),
        border_radius="10px",
        height="auto",
        padding_y="11px",
        padding_x="14px",
        width="100%",
        justify="start",
        cursor="pointer",
        _hover={
            "background": rx.cond(selecionado, COR_PRINCIPAL_SUAVE, COR_DESTAQUE),
            "border_color": COR_PRINCIPAL,
        },
    )


def opcao_atividade(atividade: dict):
    selecionada = VoluntariosState.atividade_selecionada_id == atividade["id"]
    return rx.button(
        rx.hstack(
            rx.vstack(
                rx.text(
                    atividade["tipo_atividade"],
                    font_size="15px",
                    font_weight=rx.cond(selecionada, "600", "500"),
                    color=COR_TITULO,
                    text_align="left",
                    line_height="1.3",
                ),
                rx.hstack(
                    rx.icon("calendar", size=13, color=COR_TEXTO_CLARO),
                    rx.text(
                        atividade["data_atividade"],
                        font_size="13px",
                        color=COR_TEXTO_CLARO,
                    ),
                    spacing="1",
                    align="center",
                ),
                align="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.cond(
                selecionada,
                rx.icon("circle-check", color=COR_PRINCIPAL, size=18),
                rx.icon("circle", color=COR_TEXTO_CLARO, size=18),
            ),
            width="100%",
            align="center",
            spacing="3",
        ),
        on_click=lambda: VoluntariosState.set_atividade_selecionada_id(
            atividade["id"]
        ),
        background=rx.cond(selecionada, COR_PRINCIPAL_SUAVE, COR_CARTAO),
        color=COR_TITULO,
        border=rx.cond(selecionada, f"1.5px solid {COR_PRINCIPAL}", BORDA),
        border_radius="10px",
        height="auto",
        padding_y="11px",
        padding_x="14px",
        width="100%",
        justify="start",
        cursor="pointer",
        _hover={
            "background": rx.cond(selecionada, COR_PRINCIPAL_SUAVE, COR_DESTAQUE),
            "border_color": COR_PRINCIPAL,
        },
    )


def formulario_participacao():
    return cartao_padrao(
        rx.vstack(
            rx.hstack(
                rx.center(
                    rx.icon("user-round-plus", color=COR_PRINCIPAL, size=18),
                    background=COR_PRINCIPAL_SUAVE,
                    width="34px",
                    height="34px",
                    border_radius="9px",
                ),
                rx.heading(
                    "Registrar participação",
                    size="4",
                    color=COR_TITULO,
                ),
                align="center",
                spacing="2",
            ),

            rx.vstack(
                rx.text(
                    "Selecione o voluntário",
                    color=COR_TEXTO,
                    font_size="15px",
                    font_weight="600",
                ),
                rx.vstack(
                    rx.foreach(
                        VoluntariosState.voluntarios,
                        opcao_voluntario,
                    ),
                    width="100%",
                    max_height="200px",
                    overflow_y="auto",
                    padding_right="6px",
                    spacing="2",
                ),
                align="start",
                spacing="2",
                width="100%",
            ),

            rx.divider(color="#EDE5DC"),

            rx.vstack(
                rx.text(
                    "Selecione a atividade",
                    color=COR_TEXTO,
                    font_size="15px",
                    font_weight="600",
                ),
                rx.vstack(
                    rx.foreach(
                        VoluntariosState.atividades,
                        opcao_atividade,
                    ),
                    width="100%",
                    max_height="230px",
                    overflow_y="auto",
                    padding_right="6px",
                    spacing="2",
                ),
                align="start",
                spacing="2",
                width="100%",
            ),

            campo_formulario(
                "Função na atividade",
                VoluntariosState.funcao_na_atividade,
                VoluntariosState.set_funcao_na_atividade,
                "Ex.: Organização e recepção",
            ),

            rx.button(
                rx.icon("plus", size=17),
                "Registrar participação",
                on_click=VoluntariosState.associar_voluntario_atividade,
                background=COR_PRINCIPAL,
                color="#FFFFFF",
                font_weight="600",
                size="3",
                border_radius="10px",
                height="44px",
                width="100%",
                cursor="pointer",
                _hover={"background": COR_PRINCIPAL_HOVER},
            ),

            rx.cond(
                VoluntariosState.mensagem != "",
                rx.text(
                    VoluntariosState.mensagem,
                    color=COR_SUCESSO,
                    font_size="14px",
                    font_weight="500",
                ),
                rx.box(),
            ),

            align="start",
            spacing="4",
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
                        font_weight="700",
                        font_size="16px",
                    ),
                    rx.text(
                        participacao["tipo_atividade"],
                        color=COR_TEXTO,
                        font_size="15px",
                    ),
                    align="start",
                    spacing="0",
                ),
                rx.spacer(),
                badge_terracota(participacao["data_atividade"]),
                width="100%",
                align="center",
            ),

            rx.cond(
                participacao["funcao_na_atividade"] != "",
                rx.text(
                    "Função: " + participacao["funcao_na_atividade"],
                    color=COR_TEXTO_CLARO,
                    font_size="14px",
                ),
                rx.box(),
            ),

            align="start",
            spacing="2",
            width="100%",
        ),
        background=COR_CARTAO,
        border=BORDA,
        border_radius="12px",
        padding="14px",
        box_shadow=SOMBRA_SUAVE,
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
                    badge_terracota(VoluntariosState.quantidade_participacoes),
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
                        font_size="15px",
                    ),
                    rx.box(),
                ),

                background=COR_CARTAO,
                border=BORDA,
                border_radius="14px",
                padding="20px",
                box_shadow=SOMBRA_SUAVE,
                width="100%",
                align="start",
                spacing="3",
            ),

            columns={"initial": "1", "lg": "2"},
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
                            font_size="16px",
                        ),
                        align="start",
                        spacing="1",
                        width="100%",
                    ),

                    # INDICADORES COMPACTOS EM LINHA
                    rx.grid(
                        indicador_compacto(
                            titulo="Voluntários cadastrados",
                            valor=VoluntariosState.quantidade_voluntarios,
                            icone="users",
                            fundo=COR_PRINCIPAL_SUAVE,
                            borda_cor="#E6CFC3",
                            cor_icone=COR_PRINCIPAL,
                        ),
                        indicador_compacto(
                            titulo="Atividades cadastradas",
                            valor=VoluntariosState.quantidade_atividades,
                            icone="calendar-days",
                            fundo=COR_OLIVA_SUAVE,
                            borda_cor="#D3D8BA",
                            cor_icone=COR_OLIVA_TEXTO,
                            cor_valor=COR_OLIVA_TEXTO,
                        ),
                        indicador_compacto(
                            titulo="Participações registradas",
                            valor=VoluntariosState.quantidade_participacoes,
                            icone="handshake",
                            fundo=COR_AREIA,
                            borda_cor="#DFD3C3",
                            cor_icone=COR_PRINCIPAL,
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
                    spacing="4",
                    width="100%",
                ),
                padding="24px 28px",
                width="100%",
                min_height="100vh",
                background=COR_FUNDO,
                flex="1",
                min_width="0",
            ),

            width="100%",
            align="start",
            spacing="0",
        ),
        width="100%",
        min_height="100vh",
        background=COR_FUNDO,
    )