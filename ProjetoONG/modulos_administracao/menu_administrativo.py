
import reflex as rx

# ============================================================
# SISTEMA DE DESIGN: TOKENS VISUAIS
# ============================================================
COR_PRINCIPAL = "#A96348"
COR_TITULO = "#FFFFFF"
COR_TEXTO = "#FFFFFF"
COR_TEXTO_CLARO = "#F8EDE5"
COR_FUNDO_SIDEBAR = "#C77D5B"
COR_CARTAO = "#A96348"
COR_DESTAQUE = "#B96F50"

SOMBRA_LEVE = "0 1px 3px rgba(0, 0, 0, 0.03)"

RAIO_BORDA_MEDIO = "10px"

ESPACO_PEQUENO = "8px"
ESPACO_GRANDE = "20px"


# ============================================================
# COMPONENTE: ITEM DE NAVEGAÇÃO
# ============================================================
def item_sidebar(icone: str, rotulo: str, rota: str = "#"):
    ativo = rx.State.router.page.path == rota

    return rx.link(
        rx.hstack(
            rx.icon(
                icone,
                size=20,
                color=rx.cond(ativo, "#FFFFFF", COR_TEXTO_CLARO),
                flex_shrink="0",
            ),
            rx.text(
                rotulo,
                font_size="16px",
                font_weight=rx.cond(ativo, "600", "500"),
                color=rx.cond(ativo, COR_TITULO, COR_TEXTO),
                white_space="nowrap",
            ),
            padding="12px 16px",
            border_radius=RAIO_BORDA_MEDIO,
            background=rx.cond(ativo, COR_CARTAO, "transparent"),
            box_shadow=rx.cond(ativo, SOMBRA_LEVE, "none"),
            width="100%",
            spacing="3",
            align="center",
            transition="all 0.2s ease",
            _hover={
                "background": rx.cond(ativo, COR_CARTAO, COR_DESTAQUE),
                "transform": "translateX(3px)",
            },
        ),
        href=rota,
        underline="none",
        width="100%",
    )


# ============================================================
# COMPONENTE: SIDEBAR ADMINISTRATIVA
# ============================================================
def sidebar_administracao():
    return rx.vstack(
        rx.hstack(
            rx.center(
                rx.icon("paw-print", size=20, color="#FFFFFF"),
                background="#A3A982",
                width="38px",
                height="38px",
                border_radius="10px",
            ),
            rx.vstack(
                rx.text(
                    "Porto Seguro Pet",
                    color=COR_TITULO,
                    font_weight="bold",
                    font_size="18px",
                ),
            
                spacing="0",
                align="start",
            ),
            align="center",
            spacing="3",
            margin_bottom=ESPACO_GRANDE,
            padding_x="4px",
        ),
        rx.text(
            "PRINCIPAL",
            font_size="12px",
            font_weight="bold",
            color=COR_TEXTO_CLARO,
            margin_top=ESPACO_PEQUENO,
            margin_bottom="2px",
            padding_x="8px",
        ),
        item_sidebar("layout-grid", "Início", "/administrativo"),
        item_sidebar("paw-print", "Gestão de Animais", "/animais"),
        item_sidebar("home", "Lares Temporários", "/lares-temporarios"),
        rx.text(
            "ATENDIMENTO",
            font_size="12px",
            font_weight="bold",
            color=COR_TEXTO_CLARO,
            margin_top="16px",
            margin_bottom="2px",
            padding_x="8px",
        ),
        item_sidebar("heart", "Atendimento Veterinário", "/atendimento-vet"),
        item_sidebar("heart-handshake", "Adoções", "/adocoes"),
        item_sidebar("clipboard-list", "Pós-Adoção", "/pos-adocao"),
        rx.text(
            "ADMINISTRAÇÃO",
            font_size="12px",
            font_weight="bold",
            color=COR_TEXTO_CLARO,
            margin_top="16px",
            margin_bottom="2px",
            padding_x="8px",
        ),
        item_sidebar("users", "Voluntários", "/voluntarios"),
        item_sidebar("heart", "Doações", "/doacoes"),
        rx.box(
            height="40px",
            width="100%",
            flex_shrink="0",
        ),
        width="100%",
        height="100%",
        overflow_y="auto",
        padding="20px 14px",
        background=COR_FUNDO_SIDEBAR,
        border_right="1px solid #E2D7C7",
        box_sizing="border-box",
        spacing="1",
        align="start",
    )
