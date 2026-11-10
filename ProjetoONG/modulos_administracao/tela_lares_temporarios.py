
import reflex as rx

from ProjetoONG.state.lares_temporarios_state import (
    LaresTemporariosState,
)

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
COR_ERRO = "#DC2626"

SOMBRA_SUAVE = "0 2px 8px rgba(45, 31, 24, 0.04)"
BORDA = "1px solid #EDE5DC"


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
):
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
                rx.center(
                    rx.icon(
                        icone,
                        color=COR_PRINCIPAL,
                        size=19,
                    ),
                    background=COR_DESTAQUE,
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
        background=COR_CARTAO,
        border=BORDA,
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
                        color_scheme="orange",
                        variant="soft",
                    ),
                    rx.badge(
                        "Com vagas",
                        color_scheme="green",
                        variant="soft",
                    ),
                ),
                width="100%",
                align="center",
                spacing="2",
            ),

            rx.divider(color="#EEE5DC"),

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
                rx.icon("eye", size=14),
                "Visualizar ficha",
                size="2",
                width="100%",
                background=COR_DESTAQUE,
                color=COR_PRINCIPAL,
                border="1px solid #E8D9CA",
                border_radius="8px",
                _hover={
                    "background": "#F2E6D9",
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
        border=BORDA,
        border_radius="12px",
        padding="12px",
        box_shadow=SOMBRA_SUAVE,
        width="100%",
        height="100%",
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
            border_radius="14px",
            width="100%",
        ),
    )


# ============================================================
# ANIMAIS DISPONÍVEIS PARA ALOCAÇÃO
# ============================================================

def item_animal_disponivel(animal: dict):
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
            "Selecionar",
            size="2",
            color_scheme="brown",
            variant="soft",
            on_click=lambda: (
                LaresTemporariosState.set_animal_selecionado(
                    animal["id"]
                )
            ),
        ),
        width="100%",
        padding="10px 12px",
        border=BORDA,
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
                    rx.cond(
                        LaresTemporariosState.animal_selecionado_id != "",
                        LaresTemporariosState.animal_selecionado_id,
                        "Nenhum",
                    ),
                    color=COR_TEXTO,
                    font_size="16px",
                ),

                rx.foreach(
                    LaresTemporariosState.animais_disponiveis,
                    item_animal_disponivel,
                ),

                rx.text(
                    "Data de início",
                    font_weight="600",
                    color=COR_TEXTO,
                    font_size="16px",
                ),
                rx.input(
                    value=LaresTemporariosState.data_inicio,
                    on_change=LaresTemporariosState.set_data_inicio,
                    placeholder="DD/MM/AAAA",
                    width="100%",
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
                ),

                rx.button(
                    rx.icon("plus", size=16),
                    "Confirmar alocação",
                    width="100%",
                    background=COR_PRINCIPAL,
                    color="#FFFFFF",
                    _hover={
                        "background": COR_PRINCIPAL_HOVER,
                    },
                    on_click=LaresTemporariosState.alocar_animal,
                ),

                rx.text(
                    LaresTemporariosState.mensagem,
                    color=COR_SUCESSO,
                    font_size="16px",
                ),

                align="start",
                spacing="3",
                width="100%",
            ),
        ),
        background=COR_CARTAO,
        border=BORDA,
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
                        "green",
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
                        value=LaresTemporariosState.data_saida,
                        on_change=LaresTemporariosState.set_data_saida,
                        placeholder="DD/MM/AAAA",
                        width="100%",
                    ),
                    rx.button(
                        rx.icon("log-out", size=16),
                        "Registrar saída",
                        size="2",
                        color_scheme="orange",
                        variant="soft",
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
        padding="12px",
        border=BORDA,
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
                        variant="ghost",
                        color=COR_TEXTO,
                        on_click=lambda: (
                            LaresTemporariosState.selecionar_lar("")
                        ),
                    ),
                    width="100%",
                    align="center",
                ),

                rx.divider(color="#EEE5DC"),

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

                rx.divider(color="#EEE5DC"),

                area_alocacao(),

                rx.divider(color="#EEE5DC"),

                area_historico(),

                align="start",
                spacing="4",
                width="100%",
            ),
            background=COR_CARTAO,
            border=BORDA,
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
                        ),
                        cartao_metrica(
                            "Animais acolhidos",
                            LaresTemporariosState.total_animais_acolhidos,
                            "Permanências em andamento",
                            "paw-print",
                        ),
                        cartao_metrica(
                            "Vagas disponíveis",
                            LaresTemporariosState.total_vagas_disponiveis,
                            "Espaços disponíveis nos lares",
                            "bed-double",
                        ),
                        cartao_metrica(
                            "Lares com vagas",
                            LaresTemporariosState.total_lares_com_vagas,
                            "Lares que podem receber animais",
                            "door-open",
                        ),
                        columns={
                            "initial": "1",
                            "sm": "2",
                            "lg": "4",
                        },
                        spacing="3",
                        width="100%",
                    ),

                    # TÍTULO E FILTROS
                    rx.hstack(
                        titulo_secao(
                            "Lares cadastrados",
                            "Visualize a ocupação e a disponibilidade.",
                        ),
                        rx.spacer(),
                        width="100%",
                        align="center",
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
