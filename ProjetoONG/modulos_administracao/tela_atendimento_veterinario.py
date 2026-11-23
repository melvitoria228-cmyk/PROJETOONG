import reflex as rx

from ProjetoONG.state.atendimento_veterinario_state import (
    AtendimentoVeterinarioState,
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
COR_BORDA = "#E6DACB"
COR_DESTAQUE = "#F5E7DF"
COR_SUCESSO = "#5F6B35"
COR_AVISO = "#B87A3D"
COR_ERRO = "#B84A39"

SOMBRA_SUAVE = "0 2px 8px rgba(36, 30, 27, 0.04)"


# ============================================================
# ESTILOS DE BOTÕES
# ============================================================

def botao_principal(texto: str, acao):
    return rx.button(
        texto,
        on_click=acao,
        background=COR_PRINCIPAL,
        color=COR_CARTAO,
        font_weight="600",
        border="1px solid #B36947",
        border_radius="9px",
        box_shadow="0 1px 3px rgba(199, 125, 91, 0.25)",
        _hover={
            "background": COR_PRINCIPAL_HOVER,
            "border_color": "#9E5838",
        },
    )


def botao_secundario(texto: str, acao):
    return rx.button(
        texto,
        on_click=acao,
        background=COR_AREIA,
        color=COR_TITULO,
        font_weight="600",
        border=f"1px solid {COR_CARAMELO}",
        border_radius="9px",
        _hover={
            "background": "#E5D8C7",
            "border_color": "#C4A380",
        },
    )


# ============================================================
# CABEÇALHO
# ============================================================

def cabecalho_veterinario():
    return rx.vstack(
        rx.heading(
            "Atendimento Veterinário",
            size="7",
            color=COR_TITULO,
            font_weight="700",
        ),
        rx.text(
            "Agenda clínica e acompanhamento dos animais",
            color=COR_TEXTO_CLARO,
            font_size="16px",
        ),
        spacing="1",
        align="start",
        width="100%",
        margin_bottom="8px",
    )

# ============================================================
# MENSAGENS
# ============================================================

def mensagens_estado():
    return rx.vstack(
        rx.cond(
            AtendimentoVeterinarioState.mensagem_erro != "",
            rx.text(
                AtendimentoVeterinarioState.mensagem_erro,
                color=COR_ERRO,
                font_size="14px",
                font_weight="600",
            ),
            rx.fragment(),
        ),
        rx.cond(
            AtendimentoVeterinarioState.mensagem_sucesso != "",
            rx.text(
                AtendimentoVeterinarioState.mensagem_sucesso,
                color=COR_SUCESSO,
                font_size="14px",
                font_weight="600",
            ),
            rx.fragment(),
        ),
        width="100%",
        align="start",
        spacing="1",
    )


# ============================================================
# PAINEL DE MÉTRICAS (KPIs)
# ============================================================

def card_kpi(
    titulo: str,
    valor,
    icone: str,
    bg_cartao: str,
    borda_cartao: str,
    cor_icone: str,
):
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(
                    titulo,
                    color=COR_TEXTO,
                    font_size="14px",
                    font_weight="600",
                ),
                rx.heading(
                    valor,
                    size="6",
                    color=COR_TITULO,
                    font_weight="700",
                ),
                align="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.center(
                rx.icon(icone, size=20, color=cor_icone),
                width="40px",
                height="40px",
                border_radius="10px",
                background=COR_CARTAO,
                border=f"1px solid {borda_cartao}",
            ),
            width="100%",
            align="center",
        ),
        padding="16px 20px",
        background=bg_cartao,
        border=f"1px solid {borda_cartao}",
        border_radius="14px",
        box_shadow=SOMBRA_SUAVE,
        flex="1",
        min_width="200px",
    )


def resumo_kpis():
    return rx.flex(
        card_kpi(
            "Total de Atendimentos",
            AtendimentoVeterinarioState.total_do_mes,
            "stethoscope",
            bg_cartao="#F3E1D8",
            borda_cartao="#E3C2B2",
            cor_icone=COR_PRINCIPAL,
        ),
        card_kpi(
            "Agendados Pendentes",
            AtendimentoVeterinarioState.total_agendados,
            "calendar-clock",
            bg_cartao="#F3E9DC",
            borda_cartao=COR_CARAMELO,
            cor_icone=COR_AVISO,
        ),
        card_kpi(
            "Custo Total (R$)",
            AtendimentoVeterinarioState.custo_total_mes,
            "circle-dollar-sign",
            bg_cartao="#ECEEDB",
            borda_cartao="#CFD4AE",
            cor_icone=COR_SUCESSO,
        ),
        width="100%",
        gap="16px",
        wrap="wrap",
    )


