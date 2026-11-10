import httpx
import reflex as rx

# URLs DIRETAS DOS ENDPOINTS PÚBLICOS NO XANO
URL_GET_PROCESSOS = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/processo_adocao"
URL_GET_POS_ADOCAO = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/pos_adocao"
URL_POST_POS_ADOCAO = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/pos_adocao"

class PosAdocaoState(rx.State):
    """Estado do Módulo de Pós-Adoção."""

    # Controlo do formulário
    formulario_aberto: bool = False

    # Filtros e Formulários
    filtro_texto: str = ""
    data_acompanhamento: str = ""
    relatorio_observacao: str = ""

    # Dados
    processos: list[dict[str, str]] = []
    acompanhamentos: list[dict[str, str]] = []
    processo_selecionado: dict[str, str] = {}

    # Estados de Carregamento e Notificações
    carregando_processos: bool = False
    carregando_acompanhamentos: bool = False
    salvando_acompanhamento: bool = False

    erro: str = ""
    mensagem: str = ""

    @rx.event
    def abrir_formulario(self):
        self.formulario_aberto = True
        self.erro = ""
        self.mensagem = ""

    @rx.event
    def fechar_formulario(self):
        self.formulario_aberto = False
        self.data_acompanhamento = ""
        self.relatorio_observacao = ""
        self.erro = ""
        self.mensagem = ""

    @rx.event
    def set_filtro_texto(self, valor: str):
        self.filtro_texto = valor

    @rx.event
    def set_data_acompanhamento(self, valor: str):
        self.data_acompanhamento = valor

    @rx.event
    def set_relatorio_observacao(self, valor: str):
        self.relatorio_observacao = valor

    # --- CARREGAMENTO DOS PROCESSOS DE ADOÇÃO CONCLUÍDOS ---
    @rx.event
    async def carregar_processos(self):
        """Carrega os processos de adoção do Xano (Endpoint Público)."""
        self.carregando_processos = True
        self.erro = ""

        async with httpx.AsyncClient(timeout=20.0) as cliente:
            try:
                resposta = await cliente.get(URL_GET_PROCESSOS)

                if resposta.status_code == 200:
                    dados = resposta.json()
                    normalizados = []

                    for item in dados:
                        if not isinstance(item, dict):
                            continue

                        status = str(item.get("status_processo") or item.get("status") or "").strip()
                        animal = item.get("_animal_1") or item.get("_animal") or {}
                        tutor = item.get("_tutor_adotante") or {}

                        # Ignora registros sem animal/tutor vinculados
                        if not animal.get("nome") and not tutor.get("nome"):
                            continue

                        normalizados.append({
                            "id": str(item.get("id", "")),
                            "processo_id": str(item.get("id", "")),
                            "nome_animal": str(animal.get("nome") or "Pet sem nome"),
                            "especie": f"{animal.get('especie', '')}, {animal.get('raca', '')}".strip(", "),
                            "nome_tutor": str(tutor.get("nome") or "Tutor Desconhecido"),
                            "telefone": str(tutor.get("telefone") or "Não informado"),
                            "endereco": str(tutor.get("endereco") or "Não informado"),
                            "status": status or "Concluído",
                        })

                    self.processos = normalizados

                    if self.processos and not self.processo_selecionado.get("id"):
                        await self.selecionar_processo(self.processos[0]["id"])
                else:
                    self.erro = f"Erro Xano ao carregar processos ({resposta.status_code})"

            except Exception as e:
                self.erro = f"Falha de conexão: {str(e)}"
            finally:
                self.carregando_processos = False

    # --- SELEÇÃO DE UM ANIMAL E CARREGAMENTO DO HISTÓRICO DE PÓS-ADOÇÃO ---
    @rx.event
    async def selecionar_processo(self, processo_id: str):
        self.erro = ""
        self.mensagem = ""

        for p in self.processos:
            if p["id"] == processo_id:
                self.processo_selecionado = dict(p)
                break

        await self.carregar_acompanhamentos()

    @rx.event
    async def carregar_acompanhamentos(self):
        proc_id = self.processo_selecionado.get("id", "")
        if not proc_id:
            return

        self.carregando_acompanhamentos = True
        self.erro = ""

        async with httpx.AsyncClient(timeout=20.0) as cliente:
            try:
                resposta = await cliente.get(URL_GET_POS_ADOCAO)

                if resposta.status_code == 200:
                    dados = resposta.json()
                    lista = []

                    for item in dados:
                        if not isinstance(item, dict):
                            continue

                        p_id = str(item.get("processo_adocao_id", ""))
                        if p_id == proc_id:
                            lista.append({
                                "id": str(item.get("id", "")),
                                "processo_adocao_id": p_id,
                                "data_acompanhamento": str(item.get("data_acompanhamento") or "Sem data"),
                                "relatorio_observacao": str(item.get("relatorio_observacao") or "Sem relatório registrado."),
                            })

                    lista.sort(key=lambda x: x["data_acompanhamento"], reverse=True)
                    self.acompanhamentos = lista
                else:
                    self.erro = f"Erro ao buscar histórico ({resposta.status_code})"

            except Exception as e:
                self.erro = f"Falha de conexão: {str(e)}"
            finally:
                self.carregando_acompanhamentos = False

    # --- SALVAR NOVO REGISTO DE ACOMPANHAMENTO ---
    @rx.event
    async def salvar_acompanhamento(self):
        proc_id = self.processo_selecionado.get("id", "")
        if not proc_id:
            self.erro = "Selecione um processo de adoção."
            return

        if not self.data_acompanhamento:
            self.erro = "Informe a data do acompanhamento."
            return

        if not self.relatorio_observacao.strip():
            self.erro = "Informe o relatório de observação."
            return

        self.salvando_acompanhamento = True
        self.erro = ""
        self.mensagem = ""

        async with httpx.AsyncClient(timeout=20.0) as cliente:
            try:
                resposta = await cliente.post(
                    URL_POST_POS_ADOCAO,
                    json={
                        "data_acompanhamento": self.data_acompanhamento,
                        "relatorio_observacao": self.relatorio_observacao.strip(),
                        "processo_adocao_id": int(proc_id),
                    },
                )

                if resposta.status_code in (200, 201):
                    self.data_acompanhamento = ""
                    self.relatorio_observacao = ""
                    self.mensagem = "Acompanhamento registrado com sucesso."
                    self.formulario_aberto = False
                    await self.carregar_acompanhamentos()
                else:
                    self.erro = f"Não foi possível registrar o acompanhamento ({resposta.status_code})."

            except Exception as e:
                self.erro = f"Falha de conexão: {str(e)}"
            finally:
                self.salvando_acompanhamento = False

    # --- VARS CALCULADAS ---
    @rx.var
    def processos_filtrados(self) -> list[dict[str, str]]:
        if not self.filtro_texto:
            return self.processos
        termo = self.filtro_texto.lower()
        return [
            p for p in self.processos
            if termo in p["nome_animal"].lower() or termo in p["nome_tutor"].lower()
        ]

    @rx.var
    def total_adocoes(self) -> int:
        return len(self.processos)

    @rx.var
    def total_acompanhamentos(self) -> int:
        return len(self.acompanhamentos)