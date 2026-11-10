import reflex as rx
from ProjetoONG.state.pos_adocao_state import PosAdocaoState
from ProjetoONG.modulos_administracao.menu_administrativo import sidebar_administracao

# ==========================================
# PALETA DE CORES
# ==========================================
COR_PRINCIPAL = "#58392B"
COR_PRINCIPAL_HOVER = "#422A1F"
COR_TITULO = "#2D1F18"
COR_TEXTO = "#52433D"
COR_TEXTO_CLARO = "#78675E"

COR_FUNDO = "#F8F3EC"
COR_CARTAO = "#FFFFFF"
COR_DESTAQUE = "#FFF8F0"

COR_SUCESSO = "#059669"
COR_AVISO = "#D97706"


def cabecalho_pos_adocao():
    return rx.vstack(
        rx.text(
            "Pós-Adoção",
            font_size="28px",
            font_weight="bold",
            color=COR_TITULO,
        ),
        rx.text(
            "Acompanhe a adaptação e o bem-estar dos animais adotados.",
            font_size="18px",
            color=COR_TEXTO_CLARO,
        ),
        align="start",
        spacing="1",
        width="100%",
    )


def cartao_indicador(icone, titulo, valor, descricao):
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon(icone, size=24, color=COR_PRINCIPAL),
                padding="12px",
                background=COR_DESTAQUE,
                border_radius="12px",
            ),
            rx.spacer(),
            rx.text(valor, font_size="26px", font_weight="bold", color=COR_TITULO),
            align="center",
            width="100%",
        ),
        rx.vstack(
            rx.text(titulo, font_size="16px", font_weight="bold", color=COR_TITULO),
            rx.text(descricao, font_size="14px", color=COR_TEXTO_CLARO),
            align="start",
            spacing="1",
            margin_top="12px",
        ),
        background=COR_CARTAO,
        padding="20px",
        border_radius="14px",
        box_shadow="0 2px 8px rgba(45, 31, 24, 0.06)",
        width="100%",
    )


def indicadores_pos_adocao():
    return rx.grid(
        cartao_indicador("heart-handshake", "Adoções efetivadas", PosAdocaoState.total_adocoes.to_string(), "Animais com adoção concluída"),
        cartao_indicador("clipboard-list", "Acompanhamentos", PosAdocaoState.total_acompanhamentos.to_string(), "Registros do animal selecionado"),
        cartao_indicador("calendar-check", "Registros recentes", "08", "Acompanhamentos neste mês"),
        columns="3",
        spacing="4",
        width="100%",
    )


def cartao_animal_pos_adocao(item: dict):
    """Cartão de animal gerado dinamicamente a partir dos processos do Xano."""
    is_selected = PosAdocaoState.processo_selecionado["id"] == item["id"]
    
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("paw-print", size=26, color=COR_PRINCIPAL),
                background=COR_DESTAQUE,
                padding="14px",
                border_radius="12px",
            ),
            rx.vstack(
                rx.text(item["nome_animal"], font_size="18px", font_weight="bold", color=COR_TITULO),
                rx.text(item["especie"], font_size="16px", color=COR_TEXTO_CLARO),
                rx.text(f"Tutor: {item['nome_tutor']}", font_size="16px", color=COR_TEXTO),
                rx.text(item["telefone"], font_size="16px", color=COR_TEXTO_CLARO),
                align="start",
                spacing="1",
                flex="1",
            ),
            align="center",
            width="100%",
        ),
        rx.text("Adoção efetivada", font_size="14px", font_weight="bold", color=COR_SUCESSO, margin_top="12px"),
        padding="14px",
        background=rx.cond(is_selected, COR_DESTAQUE, COR_CARTAO),
        border_radius="12px",
        border=rx.cond(is_selected, f"2px solid {COR_PRINCIPAL}", "1px solid #EAE1D7"),
        cursor="pointer",
        on_click=lambda: PosAdocaoState.selecionar_processo(item["id"]),
        width="100%",
    )


