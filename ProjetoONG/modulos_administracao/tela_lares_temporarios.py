import reflex as rx

from ProjetoONG.state.lares_temporarios_state import (
    LaresTemporariosState,
)

from ProjetoONG.modulos_administracao.menu_administrativo import (
    sidebar_administracao,
)


# ============================================================
# PALETA VISUAL (SEM MARROM #58392B / TERRACOTA ABERTO #C77D5B)
# ============================================================

COR_PRINCIPAL = "#C77D5B"
COR_PRINCIPAL_HOVER = "#B56A48"
COR_TITULO = "#241E1B"
COR_TEXTO = "#4A413B"
COR_TEXTO_CLARO = "#61564E"
COR_FUNDO = "#F8F3EC"
COR_AREIA = "#EFE6DA"
COR_CARAMELO = "#D6B99A"
COR_VERDE_OLIVA = "#A3A66B"
COR_CARTAO = "#FFFDF9"
COR_DESTAQUE = "#F5E7DF"
COR_SUCESSO = "#5F6B35"
COR_AVISO = "#B87A3D"
COR_ERRO = "#B84A39"

SOMBRA_SUAVE = "0 2px 8px rgba(36, 30, 27, 0.04)"
BORDA_SUTIL = "1px solid #E6DACB"


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
        rx.cond(
            descricao != "",
            rx.text(
                descricao,
                color=COR_TEXTO_CLARO,
                font_size="16px",
            ),
            rx.box(),
        ),
        align="start",
        spacing="1",
        width="100%",
    )


def cartao_metrica(
    titulo: str,
    valor,
    descricao: str,
    icone: str,
    bg_cartao: str = COR_AREIA,
    borda_cartao: str = COR_CARAMELO,
    cor_icone: str = COR_PRINCIPAL,
    bg_icone: str = COR_CARTAO,
):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    titulo,
                    color=COR_TEXTO,
                    font_size="16px",
                    font_weight="600",
                ),
                rx.spacer(),
                rx.center(
                    rx.icon(
                        icone,
                        color=cor_icone,
                        size=19,
                    ),
                    background=bg_icone,
                    border=f"1px solid {borda_cartao}",
                    width="38px",
                    height="38px",
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
                descricao,
                color=COR_TEXTO_CLARO,
                font_size="16px",
            ),
            align="start",
            spacing="2",
            width="100%",
        ),
        background=bg_cartao,
        border=f"1px solid {borda_cartao}",
        border_radius="14px",
        padding="18px",
        box_shadow=SOMBRA_SUAVE,
        width="100%",
    )


# ============================================================
# CARTÃO DE LAR TEMPORÁRIO
# ============================================================

