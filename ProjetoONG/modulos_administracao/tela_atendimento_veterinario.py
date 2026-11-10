
import reflex as rx

from ProjetoONG.state.atendimento_veterinario_state import (
    AtendimentoVeterinarioState,
)

from ProjetoONG.modulos_administracao.menu_administrativo import (
    sidebar_administracao,
)


# ============================================================
# CORES DO SISTEMA
# ============================================================

COR_PRINCIPAL = "#58392B"
COR_TITULO = "#2D1F18"
COR_TEXTO = "#52433D"
COR_TEXTO_CLARO = "#78675E"
COR_FUNDO = "#F8F3EC"
COR_CARTAO = "#FFFFFF"
COR_BORDA = "#E2D7C7"
COR_DESTAQUE = "#FFF8F0"

SOMBRA_SUAVE = "0 2px 8px rgba(45, 31, 24, 0.04)"


# ============================================================
# ESTILOS DE BOTÕES
# ============================================================

def botao_principal(texto: str, acao):
    return rx.button(
        texto,
        on_click=acao,
        background=COR_PRINCIPAL,
        color="#FFFFFF",
        border_radius="9px",
        _hover={"background": "#422A1F"},
    )


def botao_secundario(texto: str, acao):
    return rx.button(
        texto,
        on_click=acao,
        background="#EFE6DA",
        color=COR_PRINCIPAL,
        border_radius="9px",
        _hover={"background": "#E2D7C7"},
    )


# ============================================================
# CABEÇALHO
# ============================================================

def cabecalho_veterinario():
    return rx.flex(
        rx.vstack(
            rx.heading(
                "Atendimento Veterinário",
                size="6",
                color=COR_TITULO,
            ),
            rx.text(
                "Agenda clínica e acompanhamento dos animais",
                color=COR_TEXTO_CLARO,
                font_size="18px",
            ),
            spacing="1",
            align="start",
        ),
        rx.spacer(),
        botao_principal(
            "＋ Novo Agendamento",
            AtendimentoVeterinarioState.abrir_formulario,
        ),
        width="100%",
        align="center",
        wrap="wrap",
        margin_bottom="24px",
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
                color="#B91C1C",
                font_size="14px",
                font_weight="600",
            ),
            rx.fragment(),
        ),
        rx.cond(
            AtendimentoVeterinarioState.mensagem_sucesso != "",
            rx.text(
                AtendimentoVeterinarioState.mensagem_sucesso,
                color="#047857",
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
            variant="soft",
            color_scheme="gray",
        ),
        rx.text(
            AtendimentoVeterinarioState.data_selecionada,
            font_weight="600",
            color=COR_TITULO,
        ),
        rx.icon_button(
            rx.icon("chevron-right"),
            on_click=AtendimentoVeterinarioState.proximo_dia,
            variant="soft",
            color_scheme="gray",
        ),
        width="100%",
        align="center",
        margin_bottom="18px",
    )


# ============================================================
# CARTÃO DE AGENDAMENTO
# ============================================================

def cartao_agendamento(item):
    cor_status = rx.cond(
        item["status"] == "Realizado",
        "#059669",
        rx.cond(
            item["status"] == "Cancelado",
            "#DC2626",
            "#D97706",
        ),
    )

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
                    font_size="16px",
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
                        "green",
                        rx.cond(
                            item["status"] == "Cancelado",
                            "red",
                            "orange",
                        ),
                    ),
                    variant="soft",
                ),
                rx.button(
                    "Ver detalhes",
                    on_click=lambda: (
                        AtendimentoVeterinarioState.abrir_detalhes(
                            item["id"]
                        )
                    ),
                    size="2",
                    variant="soft",
                    color_scheme="brown",
                ),
                align="end",
                spacing="2",
            ),
            width="100%",
            align="center",
            wrap="wrap",
        ),
        padding="14px",
        background=COR_DESTAQUE,
        border_left=rx.cond(
            item["status"] == "Realizado",
            "4px solid #059669",
            rx.cond(
                item["status"] == "Cancelado",
                "4px solid #DC2626",
                "4px solid #D97706",
            ),
        ),
        border_radius="9px",
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
                    color=COR_TEXTO_CLARO,
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
            padding="35px",
            width="100%",
            background=COR_DESTAQUE,
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
        border_radius="12px",
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
            font_size="16px",
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
            border_radius="12px",
            box_shadow=SOMBRA_SUAVE,
            width="100%",
            margin_bottom="20px",
        ),
        rx.fragment(),
    )


# ============================================================
# DETALHES DO ANIMAL E ATENDIMENTO
# ============================================================

