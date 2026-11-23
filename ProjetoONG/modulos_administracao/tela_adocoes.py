import reflex as rx
from ProjetoONG.state.adocoes_state import AdocoesState
from ProjetoONG.modulos_administracao.menu_administrativo import (
    sidebar_administracao,
)

# ============================================================
# SISTEMA DE DESIGN: PALETA PORTO SEGURO PET
# ============================================================
COR_PRINCIPAL = "#C77D5B"          # Terracota
COR_PRINCIPAL_HOVER = "#B26B4B"    # Terracota hover
COR_PRINCIPAL_SUAVE = "#F3E5DE"    # Terracota claro

COR_OLIVA = "#A3A66B"              # Verde oliva
COR_OLIVA_SUAVE = "#E7EAD6"        # Verde oliva claro
COR_OLIVA_TEXTO = "#5A5E36"        # Verde oliva escuro

COR_AREIA = "#EFE6DA"              # Areia
COR_CARAMELO = "#D6B99A"           # Caramelo
COR_CARAMELO_SUAVE = "#F5ECE1"     # Caramelo claro
COR_CARAMELO_TEXTO = "#7A5838"     # Caramelo escuro

COR_TITULO = "#2C2523"             # Grafite quente
COR_TEXTO = "#4F4643"              # Texto padrão
COR_TEXTO_CLARO = "#756A66"        # Subtítulos
COR_FUNDO = "#F8F3EC"              # Bege claro (fundo da página)
COR_CARTAO = "#FFFFFF"             # Branco
COR_DESTAQUE = "#F7EFEA"           # Destaque sutil terracota
COR_BORDA_SUTIL = "#E5DDD3"

COR_SUCESSO = "#5A5E36"
COR_ERRO = "#A64B3A"
COR_ERRO_SUAVE = "#F6E4E1"
COR_AVISO = "#8C6239"

SOMBRA_SUAVE = "0 2px 8px rgba(44, 37, 25, 0.04)"
RAIO_BORDA_GRANDE = "14px"
RAIO_BORDA_MEDIO = "10px"
RAIO_BORDA_PEQUENO = "8px"


# ============================================================
# COMPONENTE: INDICADOR COMPACTO EM LINHA
# ============================================================
def indicador_compacto(
    titulo: str,
    valor,
    icone: str,
    cor_icone: str = COR_PRINCIPAL,
    bg_pill: str = COR_CARTAO,
    borda_pill: str = COR_BORDA_SUTIL,
    cor_valor: str = COR_TITULO,
    extra=None,
):
    return rx.box(
        rx.hstack(
            rx.center(
                rx.icon(icone, size=16, color=cor_icone),
                background=COR_CARTAO,
                border=f"1px solid {borda_pill}",
                width="32px",
                height="32px",
                border_radius="8px",
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
                rx.hstack(
                    rx.text(
                        valor,
                        color=cor_valor,
                        font_size="18px",
                        font_weight="700",
                        line_height="1.2",
                    ),
                    extra if extra is not None else rx.fragment(),
                    align="center",
                    spacing="2",
                ),
                align="start",
                spacing="0",
            ),
            align="center",
            spacing="3",
            width="100%",
        ),
        padding="10px 14px",
        background=bg_pill,
        border=f"1px solid {borda_pill}",
        border_radius=RAIO_BORDA_MEDIO,
        width="100%",
    )


def topo_metricas_compacto():
    return rx.grid(
        indicador_compacto(
            titulo="Total de Adoções",
            valor=AdocoesState.total_adocoes,
            icone="heart-handshake",
            cor_icone=COR_PRINCIPAL,
            bg_pill=COR_PRINCIPAL_SUAVE,
            borda_pill="#E6CFC3",
            extra=rx.box(
                rx.text(
                    AdocoesState.variacao_total,
                    font_size="11px",
                    font_weight="600",
                    color=COR_OLIVA_TEXTO,
                ),
                background=COR_OLIVA_SUAVE,
                padding_x="6px",
                padding_y="1px",
                border_radius="6px",
            ),
        ),
        indicador_compacto(
            titulo="Em Processo",
            valor=AdocoesState.em_processo,
            icone="clock",
            cor_icone=COR_CARAMELO_TEXTO,
            bg_pill=COR_AREIA,
            borda_pill="#DFD3C3",
            cor_valor=COR_CARAMELO_TEXTO,
        ),
        indicador_compacto(
            titulo="Aprovadas",
            valor=AdocoesState.aprovadas,
            icone="circle-check",
            cor_icone=COR_OLIVA_TEXTO,
            bg_pill=COR_OLIVA_SUAVE,
            borda_pill="#D3D8BA",
            cor_valor=COR_OLIVA_TEXTO,
        ),
        indicador_compacto(
            titulo="Recusadas",
            valor=AdocoesState.recusadas,
            icone="circle-x",
            cor_icone=COR_ERRO,
            bg_pill=COR_ERRO_SUAVE,
            borda_pill="#E8C7C1",
            cor_valor=COR_ERRO,
        ),
        columns={"initial": "1", "sm": "2", "xl": "4"},
        spacing="3",
        width="100%",
    )