def cartao_lar(lar: dict):
    return rx.box(
        rx.vstack(
            # Cabeçalho compacto
            rx.hstack(
                rx.center(
                    rx.icon(
                        "house",
                        color=COR_PRINCIPAL,
                        size=18,
                    ),
                    background=COR_DESTAQUE,
                    border="1px solid #E3C2B2",
                    width="38px",
                    height="38px",
                    border_radius="10px",
                ),
                rx.vstack(
                    rx.heading(
                        lar["nome_responsavel"],
                        size="3",
                        color=COR_TITULO,
                        font_weight="700",
                    ),
                    rx.text(
                        lar["endereco"],
                        color=COR_TEXTO_CLARO,
                        font_size="16px",
                        max_width="100%",
                    ),
                    align="start",
                    spacing="0",
                    flex="1",
                    min_width="0",
                ),
                rx.cond(
                    lar["situacao"] == "Lotado",
                    rx.badge(
                        "Lotado",
                        color_scheme="amber",
                        variant="soft",
                    ),
                    rx.badge(
                        "Com vagas",
                        color_scheme="grass",
                        variant="soft",
                    ),
                ),
                width="100%",
                align="center",
                spacing="2",
            ),

            rx.divider(color="#EAE0D5"),

            # Indicadores em uma linha
            rx.grid(
                rx.vstack(
                    rx.text(
                        "Capacidade",
                        color=COR_TEXTO_CLARO,
                        font_size="16px",
                    ),
                    rx.heading(
                        lar["capacidade"],
                        size="3",
                        color=COR_TITULO,
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.vstack(
                    rx.text(
                        "Acolhidos",
                        color=COR_TEXTO_CLARO,
                        font_size="16px",
                    ),
                    rx.heading(
                        lar["ocupacao"],
                        size="3",
                        color=COR_TITULO,
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.vstack(
                    rx.text(
                        "Vagas",
                        color=COR_TEXTO_CLARO,
                        font_size="16px",
                    ),
                    rx.heading(
                        lar["vagas"],
                        size="3",
                        color=rx.cond(
                            lar["vagas"] == "0",
                            COR_ERRO,
                            COR_SUCESSO,
                        ),
                    ),
                    spacing="0",
                    align="start",
                ),
                columns="3",
                width="100%",
                spacing="2",
            ),

            # Animais acolhidos
            rx.text(
                rx.cond(
                    lar["nomes_animais"] != "",
                    "Animais: " + lar["nomes_animais"],
                    "Nenhum animal acolhido",
                ),
                font_size="16px",
                color=COR_TEXTO_CLARO,
                width="100%",
            ),

            # Acesso à ficha
            rx.button(
                rx.icon("eye", size=15),
                "Visualizar ficha",
                size="2",
                font_weight="600",
                width="100%",
                background=COR_PRINCIPAL,
                color=COR_CARTAO,
                border="1px solid #B36947",
                border_radius="9px",
                box_shadow="0 1px 3px rgba(199, 125, 91, 0.25)",
                cursor="pointer",
                _hover={
                    "background": COR_PRINCIPAL_HOVER,
                    "border_color": "#9E5838",
                },
                on_click=lambda: LaresTemporariosState.selecionar_lar(
                    lar["id"]
                ),
            ),

            align="start",
            spacing="2",
            width="100%",
        ),
        background=COR_CARTAO,
        border=BORDA_SUTIL,
        border_radius="12px",
        padding="14px",
        box_shadow=SOMBRA_SUAVE,
        width="100%",
        height="100%",
    )


# ============================================================
# JANELA MODAL DE CADASTRO DE NOVO LAR
# ============================================================

def modal_cadastro_lar():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=16),
                "Cadastrar Lar",
                font_weight="600",
                size="3",
                background=COR_PRINCIPAL,
                color=COR_CARTAO,
                border="1px solid #B36947",
                border_radius="10px",
                box_shadow="0 1px 3px rgba(199, 125, 91, 0.25)",
                cursor="pointer",
                _hover={"background": COR_PRINCIPAL_HOVER},
                on_click=lambda: LaresTemporariosState.set_mostrar_form_cadastro(True),
            ),
        ),
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.dialog.title(
                            "Cadastrar novo lar parceiro",
                            color=COR_TITULO,
                            font_size="20px",
                            font_weight="700",
                            margin="0",
                        ),
                        rx.dialog.description(
                            "Preencha os dados do responsável e a capacidade de acolhimento.",
                            color=COR_TEXTO_CLARO,
                            font_size="14px",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=16),
                            variant="ghost",
                            color=COR_TEXTO_CLARO,
                            cursor="pointer",
                            on_click=lambda: LaresTemporariosState.set_mostrar_form_cadastro(False),
                        ),
                    ),
                    width="100%",
                    align="start",
                ),

                rx.divider(color="#EAE0D5"),

                rx.grid(
                    rx.vstack(
                        rx.text(
                            "Nome do responsável *",
                            font_weight="600",
                            color=COR_TEXTO,
                            font_size="14px",
                        ),
                        rx.input(
                            placeholder="Ex: Ana Paula Ferreira",
                            value=LaresTemporariosState.novo_nome_responsavel,
                            on_change=LaresTemporariosState.set_novo_nome_responsavel,
                            width="100%",
                            background=COR_CARTAO,
                            border=BORDA_SUTIL,
                        ),
                        align="start",
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(
                            "Telefone *",
                            font_weight="600",
                            color=COR_TEXTO,
                            font_size="14px",
                        ),
                        rx.input(
                            placeholder="(11) 99999-9999",
                            value=LaresTemporariosState.novo_telefone,
                            on_change=LaresTemporariosState.set_novo_telefone,
                            width="100%",
                            background=COR_CARTAO,
                            border=BORDA_SUTIL,
                        ),
                        align="start",
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(
                            "Endereço completo *",
                            font_weight="600",
                            color=COR_TEXTO,
                            font_size="14px",
                        ),
                        rx.input(
                            placeholder="Rua, número, bairro - Cidade/UF",
                            value=LaresTemporariosState.novo_endereco,
                            on_change=LaresTemporariosState.set_novo_endereco,
                            width="100%",
                            background=COR_CARTAO,
                            border=BORDA_SUTIL,
                        ),
                        align="start",
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(
                            "Capacidade de animais *",
                            font_weight="600",
                            color=COR_TEXTO,
                            font_size="14px",
                        ),
                        rx.input(
                            type="number",
                            min="1",
                            value=LaresTemporariosState.nova_capacidade,
                            on_change=LaresTemporariosState.set_nova_capacidade,
                            width="100%",
                            background=COR_CARTAO,
                            border=BORDA_SUTIL,
                        ),
                        align="start",
                        spacing="1",
                        width="100%",
                    ),
                    columns={"initial": "1", "sm": "2"},
                    spacing="3",
                    width="100%",
                ),

                rx.vstack(
                    rx.text(
                        "Observações do lar",
                        font_weight="600",
                        color=COR_TEXTO,
                        font_size="14px",
                    ),
                    rx.text_area(
                        placeholder="Ex: Casa com quintal telado, aceita cães de pequeno porte...",
                        value=LaresTemporariosState.novas_observacoes,
                        on_change=LaresTemporariosState.set_novas_observacoes,
                        width="100%",
                        background=COR_CARTAO,
                        border=BORDA_SUTIL,
                    ),
                    align="start",
                    spacing="1",
                    width="100%",
                ),

                rx.cond(
                    LaresTemporariosState.mensagem_cadastro != "",
                    rx.text(
                        LaresTemporariosState.mensagem_cadastro,
                        color=COR_ERRO,
                        font_size="14px",
                        font_weight="600",
                    ),
                    rx.box(),
                ),

                rx.hstack(
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            variant="outline",
                            color=COR_TEXTO,
                            border=BORDA_SUTIL,
                            border_radius="9px",
                            cursor="pointer",
                            on_click=lambda: LaresTemporariosState.set_mostrar_form_cadastro(False),
                        ),
                    ),
                    rx.button(
                        rx.icon("check", size=16),
                        "Salvar lar parceiro",
                        font_weight="600",
                        background=COR_PRINCIPAL,
                        color=COR_CARTAO,
                        border="1px solid #B36947",
                        border_radius="9px",
                        cursor="pointer",
                        _hover={"background": COR_PRINCIPAL_HOVER},
                        on_click=LaresTemporariosState.cadastrar_lar,
                    ),
                    spacing="2",
                    width="100%",
                ),

                align="start",
                spacing="3",
                width="100%",
            ),
            max_width="560px",
            background=COR_CARTAO,
            border=BORDA_SUTIL,
            border_radius="16px",
            padding="24px",
        ),
        open=LaresTemporariosState.mostrar_form_cadastro,
        on_open_change=LaresTemporariosState.set_mostrar_form_cadastro,
    )


