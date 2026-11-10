import reflex as rx
from ProjetoONG.state.adocoes_state import AdocoesState
from ProjetoONG.modulos_administracao.menu_administrativo import (
    sidebar_administracao,
)

# ============================================================
# SISTEMA DE DESIGN: TOKENS VISUAIS
# ============================================================
COR_PRINCIPAL = "#58392B"
COR_PRINCIPAL_HOVER = "#422A1F"
COR_TITULO = "#2D1F18"
COR_TEXTO = "#52433D"
COR_TEXTO_CLARO = "#66534A"
COR_FUNDO = "#F8F3EC"
COR_FUNDO_SIDEBAR = "#EFE6DA"
COR_CARTAO = "#FFFFFF"
COR_DESTAQUE = "#FFF8F0"
COR_SUCESSO = "#059669"
COR_ERRO = "#DC2626"
COR_AVISO = "#D97706"
SOMBRA_SUAVE = "0 2px 8px rgba(45, 31, 24, 0.04)"
SOMBRA_LEVE = "0 1px 3px rgba(0, 0, 0, 0.03)"
RAIO_BORDA_GRANDE = "12px"
RAIO_BORDA_MEDIO = "10px"
RAIO_BORDA_PEQUENO = "8px"
ESPACO_PEQUENO = "8px"
ESPACO_MEDIO = "14px"
ESPACO_GRANDE = "20px"


# ============================================================
# COMPONENTE: CARD DE MÉTRICA
# ============================================================
def card_metrica(titulo: str, valor, cor_valor=COR_TITULO, componente_extra=None):
    return rx.box(
        rx.vstack(
            rx.text(titulo, color=COR_TEXTO_CLARO, font_size="16px", font_weight="600"),
            rx.hstack(
                rx.heading(valor, size="5", color=cor_valor),
                rx.spacer(),
                componente_extra if componente_extra is not None else rx.fragment(),
                width="100%",
            ),
            align="start",
        ),
        padding=ESPACO_GRANDE,
        background=COR_CARTAO,
        border_radius=RAIO_BORDA_GRANDE,
        border=f"1px solid {COR_FUNDO_SIDEBAR}",
        box_shadow=SOMBRA_SUAVE,
        width="100%",
        transition="transform 0.2s, box-shadow 0.2s",
        _hover={"transform": "translateY(-2px)", "box_shadow": "0 4px 12px rgba(45, 31, 24, 0.06)"},
    )


# ============================================================
# COMPONENTE: PAINEL DE MÉTRICAS
# ============================================================
def topo_metricas():
    return rx.grid(
        card_metrica(
            "Total de Adoções",
            AdocoesState.total_adocoes,
            componente_extra=rx.badge(AdocoesState.variacao_total, color_scheme="green", variant="soft", size="2"),
        ),
        card_metrica(
            "Em Processo",
            AdocoesState.em_processo,
            cor_valor=COR_AVISO,
            componente_extra=rx.badge("Aguardando", color_scheme="amber", variant="soft", size="2"),
        ),
        card_metrica("Aprovadas", AdocoesState.aprovadas, cor_valor=COR_SUCESSO),
        card_metrica("Recusadas", AdocoesState.recusadas, cor_valor=COR_ERRO),
        columns="4",
        spacing="4",
        width="100%",
        margin_bottom=ESPACO_GRANDE,
    )