# ============================================================
# NAVEGAÇÃO DA AGENDA
# ============================================================

def navegacao_agenda():
    return rx.hstack(
        rx.heading(
            "Agenda Clínica",
            size="4",
            color=COR_TITULO,
        ),
        rx.spacer(),
        rx.icon_button(
            rx.icon("chevron-left"),
            on_click=AtendimentoVeterinarioState.dia_anterior,
            background=COR_AREIA,
            color=COR_TITULO,
            border=f"1px solid {COR_CARAMELO}",
            _hover={"background": "#E5D8C7"},
        ),
        rx.text(
            AtendimentoVeterinarioState.data_selecionada,
            font_weight="600",
            color=COR_TITULO,
        ),
        rx.icon_button(
            rx.icon("chevron-right"),
            on_click=AtendimentoVeterinarioState.proximo_dia,
            background=COR_AREIA,
            color=COR_TITULO,
            border=f"1px solid {COR_CARAMELO}",
            _hover={"background": "#E5D8C7"},
        ),
        width="100%",
        align="center",
        margin_bottom="14px",
    )


# ============================================================
# CARTÃO DE AGENDAMENTO
# ============================================================

def cartao_agendamento(item):
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(
                    item["horario"],
                    font_weight="bold",
                    font_size="16px",
                    color=COR_PRINCIPAL,
                ),
                rx.text(
                    item["animal"],
                    font_weight="bold",
                    color=COR_TITULO,
                    font_size="16px",
                ),
                rx.text(
                    item["procedimento"],
                    color=COR_TEXTO,
                    font_size="15px",
                ),
                rx.text(
                    item["veterinario"],
                    color=COR_TEXTO_CLARO,
                    font_size="14px",
                ),
                align="start",
                spacing="1",
                flex="1",
            ),
            rx.vstack(
                rx.badge(
                    item["status"],
                    color_scheme=rx.cond(
                        item["status"] == "Realizado",
                        "grass",
                        rx.cond(
                            item["status"] == "Cancelado",
                            "red",
                            "amber",
                        ),
                    ),
                    variant="soft",
                ),
                rx.button(
                    rx.icon("eye", size=14),
                    "Ver detalhes",
                    on_click=lambda: (
                        AtendimentoVeterinarioState.abrir_detalhes(
                            item["id"]
                        )
                    ),
                    size="2",
                    font_weight="600",
                    background=COR_DESTAQUE,
                    color=COR_PRINCIPAL,
                    border="1px solid #DFB9A6",
                    border_radius="8px",
                    _hover={
                        "background": "#EDD7CC",
                        "border_color": COR_PRINCIPAL,
                    },
                ),
                align="end",
                spacing="2",
            ),
            width="100%",
            align="center",
            wrap="wrap",
        ),
        padding="14px 16px",
        background=COR_CARTAO,
        border=f"1px solid {COR_BORDA}",
        border_left=rx.cond(
            item["status"] == "Realizado",
            f"4px solid {COR_SUCESSO}",
            rx.cond(
                item["status"] == "Cancelado",
                f"4px solid {COR_ERRO}",
                f"4px solid {COR_AVISO}",
            ),
        ),
        border_radius="10px",
        width="100%",
    )


# ============================================================
# LISTA DE ATENDIMENTOS DO DIA
# ============================================================

def lista_agendamentos():
    return rx.cond(
        AtendimentoVeterinarioState.tem_agendamentos,
        rx.vstack(
            rx.foreach(
                AtendimentoVeterinarioState.agendamentos_do_dia,
                cartao_agendamento,
            ),
            width="100%",
            spacing="3",
            align="start",
        ),
        rx.box(
            rx.vstack(
                rx.icon(
                    "calendar-days",
                    size=30,
                    color=COR_PRINCIPAL,
                ),
                rx.text(
                    "Nenhum atendimento nesta data.",
                    color=COR_TEXTO,
                    font_weight="600",
                ),
                rx.text(
                    "Selecione outro dia ou cadastre um novo agendamento.",
                    color=COR_TEXTO_CLARO,
                    font_size="14px",
                    text_align="center",
                ),
                align="center",
                spacing="2",
                width="100%",
            ),
            padding="32px",
            width="100%",
            background=COR_AREIA,
            border=f"1px solid {COR_BORDA}",
            border_radius="10px",
        ),
    )


# ============================================================
# PAINEL DA AGENDA
# ============================================================