# ============================================================
# FILTROS
# ============================================================

def area_filtros():
    return rx.vstack(
        rx.hstack(
            rx.input(
                placeholder="Pesquisar responsável, endereço ou animal...",
                value=LaresTemporariosState.filtro_texto,
                on_change=LaresTemporariosState.set_filtro_texto,
                width="100%",
                max_width="480px",
                size="3",
                border_radius="10px",
                background=COR_CARTAO,
                border=BORDA_SUTIL,
            ),
            rx.select(
                LaresTemporariosState.opcoes_filtro,
                value=LaresTemporariosState.filtro_status,
                on_change=LaresTemporariosState.set_filtro_status,
                width="190px",
                size="3",
            ),
            width="100%",
            align="center",
            wrap="wrap",
            spacing="3",
        ),
        width="100%",
    )


# ============================================================
# GRADE DE LARES
# ============================================================

def grade_lares():
    return rx.cond(
        LaresTemporariosState.lares_filtrados.length() > 0,
        rx.grid(
            rx.foreach(
                LaresTemporariosState.lares_filtrados,
                cartao_lar,
            ),
            columns={
                "initial": "1",
                "sm": "2",
                "md": "2",
                "lg": "3",
                "xl": "3",
            },
            spacing="4",
            width="100%",
        ),
        rx.center(
            rx.vstack(
                rx.icon(
                    "house",
                    size=36,
                    color=COR_TEXTO_CLARO,
                ),
                rx.heading(
                    "Nenhum lar encontrado",
                    size="4",
                    color=COR_TITULO,
                ),
                rx.text(
                    "Tente alterar os filtros ou a pesquisa.",
                    color=COR_TEXTO_CLARO,
                    font_size="16px",
                ),
                align="center",
                spacing="2",
            ),
            padding="40px",
            background=COR_CARTAO,
            border=BORDA_SUTIL,
            border_radius="14px",
            width="100%",
        ),
    )