# ============================================================
# BADGES DE STATUS PADRONIZADOS
# ============================================================
def badge_status_adocao(status, compacto: bool = False):
    return rx.box(
        rx.text(
            status,
            font_size="11.5px" if compacto else "13px",
            font_weight="600",
            white_space="nowrap",
            color=rx.match(
                status,
                ("Aprovada", COR_OLIVA_TEXTO),
                ("Adoção efetivada", COR_OLIVA_TEXTO),
                ("Não aprovada", COR_ERRO),
                ("Recusada", COR_ERRO),
                COR_CARAMELO_TEXTO,
            ),
        ),
        background=rx.match(
            status,
            ("Aprovada", COR_OLIVA_SUAVE),
            ("Adoção efetivada", COR_OLIVA_SUAVE),
            ("Não aprovada", COR_ERRO_SUAVE),
            ("Recusada", COR_ERRO_SUAVE),
            COR_CARAMELO_SUAVE,
        ),
        padding_x="7px" if compacto else "10px",
        padding_y="2px" if compacto else "4px",
        border_radius="6px" if compacto else "7px",
        flex_shrink="0",
    )


def badge_status_pet(status):
    return rx.box(
        rx.text(
            status,
            font_size="13px",
            font_weight="600",
            white_space="nowrap",
            color=rx.match(
                status,
                ("Disponível", COR_OLIVA_TEXTO),
                ("Adotado", COR_PRINCIPAL),
                COR_CARAMELO_TEXTO,
            ),
        ),
        background=rx.match(
            status,
            ("Disponível", COR_OLIVA_SUAVE),
            ("Adotado", COR_PRINCIPAL_SUAVE),
            COR_CARAMELO_SUAVE,
        ),
        padding_x="10px",
        padding_y="4px",
        border_radius="7px",
        flex_shrink="0",
    )


# ============================================================
# ITEM ENXUTO DA LISTA DE SOLICITAÇÕES (AVATAR UNISSEX)
# ============================================================
def item_solicitacao_lista(item):
    is_selected = AdocoesState.solicitacao_selecionada["id"] == item["id"]
    return rx.box(
        rx.hstack(
            rx.center(
                rx.icon(
                    "user",
                    size=20,
                    color=rx.cond(is_selected, COR_CARTAO, COR_PRINCIPAL),
                ),
                width="40px",
                height="40px",
                border_radius="full",
                flex_shrink="0",
                background=rx.cond(is_selected, COR_PRINCIPAL, COR_PRINCIPAL_SUAVE),
                border=rx.cond(
                    is_selected,
                    f"1.5px solid {COR_PRINCIPAL}",
                    f"1px solid {COR_CARAMELO}",
                ),
            ),
            rx.vstack(
                rx.text(
                    item["nome_tutor"],
                    font_weight="700",
                    font_size="14px",
                    color=COR_TITULO,
                    width="100%",
                    truncate=True,
                ),
                rx.hstack(
                    rx.icon("paw-print", size=13, color=COR_PRINCIPAL, flex_shrink="0"),
                    rx.text(
                        item["pet_nome"],
                        font_size="13px",
                        font_weight="500",
                        color=COR_TEXTO,
                        truncate=True,
                    ),
                    rx.text("•", font_size="12px", color=COR_TEXTO_CLARO),
                    rx.text(
                        item["data"],
                        font_size="12px",
                        color=COR_TEXTO_CLARO,
                        white_space="nowrap",
                    ),
                    align="center",
                    spacing="1",
                    width="100%",
                ),
                badge_status_adocao(item["status"], compacto=True),
                spacing="1",
                flex="1",
                min_width="0",
                align="start",
            ),
            width="100%",
            spacing="3",
            align="center",
        ),
        padding="10px 12px",
        border_radius=RAIO_BORDA_MEDIO,
        border=rx.cond(
            is_selected,
            f"1.5px solid {COR_PRINCIPAL}",
            "1px solid transparent",
        ),
        border_bottom=rx.cond(
            is_selected,
            f"1.5px solid {COR_PRINCIPAL}",
            f"1px solid {COR_BORDA_SUTIL}",
        ),
        background=rx.cond(is_selected, COR_DESTAQUE, "transparent"),
        cursor="pointer",
        on_click=lambda: AdocoesState.selecionar_solicitacao(item["id"]),
        _hover={"background": COR_DESTAQUE},
        width="100%",
    )


