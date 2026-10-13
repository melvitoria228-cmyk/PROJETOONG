
import os
from datetime import date, datetime, timezone

import httpx
import reflex as rx
from dotenv import load_dotenv

# Este módulo é importado antes do load_dotenv() do arquivo principal,
# por isso o .env é carregado aqui também.
load_dotenv()

COR_PRINCIPAL = "#684638"
COR_TEXTO = "#342D29"
COR_SECUNDARIA = "#766A62"
COR_FUNDO = "#FAF6F0"
COR_BORDA = "#EAE1D7"
COR_DESTAQUE = "#F4E8DC"

# Opções dos campos de seleção do formulário.
# AJUSTE se os valores aceitos no Xano forem outros.
ESPECIES = ["Cão", "Gato", "Outro"]
SEXOS = ["Macho", "Fêmea"]
PORTES = ["Pequeno", "Médio", "Grande"]
STATUS = [
    "Disponível",
    "Em lar temporário",
    "Em processo de adoção",
    "Adotado",
    "Falecido",
]
TODAS_ESPECIES = "Todas as espécies"
TODOS_PORTES = "Todos os portes"
TODOS_STATUS = "Todos os status"

# ---------------------------------------------------------------------------
# Configuração do Xano
# ---------------------------------------------------------------------------
XANO_ANIMAL_LIST_URL = os.getenv("XANO_ANIMAL_LIST_URL")
XANO_ANIMAL_CREATE_URL = os.getenv("XANO_ANIMAL_CREATE_URL")
XANO_ANIMAL_UPDATE_URL = os.getenv("XANO_ANIMAL_UPDATE_URL")
XANO_ANIMAL_DELETE_URL = os.getenv("XANO_ANIMAL_DELETE_URL")
METODO_ATUALIZAR = os.getenv("XANO_ANIMAL_UPDATE_METHOD", "PATCH").upper()

# Nome de cada campo da tela -> nome da coluna na tabela ANIMAL do Xano.
CAMPOS = {
    "id": "id",
    "nome": "nome",
    "especie": "especie",
    "especie_outro": "especie_outro",
    "descricao": "descricao",
    "raca": "raca",
    "idade": "idade_estimada_meses",  # integer
    "sexo": "sexo",
    "porte": "porte",
    "condicao": "condicao_saude",
    "data_resgate": "data_resgate",
    "status": "status_atual",
}
# Nomes alternativos aceitos na LEITURA, caso alguma coluna tenha outro nome.
ALTERNATIVAS: dict[str, list[str]] = {}

# A coluna idade_estimada guarda a idade em MESES (True) ou em ANOS (False).
IDADE_EM_MESES = True
ROTULO_IDADE = "Idade estimada (meses)" if IDADE_EM_MESES else "Idade estimada (anos)"
EXEMPLO_IDADE = "Ex.: 18" if IDADE_EM_MESES else "Ex.: 2"


