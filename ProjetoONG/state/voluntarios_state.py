import httpx
import reflex as rx


# ========================================================
# URLS DOS ENDPOINTS DO XANO
# ========================================================

URL_VOLUNTARIO = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/voluntario"
URL_ATIVIDADE = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/atividade"
URL_VOLUNTARIO_ATIVIDADE = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/voluntario_atividade"


class VoluntariosState(rx.State):
    """Estado do módulo de Voluntários."""

    # ========================================================
    # ABAS
    # ========================================================

    aba_ativa: str = "voluntarios"

    def selecionar_aba(self, aba: str):
        self.aba_ativa = aba

    # ========================================================
    # FILTROS
    # ========================================================

    filtro_voluntario: str = ""
    filtro_atividade: str = ""
    filtro_historico: str = ""

    def set_filtro_voluntario(self, valor: str):
        self.filtro_voluntario = valor

    def set_filtro_atividade(self, valor: str):
        self.filtro_atividade = valor

    def set_filtro_historico(self, valor: str):
        self.filtro_historico = valor

    # ========================================================
    # DADOS CARREGADOS DO XANO
    # ========================================================

    voluntarios: list[dict[str, str]] = []
    atividades: list[dict[str, str]] = []
    participacoes: list[dict[str, str]] = []

    carregando: bool = False
    erro: str = ""

    # ========================================================
    # CARREGAMENTO DOS DADOS DO XANO
    # ========================================================

    @rx.event
    async def carregar_dados(self):
        """Carrega voluntários, atividades e participações do Xano."""
        self.carregando = True
        self.erro = ""

        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta_vol = await cliente.get(URL_VOLUNTARIO)
                resposta_atv = await cliente.get(URL_ATIVIDADE)
                resposta_part = await cliente.get(URL_VOLUNTARIO_ATIVIDADE)

            respostas = (
                ("voluntários", resposta_vol),
                ("atividades", resposta_atv),
                ("participações", resposta_part),
            )

            for nome, resposta in respostas:
                if resposta.status_code != 200:
                    self.erro = (
                        f"Erro ao carregar {nome} do Xano "
                        f"({resposta.status_code})."
                    )
                    return

            dados_vol = resposta_vol.json()
            dados_atv = resposta_atv.json()
            dados_part = resposta_part.json()

            if not all(isinstance(dados, list) for dados in (
                dados_vol, dados_atv, dados_part
            )):
                self.erro = "O Xano retornou um formato de dados inesperado."
                return

            self.voluntarios = [
                {
                    "id": str(item.get("id", "")),
                    "nome": str(item.get("nome") or ""),
                    "telefone": str(item.get("telefone") or ""),
                    "email": str(item.get("email") or ""),
                    "status": str(item.get("status") or ""),
                }
                for item in dados_vol
                if isinstance(item, dict)
            ]

            self.atividades = [
                {
                    "id": str(item.get("id", "")),
                    "tipo_atividade": str(item.get("tipo_atividade") or ""),
                    "data_atividade": str(item.get("data_atividade") or ""),
                    "descricao": str(item.get("descricao") or ""),
                }
                for item in dados_atv
                if isinstance(item, dict)
            ]

            self.participacoes = [
                {
                    "id": str(item.get("id", "")),
                    "voluntario_id": str(item.get("voluntario_id", "")),
                    "atividade_id": str(item.get("atividade_id", "")),
                    "funcao_na_atividade": str(
                        item.get("funcao_na_atividade") or ""
                    ),
                }
                for item in dados_part
                if isinstance(item, dict)
            ]

        except httpx.RequestError as e:
            self.erro = f"Falha de conexão com o Xano: {str(e)}"
        except (ValueError, TypeError) as e:
            self.erro = f"Não foi possível interpretar os dados do Xano: {str(e)}"
        finally:
            self.carregando = False

    # ========================================================
    # CAMPOS DO FORMULÁRIO DE VOLUNTÁRIOS
    # ========================================================

    nome_voluntario: str = ""
    telefone_voluntario: str = ""
    email_voluntario: str = ""
    status_voluntario: str = "Ativo"

    def set_nome_voluntario(self, valor: str):
        self.nome_voluntario = valor

    def set_telefone_voluntario(self, valor: str):
        self.telefone_voluntario = valor

    def set_email_voluntario(self, valor: str):
        self.email_voluntario = valor

    def set_status_voluntario(self, valor: str):
        self.status_voluntario = valor

    # ========================================================
    # CAMPOS DO FORMULÁRIO DE ATIVIDADES
    # ========================================================

    tipo_atividade: str = ""
    data_atividade: str = ""
    descricao_atividade: str = ""

    def set_tipo_atividade(self, valor: str):
        self.tipo_atividade = valor

    def set_data_atividade(self, valor: str):
        self.data_atividade = valor

    def set_descricao_atividade(self, valor: str):
        self.descricao_atividade = valor

    # ========================================================
    # CAMPOS DO FORMULÁRIO DE PARTICIPAÇÕES
    # ========================================================

    voluntario_selecionado_id: str = ""
    atividade_selecionada_id: str = ""
    funcao_na_atividade: str = ""

    def set_voluntario_selecionado_id(self, valor: str):
        self.voluntario_selecionado_id = valor

    def set_atividade_selecionada_id(self, valor: str):
        self.atividade_selecionada_id = valor

    def set_funcao_na_atividade(self, valor: str):
        self.funcao_na_atividade = valor

    # ========================================================
    # MENSAGENS
    # ========================================================

    mensagem: str = ""

    # ========================================================
    # CADASTRO DE VOLUNTÁRIOS
    # ========================================================

    @rx.event
    async def cadastrar_voluntario(self):
        if not self.nome_voluntario.strip():
            self.mensagem = "Informe o nome do voluntário."
            return

        payload = {
            "nome": self.nome_voluntario.strip(),
            "telefone": self.telefone_voluntario.strip(),
            "email": self.email_voluntario.strip(),
            "status": self.status_voluntario,
        }

        self.erro = ""
        self.mensagem = ""

        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta = await cliente.post(URL_VOLUNTARIO, json=payload)

            if resposta.status_code in (200, 201):
                await self.carregar_dados()
                if not self.erro:
                    self.nome_voluntario = ""
                    self.telefone_voluntario = ""
                    self.email_voluntario = ""
                    self.status_voluntario = "Ativo"
                    self.mensagem = "Voluntário cadastrado com sucesso."
            else:
                self.erro = (
                    "Não foi possível cadastrar o voluntário "
                    f"({resposta.status_code})."
                )

        except httpx.RequestError as e:
            self.erro = f"Falha de conexão com o Xano: {str(e)}"

    # ========================================================
    # CADASTRO DE ATIVIDADES
    # ========================================================

    @rx.event
    async def cadastrar_atividade(self):
        print("TESTE: botão Cadastrar atividade foi acionado")
        if not self.tipo_atividade.strip():
            self.mensagem = "Informe o tipo da atividade."
            return

        if not self.data_atividade.strip():
            self.mensagem = "Informe a data da atividade."
            return

        payload = {
            "tipo_atividade": self.tipo_atividade.strip(),
            "data_atividade": self.data_atividade.strip(),
            "descricao": self.descricao_atividade.strip(),
        }

        self.erro = ""
        self.mensagem = ""

        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta = await cliente.post(URL_ATIVIDADE, json=payload)

            if resposta.status_code in (200, 201):
                await self.carregar_dados()
                if not self.erro:
                    self.tipo_atividade = ""
                    self.data_atividade = ""
                    self.descricao_atividade = ""
                    self.mensagem = "Atividade cadastrada com sucesso."
            else:
                self.erro = (
                    "Não foi possível cadastrar a atividade "
                    f"({resposta.status_code})."
                )

        except httpx.RequestError as e:
            self.erro = f"Falha de conexão com o Xano: {str(e)}"

    # ========================================================
    # ASSOCIAÇÃO ENTRE VOLUNTÁRIOS E ATIVIDADES
    # ========================================================

    @rx.event
    async def associar_voluntario_atividade(self):
        if not self.voluntario_selecionado_id:
            self.mensagem = "Selecione um voluntário."
            return

        if not self.atividade_selecionada_id:
            self.mensagem = "Selecione uma atividade."
            return

        for participacao in self.participacoes:
            if (
                participacao["voluntario_id"]
                == self.voluntario_selecionado_id
                and participacao["atividade_id"]
                == self.atividade_selecionada_id
            ):
                self.mensagem = "Essa participação já está registrada."
                return

        try:
            payload = {
                "voluntario_id": int(self.voluntario_selecionado_id),
                "atividade_id": int(self.atividade_selecionada_id),
                "funcao_na_atividade": self.funcao_na_atividade.strip(),
            }
        except ValueError:
            self.erro = "Selecione um voluntário e uma atividade válidos."
            return

        self.erro = ""
        self.mensagem = ""

        try:
            async with httpx.AsyncClient(timeout=20.0) as cliente:
                resposta = await cliente.post(
                    URL_VOLUNTARIO_ATIVIDADE,
                    json=payload,
                )

            if resposta.status_code in (200, 201):
                await self.carregar_dados()
                if not self.erro:
                    self.voluntario_selecionado_id = ""
                    self.atividade_selecionada_id = ""
                    self.funcao_na_atividade = ""
                    self.mensagem = "Participação registrada com sucesso."
            else:
                self.erro = (
                    "Não foi possível registrar a participação "
                    f"({resposta.status_code})."
                )

        except httpx.RequestError as e:
            self.erro = f"Falha de conexão com o Xano: {str(e)}"

    # ========================================================
    # FUNÇÕES AUXILIARES
    # ========================================================

    def nome_voluntario_por_id(self, voluntario_id: str) -> str:
        for voluntario in self.voluntarios:
            if voluntario["id"] == voluntario_id:
                return voluntario["nome"]

        return "Voluntário não encontrado"

    def tipo_atividade_por_id(self, atividade_id: str) -> str:
        for atividade in self.atividades:
            if atividade["id"] == atividade_id:
                return atividade["tipo_atividade"]

        return "Atividade não encontrada"

    def data_atividade_por_id(self, atividade_id: str) -> str:
        for atividade in self.atividades:
            if atividade["id"] == atividade_id:
                return atividade["data_atividade"]

        return ""

    # ========================================================
    # DADOS FILTRADOS E CALCULADOS
    # ========================================================

    @rx.var
    def voluntarios_filtrados(self) -> list[dict[str, str]]:
        termo = self.filtro_voluntario.lower().strip()

        if not termo:
            return self.voluntarios

        return [
            voluntario
            for voluntario in self.voluntarios
            if termo in voluntario["nome"].lower()
            or termo in voluntario["telefone"].lower()
            or termo in voluntario["email"].lower()
        ]

    @rx.var
    def atividades_filtradas(self) -> list[dict[str, str]]:
        termo = self.filtro_atividade.lower().strip()

        if not termo:
            return self.atividades

        return [
            atividade
            for atividade in self.atividades
            if termo in atividade["tipo_atividade"].lower()
            or termo in atividade["descricao"].lower()
        ]

    @rx.var
    def participacoes_detalhadas(self) -> list[dict[str, str]]:
        resultado = []

        for participacao in self.participacoes:
            registro = dict(participacao)
            atividade_id = participacao["atividade_id"]

            registro["nome_voluntario"] = (
                self.nome_voluntario_por_id(
                    participacao["voluntario_id"]
                )
            )
            registro["tipo_atividade"] = (
                self.tipo_atividade_por_id(atividade_id)
            )
            registro["data_atividade"] = (
                self.data_atividade_por_id(atividade_id)
            )

            resultado.append(registro)

        return resultado

    @rx.var
    def historico_filtrado(self) -> list[dict[str, str]]:
        termo = self.filtro_historico.lower().strip()

        if not termo:
            return self.participacoes_detalhadas

        return [
            participacao
            for participacao in self.participacoes_detalhadas
            if termo in participacao["nome_voluntario"].lower()
            or termo in participacao["tipo_atividade"].lower()
            or termo in participacao["data_atividade"].lower()
        ]

    @rx.var
    def quantidade_voluntarios(self) -> int:
        return len(self.voluntarios)

    @rx.var
    def quantidade_atividades(self) -> int:
        return len(self.atividades)

    @rx.var
    def quantidade_participacoes(self) -> int:
        return len(self.participacoes)