# ============================================================
# COMPONENTE: PAINEL ESQUERDO
# ============================================================
def painel_master_esquerda():
    return rx.vstack(
        rx.input(
            placeholder="Buscar tutor ou pet...",
            on_change=AdocoesState.set_filtro_texto,
            width="100%",
            size="2",
            border_radius=RAIO_BORDA_PEQUENO,
            background=COR_CARTAO,
        ),
        rx.select(
            AdocoesState.opcoes_status,
            value=AdocoesState.filtro_status,
            on_change=AdocoesState.set_filtro_status,
            size="2",
            width="100%",
        ),
        rx.divider(color=COR_BORDA_SUTIL),
        rx.box(
            rx.vstack(
                rx.foreach(AdocoesState.solicitacoes_filtradas, item_solicitacao_lista),
                width="100%",
                spacing="1",
            ),
            width="100%",
            max_height=rx.cond(
                AdocoesState.tem_muitas_solicitacoes,
                "calc(100vh - 250px)",
                "none",
            ),
            overflow_y=rx.cond(AdocoesState.tem_muitas_solicitacoes, "auto", "visible"),
            overflow_x="hidden",
            padding_right="4px",
        ),
        width="305px",
        min_width="290px",
        padding="14px",
        background=COR_CARTAO,
        border_radius=RAIO_BORDA_GRANDE,
        border=f"1px solid {COR_BORDA_SUTIL}",
        box_shadow=SOMBRA_SUAVE,
        spacing="2",
        flex_shrink="0",
    )


# ============================================================
# COMPONENTE: CAMPOS DE INFORMAÇÃO
# ============================================================
def item_campo_pet(rotulo: str, valor):
    return rx.hstack(
        rx.text(
            rotulo,
            font_weight="600",
            font_size="13px",
            color=COR_TEXTO_CLARO,
            min_width="82px",
            flex_shrink="0",
        ),
        rx.text(
            valor,
            font_size="13.5px",
            font_weight="500",
            color=COR_TITULO,
            flex="1",
            min_width="0",
            line_height="1.4",
        ),
        align="start",
        spacing="2",
        width="100%",
    )


def item_campo_tutor(rotulo: str, valor, tag_protegido: bool = False):
    return rx.hstack(
        rx.text(
            rotulo,
            font_weight="600",
            font_size="14px",
            color=COR_TEXTO_CLARO,
            min_width="115px",
            flex_shrink="0",
        ),
        rx.text(
            valor,
            font_size="14px",
            font_weight="500",
            color=COR_TITULO,
            flex="1",
            min_width="0",
        ),
        rx.box(
            rx.text("Protegido", font_size="12px", font_weight="600", color=COR_TEXTO_CLARO),
            background=COR_AREIA,
            padding_x="8px",
            padding_y="2px",
            border_radius="6px",
        )
        if tag_protegido
        else rx.fragment(),
        align="center",
        spacing="2",
        width="100%",
    )


def titulo_bloco_detalhe(icone: str, texto: str, extra=None):
    return rx.hstack(
        rx.center(
            rx.icon(icone, size=15, color=COR_PRINCIPAL),
            background=COR_PRINCIPAL_SUAVE,
            width="26px",
            height="26px",
            border_radius="7px",
            flex_shrink="0",
        ),
        rx.heading(texto, size="3", color=COR_TITULO, font_weight="700"),
        rx.spacer(),
        extra if extra is not None else rx.fragment(),
        align="center",
        spacing="2",
        width="100%",
        margin_bottom="4px",
    )


