from datetime import datetime, timedelta
import os
import reflex as rx
import httpx

# ============================================================
# ENDPOINTS DO XANO - ATENDIMENTO VETERINÁRIO
# ============================================================
BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N"

XANO_ATENDIMENTO_VET_URL = f"{BASE_URL}/atendimento_veterinario"
XANO_ANIMAL_URL = f"{BASE_URL}/animal"


class AtendimentoVeterinarioState(rx.State):
    """Estado do módulo de Atendimento Veterinário integrado ao Xano."""

    # ========================================================
    # ESTADO E DADOS DA API XANO
    # ========================================================
    data_selecionada: str = datetime.now().strftime("%d/%m/%Y")
    
    animais: list[dict[str, str]] = []
    agendamentos: list[dict[str, str]] = []
    carregando: bool = False

    # Mensagens de feedback
    mensagem_erro: str = ""
    mensagem_sucesso: str = ""

    # ========================================================
    # CARREGAMENTO DOS DADOS (GET)
    # ========================================================
    def carregar_dados(self):
        """Carrega animais e atendimentos cadastrados diretamente do Xano."""
        self.carregando = True
        try:
            with httpx.Client(timeout=8.0) as client:
                # 1. Carregar Animais
                res_animais = client.get(XANO_ANIMAL_URL)
                if res_animais.status_code == 200:
                    dados_animais = res_animais.json()
                    self.animais = [
                        {
                            "id": str(a.get("id", "")),
                            "nome": str(a.get("nome", "")),
                            "especie": str(a.get("especie", "")),
                            "alergias": str(a.get("alergias", "Nenhuma alergia informada")),
                            "restricoes_clinicas": str(a.get("restricoes_clinicas", "Nenhuma restrição informada")),
                        }
                        for a in dados_animais
                    ]

                # 2. Carregar Atendimentos Veterinários
                res_atend = client.get(XANO_ATENDIMENTO_VET_URL)
                if res_atend.status_code == 200:
                    dados_atend = res_atend.json()
                    novos_agendamentos = []
                    for item in dados_atend:
                        # Trata a data para exibir no formato DD/MM/AAAA
                        raw_date = str(item.get("data_atendimento", ""))
                        if "-" in raw_date:
                            partes = raw_date.split("-")
                            data_fmt = f"{partes[2]}/{partes[1]}/{partes[0]}" if len(partes) == 3 else raw_date
                        else:
                            data_fmt = raw_date

                        nome_anim = self._obter_nome_animal(str(item.get("animal_id", "")))

                        novos_agendamentos.append({
                            "id": str(item.get("id", "")),
                            "animal": nome_anim,
                            "animal_id": str(item.get("animal_id", "")),
                            "data": data_fmt,
                            "horario": str(item.get("horario_atendimento", "")),
                            "procedimento": str(item.get("procedimentos", "") or "Consulta / Exame"),
                            "veterinario": str(item.get("veterinario_responsavel", "")),
                            "status": str(item.get("status_atendimento", "Agendado")),
                            "diagnostico": str(item.get("diagnostico", "") or ""),
                            "procedimentos_realizados": str(item.get("procedimentos", "") or ""),
                            "tratamento": str(item.get("tratamento", "") or ""),
                            "peso": str(item.get("peso", "")),
                            "custo": str(item.get("custo", "")),
                        })
                    self.agendamentos = novos_agendamentos
        except Exception as e:
            self.mensagem_erro = f"Erro ao comunicar com a API Xano: {str(e)}"
        finally:
            self.carregando = False

    def _obter_nome_animal(self, animal_id: str) -> str:
        for animal in self.animais:
            if animal["id"] == animal_id:
                return animal["nome"]
        return "Animal não cadastrado"

    # ========================================================
    # DADOS DERIVADOS DA AGENDA
    # ========================================================
    @rx.var
    def agendamentos_do_dia(self) -> list[dict[str, str]]:
        return sorted(
            [
                item
                for item in self.agendamentos
                if item["data"] == self.data_selecionada
            ],
            key=lambda item: item["horario"],
        )

    @rx.var
    def nomes_animais(self) -> list[str]:
        return [animal["nome"] for animal in self.animais]

    @rx.var
    def tem_agendamentos(self) -> bool:
        return len(self.agendamentos_do_dia) > 0

    # ========================================================
    # NOVAS MÉTRICAS E HISTÓRICO PARA A INTERFACE
    # ========================================================
    @rx.var
    def total_do_mes(self) -> int:
        """Total de atendimentos cadastrados."""
        return len(self.agendamentos)

    @rx.var
    def total_agendados(self) -> int:
        """Total de atendimentos pendentes/agendados."""
        return len([a for a in self.agendamentos if a["status"] == "Agendado"])

    @rx.var
    def custo_total_mes(self) -> str:
        """Soma o valor total de custos veterinários."""
        total = 0.0
        for item in self.agendamentos:
            val = item.get("custo", "").replace(",", ".").strip()
            if val:
                try:
                    total += float(val)
                except ValueError:
                    pass
        return f"{total:.2f}".replace(".", ",")

    @rx.var
    def atendimentos_passados(self) -> list[dict[str, str]]:
        """Retorna os últimos atendimentos marcados como Realizados ou Cancelados."""
        passados = [
            item for item in self.agendamentos 
            if item["status"] in ["Realizado", "Cancelado"]
        ]
        return passados[-5:]
    
    # ========================================================
    # SELEÇÃO DE ANIMAL
    # ========================================================
    animal_selecionado: dict[str, str] = {
        "id": "",
        "nome": "",
        "especie": "",
        "alergias": "Nenhuma alergia informada",
        "restricoes_clinicas": "Nenhuma restrição informada",
    }

    def atualizar_animal(self, valor: str):
        for animal in self.animais:
            if animal["nome"] == valor:
                self.animal_selecionado = animal
                self.animal_id_form = animal["id"]
                break

    # ========================================================
    # NAVEGAÇÃO DA AGENDA
    # ========================================================
    def dia_anterior(self):
        try:
            data = datetime.strptime(self.data_selecionada, "%d/%m/%Y")
            self.data_selecionada = (data - timedelta(days=1)).strftime("%d/%m/%Y")
            self.mensagem_erro = ""
            self.mensagem_sucesso = ""
        except ValueError:
            pass

    def proximo_dia(self):
        try:
            data = datetime.strptime(self.data_selecionada, "%d/%m/%Y")
            self.data_selecionada = (data + timedelta(days=1)).strftime("%d/%m/%Y")
            self.mensagem_erro = ""
            self.mensagem_sucesso = ""
        except ValueError:
            pass

    # ========================================================
    # FORMULÁRIO DE AGENDAMENTO (POST XANO)
    # ========================================================
    formulario_aberto: bool = False

    animal_id_form: str = ""
    data_atendimento_form: str = ""
    horario_form: str = "09:00"
    procedimento_form: str = ""
    veterinario_responsavel_form: str = ""

    def abrir_formulario(self):
        if self.animais:
            self.animal_id_form = self.animais[0]["id"]
            self.animal_selecionado = self.animais[0]
        else:
            self.animal_id_form = ""
            self.animal_selecionado = {"id": "", "nome": "", "especie": "", "alergias": "", "restricoes_clinicas": ""}

        self.data_atendimento_form = self.data_selecionada
        self.horario_form = "09:00"
        self.procedimento_form = ""
        self.veterinario_responsavel_form = ""
        self.mensagem_erro = ""
        self.mensagem_sucesso = ""
        self.formulario_aberto = True

    def fechar_formulario(self):
        self.formulario_aberto = False
        self.mensagem_erro = ""

    def atualizar_data(self, valor: str):
        self.data_atendimento_form = valor

    def atualizar_horario(self, valor: str):
        self.horario_form = valor

    def atualizar_procedimento(self, valor: str):
        self.procedimento_form = valor

    def atualizar_veterinario(self, valor: str):
        self.veterinario_responsavel_form = valor

    def salvar_agendamento(self):
        if not all([
            self.animal_id_form,
            self.data_atendimento_form,
            self.horario_form,
            self.procedimento_form.strip(),
            self.veterinario_responsavel_form.strip(),
        ]):
            self.mensagem_erro = "Preencha todos os campos obrigatórios."
            return

        try:
            dt_obj = datetime.strptime(self.data_atendimento_form, "%d/%m/%Y")
            data_xano = dt_obj.strftime("%Y-%m-%d")
            datetime.strptime(self.horario_form, "%H:%M")
        except ValueError:
            self.mensagem_erro = "Informe uma data no formato DD/MM/AAAA e um horário válido."
            return

        # Monta payload para o Xano
        payload = {
            "animal_id": int(self.animal_id_form),
            "data_atendimento": data_xano,
            "horario_atendimento": self.horario_form,
            "procedimentos": self.procedimento_form.strip(),
            "veterinario_responsavel": self.veterinario_responsavel_form.strip(),
            "status_atendimento": "Agendado",
            "diagnostico": "",
            "tratamento": "",
            "peso": 0.0,
            "custo": 0.0,
        }

        try:
            with httpx.Client(timeout=8.0) as client:
                res = client.post(XANO_ATENDIMENTO_VET_URL, json=payload)
                if res.status_code in (200, 201):
                    self.data_selecionada = self.data_atendimento_form
                    self.formulario_aberto = False
                    self.mensagem_erro = ""
                    self.mensagem_sucesso = "Agendamento cadastrado com sucesso no Xano!"
                    self.carregar_dados()
                else:
                    self.mensagem_erro = f"Erro ao cadastrar atendimento no servidor ({res.status_code})."
        except Exception as e:
            self.mensagem_erro = f"Erro ao comunicar com a API: {str(e)}"

    # ========================================================
    # DETALHES DO ATENDIMENTO E REGISTRO CLÍNICO (PATCH XANO)
    # ========================================================
    detalhes_abertos: bool = False

    atendimento_selecionado: dict[str, str] = {
        "id": "",
        "animal": "",
        "animal_id": "",
        "data": "",
        "horario": "",
        "procedimento": "",
        "veterinario": "",
        "status": "",
        "diagnostico": "",
        "procedimentos_realizados": "",
        "tratamento": "",
        "peso": "",
        "custo": "",
    }

    alergias_animal_selecionado: str = ""
    restricoes_animal_selecionado: str = ""

    diagnostico_form: str = ""
    procedimentos_realizados_form: str = ""
    tratamento_form: str = ""
    peso_form: str = ""
    custo_form: str = ""

    def abrir_detalhes(self, atendimento_id: str):
        for item in self.agendamentos:
            if item["id"] == atendimento_id:
                self.atendimento_selecionado = dict(item)

                animal = next((a for a in self.animais if a["id"] == item["animal_id"]), None)
                if animal:
                    self.alergias_animal_selecionado = animal["alergias"]
                    self.restricoes_animal_selecionado = animal["restricoes_clinicas"]

                self.diagnostico_form = item["diagnostico"]
                self.procedimentos_realizados_form = item["procedimentos_realizados"]
                self.tratamento_form = item["tratamento"]
                self.peso_form = item["peso"]
                self.custo_form = item["custo"]

                self.mensagem_erro = ""
                self.mensagem_sucesso = ""
                self.detalhes_abertos = True
                break

    def fechar_detalhes(self):
        self.detalhes_abertos = False
        self.mensagem_erro = ""
        self.mensagem_sucesso = ""

    def atualizar_diagnostico(self, valor: str):
        self.diagnostico_form = valor

    def atualizar_procedimentos_realizados(self, valor: str):
        self.procedimentos_realizados_form = valor

    def atualizar_tratamento(self, valor: str):
        self.tratamento_form = valor

    def atualizar_peso(self, valor: str):
        self.peso_form = valor

    def atualizar_custo(self, valor: str):
        self.custo_form = valor

    def salvar_registro_clinico(self):
        atendimento_id = self.atendimento_selecionado.get("id", "")
        if not atendimento_id:
            return

        try:
            peso_val = float(self.peso_form.replace(",", ".")) if self.peso_form.strip() else 0.0
            custo_val = float(self.custo_form.replace(",", ".")) if self.custo_form.strip() else 0.0
        except ValueError:
            self.mensagem_erro = "Peso e custo devem conter valores numéricos válidos."
            return

        payload = {
            "diagnostico": self.diagnostico_form.strip(),
            "procedimentos": self.procedimentos_realizados_form.strip(),
            "tratamento": self.tratamento_form.strip(),
            "peso": peso_val,
            "custo": custo_val,
            "status_atendimento": "Realizado",
        }

        try:
            with httpx.Client(timeout=8.0) as client:
                res = client.patch(f"{XANO_ATENDIMENTO_VET_URL}/{atendimento_id}", json=payload)
                if res.status_code == 200:
                    self.mensagem_erro = ""
                    self.mensagem_sucesso = "Registro clínico salvo! Atendimento marcado como realizado."
                    self.carregar_dados()
                    # Atualiza o item local selecionado para refletir o modal imediatamente
                    self.atendimento_selecionado["status"] = "Realizado"
                else:
                    self.mensagem_erro = "Erro ao atualizar registro clínico no Xano."
        except Exception as e:
            self.mensagem_erro = f"Erro na requisição com a API: {str(e)}"

    def atualizar_status(self, novo_status: str):
        atendimento_id = self.atendimento_selecionado.get("id", "")
        if not atendimento_id or novo_status not in ["Agendado", "Realizado", "Cancelado"]:
            return

        try:
            with httpx.Client(timeout=8.0) as client:
                res = client.patch(
                    f"{XANO_ATENDIMENTO_VET_URL}/{atendimento_id}",
                    json={"status_atendimento": novo_status},
                )
                if res.status_code == 200:
                    self.mensagem_erro = ""
                    self.mensagem_sucesso = f"Status atualizado para {novo_status}!"
                    self.atendimento_selecionado["status"] = novo_status
                    self.carregar_dados()
                else:
                    self.mensagem_erro = "Erro ao atualizar status no Xano."
        except Exception as e:
            self.mensagem_erro = f"Erro na conexão: {str(e)}"

    def on_load(self):
        """Disparado quando a página carrega."""
        self.carregar_dados()

    @rx.var
    def atendimentos_passados(self) -> list[dict[str, str]]:
        # Retorna apenas atendimentos com status Realizado ou Cancelado (ou com datas passadas)
        passados = [
            item for item in self.agendamentos 
            if item["status"] in ["Realizado", "Cancelado"]
        ]
        # Retorna os últimos 5 registros
        return passados[-5:]