# ============================================================
# ANIMAIS DISPONÍVEIS PARA ALOCAÇÃO
# ============================================================

def item_animal_disponivel(animal: dict):
    selecionado = LaresTemporariosState.animal_selecionado_id == animal["id"]
    return rx.hstack(
        rx.vstack(
            rx.text(
                animal["nome"],
                color=COR_TITULO,
                font_weight="600",
            ),
            rx.text(
                animal["especie"] + " • " + animal["porte"],
                color=COR_TEXTO_CLARO,
                font_size="16px",
            ),
            align="start",
            spacing="1",
        ),
        rx.spacer(),
        rx.button(
            rx.cond(selecionado, "Selecionado", "Selecionar"),
            size="2",
            font_weight="600",
            background=rx.cond(selecionado, COR_PRINCIPAL, COR_DESTAQUE),
            color=rx.cond(selecionado, COR_CARTAO, COR_PRINCIPAL),
            border="1px solid #DFB9A6",
            border_radius="8px",
            _hover={
                "background": rx.cond(selecionado, COR_PRINCIPAL_HOVER, "#EDD7CC"),
                "border_color": COR_PRINCIPAL,
            },
            on_click=lambda: (
                LaresTemporariosState.set_animal_selecionado(
                    animal["id"]
                )
            ),
        ),
        width="100%",
        padding="10px 12px",
        background=rx.cond(selecionado, COR_DESTAQUE, COR_CARTAO),
        border=rx.cond(selecionado, f"1px solid {COR_PRINCIPAL}", BORDA_SUTIL),
        border_radius="9px",
        align="center",
    )