# ============================================================
# COMPONENTE: PAINEL DIREITO — DETALHES UNIFICADOS
# ============================================================
def detalhes_solicitacao():
    sol = AdocoesState.solicitacao_selecionada
    return rx.box(
        rx.vstack(
            # Cabeçalho: Nome do Tutor + Status único (se Efetivada) ou Status do Pet + Etapa
            rx.hstack(
               # Cabeçalho: Nome do Tutor + Status único da Solicitação (ou Adotado ao efetivar)
            rx.hstack(
                rx.heading(
                    "Solicitação — ",
                    sol["nome_tutor"],
                    size="5",
                    color=COR_TITULO,
                    font_weight="700",
                ),
                rx.spacer(),
                rx.cond(
                    sol["status"] == "Adoção efetivada",
                    badge_status_pet("Adotado"),
                    badge_status_adocao(sol["status"]),
                ),
                width="100%",
                align="center",
                wrap="wrap",
                spacing="2",
            ),
                width="100%",
                align="center",
                wrap="wrap",
                spacing="2",
            ),
            rx.divider(color=COR_BORDA_SUTIL),

            # Conteúdo em 2 colunas dentro do mesmo container limpo
            rx.flex(
                # Coluna do Pet (moldura que exibe a foto inteira sem cortar)
                rx.vstack(
                    rx.center(
                        rx.image(
                            src=sol["foto_detalhe"],
                            width="100%",
                            max_height="240px",
                            object_fit="contain",
                            border_radius="8px",
                        ),
                        width="100%",
                        height="240px",
                        background=COR_AREIA,
                        border_radius="10px",
                        border=f"1px solid {COR_BORDA_SUTIL}",
                        overflow="hidden",
                        padding="4px",
                    ),
                    titulo_bloco_detalhe("paw-print", "Dados do Pet"),
                    item_campo_pet("Nome:", sol["pet_nome"]),
                    item_campo_pet("Espécie:", sol["pet_especie"]),
                    item_campo_pet("Porte:", sol["pet_detalhes"]),
                    item_campo_pet("Saúde:", sol["pet_saude"]),
                    item_campo_pet("Perfil:", sol["pet_descricao"]),
                    item_campo_pet("Cuidados:", sol["pet_cuidados"]),
                    spacing="2",
                    align="start",
                    width="320px",
                    flex_shrink="0",
                ),

                # Coluna do Tutor, Lar e Decisão
                rx.vstack(
                    titulo_bloco_detalhe("user", "Dados do Tutor"),
                    item_campo_tutor("Nome:", sol["nome_tutor"]),
                    item_campo_tutor("CPF:", sol["cpf"], tag_protegido=True),
                    item_campo_tutor("Telefone:", sol["telefone"]),
                    item_campo_tutor("E-mail:", sol["email"]),
                    item_campo_tutor("Endereço:", sol["endereco"]),

                    rx.divider(margin_y="6px", color=COR_BORDA_SUTIL),

                    titulo_bloco_detalhe("home", "Perfil do Lar e Verificações"),
                    item_campo_tutor("Moradia:", sol["lar_tipo"]),
                    item_campo_tutor("Família:", sol["lar_familia"]),
                    item_campo_tutor("Tempo em casa:", sol["lar_tempo"]),
                    item_campo_tutor("Experiência:", sol["exp_animal"]),
                    item_campo_tutor("Cerca / Espaço:", sol["check_cerca"]),
                    item_campo_tutor("Outros animais:", sol["check_outros"]),

                    rx.divider(margin_y="6px", color=COR_BORDA_SUTIL),

                    # Barra de ações de decisão
                    rx.hstack(
                        rx.button(
                            rx.icon("check", size=15),
                            "Aprovar",
                            on_click=lambda: AdocoesState.alterar_status("Aprovada"),
                            is_disabled=sol["status"] == "Adoção efetivada",
                            size="2",
                            font_weight="600",
                            background=COR_OLIVA_SUAVE,
                            color=COR_OLIVA_TEXTO,
                            border="1px solid #C5C99A",
                            border_radius="9px",
                            cursor="pointer",
                            _hover={"background": "#DCE1C3"},
                        ),
                        rx.cond(
                            sol["status"] == "Aprovada",
                            rx.button(
                                rx.icon("heart-handshake", size=15),
                                "Efetivar Adoção",
                                on_click=lambda: AdocoesState.alterar_status("Adoção efetivada"),
                                is_disabled=sol["status"] == "Adoção efetivada",
                                size="2",
                                font_weight="600",
                                background=COR_PRINCIPAL,
                                color=COR_CARTAO,
                                border=f"1px solid {COR_PRINCIPAL}",
                                border_radius="9px",
                                cursor="pointer",
                                _hover={"background": COR_PRINCIPAL_HOVER},
                            ),
                        ),
                        rx.button(
                            rx.icon("message-square", size=15),
                            "Solicitar Info",
                            on_click=lambda: AdocoesState.alterar_status("Mais informações necessárias"),
                            is_disabled=sol["status"] == "Adoção efetivada",
                            size="2",
                            font_weight="600",
                            background=COR_PRINCIPAL_SUAVE,
                            color=COR_PRINCIPAL,
                            border="1px solid #DFB9A6",
                            border_radius="9px",
                            cursor="pointer",
                            _hover={"background": "#ECD4C8"},
                        ),
                        rx.button(
                            rx.icon("x", size=15),
                            "Recusar",
                            on_click=lambda: AdocoesState.alterar_status("Não aprovada"),
                            is_disabled=sol["status"] == "Adoção efetivada",
                            size="2",
                            font_weight="600",
                            background=COR_ERRO_SUAVE,
                            color=COR_ERRO,
                            border="1px solid #E5B5AE",
                            border_radius="9px",
                            cursor="pointer",
                            _hover={"background": "#F2D5CF"},
                        ),
                        spacing="3",
                        wrap="wrap",
                    ),

                    # Legenda breve das etapas e botões
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "• Aprovar: valida o perfil do tutor e habilita a etapa final de entrega.",
                                font_size="12px",
                                color=COR_TEXTO_CLARO,
                            ),
                            rx.text(
                                "• Efetivar Adoção: conclui o processo e altera o status do pet para Adotado.",
                                font_size="12px",
                                color=COR_TEXTO_CLARO,
                            ),
                            rx.text(
                                "• Solicitar Info / Recusar: pede complementação de dados ou encerra o pedido sem aprovação.",
                                font_size="12px",
                                color=COR_TEXTO_CLARO,
                            ),
                            spacing="1",
                            align="start",
                        ),
                        background=COR_FUNDO,
                        border=f"1px solid {COR_BORDA_SUTIL}",
                        border_radius="8px",
                        padding="8px 12px",
                        margin_top="4px",
                        width="100%",
                    ),
                    spacing="2",
                    align="start",
                    flex="1",
                    min_width="300px",
                ),
                spacing="5",
                align="start",
                width="100%",
                wrap="wrap",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="22px",
        background=COR_CARTAO,
        border=f"1px solid {COR_BORDA_SUTIL}",
        border_radius=RAIO_BORDA_GRANDE,
        box_shadow=SOMBRA_SUAVE,
        width="100%",
    )