def _data_iso(v) -> str:
    """Converte a data do Xano (texto ou timestamp em ms) para AAAA-MM-DD."""
    if v is None or v == "":
        return ""
    if isinstance(v, (int, float)):
        return datetime.fromtimestamp(v / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
    return str(v)[:10]


def _data_br(iso: str) -> str:
    try:
        ano, mes, dia = iso.split("-")
        return f"{dia}/{mes}/{ano}"
    except ValueError:
        return "Não informada"


def _idade_texto(v: str) -> str:
    try:
        n = int(v)
    except (TypeError, ValueError):
        return "Não informada"
    if not IDADE_EM_MESES:
        return f"{n} ano" if n == 1 else f"{n} anos"
    if n < 12:
        return f"{n} mês" if n == 1 else f"{n} meses"
    anos, meses = divmod(n, 12)
    texto = f"{anos} ano" if anos == 1 else f"{anos} anos"
    if meses:
        texto += f" e {meses} " + ("mês" if meses == 1 else "meses")
    return texto


def xano_para_tela(item: dict) -> dict[str, str]:
    """Converte um registro do Xano no formato usado pela tela."""

    def bruto(chave: str):
        v = item.get(CAMPOS[chave])
        if v is None:
            for alt in ALTERNATIVAS.get(chave, []):
                v = item.get(alt)
                if v is not None:
                    break
        return v

    def valor(chave: str) -> str:
        v = bruto(chave)
        return "" if v is None else str(v)

    id_ = valor("id")
    try:
        codigo = f"#{int(id_):03d}"
    except ValueError:
        codigo = f"#{id_}"

    data_iso = _data_iso(bruto("data_resgate"))

    return {
        "id": id_,
        "codigo": codigo,
        "nome": valor("nome") or "Sem nome",
        "especie": valor("especie") or "Outros",
        "especie_outro": valor("especie_outro"),
        "descricao": valor("descricao"),
        "raca": valor("raca") or "Sem raça definida",
        "sexo": valor("sexo") or "Não informado",
        "porte": valor("porte") or "Não informado",
        "condicao": valor("condicao"),
        "condicao_txt": valor("condicao") or "Não informada",
        "data_resgate": data_iso,
        "resgate": _data_br(data_iso) if data_iso else "Não informada",
        "idade_valor": valor("idade"),
        "idade": _idade_texto(valor("idade")),
        "status": valor("status") or "Sem status",
    }


def tela_para_xano(dados: dict) -> dict:
    """Converte os dados do formulário no corpo enviado ao Xano."""
    return {
        CAMPOS[chave]: dados[chave]
        for chave in (
            "nome", "especie", "especie_outro", "raca", "idade", "sexo",
            "porte", "condicao", "descricao", "data_resgate", "status",
        )
    }


def url_animal(base: str | None, id_: str) -> str:
    """Monta a URL de um animal: aceita {animal_id}/{id} ou acrescenta /id."""
    if not base:
        return ""
    for marcador in ("{animal_id}", "{id}"):
        if marcador in base:
            return base.replace(marcador, id_)
    return base.rstrip("/") + "/" + id_


# ---------------------------------------------------------------------------
# Estado
# ---------------------------------------------------------------------------
class AnimalState(rx.State):
    token: str = ""
    animais: list[dict[str, str]] = []
    carregando: bool = False
    salvando: bool = False
    erro_api: str = ""

    # filtros e paginação
    busca: str = ""
    filtro_especie: str = TODAS_ESPECIES
    filtro_porte: str = TODOS_PORTES
    filtro_status: str = TODOS_STATUS
    pagina: int = 1
    por_pagina: int = 5

    # formulário (cadastro / edição)
    dialogo_form_aberto: bool = False
    editando_id: str = ""
    form_nome: str = ""
    form_especie: str = "Cão"
    form_especie_outro: str = ""
    form_sexo: str = "Macho"
    form_porte: str = "Médio"
    form_raca: str = ""
    form_idade: str = ""
    form_condicao: str = ""
    form_descricao: str = ""
    form_data_resgate: str = ""
    form_status: str = "Disponível"
    erro_form: str = ""

    # visualização e exclusão
    dialogo_ver_aberto: bool = False
    animal_visto: dict[str, str] = {}
    dialogo_excluir_aberto: bool = False
    id_excluir: str = ""
    nome_excluir: str = ""

    # ---- acesso ao Xano ----
    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    async def _buscar_animais(self) -> str:
        """Carrega a lista. Retorna "" em caso de sucesso ou a mensagem de erro."""
        if not XANO_ANIMAL_LIST_URL:
            return "A URL de listagem não está configurada (XANO_ANIMAL_LIST_URL)."
        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta = await cliente.get(
                    XANO_ANIMAL_LIST_URL, headers=self._headers()
                )
        except httpx.RequestError as erro:
            print(f"Falha de conexão ao listar animais: {type(erro).__name__}")
            return "Falha de conexão com o servidor."

        if resposta.status_code in (401, 403):
            return "Sessão expirada. Faça login novamente."
        if resposta.status_code != 200:
            print(f"Erro ao listar animais: HTTP {resposta.status_code} {resposta.text[:300]}")
            return f"O servidor não conseguiu listar os animais (HTTP {resposta.status_code})."

        try:
            dados = resposta.json()
        except ValueError:
            print("A listagem de animais não retornou JSON.")
            return "Resposta inválida do servidor."

        if isinstance(dados, dict):
            dados = dados.get("items", [])
        if not isinstance(dados, list):
            return "Formato de resposta inesperado."

        # TEMPORÁRIO: mostra no terminal um registro de exemplo, para conferir
        # nomes de campos e valores (sexo, porte, status...). 
        if dados:
            print("Exemplo de registro do Xano:", dados[0])

        self.animais = [xano_para_tela(i) for i in dados if isinstance(i, dict)]
        return ""

    async def _requisicao(self, metodo: str, url: str, corpo: dict | None = None) -> str:
        """Envia POST/PATCH/PUT/DELETE. Retorna "" em caso de sucesso ou o erro."""
        if not url:
            return "URL não configurada no arquivo .env."
        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta = await cliente.request(
                    metodo, url, json=corpo, headers=self._headers()
                )
        except httpx.RequestError as erro:
            print(f"Falha de conexão ({metodo}): {type(erro).__name__}")
            return "Falha de conexão com o servidor."

        if resposta.status_code in (401, 403):
            return "Sessão expirada. Faça login novamente."
        if resposta.status_code not in (200, 201, 204):
            print(f"Erro {metodo}: HTTP {resposta.status_code} {resposta.text[:300]}")
            return f"O servidor recusou a operação (HTTP {resposta.status_code})."
        return ""

    # ---- carga inicial ----
    @rx.event
    async def carregar(self, token: str):
        self.token = token
        self.carregando = True
        self.erro_api = ""
        yield
        self.erro_api = await self._buscar_animais()
        self.carregando = False

    # ---- setters explícitos ----
    @rx.event
    def set_busca(self, valor: str):
        self.busca = valor
        self.pagina = 1

    @rx.event
    def set_filtro_especie(self, valor: str):
        self.filtro_especie = valor
        self.pagina = 1

    @rx.event
    def set_filtro_porte(self, valor: str):
        self.filtro_porte = valor
        self.pagina = 1

    @rx.event
    def set_filtro_status(self, valor: str):
        self.filtro_status = valor
        self.pagina = 1

    @rx.event
    def limpar_filtros(self):
        self.busca = ""
        self.filtro_especie = TODAS_ESPECIES
        self.filtro_porte = TODOS_PORTES
        self.filtro_status = TODOS_STATUS
        self.pagina = 1

    @rx.event
    def set_form_nome(self, valor: str):
        self.form_nome = valor

    @rx.event
    def set_form_especie(self, valor: str):
        self.form_especie = valor

    @rx.event
    def set_form_especie_outro(self, valor: str):
        self.form_especie_outro = valor

    @rx.event
    def set_form_sexo(self, valor: str):
        self.form_sexo = valor

    @rx.event
    def set_form_porte(self, valor: str):
        self.form_porte = valor

    @rx.event
    def set_form_raca(self, valor: str):
        self.form_raca = valor

    @rx.event
    def set_form_idade(self, valor: str):
        self.form_idade = valor

    @rx.event
    def set_form_condicao(self, valor: str):
        self.form_condicao = valor

    @rx.event
    def set_form_descricao(self, valor: str):
       self.form_descricao = valor

    @rx.event
    def set_form_data_resgate(self, valor: str):
        self.form_data_resgate = valor

    @rx.event
    def set_form_status(self, valor: str):
        self.form_status = valor

    @rx.event
    def set_dialogo_form_aberto(self, aberto: bool):
        self.dialogo_form_aberto = aberto

    @rx.event
    def set_dialogo_ver_aberto(self, aberto: bool):
        self.dialogo_ver_aberto = aberto

    @rx.event
    def set_dialogo_excluir_aberto(self, aberto: bool):
        self.dialogo_excluir_aberto = aberto

    # ---- paginação ----
    @rx.event
    def pagina_anterior(self):
        if self.pagina > 1:
            self.pagina -= 1

    @rx.event
    def pagina_seguinte(self):
        if self.pagina < self.total_paginas:
            self.pagina += 1

    # ---- cadastro / edição ----
    @rx.event
    def abrir_cadastro(self):
        self.editando_id = ""
        self.form_nome = ""
        self.form_especie = "Cão"
        self.form_especie_outro = ""
        self.form_sexo = "Macho"
        self.form_porte = "Médio"
        self.form_raca = ""
        self.form_idade = ""
        self.form_condicao = ""
        self.form_descricao = ""
        self.form_data_resgate = ""
        self.form_status = "Disponível"
        self.erro_form = ""
        self.dialogo_form_aberto = True

    @rx.event
    def abrir_edicao(self, id_animal: str):
        for a in self.animais:
            if a["id"] == id_animal:
                self.editando_id = id_animal
                self.form_nome = a["nome"]
                self.form_especie = a["especie"]
                self.form_especie_outro = a.get("especie_outro", "")
                self.form_sexo = a["sexo"]
                self.form_porte = a["porte"]
                self.form_raca = a["raca"]
                self.form_idade = a["idade_valor"]
                self.form_condicao = a["condicao"]
                self.form_descricao = a.get("descricao", "")
                self.form_data_resgate = a["data_resgate"]
                self.form_status = a["status"]
                self.erro_form = ""
                self.dialogo_form_aberto = True
                return

    @rx.event
    async def salvar_animal(self):
        nome = self.form_nome.strip()
        raca = self.form_raca.strip()
        idade = self.form_idade.strip()
        data_resgate = self.form_data_resgate.strip()
        condicao = self.form_condicao.strip()

        # Todos os campos da tabela ANIMAL são obrigatórios, menos ID e created_at.
        faltando = [
            rotulo
            for rotulo, valor in (
                ("nome", nome),
                ("raça", raca),
                ("idade estimada", idade),
                ("data do resgate", data_resgate),
                ("condição de saúde", condicao),
            )
            if not valor
        ]
        if faltando:
            self.erro_form = "Preencha: " + ", ".join(faltando) + "."
            return
        if not idade.isdigit():
            self.erro_form = "A idade estimada deve ser um número inteiro."
            return

        corpo = tela_para_xano(
            {
                "nome": nome,
                "especie": self.form_especie,
                "especie_outro": self.form_especie_outro.strip() if self.form_especie == "Outro" else "",
                "raca": raca,
                "idade": int(idade),
                "sexo": self.form_sexo,
                "porte": self.form_porte,
                "condicao": condicao,
                "descricao": self.form_descricao.strip(),
                "data_resgate": data_resgate,
                "status": self.form_status,
            }
        )

        self.salvando = True
        self.erro_form = ""
        yield

        if self.editando_id:
            erro = await self._requisicao(
                METODO_ATUALIZAR,
                url_animal(XANO_ANIMAL_UPDATE_URL, self.editando_id),
                corpo,
            )
            mensagem = f"{nome} foi atualizado."
        else:
            erro = await self._requisicao("POST", XANO_ANIMAL_CREATE_URL or "", corpo)
            mensagem = f"{nome} foi cadastrado."

        self.salvando = False
        if erro:
            self.erro_form = erro
            return

        self.dialogo_form_aberto = False
        self.erro_api = await self._buscar_animais()
        yield rx.toast.success(mensagem)

    # ---- visualização ----
    @rx.event
    def abrir_visualizacao(self, id_animal: str):
        for a in self.animais:
            if a["id"] == id_animal:
                self.animal_visto = a
                self.dialogo_ver_aberto = True
                return

    # ---- exclusão ----
    @rx.event
    def pedir_exclusao(self, id_animal: str, nome: str):
        self.id_excluir = id_animal
        self.nome_excluir = nome
        self.dialogo_excluir_aberto = True

    @rx.event
    async def confirmar_exclusao(self):
        self.salvando = True
        yield
        erro = await self._requisicao(
            "DELETE", url_animal(XANO_ANIMAL_DELETE_URL, self.id_excluir)
        )
        self.salvando = False
        self.dialogo_excluir_aberto = False
        if erro:
            yield rx.toast.error(erro)
            return

        self.animais = [a for a in self.animais if a["id"] != self.id_excluir]
        if self.pagina > self.total_paginas:
            self.pagina = self.total_paginas
        yield rx.toast.info(f"{self.nome_excluir} foi removido.")

    # ---- valores calculados ----
    @rx.var
    def total(self) -> int:
        return len(self.animais)

    @rx.var
    def qtd_caes(self) -> int:
        return sum(1 for a in self.animais if a["especie"] == "Cão")

    @rx.var
    def qtd_gatos(self) -> int:
        return sum(1 for a in self.animais if a["especie"] == "Gato")

    @rx.var
    def qtd_recentes(self) -> int:
        """Animais resgatados nos últimos 30 dias."""
        hoje = date.today()
        n = 0
        for a in self.animais:
            try:
                d = date.fromisoformat(a["data_resgate"])
            except ValueError:
                continue
            if 0 <= (hoje - d).days <= 30:
                n += 1
        return n

    @rx.var
    def opcoes_status(self) -> list[str]:
        """Opções do filtro de status, montadas a partir dos dados reais."""
        return [TODOS_STATUS] + sorted({a["status"] for a in self.animais})

    @rx.var
    def animais_filtrados(self) -> list[dict[str, str]]:
        termo = self.busca.strip().lower()
        resultado = []
        for a in self.animais:
            if termo and termo not in a["nome"].lower() and termo not in a["codigo"].lower():
                continue
            if self.filtro_especie != TODAS_ESPECIES and a["especie"] != self.filtro_especie:
                continue
            if self.filtro_porte != TODOS_PORTES and a["porte"] != self.filtro_porte:
                continue
            if self.filtro_status != TODOS_STATUS and a["status"] != self.filtro_status:
                continue
            resultado.append(a)
        return resultado

    @rx.var
    def total_filtrado(self) -> int:
        return len(self.animais_filtrados)

    @rx.var
    def total_paginas(self) -> int:
        return max(1, -(-len(self.animais_filtrados) // self.por_pagina))

    @rx.var
    def animais_pagina(self) -> list[dict[str, str]]:
        pagina = min(max(self.pagina, 1), self.total_paginas)
        inicio = (pagina - 1) * self.por_pagina
        return self.animais_filtrados[inicio : inicio + self.por_pagina]

    @rx.var
    def texto_exibicao(self) -> str:
        total = len(self.animais_filtrados)
        if total == 0:
            return "Nenhum animal encontrado"
        pagina = min(max(self.pagina, 1), self.total_paginas)
        inicio = (pagina - 1) * self.por_pagina + 1
        fim = min(pagina * self.por_pagina, total)
        return f"Exibindo {inicio}–{fim} de {total}"

    @rx.var
    def tem_filtro(self) -> bool:
        return (
            bool(self.busca.strip())
            or self.filtro_especie != TODAS_ESPECIES
            or self.filtro_porte != TODOS_PORTES
            or self.filtro_status != TODOS_STATUS
        )

    @rx.var
    def titulo_form(self) -> str:
        return "Editar animal" if self.editando_id else "Cadastrar animal"


# ---------------------------------------------------------------------------
# Componentes
# ---------------------------------------------------------------------------
def cartao_resumo(titulo: str, numero, descricao: str, icone: str, cor: str):
    return rx.hstack(
        rx.center(
            rx.icon(icone, size=22, color=cor),
            background=COR_DESTAQUE,
            border_radius="12px",
            width="46px",
            height="46px",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.text(titulo, color=COR_SECUNDARIA, size="2", weight="medium"),
            rx.heading(numero, size="7", color=COR_TEXTO),
            rx.text(descricao, color=COR_SECUNDARIA, size="1"),
            spacing="0",
            align="start",
        ),
        spacing="3",
        align="center",
        padding="18px",
        background="white",
        border=f"1px solid {COR_BORDA}",
        border_radius="16px",
        width="100%",
    )


def status_animal(status):
    return rx.badge(
        status,
        color_scheme=rx.match(
            status,
            ("Disponível", "green"),
            ("Em lar temporário", "orange"),
            ("Adotado", "blue"),
            ("Em processo de adoção", "purple"),
            "gray",
        ),
        variant="soft",
        radius="full",
        size="2",
    )


def avatar_especie(especie):
    return rx.center(
        rx.icon(
            rx.match(especie, ("Cão", "dog"), ("Gato", "cat"), "paw-print"),
            size=18,
            color=COR_PRINCIPAL,
        ),
        background=COR_DESTAQUE,
        border_radius="50%",
        width="38px",
        height="38px",
        flex_shrink="0",
    )


def celula(conteudo):
    return rx.table.cell(conteudo, vertical_align="middle")


def texto_celula(valor):
    return celula(rx.text(valor, color=COR_TEXTO, size="2"))


def linha_animal(animal: rx.Var[dict[str, str]]):
    return rx.table.row(
        celula(rx.text(animal["codigo"], color=COR_SECUNDARIA, size="2")),
        celula(
            rx.hstack(
                avatar_especie(animal["especie"]),
                rx.vstack(
                    rx.text(animal["nome"], color=COR_TEXTO, weight="bold"),
                    rx.text(
                        animal["especie"] + " · " + animal["sexo"],
                        color=COR_SECUNDARIA,
                        size="1",
                    ),
                    align="start",
                    spacing="0",
                ),
                spacing="3",
                align="center",
            )
        ),
        texto_celula(animal["raca"]),
        texto_celula(animal["porte"]),
        texto_celula(animal["idade"]),
        texto_celula(animal["resgate"]),
        texto_celula(animal["condicao_txt"]),
        celula(status_animal(animal["status"])),
        celula(
            rx.hstack(
                rx.tooltip(
                    rx.icon_button(
                        rx.icon("eye", size=16),
                        aria_label="Visualizar animal",
                        variant="soft",
                        color_scheme="brown",
                        size="2",
                        on_click=AnimalState.abrir_visualizacao(animal["id"]),
                    ),
                    content="Visualizar",
                ),
                rx.tooltip(
                    rx.icon_button(
                        rx.icon("pencil", size=16),
                        aria_label="Editar animal",
                        variant="soft",
                        color_scheme="gray",
                        size="2",
                        on_click=AnimalState.abrir_edicao(animal["id"]),
                    ),
                    content="Editar",
                ),
                rx.tooltip(
                    rx.icon_button(
                        rx.icon("trash-2", size=16),
                        aria_label="Excluir animal",
                        variant="soft",
                        color_scheme="red",
                        size="2",
                        on_click=AnimalState.pedir_exclusao(
                            animal["id"], animal["nome"]
                        ),
                    ),
                    content="Excluir",
                ),
                spacing="2",
            )
        ),
    )


def estado_vazio():
    return rx.center(
        rx.vstack(
            rx.center(
                rx.icon("search-x", size=28, color=COR_PRINCIPAL),
                background=COR_DESTAQUE,
                border_radius="50%",
                width="60px",
                height="60px",
            ),
            rx.heading("Nenhum animal encontrado", size="4", color=COR_TEXTO),
            rx.text(
                "Ajuste a busca ou os filtros, ou cadastre um novo animal.",
                color=COR_SECUNDARIA,
                size="2",
            ),
            rx.cond(
                AnimalState.tem_filtro,
                rx.button(
                    "Limpar filtros",
                    variant="outline",
                    color_scheme="brown",
                    on_click=AnimalState.limpar_filtros,
                ),
            ),
            align="center",
            spacing="3",
        ),
        padding="48px 16px",
        width="100%",
    )


def estado_carregando():
    return rx.center(
        rx.vstack(
            rx.spinner(size="3"),
            rx.text("Carregando animais...", color=COR_SECUNDARIA, size="2"),
            align="center",
            spacing="3",
        ),
        padding="48px 16px",
        width="100%",
    )


def aviso_erro_api():
    return rx.callout(
        rx.hstack(
            rx.text(AnimalState.erro_api),
            rx.spacer(),
            rx.button(
                "Tentar novamente",
                size="1",
                variant="soft",
                color_scheme="red",
                on_click=AnimalState.carregar(AnimalState.token),
            ),
            align="center",
            width="100%",
        ),
        icon="triangle-alert",
        color_scheme="red",
        width="100%",
    )


def tabela_animais():
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Código"),
                    rx.table.column_header_cell("Animal"),
                    rx.table.column_header_cell("Raça"),
                    rx.table.column_header_cell("Porte"),
                    rx.table.column_header_cell("Idade"),
                    rx.table.column_header_cell("Resgate"),
                    rx.table.column_header_cell("Saúde"),
                    rx.table.column_header_cell("Status"),
                    rx.table.column_header_cell("Ações"),
                )
            ),
            rx.table.body(rx.foreach(AnimalState.animais_pagina, linha_animal)),
            width="100%",
            variant="surface",
            size="3",
        ),
        overflow_x="auto",
        width="100%",
    )


