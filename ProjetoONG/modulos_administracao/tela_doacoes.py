import reflex as rx

from ProjetoONG.state.doacoes_state import DoacoesState
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
COR_CARAMELO_SUAVE = "#F5ECE1"     # Caramelo claro (badge material)
COR_CARAMELO_TEXTO = "#7A5838"     # Caramelo escuro (texto badge material)

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


def cartao_metrica(
    titulo: str,
    valor,
    subtitulo: str,
    icone: str,
    fundo: str = COR_PRINCIPAL_SUAVE,
    borda_cor: str = "#E6CFC3",
    cor_icone: str = COR_PRINCIPAL,
):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    titulo,
                    color=COR_TITULO,
                    font_size="15px",
                    font_weight="600",
                ),
                rx.spacer(),
                rx.center(
                    rx.icon(
                        icone,
                        color=cor_icone,
                        size=18,
                    ),
                    background=COR_CARTAO,
                    border=f"1px solid {borda_cor}",
                    width="36px",
                    height="36px",
                    border_radius="10px",
                ),
                width="100%",
                align="center",
            ),
            rx.heading(
                valor,
                size="7",
                color=COR_TITULO,
                font_weight="700",
            ),
            rx.text(
                subtitulo,
                color=COR_TEXTO_CLARO,
                font_size="14px",
            ),
            align="start",
            spacing="2",
            width="100%",
        ),
        background=fundo,
        border=f"1px solid {borda_cor}",
        border_radius="14px",
        padding="18px",
        box_shadow=SOMBRA_SUAVE,
        width="100%",
    )