# ============================================================
# COMPONENTE: CARD DE SOLICITAÇÃO
# ============================================================
def card_solicitacao_compacto(item):
    is_selected = AdocoesState.solicitacao_selecionada["id"] == item["id"]
    return rx.box(
        rx.hstack(
            rx.avatar(
                src=item["avatar"],
                fallback=item["nome_tutor"][:2],
                size="3",
                radius="full",
                border=rx.cond(
                    is_selected,
                    f"2px solid {COR_PRINCIPAL}",
                    f"2px solid {COR_FUNDO_SIDEBAR}",
                ),
            ),
            rx.vstack(
                rx.vstack(
                    rx.text(item["nome_tutor"], font_weight="600", font_size="16px", color=COR_TITULO),
                    rx.badge(
                        item["status"],
                        color_scheme=rx.match(
                            item["status"],
                            ("Aguardando Aprovação", "amber"),
                            ("Em Análise", "blue"),
                            ("Revisão Pendente", "orange"),
                            ("Recusada", "red"),
                            "green",
                        ),
                        variant="soft",
                        size="1",
                    ),
                    align="start",
                    width="100%",
                    spacing="1",
                ),
                rx.text("🐾 ", item["pet_nome"], font_size="16px", color=COR_TEXTO_CLARO),
                rx.text(item["data"], font_size="14px", color="#94A3B8"),
                spacing="1",
                width="100%",
                align="start",
            ),
            width="100%",
            spacing="3",
            align="center",
        ),
        padding=ESPACO_MEDIO,
        border_radius=RAIO_BORDA_GRANDE,
        border=rx.cond(is_selected, f"2px solid {COR_PRINCIPAL}", f"1px solid {COR_FUNDO_SIDEBAR}"),
        background=rx.cond(is_selected, COR_DESTAQUE, COR_CARTAO),
        cursor="pointer",
        on_click=lambda: AdocoesState.selecionar_solicitacao(item["id"]),
        margin_bottom=ESPACO_PEQUENO,
        width="100%",
        transition="all 0.2s ease",
        _hover={"border_color": COR_PRINCIPAL, "background": "#FFFAF5"},
    )


# ============================================================
# COMPONENTE: PAINEL ESQUERDO
# ============================================================
def painel_master_esquerda():
    return rx.vstack(
        rx.input(
            placeholder="Buscar tutor...",
            on_change=AdocoesState.set_filtro_texto,
            width="100%",
            size="2",
            border_radius=RAIO_BORDA_MEDIO,
        ),
        rx.box(
            rx.select(
                AdocoesState.opcoes_status,
                value=AdocoesState.filtro_status,
                on_change=AdocoesState.set_filtro_status,
                size="2",
                width="100%",
            ),
            width="100%",
            margin_y="6px",
        ),
        rx.divider(margin_y="8px", color_scheme="gray"),
        rx.box(
            rx.vstack(
                rx.foreach(AdocoesState.solicitacoes_filtradas, card_solicitacao_compacto),
                width="100%",
                spacing="1",
            ),
            width="100%",
            max_height=rx.cond(AdocoesState.tem_muitas_solicitacoes, "calc(100vh - 280px)", "none"),
            overflow_y=rx.cond(AdocoesState.tem_muitas_solicitacoes, "auto", "visible"),
            padding_right="4px",
        ),
        width="290px",
        min_width="260px",
        padding=ESPACO_MEDIO,
        background=COR_CARTAO,
        border_radius=RAIO_BORDA_GRANDE,
        border=f"1px solid {COR_FUNDO_SIDEBAR}",
        box_sizing="border-box",
        overflow="hidden",
        flex_shrink="0",
    )


# ============================================================
# COMPONENTE: CAMPO DO TUTOR
# ============================================================
def item_campo_tutor(rotulo: str, valor, tag_protegido: bool = False):
    return rx.hstack(
        rx.text(rotulo, font_weight="600", font_size="16px", color=COR_TEXTO, min_width="80px"),
        rx.text(
            valor,
            font_size="16px",
            color=COR_TITULO,
            white_space="nowrap",
            overflow="hidden",
            text_overflow="ellipsis",
        ),
        rx.badge("Protegido", color_scheme="red", variant="soft", size="1") if tag_protegido else rx.fragment(),
        align="center",
        spacing="3",
        width="100%",
    )