def campo(rotulo: str, componente):
    return rx.vstack(
        rx.text(rotulo, size="2", weight="medium", color=COR_TEXTO),
        componente,
        spacing="1",
        align="stretch",
        width="100%",
    )


def dialogo_formulario():
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(AnimalState.titulo_form),
            rx.dialog.description(
                "Preencha os dados do animal resgatado. Todos os campos são obrigatórios.",
                size="2",
                color=COR_SECUNDARIA,
                margin_bottom="16px",
            ),
            rx.vstack(
                campo(
                    "Nome",
                    rx.input(
                        placeholder="Ex.: Caramelo",
                        value=AnimalState.form_nome,
                        on_change=AnimalState.set_form_nome,
                        size="3",
                    ),
                ),
                rx.grid(
                    campo(
                        "Espécie",
                        rx.select(
                            ESPECIES,
                            value=AnimalState.form_especie,
                            on_change=AnimalState.set_form_especie,
                            size="3",
                            width="100%",
                        ),
                    ),
                    campo(
                        "Sexo",
                        rx.select(
                            SEXOS,
                            value=AnimalState.form_sexo,
                            on_change=AnimalState.set_form_sexo,
                            size="3",
                            width="100%",
                        ),
                    ),
                    campo(
                        "Porte",
                        rx.select(
                            PORTES,
                            value=AnimalState.form_porte,
                            on_change=AnimalState.set_form_porte,
                            size="3",
                            width="100%",
                        ),
                    ),
                    columns="3",
                    spacing="3",
                    width="100%",
                ),


                  rx.cond(
                      AnimalState.form_especie == "Outro",
                       campo(
                            "Qual é a espécie?",
                            rx.input(
                              placeholder="Ex.: Coelho, Ave ou Tartaruga",
                              value=AnimalState.form_especie_outro,
                              on_change=AnimalState.set_form_especie_outro,
                              size="3",
                            ),
                        ),
                    ),


                rx.grid(
                    campo(
                        "Raça",
                        rx.input(
                            placeholder="Ex.: Poodle ou Sem raça definida",
                            value=AnimalState.form_raca,
                            on_change=AnimalState.set_form_raca,
                            size="3",
                        ),
                    ),
                    campo(
                        ROTULO_IDADE,
                        rx.input(
                            type="number",
                            min="0",
                            placeholder=EXEMPLO_IDADE,
                            value=AnimalState.form_idade,
                            on_change=AnimalState.set_form_idade,
                            size="3",
                        ),
                    ),
                    columns="2",
                    spacing="3",
                    width="100%",
                ),
                rx.grid(
                    campo(
                        "Data do resgate",
                        rx.input(
                            type="date",
                            value=AnimalState.form_data_resgate,
                            on_change=AnimalState.set_form_data_resgate,
                            size="3",
                        ),
                    ),
                    campo(
                        "Status",
                        rx.select(
                            STATUS,
                            value=AnimalState.form_status,
                            on_change=AnimalState.set_form_status,
                            size="3",
                            width="100%",
                        ),
                    ),
                    columns="2",
                    spacing="3",
                    width="100%",
                ),
                campo(
                    "Condição de saúde",
                    rx.input(
                        placeholder="Ex.: Saudável, vacinado, em tratamento",
                        value=AnimalState.form_condicao,
                        on_change=AnimalState.set_form_condicao,
                        size="3",
                    ),
                ),

                campo(
                    "Descrição do animal",
                   rx.text_area(
                      placeholder="Descreva a personalidade, o comportamento e as características do animal",
                      value=AnimalState.form_descricao,
                      on_change=AnimalState.set_form_descricao,
                    ),
                ),


                rx.cond(
                    AnimalState.erro_form != "",
                    rx.callout(
                        AnimalState.erro_form,
                        icon="triangle-alert",
                        color_scheme="red",
                        size="1",
                    ),
                ),
                spacing="4",
                width="100%",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="gray")
                ),
                rx.button(
                    "Salvar",
                    background=COR_PRINCIPAL,
                    color="white",
                    loading=AnimalState.salvando,
                    on_click=AnimalState.salvar_animal,
                ),
                spacing="3",
                justify="end",
                margin_top="20px",
            ),
            max_width="560px",
        ),
        open=AnimalState.dialogo_form_aberto,
        on_open_change=AnimalState.set_dialogo_form_aberto,
    )