def painel_lista_animais():
    return rx.box(
        rx.vstack(
            rx.heading("Animais adotados", size="4", color=COR_TITULO),
            rx.text("Selecione um animal para consultar seu histórico.", font_size="14px", color=COR_TEXTO_CLARO),
            rx.input(
                placeholder="Pesquisar animal ou tutor...",
                on_change=PosAdocaoState.set_filtro_texto,
                width="100%",
                background=COR_FUNDO,
                border="1px solid #EAE1D7",
            ),
            rx.cond(
                PosAdocaoState.carregando_processos,
                rx.spinner(color=COR_PRINCIPAL),
                rx.foreach(
                    PosAdocaoState.processos_filtrados,
                    cartao_animal_pos_adocao,
                ),
            ),
            align="start",
            spacing="3",
            width="100%",
        ),
        background=COR_CARTAO,
        padding="20px",
        border_radius="14px",
        box_shadow="0 2px 8px rgba(45, 31, 24, 0.06)",
        width="100%",
    )


def informacoes_animal_tutor():
    proc = PosAdocaoState.processo_selecionado

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("paw-print", size=28, color=COR_PRINCIPAL),
                rx.vstack(
                    rx.heading(proc["nome_animal"], size="5", color=COR_TITULO),
                    rx.text(f"{proc['especie']} • {proc['status']}", font_size="12px", color=COR_SUCESSO),
                    align="start",
                    spacing="1",
                ),
                align="center",
                width="100%",
            ),
            rx.divider(),
            rx.heading("Informações do tutor", size="3", color=COR_TITULO),
            rx.hstack(
                rx.icon("user", color=COR_PRINCIPAL),
                rx.text(proc["nome_tutor"], font_size="16px", color=COR_TEXTO),
                align="center",
            ),
            rx.hstack(
                rx.icon("phone", color=COR_PRINCIPAL),
                rx.text(proc["telefone"], font_size="16px", color=COR_TEXTO),
                align="center",
            ),
            rx.hstack(
                rx.icon("map-pin", color=COR_PRINCIPAL),
                rx.text(proc["endereco"], font_size="16px", color=COR_TEXTO),
                align="center",
            ),
            align="start",
            spacing="3",
            width="100%",
        ),
        background=COR_CARTAO,
        padding="20px",
        border_radius="14px",
        box_shadow="0 2px 8px rgba(45, 31, 24, 0.06)",
        width="100%",
    )


def cartao_acompanhamento(item: dict):
    return rx.hstack(
        rx.box(
            rx.icon("calendar-check", color=COR_PRINCIPAL, size=20),
            background=COR_DESTAQUE,
            padding="10px",
            border_radius="50%",
        ),
        rx.vstack(
            rx.text(item["data_acompanhamento"], font_size="14px", font_weight="bold", color=COR_TITULO),
            rx.text(item["relatorio_observacao"], font_size="16px", color=COR_TEXTO),
            align="start",
            spacing="2",
            flex="1",
        ),
        align="start",
        width="100%",
        padding="14px",
        border_bottom="1px solid #EAE1D7",
    )


def linha_tempo_acompanhamentos():
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.heading(
                    "Histórico de acompanhamentos",
                    size="4",
                    color=COR_TITULO,
                    flex="1",
                ),
                rx.button(
                    rx.icon("plus", size=16),
                    "Novo registro",
                    on_click=PosAdocaoState.abrir_formulario,
                    background=COR_PRINCIPAL,
                    color="white",
                    _hover={"background": COR_PRINCIPAL_HOVER},
                    white_space="nowrap",
                    shrink="0",
                ),
                width="100%",
                align="center",
                justify="between",
                flex_wrap="wrap",
                gap="12px",
            ),
            rx.cond(
                PosAdocaoState.carregando_acompanhamentos,
                rx.spinner(color=COR_PRINCIPAL),
                rx.cond(
                    PosAdocaoState.acompanhamentos.length() > 0,
                    rx.vstack(
                        rx.foreach(PosAdocaoState.acompanhamentos, cartao_acompanhamento),
                        width="100%",
                        spacing="2",
                    ),
                    rx.text(
                        "Nenhum acompanhamento registrado para este animal.",
                        color=COR_TEXTO_CLARO,
                        padding_y="16px",
                        font_size="14px",
                    ),
                ),
            ),
            align="start",
            spacing="4",
            width="100%",
        ),
        background=COR_CARTAO,
        padding="20px",
        border_radius="14px",
        box_shadow="0 2px 8px rgba(45, 31, 24, 0.06)",
        width="100%",
    )