def painel_agenda():
    return rx.box(
        rx.vstack(
            navegacao_agenda(),
            lista_agendamentos(),
            width="100%",
            align="start",
        ),
        padding="20px",
        background=COR_CARTAO,
        border=f"1px solid {COR_BORDA}",
        border_radius="14px",
        box_shadow=SOMBRA_SUAVE,
        width="100%",
    )


# ============================================================
# CAMPO PADRÃO DE FORMULÁRIO
# ============================================================

def campo_formulario(rotulo: str, campo):
    return rx.vstack(
        rx.text(
            rotulo,
            font_weight="600",
            color=COR_TEXTO,
            font_size="15px",
        ),
        campo,
        width="100%",
        align="start",
        spacing="1",
    )


# ============================================================
# FORMULÁRIO DE AGENDAMENTO
# ============================================================

def formulario_agendamento():
    return rx.cond(
        AtendimentoVeterinarioState.formulario_aberto,
        rx.box(
            rx.vstack(
                rx.heading(
                    "Novo Agendamento",
                    size="4",
                    color=COR_TITULO,
                ),
                rx.text(
                    "Preencha os dados para agendar um atendimento veterinário.",
                    color=COR_TEXTO_CLARO,
                    font_size="14px",
                ),

                mensagens_estado(),

                campo_formulario(
                    "Animal",
                    rx.select(
                        AtendimentoVeterinarioState.nomes_animais,
                        placeholder="Selecione um animal",
                        value=(
                            AtendimentoVeterinarioState
                            .animal_selecionado["nome"]
                        ),
                        on_change=(
                            AtendimentoVeterinarioState.atualizar_animal
                        ),
                        width="100%",
                    ),
                ),

                campo_formulario(
                    "Data do atendimento",
                    rx.input(
                        value=(
                            AtendimentoVeterinarioState
                            .data_atendimento_form
                        ),
                        on_change=(
                            AtendimentoVeterinarioState.atualizar_data
                        ),
                        placeholder="DD/MM/AAAA",
                        width="100%",
                        background=COR_CARTAO,
                        border=f"1px solid {COR_BORDA}",
                    ),
                ),

                campo_formulario(
                    "Horário",
                    rx.input(
                        type="time",
                        value=(
                            AtendimentoVeterinarioState.horario_form
                        ),
                        on_change=(
                            AtendimentoVeterinarioState.atualizar_horario
                        ),
                        width="100%",
                        background=COR_CARTAO,
                        border=f"1px solid {COR_BORDA}",
                    ),
                ),

                campo_formulario(
                    "Procedimento previsto",
                    rx.input(
                        value=(
                            AtendimentoVeterinarioState
                            .procedimento_form
                        ),
                        on_change=(
                            AtendimentoVeterinarioState
                            .atualizar_procedimento
                        ),
                        placeholder="Ex.: Consulta, vacinação ou exame",
                        width="100%",
                        background=COR_CARTAO,
                        border=f"1px solid {COR_BORDA}",
                    ),
                ),

                campo_formulario(
                    "Veterinário responsável",
                    rx.input(
                        value=(
                            AtendimentoVeterinarioState
                            .veterinario_responsavel_form
                        ),
                        on_change=(
                            AtendimentoVeterinarioState
                            .atualizar_veterinario
                        ),
                        placeholder="Nome do veterinário",
                        width="100%",
                        background=COR_CARTAO,
                        border=f"1px solid {COR_BORDA}",
                    ),
                ),

                rx.hstack(
                    rx.spacer(),
                    botao_secundario(
                        "Cancelar",
                        AtendimentoVeterinarioState.fechar_formulario,
                    ),
                    botao_principal(
                        "Agendar atendimento",
                        AtendimentoVeterinarioState.salvar_agendamento,
                    ),
                    width="100%",
                    justify="end",
                    margin_top="10px",
                    wrap="wrap",
                ),

                width="100%",
                align="start",
                spacing="3",
            ),
            padding="24px",
            background=COR_CARTAO,
            border=f"1px solid {COR_BORDA}",
            border_radius="14px",
            box_shadow=SOMBRA_SUAVE,
            width="100%",
        ),
        rx.fragment(),
    )


# ============================================================
# JANELA MODAL DE DETALHES DO ATENDIMENTO
# ============================================================