def painel_detalhes():
    return rx.cond(
        AtendimentoVeterinarioState.detalhes_abertos,
        rx.box(
            rx.vstack(
                rx.flex(
                    rx.heading(
                        "Detalhes do Atendimento",
                        size="4",
                        color=COR_TITULO,
                    ),
                    rx.spacer(),
                    rx.icon_button(
                        rx.icon("x"),
                        on_click=(
                            AtendimentoVeterinarioState.fechar_detalhes
                        ),
                        variant="soft",
                        color_scheme="gray",
                    ),
                    width="100%",
                    align="center",
                ),

                rx.divider(color=COR_BORDA),

                rx.heading(
                    AtendimentoVeterinarioState
                    .atendimento_selecionado["animal"],
                    size="5",
                    color=COR_PRINCIPAL,
                ),

                rx.text(
                    "Data: "
                    + AtendimentoVeterinarioState
                    .atendimento_selecionado["data"],
                    color=COR_TEXTO,
                ),

                rx.text(
                    "Horário: "
                    + AtendimentoVeterinarioState
                    .atendimento_selecionado["horario"],
                    color=COR_TEXTO,
                ),

                rx.text(
                    "Procedimento previsto: "
                    + AtendimentoVeterinarioState
                    .atendimento_selecionado["procedimento"],
                    color=COR_TEXTO,
                ),

                rx.text(
                    "Veterinário: "
                    + AtendimentoVeterinarioState
                    .atendimento_selecionado["veterinario"],
                    color=COR_TEXTO,
                ),

                rx.text(
                    "Alergias: "
                    + AtendimentoVeterinarioState
                    .alergias_animal_selecionado,
                    color=COR_TEXTO,
                ),

                rx.text(
                    "Restrições clínicas: "
                    + AtendimentoVeterinarioState
                    .restricoes_animal_selecionado,
                    color=COR_TEXTO,
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
                    ),
                ),

                campo_formulario(
                    "Peso do animal (kg)",
                    rx.input(
                        value=AtendimentoVeterinarioState.peso_form,
                        on_change=AtendimentoVeterinarioState.atualizar_peso,
                        placeholder="Ex.: 12,5",
                        width="100%",
                    ),
                ),

                campo_formulario(
                    "Custo do atendimento (R$)",
                    rx.input(
                        value=AtendimentoVeterinarioState.custo_form,
                        on_change=AtendimentoVeterinarioState.atualizar_custo,
                        placeholder="Ex.: 150,00",
                        width="100%",
                    ),
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
                        background="#D1FAE5",
                        color="#065F46",
                        border_radius="9px",
                        _hover={"background": "#A7F3D0"},
                    ),
                    rx.button(
                        "Cancelar",
                        on_click=lambda: (
                            AtendimentoVeterinarioState
                            .atualizar_status("Cancelado")
                        ),
                        background="#FEE2E2",
                        color="#991B1B",
                        border_radius="9px",
                        _hover={"background": "#FECACA"},
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
            padding="24px",
            background=COR_CARTAO,
            border=f"1px solid {COR_BORDA}",
            border_radius="12px",
            box_shadow=SOMBRA_SUAVE,
            width="100%",
            margin_bottom="20px",
        ),
        rx.fragment(),
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
                    mensagens_estado(),
                    formulario_agendamento(),
                    painel_detalhes(),
                    painel_agenda(),
                    painel_historico_passado(),
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
        on_mount=AtendimentoVeterinarioState.on_load
    )

def painel_historico_passado():
    return rx.box(
        rx.vstack(
            rx.heading("Histórico Recente de Atendimentos", size="4", color=COR_TITULO),
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
                        cartao_agendamento, # Reutiliza o mesmo cartão já existente!
                    ),
                    width="100%",
                    spacing="2",
                ),
                rx.text("Nenhum histórico passado registrado.", color=COR_TEXTO_CLARO, font_size="14px"),
            ),
            width="100%",
            align="start",
            spacing="3",
        ),
        padding="20px",
        background=COR_CARTAO,
        border=f"1px solid {COR_BORDA}",
        border_radius="12px",
        box_shadow=SOMBRA_SUAVE,
        width="100%",
    )



# ============================================================
# PAINEL DE MÉTRICAS (KPIs)
# ============================================================

def card_kpi(titulo: str, valor: str, icone: str, cor_icone: str = COR_PRINCIPAL):
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(titulo, color=COR_TEXTO_CLARO, font_size="13px", font_weight="500"),
                rx.heading(valor, size="6", color=COR_TITULO),
                align="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.icon(icone, size=28, color=cor_icone),
            width="100%",
            align="center",
        ),
        padding="16px 20px",
        background=COR_CARTAO,
        border=f"1px solid {COR_BORDA}",
        border_radius="12px",
        box_shadow=SOMBRA_SUAVE,
        flex="1",
        min_width="200px",
    )


def resumo_kpis():
    return rx.flex(
        card_kpi("Total de Atendimentos", AtendimentoVeterinarioState.total_do_mes, "stethoscope"),
        card_kpi("Agendados Pendentes", AtendimentoVeterinarioState.total_agendados, "calendar-clock", "#D97706"),
        card_kpi("Custo Total (R$)", AtendimentoVeterinarioState.custo_total_mes, "circle-dollar-sign", "#059669"),
        width="100%",
        gap="16px",
        wrap="wrap",
        margin_bottom="12px",
    )


# ============================================================
# HISTÓRICO RECENTE DE ATENDIMENTOS
# ============================================================

def painel_historico_passado():
    return rx.box(
        rx.vstack(
            rx.heading("Histórico Recente de Atendimentos", size="4", color=COR_TITULO),
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
                rx.text("Nenhum atendimento finalizado registrado.", color=COR_TEXTO_CLARO, font_size="14px"),
            ),
            width="100%",
            align="start",
            spacing="3",
        ),
        padding="20px",
        background=COR_CARTAO,
        border=f"1px solid {COR_BORDA}",
        border_radius="12px",
        box_shadow=SOMBRA_SUAVE,
        width="100%",
    )