def area_alocacao():
    return rx.vstack(
        titulo_secao(
            "Alocar animal",
            "Selecione um animal disponível para encaminhá-lo a este lar.",
        ),

        rx.cond(
            LaresTemporariosState.lares_com_resumo.length() > 0,
            rx.vstack(
                rx.text(
                    "Animal selecionado: ",
                    rx.text.span(
                        LaresTemporariosState.nome_animal_selecionado,
                        font_weight="600",
                        color=COR_TITULO,
                    ),
                    color=COR_TEXTO,
                    font_size="16px",
                ),

                rx.cond(
                    LaresTemporariosState.animais_disponiveis.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            LaresTemporariosState.animais_disponiveis,
                            item_animal_disponivel,
                        ),
                        width="100%",
                        spacing="2",
                    ),
                    rx.text(
                        "Nenhum animal com status 'Disponível' encontrado no momento.",
                        color=COR_AVISO,
                        font_size="15px",
                    ),
                ),

                rx.text(
                    "Data de início",
                    font_weight="600",
                    color=COR_TEXTO,
                    font_size="16px",
                ),
                rx.input(
                    type="date",
                    value=LaresTemporariosState.data_inicio,
                    on_change=LaresTemporariosState.set_data_inicio,
                    width="100%",
                    background=COR_CARTAO,
                    border=BORDA_SUTIL,
                ),

                rx.text(
                    "Observações",
                    font_weight="600",
                    color=COR_TEXTO,
                    font_size="16px",
                ),
                rx.text_area(
                    value=LaresTemporariosState.observacoes_alocacao,
                    on_change=(
                        LaresTemporariosState.set_observacoes_alocacao
                    ),
                    placeholder="Observações sobre a permanência...",
                    width="100%",
                    background=COR_CARTAO,
                    border=BORDA_SUTIL,
                ),

                rx.button(
                    rx.icon("plus", size=16),
                    "Confirmar alocação",
                    font_weight="600",
                    width="100%",
                    background=COR_PRINCIPAL,
                    color=COR_CARTAO,
                    border="1px solid #B36947",
                    border_radius="9px",
                    box_shadow="0 1px 3px rgba(199, 125, 91, 0.25)",
                    _hover={
                        "background": COR_PRINCIPAL_HOVER,
                        "border_color": "#9E5838",
                    },
                    on_click=LaresTemporariosState.alocar_animal,
                ),

                rx.cond(
                    LaresTemporariosState.mensagem != "",
                    rx.text(
                        LaresTemporariosState.mensagem,
                        color=COR_SUCESSO,
                        font_size="16px",
                        font_weight="600",
                    ),
                    rx.box(),
                ),

                align="start",
                spacing="3",
                width="100%",
            ),
        ),
        background=COR_CARTAO,
        border=BORDA_SUTIL,
        border_radius="14px",
        padding="18px",
        width="100%",
        align="start",
    )


# ============================================================
# HISTÓRICO DE PERMANÊNCIAS
# ============================================================