def painel_detalhes():
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.flex(
                    rx.vstack(
                        rx.dialog.title(
                            "Detalhes do Atendimento",
                            size="5",
                            color=COR_TITULO,
                            weight="bold",
                        ),
                        rx.dialog.description(
                            "Consulte e registre os dados clínicos da consulta.",
                            color=COR_TEXTO_CLARO,
                            font_size="14px",
                        ),
                        spacing="1",
                        align="start",
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon_button(
                            rx.icon("x", size=16),
                            on_click=(
                                AtendimentoVeterinarioState.fechar_detalhes
                            ),
                            background=COR_AREIA,
                            color=COR_TITULO,
                            border=f"1px solid {COR_CARAMELO}",
                            _hover={"background": "#E5D8C7"},
                        ),
                    ),
                    width="100%",
                    align="start",
                ),

                rx.divider(color=COR_BORDA),

                rx.heading(
                    AtendimentoVeterinarioState
                    .atendimento_selecionado["animal"],
                    size="5",
                    color=COR_PRINCIPAL,
                ),

                rx.grid(
                    rx.text(
                        "Data: "
                        + AtendimentoVeterinarioState
                        .atendimento_selecionado["data"],
                        color=COR_TEXTO,
                        font_size="14px",
                    ),
                    rx.text(
                        "Horário: "
                        + AtendimentoVeterinarioState
                        .atendimento_selecionado["horario"],
                        color=COR_TEXTO,
                        font_size="14px",
                    ),
                    rx.text(
                        "Procedimento: "
                        + AtendimentoVeterinarioState
                        .atendimento_selecionado["procedimento"],
                        color=COR_TEXTO,
                        font_size="14px",
                    ),
                    rx.text(
                        "Veterinário: "
                        + AtendimentoVeterinarioState
                        .atendimento_selecionado["veterinario"],
                        color=COR_TEXTO,
                        font_size="14px",
                    ),
                    columns={"initial": "1", "sm": "2"},
                    spacing="2",
                    width="100%",
                ),

                rx.box(
                    rx.vstack(
                        rx.text(
                            "Alergias: "
                            + AtendimentoVeterinarioState
                            .alergias_animal_selecionado,
                            color=COR_TEXTO,
                            font_size="14px",
                        ),
                        rx.text(
                            "Restrições clínicas: "
                            + AtendimentoVeterinarioState
                            .restricoes_animal_selecionado,
                            color=COR_TEXTO,
                            font_size="14px",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    padding="12px",
                    background=COR_FUNDO,
                    border=f"1px solid {COR_BORDA}",
                    border_radius="10px",
                    width="100%",
                ),

                rx.divider(color=COR_BORDA),

                rx.heading(
                    "Registro do Atendimento",
                    size="4",
                    color=COR_TITULO,
                ),

                rx.text(
                    "Preencha os dados clínicos após a realização do atendimento.",
                    color=COR_TEXTO_CLARO,
                    font_size="14px",
                ),

                campo_formulario(
                    "Diagnóstico",
                    rx.text_area(
                        value=(
                            AtendimentoVeterinarioState
                            .diagnostico_form
                        ),
                        on_change=(
                            AtendimentoVeterinarioState
                            .atualizar_diagnostico
                        ),
                        placeholder="Descreva o diagnóstico...",
                        width="100%",
                        background=COR_CARTAO,
                        border=f"1px solid {COR_BORDA}",
                    ),
                ),

                campo_formulario(
                    "Procedimentos realizados",
                    rx.text_area(
                        value=(
                            AtendimentoVeterinarioState
                            .procedimentos_realizados_form
                        ),
                        on_change=(
                            AtendimentoVeterinarioState
                            .atualizar_procedimentos_realizados
                        ),
                        placeholder="Descreva os procedimentos realizados...",
                        width="100%",
                        background=COR_CARTAO,
                        border=f"1px solid {COR_BORDA}",
                    ),
                ),

                campo_formulario(
                    "Tratamento indicado",
                    rx.text_area(
                        value=(
                            AtendimentoVeterinarioState
                            .tratamento_form
                        ),
                        on_change=(
                            AtendimentoVeterinarioState
                            .atualizar_tratamento
                        ),
                        placeholder="Informe o tratamento indicado...",
                        width="100%",
                        background=COR_CARTAO,
                        border=f"1px solid {COR_BORDA}",
                    ),
                ),

                rx.grid(
                    campo_formulario(
                        "Peso do animal (kg)",
                        rx.input(
                            value=AtendimentoVeterinarioState.peso_form,
                            on_change=AtendimentoVeterinarioState.atualizar_peso,
                            placeholder="Ex.: 12,5",
                            width="100%",
                            background=COR_CARTAO,
                            border=f"1px solid {COR_BORDA}",
                        ),
                    ),
                    campo_formulario(
                        "Custo do atendimento (R$)",
                        rx.input(
                            value=AtendimentoVeterinarioState.custo_form,
                            on_change=AtendimentoVeterinarioState.atualizar_custo,
                            placeholder="Ex.: 150,00",
                            width="100%",
                            background=COR_CARTAO,
                            border=f"1px solid {COR_BORDA}",
                        ),
                    ),
                    columns={"initial": "1", "sm": "2"},
                    spacing="3",
                    width="100%",
                ),

                mensagens_estado(),

                rx.heading(
                    "Atualizar Status",
                    size="3",
                    color=COR_TITULO,
                ),

                rx.flex(
                    botao_secundario(
                        "Agendado",
                        lambda: (
                            AtendimentoVeterinarioState
                            .atualizar_status("Agendado")
                        ),
                    ),
                    rx.button(
                        "Realizado",
                        on_click=lambda: (
                            AtendimentoVeterinarioState
                            .atualizar_status("Realizado")
                        ),
                        font_weight="600",
                        background="#ECEEDB",
                        color=COR_SUCESSO,
                        border="1px solid #C5C99A",
                        border_radius="9px",
                        _hover={
                            "background": "#E0E4C7",
                            "border_color": COR_VERDE_OLIVA,
                        },
                    ),
                    rx.button(
                        "Cancelar",
                        on_click=lambda: (
                            AtendimentoVeterinarioState
                            .atualizar_status("Cancelado")
                        ),
                        font_weight="600",
                        background="#FBE5E2",
                        color=COR_ERRO,
                        border="1px solid #E5B5AE",
                        border_radius="9px",
                        _hover={
                            "background": "#F5D2CD",
                            "border_color": COR_ERRO,
                        },
                    ),
                    width="100%",
                    wrap="wrap",
                    gap="2",
                ),

                rx.hstack(
                    rx.spacer(),
                    botao_principal(
                        "Salvar registro e marcar como realizado",
                        AtendimentoVeterinarioState
                        .salvar_registro_clinico,
                    ),
                    width="100%",
                    justify="end",
                    wrap="wrap",
                    margin_top="8px",
                ),

                width="100%",
                align="start",
                spacing="3",
            ),
            background=COR_CARTAO,
            border=f"1px solid {COR_BORDA}",
            border_radius="16px",
            max_width="640px",
            width="100%",
            max_height="88vh",
            overflow_y="auto",
            padding="24px",
        ),
        open=AtendimentoVeterinarioState.detalhes_abertos,
        on_open_change=lambda aberto: rx.cond(
            ~aberto,
            AtendimentoVeterinarioState.fechar_detalhes(),
            rx.noop(),
        ),
    )