def botao_aba(texto: str, identificador: str):
    ativo = DoacoesState.aba_ativa == identificador
    return rx.button(
        texto,
        on_click=lambda: DoacoesState.selecionar_aba(identificador),
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


def badge_tipo_doacao(tipo):
    financeira = tipo == "Financeira"
    return rx.box(
        rx.text(
            tipo,
            color=rx.cond(financeira, COR_OLIVA_TEXTO, COR_CARAMELO_TEXTO),
            font_size="12px",
            font_weight="600",
        ),
        background=rx.cond(financeira, COR_OLIVA_SUAVE, COR_CARAMELO_SUAVE),
        padding_x="10px",
        padding_y="3px",
        border_radius="8px",
    )


# ============================================================
# ABA: DOADORES
# ============================================================

def formulario_doador():
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
                rx.icon("plus", size=17),
                "Cadastrar doador",
                on_click=DoacoesState.cadastrar_doador,
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
                DoacoesState.mensagem != "",
                rx.text(
                    DoacoesState.mensagem,
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
                    background=COR_PRINCIPAL_SUAVE,
                    border="1px solid #E6CFC3",
                    width="40px",
                    height="40px",
                    border_radius="10px",
                ),
                rx.vstack(
                    rx.text(
                        doador["nome"],
                        color=COR_TITULO,
                        font_weight="700",
                        font_size="16px",
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
                spacing="3",
            ),

            rx.divider(color="#EDE5DC"),

            rx.hstack(
                rx.icon("phone", size=15, color=COR_TEXTO_CLARO),
                rx.text(
                    doador["telefone"],
                    color=COR_TEXTO,
                    font_size="15px",
                ),
                align="center",
                spacing="2",
            ),

            rx.hstack(
                rx.icon("mail", size=15, color=COR_TEXTO_CLARO),
                rx.text(
                    doador["email"],
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
                    badge_terracota(DoacoesState.quantidade_doadores),
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
# SELEÇÃO DE DOADOR PARA UMA DOAÇÃO
# ============================================================

def opcao_doador(doador: dict):
    selecionado = DoacoesState.doador_selecionado_id == doador["id"]
    return rx.button(
        rx.hstack(
            rx.text(
                doador["nome"],
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
        on_click=lambda: DoacoesState.set_doador_selecionado(
            doador["id"]
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


def selecao_doador():
    return rx.vstack(
        rx.text(
            "Selecione o doador",
            color=COR_TEXTO,
            font_size="15px",
            font_weight="600",
        ),

        rx.vstack(
            rx.foreach(
                DoacoesState.doadores,
                opcao_doador,
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
    )


# ============================================================
# ABA: DOAÇÕES FINANCEIRAS
# ============================================================

def item_doacao_financeira(doacao: dict):
    return rx.cond(
        doacao["tipo_doacao"] == "Financeira",
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        doacao["nome_doador"],
                        color=COR_TITULO,
                        font_weight="700",
                        font_size="16px",
                    ),
                    rx.spacer(),
                    badge_tipo_doacao("Financeira"),
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
            background=COR_CARTAO,
            padding="14px",
            border=BORDA,
            border_radius="12px",
            box_shadow=SOMBRA_SUAVE,
            width="100%",
        ),
        rx.box(),
    )


def aba_doacoes_financeiras():
    return rx.vstack(
        titulo_secao(
            "Doações financeiras",
            "Registre os valores recebidos e consulte os respectivos registros.",
        ),

        rx.grid(
            cartao_padrao(
                rx.vstack(
                    rx.hstack(
                        rx.center(
                            rx.icon("hand-coins", color=COR_PRINCIPAL, size=18),
                            background=COR_PRINCIPAL_SUAVE,
                            width="34px",
                            height="34px",
                            border_radius="9px",
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
                        rx.icon("plus", size=17),
                        "Registrar doação",
                        on_click=DoacoesState.registrar_doacao_financeira,
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
                        DoacoesState.mensagem != "",
                        rx.text(
                            DoacoesState.mensagem,
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
                padding="20px",
                box_shadow=SOMBRA_SUAVE,
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


# ============================================================
# ABA: DOAÇÕES MATERIAIS
# ============================================================

def item_doacao_material(doacao: dict):
    return rx.cond(
        doacao["tipo_doacao"] == "Material",
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        doacao["nome_doador"],
                        color=COR_TITULO,
                        font_weight="700",
                        font_size="16px",
                    ),
                    rx.spacer(),
                    badge_tipo_doacao("Material"),
                    width="100%",
                    align="center",
                ),
                rx.text(
                    doacao["descricao"],
                    color=COR_TEXTO,
                    font_size="15px",
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
            background=COR_CARTAO,
            padding="14px",
            border=BORDA,
            border_radius="12px",
            box_shadow=SOMBRA_SUAVE,
            width="100%",
        ),
        rx.box(),
    )


def aba_doacoes_materiais():
    return rx.vstack(
        titulo_secao(
            "Doações materiais",
            "Registre os materiais recebidos pela ONG, com sua descrição e data de recebimento.",
        ),

        rx.grid(
            cartao_padrao(
                rx.vstack(
                    rx.hstack(
                        rx.center(
                            rx.icon("package-check", color=COR_PRINCIPAL, size=18),
                            background=COR_PRINCIPAL_SUAVE,
                            width="34px",
                            height="34px",
                            border_radius="9px",
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
                            font_size="15px",
                            font_weight="600",
                        ),
                        rx.text_area(
                            value=DoacoesState.descricao_doacao,
                            on_change=DoacoesState.set_descricao_doacao,
                            placeholder="Descreva os materiais recebidos...",
                            width="100%",
                            min_height="100px",
                            border_radius="9px",
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
                        rx.icon("plus", size=17),
                        "Registrar recebimento",
                        on_click=DoacoesState.registrar_doacao_material,
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
                        DoacoesState.mensagem != "",
                        rx.text(
                            DoacoesState.mensagem,
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
                padding="20px",
                box_shadow=SOMBRA_SUAVE,
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
                        font_weight="700",
                        font_size="16px",
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
                badge_tipo_doacao(doacao["tipo_doacao"]),
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
                    font_size="15px",
                ),
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
# ÚLTIMAS DOAÇÕES
# ============================================================

def item_ultima_doacao(doacao: dict):
    return rx.hstack(
        rx.text(
            doacao["data_doacao"],
            color=COR_TEXTO_CLARO,
            font_size="14px",
            width="105px",
            flex_shrink="0",
        ),

        rx.box(
            badge_tipo_doacao(doacao["tipo_doacao"]),
            width="105px",
            flex_shrink="0",
        ),

        rx.text(
            doacao["nome_doador"],
            color=COR_TITULO,
            font_weight="600",
            font_size="15px",
            flex="1",
            min_width="0",
        ),

        rx.text(
            rx.cond(
                doacao["tipo_doacao"] == "Financeira",
                "R$ " + doacao["valor"],
                doacao["descricao"],
            ),
            color=rx.cond(
                doacao["tipo_doacao"] == "Financeira",
                COR_SUCESSO,
                COR_TEXTO,
            ),
            font_weight=rx.cond(
                doacao["tipo_doacao"] == "Financeira",
                "600",
                "400",
            ),
            font_size="15px",
            flex="1",
            min_width="0",
            text_align="right",
        ),

        width="100%",
        align="center",
        spacing="3",
        padding_y="12px",
        padding_x="10px",
        border_bottom=BORDA,
    )


def secao_ultimas_doacoes():
    return cartao_padrao(
        rx.vstack(
            rx.hstack(
                rx.center(
                    rx.icon("clock", color=COR_PRINCIPAL, size=18),
                    background=COR_PRINCIPAL_SUAVE,
                    width="34px",
                    height="34px",
                    border_radius="9px",
                ),

                rx.heading(
                    "Últimas Doações",
                    size="4",
                    color=COR_TITULO,
                ),

                rx.spacer(),

                rx.button(
                    "Ver todas",
                    on_click=lambda: DoacoesState.selecionar_aba("historico"),
                    background=COR_PRINCIPAL_SUAVE,
                    color=COR_PRINCIPAL,
                    font_weight="600",
                    size="2",
                    border_radius="8px",
                    cursor="pointer",
                    _hover={
                        "background": COR_PRINCIPAL,
                        "color": "#FFFFFF",
                    },
                ),

                width="100%",
                align="center",
            ),

            rx.vstack(
                rx.foreach(
                    DoacoesState.doacoes_com_doador,
                    item_ultima_doacao,
                ),
                width="100%",
                spacing="0",
            ),

            width="100%",
            align="start",
            spacing="3",
        )
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
                            font_size="17px",
                        ),

                        align="start",
                        spacing="1",
                        width="100%",
                    ),

                    # INDICADORES NO TOPO (PADRÃO LARES TEMPORÁRIOS E VOLUNTÁRIOS)
                    rx.grid(
                        cartao_metrica(
                            titulo="Total financeiro recebido",
                            valor="R$ " + DoacoesState.total_doacoes_financeiras.to_string(),
                            subtitulo="Soma das contribuições financeiras",
                            icone="heart",
                            fundo=COR_PRINCIPAL_SUAVE,
                            borda_cor="#E6CFC3",
                            cor_icone=COR_PRINCIPAL,
                        ),
                        cartao_metrica(
                            titulo="Doações registradas",
                            valor=DoacoesState.quantidade_doacoes,
                            subtitulo="Financeiras e materiais recebidas",
                            icone="handshake",
                            fundo=COR_OLIVA_SUAVE,
                            borda_cor="#D3D8BA",
                            cor_icone=COR_OLIVA_TEXTO,
                        ),
                        cartao_metrica(
                            titulo="Doadores cadastrados",
                            valor=DoacoesState.quantidade_doadores,
                            subtitulo="Pessoas e empresas parceiras",
                            icone="users",
                            fundo=COR_AREIA,
                            borda_cor="#DFD3C3",
                            cor_icone=COR_PRINCIPAL,
                        ),
                        columns={
                            "initial": "1",
                            "sm": "2",
                            "lg": "3",
                        },
                        spacing="4",
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

                    # ÚLTIMAS DOAÇÕES
                    secao_ultimas_doacoes(),

                    align="start",
                    spacing="5",
                    width="100%",
                ),

                padding="28px",
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