# ============================================================
# COMPONENTE: PAINEL DIREITO — DETALHES
# ============================================================
def detalhes_solicitacao():
    sol = AdocoesState.solicitacao_selecionada
    return rx.vstack(
        rx.heading("Solicitação — ", sol["nome_tutor"], size="3", color=COR_TITULO, margin_bottom="10px"),
        rx.flex(
            rx.box(
                rx.image(
                    src=sol["foto_detalhe"],
                    width="100%",
                    height="180px",
                    object_fit="cover",
                    border_radius="10px",
                    margin_y="8px",
                ),
                rx.heading("🐾 Dados do Pet", size="3", color=COR_PRINCIPAL, margin_top="6px"),
                rx.text("Nome: ", sol["pet_nome"], font_weight="700", font_size="16px", color=COR_TITULO),
                rx.text("Espécie: ", sol["pet_especie"], font_size="16px", color=COR_TEXTO),
                rx.text("Saúde: ", sol["pet_saude"], font_size="16px", font_weight="600", color=COR_SUCESSO),
                rx.text("Personalidade: ", sol["pet_personalidade"], font_size="16px", color=COR_TEXTO),
                rx.text("Histórico: ", sol["pet_historico"], font_size="16px", color=COR_TEXTO),
                padding="18px",
                background="#FFF9F2",
                border="1px solid #F2E4D4",
                border_radius=RAIO_BORDA_GRANDE,
                width="260px",
                flex_shrink="0",
            ),
            rx.box(
                rx.heading("👤 Dados do Tutor", size="3", color=COR_PRINCIPAL, margin_bottom="12px"),
                item_campo_tutor("Nome:", sol["nome_tutor"]),
                item_campo_tutor("CPF:", sol["cpf"], tag_protegido=True),
                item_campo_tutor("Telefone:", sol["telefone"]),
                item_campo_tutor("E-mail:", sol["email"]),
                item_campo_tutor("Endereço:", sol["endereco"]),
                rx.divider(margin_y="12px"),
                rx.heading("🏠 Perfil do Lar", size="3", color=COR_PRINCIPAL, margin_bottom="10px"),
                item_campo_tutor("Moradia:", sol["lar_tipo"]),
                item_campo_tutor("Família:", sol["lar_familia"]),
                item_campo_tutor("Tempo em casa:", sol["lar_tempo"]),
                item_campo_tutor("Experiência:", sol["exp_animal"]),
                rx.divider(margin_y="12px"),
                rx.heading("✅ Verificações", size="3", color=COR_PRINCIPAL, margin_bottom="10px"),
                item_campo_tutor("Cerca:", sol["check_cerca"]),
                item_campo_tutor("Espaço:", sol["check_espaco"]),
                item_campo_tutor("Outros animais:", sol["check_outros"]),
                rx.divider(margin_y="12px"),
                rx.heading("📊 Status", size="3", color=COR_PRINCIPAL, margin_bottom="10px"),
                rx.badge(sol["status"], color_scheme="blue", variant="solid", size="2"),
                rx.hstack(
                    rx.button("✅ Aprovar", on_click=lambda: AdocoesState.alterar_status("Aprovada"), color_scheme="green", size="2"),
                    rx.button("⏳ Solicitar Info", on_click=lambda: AdocoesState.alterar_status("Revisão Pendente"), color_scheme="amber", size="2"),
                    rx.button("❌ Recusar", on_click=lambda: AdocoesState.alterar_status("Recusada"), color_scheme="red", size="2"),
                    margin_top="15px",
                    spacing="3",
                ),
                padding="20px",
                background=COR_CARTAO,
                border_radius=RAIO_BORDA_GRANDE,
                box_shadow=SOMBRA_SUAVE,
                flex="1",
                min_width="320px",
            ),
            spacing="4",
            align="start",
            wrap="wrap",
        ),
        width="100%",
        align="start",
        padding="10px 0",
    )


def painel_detail_direita():
    return rx.cond(
        AdocoesState.solicitacao_selecionada["id"] != "",
        detalhes_solicitacao(),
        rx.center(
            rx.text("Selecione uma solicitação da lista", color=COR_TEXTO_CLARO, font_size="16px"),
            min_height="400px",
            width="100%",
        ),
    )


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================
@rx.page(route="/adocoes", title="Adoções | Porto Seguro Pet", on_load=AdocoesState.on_load)
def adocoes_page():
    """Página de Gerenciamento de Solicitações de Adoção."""
    return rx.box(
        rx.flex(
            # Barra lateral à esquerda
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
                rx.vstack(
                    rx.heading(
                        "Gestão de Adoções",
                        size="6",
                        color=COR_TITULO,
                        margin_bottom=ESPACO_MEDIO,
                    ),
                    topo_metricas(),
                    rx.flex(
                        painel_master_esquerda(),
                        rx.box(
                            painel_detail_direita(),
                            flex="1",
                            min_width="0",
                        ),
                        spacing="4",
                        align="start",
                        width="100%",
                    ),
                    width="100%",
                    align="start",
                ),
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
    )