def item_historico(permanencia: dict):
    return rx.box(
        rx.vstack(
            # Informações da permanência
            rx.hstack(
                rx.vstack(
                    rx.text(
                        permanencia["nome_animal"],
                        font_weight="600",
                        color=COR_TITULO,
                    ),
                    rx.text(
                        "Início: " + permanencia["data_inicio"],
                        color=COR_TEXTO_CLARO,
                        font_size="16px",
                    ),
                    rx.text(
                        rx.cond(
                            permanencia["data_fim"] != "",
                            "Fim: " + permanencia["data_fim"],
                            "Permanência em andamento",
                        ),
                        color=COR_TEXTO_CLARO,
                        font_size="16px",
                    ),
                    align="start",
                    spacing="1",
                ),
                rx.spacer(),
                rx.badge(
                    permanencia["situacao"],
                    color_scheme=rx.cond(
                        permanencia["situacao"] == "Em andamento",
                        "grass",
                        "gray",
                    ),
                    variant="soft",
                ),
                width="100%",
                align="center",
            ),

            # Observações
            rx.text(
                permanencia["observacoes"],
                color=COR_TEXTO,
                font_size="16px",
            ),

            # Registrar saída somente para permanências ativas
            rx.cond(
                permanencia["situacao"] == "Em andamento",
                rx.vstack(
                    rx.text(
                        "Data de saída",
                        font_weight="600",
                        color=COR_TEXTO,
                        font_size="16px",
                    ),
                    rx.input(
                        type="date",
                        value=LaresTemporariosState.data_saida,
                        on_change=LaresTemporariosState.set_data_saida,
                        width="100%",
                        background=COR_CARTAO,
                        border=BORDA_SUTIL,
                    ),
                    rx.button(
                        rx.icon("log-out", size=16),
                        "Registrar saída",
                        size="2",
                        font_weight="600",
                        background="#ECEEDB",
                        color=COR_SUCESSO,
                        border="1px solid #C5C99A",
                        border_radius="8px",
                        _hover={
                            "background": "#E0E4C7",
                            "border_color": COR_VERDE_OLIVA,
                        },
                        width="100%",
                        on_click=lambda: (
                            LaresTemporariosState.registrar_saida(
                                permanencia["id"],
                                LaresTemporariosState.data_saida,
                            )
                        ),
                    ),
                    width="100%",
                    spacing="2",
                    align="start",
                ),
                rx.box(),
            ),

            align="start",
            spacing="2",
            width="100%",
        ),
        background=COR_CARTAO,
        padding="12px",
        border=BORDA_SUTIL,
        border_radius="10px",
        width="100%",
    )


def area_historico():
    return rx.vstack(
        titulo_secao(
            "Histórico de permanências",
            "Consulte as entradas e saídas dos animais neste lar.",
        ),

        rx.foreach(
            LaresTemporariosState.historico_lar_selecionado,
            item_historico,
        ),

        rx.cond(
            LaresTemporariosState.historico_lar_selecionado.length() == 0,
            rx.text(
                "Ainda não existem registros para este lar.",
                color=COR_TEXTO_CLARO,
                font_size="16px",
            ),
            rx.box(),
        ),

        align="start",
        spacing="3",
        width="100%",
    )


# ============================================================
# FICHA DO LAR SELECIONADO
# ============================================================

def ficha_lar():
    return rx.cond(
        LaresTemporariosState.lar_selecionado["id"] != "",
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading(
                            "Ficha do lar temporário",
                            size="5",
                            color=COR_TITULO,
                        ),
                        rx.text(
                            LaresTemporariosState.lar_selecionado[
                                "nome_responsavel"
                            ],
                            color=COR_TEXTO_CLARO,
                            font_size="16px",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("x", size=16),
                        "Fechar",
                        size="2",
                        variant="outline",
                        color=COR_TEXTO,
                        border=BORDA_SUTIL,
                        border_radius="8px",
                        _hover={
                            "background": COR_AREIA,
                            "border_color": COR_CARAMELO,
                        },
                        on_click=lambda: (
                            LaresTemporariosState.selecionar_lar("")
                        ),
                    ),
                    width="100%",
                    align="center",
                ),

                rx.divider(color="#EAE0D5"),

                rx.grid(
                    rx.vstack(
                        rx.text(
                            "Telefone",
                            color=COR_TEXTO_CLARO,
                            font_size="16px",
                        ),
                        rx.text(
                            LaresTemporariosState.lar_selecionado[
                                "telefone"
                            ],
                            color=COR_TEXTO,
                            font_weight="600",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text(
                            "Capacidade",
                            color=COR_TEXTO_CLARO,
                            font_size="16px",
                        ),
                        rx.text(
                            LaresTemporariosState.lar_selecionado[
                                "capacidade"
                            ],
                            color=COR_TEXTO,
                            font_weight="600",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text(
                            "Endereço",
                            color=COR_TEXTO_CLARO,
                            font_size="16px",
                        ),
                        rx.text(
                            LaresTemporariosState.lar_selecionado[
                                "endereco"
                            ],
                            color=COR_TEXTO,
                            font_weight="600",
                        ),
                        align="start",
                        spacing="1",
                        grid_column="1 / -1",
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),

                rx.vstack(
                    rx.text(
                        "Observações do lar",
                        color=COR_TEXTO_CLARO,
                        font_size="16px",
                    ),
                    rx.text(
                        LaresTemporariosState.lar_selecionado[
                            "observacoes"
                        ],
                        color=COR_TEXTO,
                    ),
                    align="start",
                    spacing="1",
                    width="100%",
                ),

                rx.divider(color="#EAE0D5"),

                area_alocacao(),

                rx.divider(color="#EAE0D5"),

                area_historico(),

                align="start",
                spacing="4",
                width="100%",
            ),
            background=COR_CARTAO,
            border=BORDA_SUTIL,
            border_radius="14px",
            padding="20px",
            width="100%",
            box_shadow=SOMBRA_SUAVE,
        ),
        rx.box(),
    )


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