def painel_detail_direita():
    return rx.cond(
        AdocoesState.solicitacao_selecionada["id"] != "",
        detalhes_solicitacao(),
        rx.center(
            rx.text(
                "Selecione uma solicitação na lista à esquerda.",
                color=COR_TEXTO_CLARO,
                font_size="15px",
            ),
            background=COR_CARTAO,
            border=f"1px solid {COR_BORDA_SUTIL}",
            border_radius=RAIO_BORDA_GRANDE,
            box_shadow=SOMBRA_SUAVE,
            min_height="360px",
            width="100%",
        ),
    )


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================
def adocoes_page():
    """Página de Gerenciamento de Solicitações de Adoção."""
    return rx.box(
        rx.flex(
            # Barra lateral à esquerda
            rx.box(
                sidebar_administracao(),
                width="250px",
                min_width="250px",
                height="100vh",
                position="sticky",
                top="0",
            ),
            # Conteúdo principal
            rx.box(
                rx.vstack(
                    rx.vstack(
                        rx.heading(
                            "Gestão de Adoções",
                            size="7",
                            color=COR_TITULO,
                            font_weight="700",
                        ),
                        rx.text(
                            "Avalie solicitações, verifique o perfil dos tutores e acompanhe o status.",
                            color=COR_TEXTO_CLARO,
                            font_size="16px",
                        ),
                        align="start",
                        spacing="1",
                        width="100%",
                    ),
                    topo_metricas_compacto(),
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
                    spacing="4",
                    width="100%",
                    align="start",
                ),
                flex="1",
                padding="24px 28px",
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