# ============================================================
# HISTÓRICO RECENTE DE ATENDIMENTOS
# ============================================================

def painel_historico_passado():
    return rx.box(
        rx.vstack(
            rx.heading(
                "Histórico Recente de Atendimentos",
                size="4",
                color=COR_TITULO,
            ),
            rx.text(
                "Últimos atendimentos realizados ou finalizados",
                color=COR_TEXTO_CLARO,
                font_size="14px",
            ),
            rx.cond(
                AtendimentoVeterinarioState.atendimentos_passados.length() > 0,
                rx.vstack(
                    rx.foreach(
                        AtendimentoVeterinarioState.atendimentos_passados,
                        cartao_agendamento,
                    ),
                    width="100%",
                    spacing="2",
                ),
                rx.text(
                    "Nenhum atendimento finalizado registrado.",
                    color=COR_TEXTO_CLARO,
                    font_size="14px",
                ),
            ),
            width="100%",
            align="start",
            spacing="3",
        ),
        padding="20px",
        background=COR_CARTAO,
        border=f"1px solid {COR_BORDA}",
        border_radius="14px",
        box_shadow=SOMBRA_SUAVE,
        width="100%",
    )


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

def atendimento_veterinario_page():
    return rx.box(
        rx.flex(
            rx.box(
                sidebar_administracao(),
                width="260px",
                min_width="260px",
                height="100vh",
                position="sticky",
                top="0",
            ),

            rx.box(
                rx.vstack(
                    cabecalho_veterinario(),
                    resumo_kpis(),
                    rx.hstack(
                        botao_principal(
                            "＋ Novo Agendamento",
                            AtendimentoVeterinarioState.abrir_formulario,
                        ),
                        width="100%",
                        justify="end",
                    ),
                    mensagens_estado(),
                    formulario_agendamento(),
                    painel_agenda(),
                    painel_historico_passado(),
                    painel_detalhes(),
                    width="100%",
                    align="start",
                    spacing="4",
                ),
                flex="1",
                padding="24px 32px",
                min_width="0",
                overflow_y="auto",
            ),

            width="100%",
            align="start",
        ),
        background=COR_FUNDO,
        min_height="100vh",
        width="100%",
        on_mount=AtendimentoVeterinarioState.on_load,
    )