def lares_temporarios_page():
    return rx.box(
        rx.hstack(
            # MENU ADMINISTRATIVO COMPARTILHADO
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
                            "Lares Temporários",
                            size="7",
                            color=COR_TITULO,
                            font_weight="700",
                        ),
                        rx.text(
                            "Gerencie os lares, acompanhe as vagas "
                            "e organize a permanência dos animais.",
                            color=COR_TEXTO_CLARO,
                            font_size="16px",
                        ),
                        align="start",
                        spacing="1",
                        width="100%",
                    ),

                    # MÉTRICAS
                    rx.grid(
                        cartao_metrica(
                            "Lares cadastrados",
                            LaresTemporariosState.total_lares,
                            "Total de lares registrados",
                            "house",
                            bg_cartao="#F3E1D8",
                            borda_cartao="#E3C2B2",
                            cor_icone=COR_PRINCIPAL,
                        ),
                        cartao_metrica(
                            "Animais acolhidos",
                            LaresTemporariosState.total_animais_acolhidos,
                            "Permanências em andamento",
                            "paw-print",
                            bg_cartao="#ECEEDB",
                            borda_cartao="#CFD4AE",
                            cor_icone=COR_SUCESSO,
                        ),
                        cartao_metrica(
                            "Vagas disponíveis",
                            LaresTemporariosState.total_vagas_disponiveis,
                            "Espaços disponíveis nos lares",
                            "bed-double",
                            bg_cartao="#F3E9DC",
                            borda_cartao=COR_CARAMELO,
                            cor_icone=COR_PRINCIPAL,
                        ),
                        cartao_metrica(
                            "Lares com vagas",
                            LaresTemporariosState.total_lares_com_vagas,
                            "Lares que podem receber animais",
                            "door-open",
                            bg_cartao="#E4E7CE",
                            borda_cartao="#C2C89C",
                            cor_icone=COR_SUCESSO,
                        ),
                        columns={
                            "initial": "1",
                            "sm": "2",
                            "lg": "4",
                        },
                        spacing="3",
                        width="100%",
                    ),

                    # TÍTULO E BOTÃO DE CADASTRO (ABRE JANELA MODAL)
                    rx.hstack(
                        titulo_secao(
                            "Lares cadastrados",
                            "Visualize a ocupação e a disponibilidade.",
                        ),
                        rx.spacer(),
                        modal_cadastro_lar(),
                        width="100%",
                        align="center",
                        wrap="wrap",
                        spacing="3",
                    ),

                    area_filtros(),

                    # CARTÕES
                    grade_lares(),

                    # FICHA DO LAR
                    ficha_lar(),

                    align="start",
                    spacing="5",
                    width="100%",
                ),
                padding="28px",
                width="100%",
                min_height="100vh",
                background=COR_FUNDO,
            ),

            width="100%",
            align="start",
            spacing="0",
        ),
        width="100%",
        min_height="100vh",
        background=COR_FUNDO,
    )