import httpx
import reflex as rx


# Endpoints públicos do Xano - tabela DOADOR
URL_LISTAR_DOADORES = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/doador"
URL_CADASTRAR_DOADOR = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/doador"


class DoacoesState(rx.State):
    """Estado do módulo de Doações."""

    # ========================================================
    # NAVEGAÇÃO ENTRE ABAS
    # ========================================================

    aba_ativa: str = "doadores"

    def selecionar_aba(self, aba: str):
        self.aba_ativa = aba

    # ========================================================
    # FILTROS
    # ========================================================

    filtro_doador: str = ""

    def set_filtro_doador(self, valor: str):
        self.filtro_doador = valor

    # ========================================================
    # DADOS DOS DOADORES (CARREGADOS DO XANO)
    # ========================================================

    doadores: list[dict[str, str]] = []
    carregando_doadores: bool = False

    # ========================================================
    # DADOS DE DEMONSTRAÇÃO: DOAÇÕES
    # ========================================================

    doacoes: list[dict[str, str]] = [
        {
            "id": "1",
            "doador_id": "1",
            "tipo_doacao": "Financeira",
            "valor": "250.00",
            "data_doacao": "06/11/2026",
            "descricao": "",
        },
        {
            "id": "2",
            "doador_id": "3",
            "tipo_doacao": "Material",
            "valor": "",
            "data_doacao": "05/11/2026",
            "descricao": "Ração para cães adultos",
        },
        {
            "id": "3",
            "doador_id": "2",
            "tipo_doacao": "Financeira",
            "valor": "500.00",
            "data_doacao": "01/11/2026",
            "descricao": "",
        },
        {
            "id": "4",
            "doador_id": "1",
            "tipo_doacao": "Material",
            "valor": "",
            "data_doacao": "28/10/2026",
            "descricao": "Cobertores",
        },
    ]

    # ========================================================
    # FORMULÁRIO DE DOADOR
    # ========================================================

    nome_doador: str = ""
    cpf_doador: str = ""
    telefone_doador: str = ""
    email_doador: str = ""

    # ========================================================
    # FORMULÁRIO DE DOAÇÃO
    # ========================================================

    doador_selecionado_id: str = ""
    tipo_doacao: str = "Financeira"
    valor_doacao: str = ""
    descricao_doacao: str = ""
    data_doacao: str = "08/11/2026"

    mensagem: str = ""

    # ========================================================
    # SETTERS
    # ========================================================

    def set_nome_doador(self, valor: str):
        self.nome_doador = valor

    def set_cpf_doador(self, valor: str):
        self.cpf_doador = valor

    def set_telefone_doador(self, valor: str):
        self.telefone_doador = valor

    def set_email_doador(self, valor: str):
        self.email_doador = valor

    def set_doador_selecionado(self, valor: str):
        self.doador_selecionado_id = valor

    def set_tipo_doacao(self, valor: str):
        self.tipo_doacao = valor

    def set_valor_doacao(self, valor: str):
        self.valor_doacao = valor

    def set_descricao_doacao(self, valor: str):
        self.descricao_doacao = valor

    def set_data_doacao(self, valor: str):
        self.data_doacao = valor

    # ========================================================
    # CONSULTA E CADASTRO DE DOADORES NO XANO
    # ========================================================

    async def carregar_doadores(self):
        self.carregando_doadores = True
        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta = await cliente.get(URL_LISTAR_DOADORES)
                resposta.raise_for_status()
                dados = resposta.json()

            if isinstance(dados, dict):
                dados = dados.get("items", dados.get("doadores", []))

            self.doadores = [
                {
                    "id": str(item.get("id", "")),
                    "nome": str(item.get("nome") or ""),
                    "cpf": str(item.get("cpf") or ""),
                    "telefone": str(item.get("telefone") or ""),
                    "email": str(item.get("email") or ""),
                }
                for item in dados
            ]
            self.mensagem = ""

        except httpx.HTTPStatusError as erro:
            self.mensagem = (
                f"Não foi possível carregar os doadores. "
                f"Erro HTTP {erro.response.status_code}."
            )
        except (httpx.RequestError, ValueError, TypeError) as erro:
            self.mensagem = f"Erro ao carregar os doadores: {erro}"
        finally:
            self.carregando_doadores = False

    async def cadastrar_doador(self):
        if not self.nome_doador.strip():
            self.mensagem = "Informe o nome do doador."
            return

        cpf = self.cpf_doador.strip()
        cpf_normalizado = "".join(caractere for caractere in cpf if caractere.isdigit())

        if cpf_normalizado and any(
            "".join(caractere for caractere in doador["cpf"] if caractere.isdigit())
            == cpf_normalizado
            for doador in self.doadores
        ):
            self.mensagem = "Já existe um doador cadastrado com esse CPF."
            return

        dados = {
            "nome": self.nome_doador.strip(),
            "cpf": cpf,
            "telefone": self.telefone_doador.strip(),
            "email": self.email_doador.strip(),
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta = await cliente.post(URL_CADASTRAR_DOADOR, json=dados)
                resposta.raise_for_status()

            self.nome_doador = ""
            self.cpf_doador = ""
            self.telefone_doador = ""
            self.email_doador = ""
            await self.carregar_doadores()
            self.mensagem = "Doador cadastrado com sucesso."

        except httpx.HTTPStatusError as erro:
            self.mensagem = (
                f"Não foi possível cadastrar o doador. "
                f"Erro HTTP {erro.response.status_code}: {erro.response.text}"
            )
        except httpx.RequestError as erro:
            self.mensagem = f"Erro de conexão ao cadastrar doador: {erro}"

    # ========================================================
    # REGISTRO DE DOAÇÕES
    # ========================================================

    def registrar_doacao_financeira(self):
        self.tipo_doacao = "Financeira"
        self.registrar_doacao()

    def registrar_doacao_material(self):
        self.tipo_doacao = "Material"
        self.registrar_doacao()

    def registrar_doacao(self):
        if not self.doador_selecionado_id:
            self.mensagem = "Selecione um doador."
            return

        if self.tipo_doacao == "Financeira":
            try:
                valor = float(self.valor_doacao.replace(",", "."))
                if valor <= 0:
                    raise ValueError
            except ValueError:
                self.mensagem = "Informe um valor financeiro válido."
                return

            valor_registrado = f"{valor:.2f}"
            descricao = ""

        else:
            if not self.descricao_doacao.strip():
                self.mensagem = "Informe a descrição do material recebido."
                return

            valor_registrado = ""
            descricao = self.descricao_doacao.strip()

        novo_id = str(max(
            [int(d["id"]) for d in self.doacoes],
            default=0
        ) + 1)

        self.doacoes.append({
            "id": novo_id,
            "doador_id": self.doador_selecionado_id,
            "tipo_doacao": self.tipo_doacao,
            "valor": valor_registrado,
            "data_doacao": self.data_doacao,
            "descricao": descricao,
        })

        self.doador_selecionado_id = ""
        self.valor_doacao = ""
        self.descricao_doacao = ""
        self.mensagem = "Doação registrada com sucesso."

    # ========================================================
    # FUNÇÕES AUXILIARES
    # ========================================================

    def nome_doador_por_id(self, doador_id: str) -> str:
        for doador in self.doadores:
            if doador["id"] == doador_id:
                return doador["nome"]

        return "Doador não encontrado"

    # ========================================================
    # DADOS FILTRADOS E CALCULADOS
    # ========================================================

    @rx.var
    def doadores_filtrados(self) -> list[dict[str, str]]:
        termo = self.filtro_doador.lower().strip()

        if not termo:
            return self.doadores

        return [
            doador for doador in self.doadores
            if termo in doador["nome"].lower()
            or termo in doador["cpf"].lower()
        ]

    @rx.var
    def doacoes_com_doador(self) -> list[dict[str, str]]:
        resultado = []

        for doacao in self.doacoes:
            registro = dict(doacao)
            registro["nome_doador"] = self.nome_doador_por_id(
                doacao["doador_id"]
            )
            resultado.append(registro)

        return resultado

    @rx.var
    def quantidade_doadores(self) -> int:
        return len(self.doadores)

    @rx.var
    def quantidade_doacoes(self) -> int:
        return len(self.doacoes)

    @rx.var
    def total_doacoes_financeiras(self) -> float:
        return sum(
            float(d["valor"])
            for d in self.doacoes
            if d["tipo_doacao"] == "Financeira" and d["valor"]
        )