def item_detalhe(rotulo: str, valor):
    return rx.vstack(
        rx.text(rotulo, size="1", color=COR_SECUNDARIA),
        rx.text(valor, size="3", color=COR_TEXTO, weight="medium"),
        spacing="0",
        align="start",
    )


def dialogo_visualizacao():
    return rx.dialog.root(
        rx.dialog.content(
            rx.hstack(
                avatar_especie(AnimalState.animal_visto["especie"]),
                rx.vstack(
                    rx.dialog.title(AnimalState.animal_visto["nome"], margin="0"),
                    rx.text(
                        AnimalState.animal_visto["codigo"],
                        size="2",
                        color=COR_SECUNDARIA,
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.spacer(),
                status_animal(AnimalState.animal_visto["status"]),
                align="center",
                width="100%",
                margin_bottom="16px",
            ),
            rx.grid(
                item_detalhe("Espécie", AnimalState.animal_visto["especie"]),
                item_detalhe("Sexo", AnimalState.animal_visto["sexo"]),
                item_detalhe("Raça", AnimalState.animal_visto["raca"]),
                item_detalhe("Porte", AnimalState.animal_visto["porte"]),
                item_detalhe("Idade estimada", AnimalState.animal_visto["idade"]),
                item_detalhe("Data do resgate", AnimalState.animal_visto["resgate"]),
                item_detalhe("Condição de saúde", AnimalState.animal_visto["condicao_txt"]),
                item_detalhe("Descrição", AnimalState.animal_visto["descricao"]),
                columns="2",
                spacing="4",
                width="100%",
            ),
            rx.flex(
                rx.dialog.close(rx.button("Fechar", variant="soft", color_scheme="gray")),
                justify="end",
                margin_top="20px",
            ),
            max_width="480px",
        ),
        open=AnimalState.dialogo_ver_aberto,
        on_open_change=AnimalState.set_dialogo_ver_aberto,
    )


def dialogo_exclusao():
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Excluir animal"),
            rx.alert_dialog.description(
                "Tem certeza que deseja excluir ",
                rx.text(AnimalState.nome_excluir, as_="span", weight="bold"),
                "? Essa ação não pode ser desfeita.",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button("Cancelar", variant="soft", color_scheme="gray")
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Excluir",
                        color_scheme="red",
                        loading=AnimalState.salvando,
                        on_click=AnimalState.confirmar_exclusao,
                    )
                ),
                spacing="3",
                justify="end",
                margin_top="16px",
            ),
            max_width="440px",
        ),
        open=AnimalState.dialogo_excluir_aberto,
        on_open_change=AnimalState.set_dialogo_excluir_aberto,
    )