def painel_detalhes_pos_adocao():
    return rx.vstack(
        informacoes_animal_tutor(),
        linha_tempo_acompanhamentos(),
        spacing="4",
        width="100%",
    )


def formulario_acompanhamento():
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("Novo acompanhamento", size="4", color=COR_TITULO),
                rx.spacer(),
                rx.button(
                    rx.icon("x", size=16),
                    on_click=PosAdocaoState.fechar_formulario,
                    variant="ghost",
                    color=COR_TEXTO,
                ),
                align="center",
                width="100%",
            ),
            rx.text("Registre as informações sobre o acompanhamento do animal.", font_size="14px", color=COR_TEXTO_CLARO),
            rx.cond(
                PosAdocaoState.erro != "",
                rx.callout(PosAdocaoState.erro, icon="triangle_alert", color_scheme="red", width="100%"),
            ),
            rx.vstack(
                rx.text("Data do acompanhamento", font_size="16px", font_weight="bold", color=COR_TEXTO),
                rx.input(
                    type="date",
                    value=PosAdocaoState.data_acompanhamento,
                    on_change=PosAdocaoState.set_data_acompanhamento,
                    width="100%",
                    background=COR_FUNDO,
                    border="1px solid #EAE1D7",
                ),
                align="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text("Relatório de observação", font_size="16px", font_weight="bold", color=COR_TEXTO),
                rx.text_area(
                    placeholder="Descreva como está a adaptação do animal, sua saúde e seu bem-estar...",
                    value=PosAdocaoState.relatorio_observacao,
                    on_change=PosAdocaoState.set_relatorio_observacao,
                    width="100%",
                    min_height="130px",
                    background=COR_FUNDO,
                    border="1px solid #EAE1D7",
                ),
                align="start",
                spacing="2",
                width="100%",
            ),
            rx.hstack(
                rx.button(
                    "Cancelar",
                    on_click=PosAdocaoState.fechar_formulario,
                    variant="outline",
                    color=COR_PRINCIPAL,
                    border_color=COR_PRINCIPAL,
                ),
                rx.button(
                    "Salvar acompanhamento",
                    on_click=PosAdocaoState.salvar_acompanhamento,
                    background=COR_PRINCIPAL,
                    color="white",
                    _hover={"background": COR_PRINCIPAL_HOVER},
                ),
                justify="end",
                width="100%",
            ),
            align="start",
            spacing="4",
            width="100%",
        ),
        background=COR_CARTAO,
        padding="24px",
        border_radius="14px",
        box_shadow="0 2px 8px rgba(45, 31, 24, 0.06)",
        width="100%",
    )


def conteudo_pos_adocao():
    return rx.vstack(
        cabecalho_pos_adocao(),
        indicadores_pos_adocao(),
        rx.grid(
            painel_lista_animais(),
            painel_detalhes_pos_adocao(),
            columns="2",
            spacing="4",
            width="100%",
            align_items="start",
        ),
        rx.cond(
            PosAdocaoState.formulario_aberto,
            formulario_acompanhamento(),
            rx.fragment(),
        ),
        spacing="5",
        width="100%",
        padding="28px",
        background=COR_FUNDO,
    )


@rx.page(route="/admin/pos_adocao", on_load=PosAdocaoState.carregar_processos)
def pos_adocao():
    """Página de acompanhamento pós-adoção."""
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
                conteudo_pos_adocao(),
                flex="1",
                padding="24px 32px",
                overflow_y="auto",
                min_width="0",
            ),
            width="100%",
            align="start",
        ),
        background=COR_FUNDO,
        min_height="100vh",
        width="100%",
        # AQUI ESTÁ O SEGREDO: Força o disparo no carregamento visual
        on_mount=PosAdocaoState.carregar_processos,
    )