# ---------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------
def gestao_animal(token) -> rx.Component:
    """Tela de gestão. 'token' é o token de login (LoginState.token)."""
    return rx.vstack(
        # Cabeçalho
        rx.hstack(
            rx.vstack(
                rx.heading("Gestão de Animais", size="8", color=COR_TEXTO),
                rx.text(
                    "Organize os cadastros e acompanhe cada animal resgatado.",
                    color=COR_SECUNDARIA,
                    size="3",
                ),
                align="start",
                spacing="2",
            ),
            rx.spacer(),
            rx.button(
                rx.icon("plus", size=18),
                "Cadastrar animal",
                background=COR_PRINCIPAL,
                color="white",
                size="3",
                border_radius="10px",
                cursor="pointer",
                on_click=AnimalState.abrir_cadastro,
            ),
            width="100%",
            align="center",
            wrap="wrap",
            spacing="3",
        ),
        rx.cond(AnimalState.erro_api != "", aviso_erro_api()),
        # Cartões de resumo
        rx.grid(
            cartao_resumo("Total", AnimalState.total, "Animais cadastrados", "paw-print", COR_PRINCIPAL),
            cartao_resumo("Cães", AnimalState.qtd_caes, "Cadastrados na ONG", "dog", "#C17B25"),
            cartao_resumo("Gatos", AnimalState.qtd_gatos, "Cadastrados na ONG", "cat", "#7752A0"),
            cartao_resumo("Resgates recentes", AnimalState.qtd_recentes, "Nos últimos 30 dias", "calendar-check", "#23845D"),
            columns=rx.breakpoints(initial="1", sm="2", lg="4"),
            spacing="3",
            width="100%",
        ),
        # Tabela
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("Animais cadastrados", size="5", color=COR_TEXTO),
                    rx.text("Consulte os registros da ONG.", size="2", color=COR_SECUNDARIA),
                    align="start",
                    spacing="1",
                ),
                rx.spacer(),
                rx.tooltip(
                    rx.icon_button(
                        rx.icon("refresh-cw", size=16),
                        aria_label="Atualizar lista",
                        variant="soft",
                        color_scheme="gray",
                        size="2",
                        loading=AnimalState.carregando,
                        on_click=AnimalState.carregar(AnimalState.token),
                    ),
                    content="Atualizar lista",
                ),
                rx.badge(
                    AnimalState.total_filtrado.to_string() + " registros",
                    background=COR_DESTAQUE,
                    color=COR_PRINCIPAL,
                    padding="8px 12px",
                ),
                width="100%",
                align="center",
                wrap="wrap",
                spacing="3",
            ),
            # Busca e filtros
            rx.hstack(
                rx.input(
                    rx.input.slot(rx.icon("search", size=16)),
                    placeholder="Buscar por nome ou código...",
                    value=AnimalState.busca,
                    on_change=AnimalState.set_busca,
                    size="3",
                    flex="1",
                    min_width="220px",
                ),
                rx.select(
                    [TODAS_ESPECIES] + ESPECIES,
                    value=AnimalState.filtro_especie,
                    on_change=AnimalState.set_filtro_especie,
                    size="3",
                ),
                rx.select(
                    [TODOS_PORTES] + PORTES,
                    value=AnimalState.filtro_porte,
                    on_change=AnimalState.set_filtro_porte,
                    size="3",
                ),
                rx.select(
                    AnimalState.opcoes_status,
                    value=AnimalState.filtro_status,
                    on_change=AnimalState.set_filtro_status,
                    size="3",
                ),
                rx.cond(
                    AnimalState.tem_filtro,
                    rx.button(
                        rx.icon("x", size=16),
                        "Limpar",
                        variant="ghost",
                        color_scheme="gray",
                        size="3",
                        on_click=AnimalState.limpar_filtros,
                    ),
                ),
                width="100%",
                spacing="3",
                align="center",
                wrap="wrap",
            ),
            rx.cond(
                AnimalState.carregando,
                estado_carregando(),
                rx.cond(
                    AnimalState.total_filtrado == 0,
                    estado_vazio(),
                    tabela_animais(),
                ),
            ),
            # Rodapé / paginação
            rx.hstack(
                rx.text(AnimalState.texto_exibicao, color=COR_SECUNDARIA, size="2"),
                rx.spacer(),
                rx.text(
                    "Página " + AnimalState.pagina.to_string() + " de " + AnimalState.total_paginas.to_string(),
                    color=COR_SECUNDARIA,
                    size="2",
                ),
                rx.button(
                    "Anterior",
                    variant="outline",
                    color_scheme="gray",
                    size="2",
                    disabled=AnimalState.pagina <= 1,
                    on_click=AnimalState.pagina_anterior,
                ),
                rx.button(
                    "Próxima",
                    variant="outline",
                    color_scheme="gray",
                    size="2",
                    disabled=AnimalState.pagina >= AnimalState.total_paginas,
                    on_click=AnimalState.pagina_seguinte,
                ),
                width="100%",
                align="center",
                wrap="wrap",
                spacing="3",
            ),
            padding="20px",
            background="white",
            border=f"1px solid {COR_BORDA}",
            border_radius="16px",
            spacing="4",
            width="100%",
        ),
        dialogo_formulario(),
        dialogo_visualizacao(),
        dialogo_exclusao(),
        width="100%",
        max_width="1400px",
        padding="28px",
        spacing="6",
        align="stretch",
        background=COR_FUNDO,
        min_height="100%",
        # Ao abrir a tela, busca os animais no Xano usando o token do login
        on_mount=AnimalState.carregar(token),
    )