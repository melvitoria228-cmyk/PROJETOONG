import os
import unicodedata
import reflex as rx
import httpx

# URL base do seu grupo no Xano (sem repetições)
BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N"

XANO_LAR_TEMPORARIO_URL = f"{BASE_URL}/lar_temporario"
XANO_ANIMAL_URL = f"{BASE_URL}/animal"
XANO_ANIMAL_LAR_URL = f"{BASE_URL}/animal_lar_temporario"


def _normalizar_texto(texto: str) -> str:
    """Remove acentos, espaços extras e converte para minúsculo."""
    sem_acento = "".join(
        c for c in unicodedata.normalize("NFD", str(texto or ""))
        if unicodedata.category(c) != "Mn"
    )
    return sem_acento.strip().lower()


def _normalizar_data_xano(data_str: str) -> str:
    """Converte DD/MM/AAAA ou AAAA/MM/DD para AAAA-MM-DD."""
    valor = (data_str or "").strip().replace("/", "-")
    partes = valor.split("-")
    if len(partes) == 3 and len(partes[0]) == 2 and len(partes[2]) == 4:
        return f"{partes[2]}-{partes[1]}-{partes[0]}"
    return valor


class LaresTemporariosState(rx.State):
    """Estado do módulo de Lares Temporários integrado com o Xano."""

    # FILTROS
    filtro_texto: str = ""
    filtro_status: str = "Todos"
    opcoes_filtro: list[str] = ["Todos", "Com vagas", "Lotado"]

    # DADOS OBTIDOS DA API XANO
    lares: list[dict[str, str]] = []
    animais: list[dict[str, str]] = []
    permanencias: list[dict[str, str]] = []

    # SELEÇÃO E FORMULÁRIOS
    lar_selecionado: dict[str, str] = {"id": ""}
    animal_selecionado_id: str = ""
    data_inicio: str = ""
    data_saida: str = ""
    observacoes_alocacao: str = ""
    observacoes_saida: str = ""
    destino_transferencia_id: str = ""
    mensagem: str = ""
    carregando: bool = False

    # CADASTRO DE NOVO LAR (MODAL)
    mostrar_form_cadastro: bool = False
    novo_nome_responsavel: str = ""
    novo_telefone: str = ""
    novo_endereco: str = ""
    nova_capacidade: str = "1"
    novas_observacoes: str = ""
    mensagem_cadastro: str = ""

    # SETTERS
    def set_filtro_texto(self, valor: str):
        self.filtro_texto = valor

    def set_filtro_status(self, valor: str):
        self.filtro_status = valor

    def set_animal_selecionado(self, valor: str):
        self.animal_selecionado_id = valor
        self.mensagem = ""

    def set_data_inicio(self, valor: str):
        self.data_inicio = valor

    def set_data_saida(self, valor: str):
        self.data_saida = valor

    def set_observacoes_alocacao(self, valor: str):
        self.observacoes_alocacao = valor

    def set_observacoes_saida(self, valor: str):
        self.observacoes_saida = valor

    def set_mostrar_form_cadastro(self, aberto: bool):
        self.mostrar_form_cadastro = aberto
        if not aberto:
            self.mensagem_cadastro = ""

    def set_novo_nome_responsavel(self, valor: str):
        self.novo_nome_responsavel = valor

    def set_novo_telefone(self, valor: str):
        self.novo_telefone = valor

    def set_novo_endereco(self, valor: str):
        self.novo_endereco = valor

    def set_nova_capacidade(self, valor: str):
        self.nova_capacidade = valor

    def set_novas_observacoes(self, valor: str):
        self.novas_observacoes = valor

    # CARREGAMENTO DOS DADOS (GET)
    def carregar_dados(self):
        self.carregando = True
        try:
            with httpx.Client(timeout=8.0) as client:
                # 1. Lares
                res_lares = client.get(XANO_LAR_TEMPORARIO_URL)
                if res_lares.status_code == 200:
                    dados = res_lares.json()
                    self.lares = [
                        {
                            "id": str(item.get("id", "")),
                            "nome_responsavel": str(item.get("nome_responsavel", "")),
                            "telefone": str(item.get("telefone", "")),
                            "endereco": str(item.get("endereco", "")),
                            "capacidade": str(item.get("capacidade", "0")),
                            "observacoes": str(item.get("observacoes", "")),
                        }
                        for item in dados
                    ]

                # 2. Animais
                res_animais = client.get(XANO_ANIMAL_URL)
                if res_animais.status_code == 200:
                    dados = res_animais.json()
                    self.animais = [
                        {
                            "id": str(item.get("id", "")),
                            "nome": str(item.get("nome", "")),
                            "especie": str(item.get("especie", "")),
                            "raca": str(item.get("raca", "")),
                            "porte": str(item.get("porte", "")),
                            "condicao_saude": str(item.get("condicao_saude", "")),
                            "status_atual": str(item.get("status_atual", "")),
                        }
                        for item in dados
                    ]

                # 3. Permanências
                res_perm = client.get(XANO_ANIMAL_LAR_URL)
                if res_perm.status_code == 200:
                    dados = res_perm.json()
                    self.permanencias = [
                        {
                            "id": str(item.get("id", "")),
                            "animal_id": str(item.get("animal_id", "")),
                            "lar_temporario_id": str(item.get("lar_temporario_id", "")),
                            "data_inicio": str(item.get("data_inicio", "")),
                            "data_fim": str(item.get("data_fim") or ""),
                            "observacoes": str(item.get("observacoes", "")),
                        }
                        for item in dados
                    ]
        except Exception as e:
            self.mensagem = f"Erro de conexão com o banco: {str(e)}"
        finally:
            self.carregando = False

    # CÁLCULOS E AUXILIARES
    def capacidade_lar(self, lar_id: str) -> int:
        for lar in self.lares:
            if lar["id"] == lar_id:
                try:
                    digitos = "".join(c for c in str(lar["capacidade"]) if c.isdigit())
                    return int(digitos) if digitos else 0
                except (ValueError, TypeError):
                    return 0
        return 0

    def permanencias_ativas(self, lar_id: str = "") -> list[dict[str, str]]:
        resultado = [
            p for p in self.permanencias
            if not p["data_fim"] or p["data_fim"].lower() == "none"
        ]
        if lar_id:
            resultado = [p for p in resultado if p["lar_temporario_id"] == lar_id]
        return resultado

    def quantidade_ocupantes(self, lar_id: str) -> int:
        return len(self.permanencias_ativas(lar_id))

    def vagas_disponiveis(self, lar_id: str) -> int:
        capacidade = self.capacidade_lar(lar_id)
        ocupacao = self.quantidade_ocupantes(lar_id)
        return max(capacidade - ocupacao, 0)

    def nome_animal(self, animal_id: str) -> str:
        for animal in self.animais:
            if animal["id"] == animal_id:
                return animal["nome"]
        return "Animal não encontrado"

    @rx.var
    def nome_animal_selecionado(self) -> str:
        if not self.animal_selecionado_id:
            return "Nenhum"
        for animal in self.animais:
            if animal["id"] == self.animal_selecionado_id:
                return f"{animal['nome']} (ID {animal['id']})"
        return self.animal_selecionado_id

    @rx.var
    def lares_com_resumo(self) -> list[dict[str, str]]:
        resultado = []
        for lar in self.lares:
            ocupantes = self.quantidade_ocupantes(lar["id"])
            capacidade = self.capacidade_lar(lar["id"])
            vagas = max(capacidade - ocupantes, 0)

            nomes = [
                self.nome_animal(p["animal_id"])
                for p in self.permanencias_ativas(lar["id"])
            ]

            resultado.append({
                **lar,
                "ocupacao": str(ocupantes),
                "vagas": str(vagas),
                "nomes_animais": ", ".join(nomes) if nomes else "",
                "situacao": "Lotado" if vagas == 0 else "Com vagas",
            })
        return resultado

    @rx.var
    def lares_filtrados(self) -> list[dict[str, str]]:
        resultado = self.lares_com_resumo
        if self.filtro_status != "Todos":
            resultado = [lar for lar in resultado if lar["situacao"] == self.filtro_status]

        if self.filtro_texto:
            termo = self.filtro_texto.lower()
            resultado = [
                lar for lar in resultado
                if termo in lar["nome_responsavel"].lower()
                or termo in lar["endereco"].lower()
                or termo in lar["nomes_animais"].lower()
            ]
        return resultado

    @rx.var
    def total_lares(self) -> int:
        return len(self.lares)

    @rx.var
    def total_animais_acolhidos(self) -> int:
        return len(self.permanencias_ativas())

    @rx.var
    def total_vagas_disponiveis(self) -> int:
        return sum(self.vagas_disponiveis(lar["id"]) for lar in self.lares)

    @rx.var
    def total_lares_com_vagas(self) -> int:
        return len([lar for lar in self.lares_com_resumo if lar["situacao"] == "Com vagas"])

    @rx.var
    def animais_disponiveis(self) -> list[dict[str, str]]:
        alocados = {
            p["animal_id"]
            for p in self.permanencias
            if not p["data_fim"] or p["data_fim"].lower() == "none"
        }
        return [
            animal for animal in self.animais
            if _normalizar_texto(animal["status_atual"]) == "disponivel"
            and animal["id"] not in alocados
        ]

    @rx.var
    def historico_lar_selecionado(self) -> list[dict[str, str]]:
        lar_id = self.lar_selecionado.get("id", "")
        resultado = []
        for permanencia in self.permanencias:
            if permanencia["lar_temporario_id"] == lar_id:
                ativa = not permanencia["data_fim"] or permanencia["data_fim"].lower() == "none"
                resultado.append({
                    **permanencia,
                    "nome_animal": self.nome_animal(permanencia["animal_id"]),
                    "situacao": "Em andamento" if ativa else "Finalizada",
                })
        return resultado

    # AÇÕES PERSISTIDAS NO XANO (POST E PATCH)
    def cadastrar_lar(self):
        if (
            not self.novo_nome_responsavel.strip()
            or not self.novo_telefone.strip()
            or not self.novo_endereco.strip()
        ):
            self.mensagem_cadastro = "Preencha nome do responsável, telefone e endereço."
            return

        digitos_cap = "".join(c for c in str(self.nova_capacidade) if c.isdigit())
        capacidade_int = int(digitos_cap) if digitos_cap else 1
        if capacidade_int <= 0:
            self.mensagem_cadastro = "A capacidade deve ser de pelo menos 1 animal."
            return

        payload = {
            "nome_responsavel": self.novo_nome_responsavel.strip(),
            "telefone": self.novo_telefone.strip(),
            "endereco": self.novo_endereco.strip(),
            "capacidade": capacidade_int,
            "observacoes": self.novas_observacoes.strip(),
        }

        try:
            with httpx.Client(timeout=8.0) as client:
                res = client.post(XANO_LAR_TEMPORARIO_URL, json=payload)
                if res.status_code in (200, 201):
                    self.novo_nome_responsavel = ""
                    self.novo_telefone = ""
                    self.novo_endereco = ""
                    self.nova_capacidade = "1"
                    self.novas_observacoes = ""
                    self.mensagem_cadastro = ""
                    self.mostrar_form_cadastro = False
                    self.mensagem = "Lar parceiro cadastrado com sucesso!"
                    self.carregar_dados()
                    if self.lares and not self.lar_selecionado.get("id"):
                        self.lar_selecionado = dict(self.lares[-1])
                else:
                    self.mensagem_cadastro = (
                        f"Erro ao cadastrar lar ({res.status_code}): {res.text}"
                    )
        except Exception as e:
            self.mensagem_cadastro = f"Erro na chamada da API: {str(e)}"

    def selecionar_lar(self, lar_id: str):
        if not lar_id:
            self.lar_selecionado = {"id": ""}
            self.animal_selecionado_id = ""
            self.mensagem = ""
            return

        for lar in self.lares:
            if lar["id"] == lar_id:
                self.lar_selecionado = dict(lar)
                self.animal_selecionado_id = ""
                self.mensagem = ""
                break

    def alocar_animal(self):
        lar_id = self.lar_selecionado.get("id", "")
        if not lar_id or not self.animal_selecionado_id or not self.data_inicio:
            self.mensagem = "Preencha todos os campos obrigatórios (selecione o animal e a data de início)."
            return

        if self.vagas_disponiveis(lar_id) <= 0:
            self.mensagem = "Este lar não possui vagas disponíveis."
            return

        data_formatada = _normalizar_data_xano(self.data_inicio)

        payload_permanencia = {
            "animal_id": int(self.animal_selecionado_id),
            "lar_temporario_id": int(lar_id),
            "data_inicio": data_formatada,
            "data_fim": None,
            "observacoes": self.observacoes_alocacao,
        }

        try:
            with httpx.Client(timeout=8.0) as client:
                res_perm = client.post(XANO_ANIMAL_LAR_URL, json=payload_permanencia)
                if res_perm.status_code in (200, 201):
                    client.patch(
                        f"{XANO_ANIMAL_URL}/{self.animal_selecionado_id}",
                        json={"status_atual": "Em Lar Temporário"},
                    )
                    self.mensagem = "Animal alocado com sucesso!"
                    self.animal_selecionado_id = ""
                    self.data_inicio = ""
                    self.observacoes_alocacao = ""
                    self.carregar_dados()
                else:
                    self.mensagem = f"Erro ao registrar alocação no servidor ({res_perm.status_code}): {res_perm.text}"
        except Exception as e:
            self.mensagem = f"Erro na chamada da API: {str(e)}"

    def registrar_saida(self, permanencia_id: str, data_fim: str):
        if not data_fim:
            self.mensagem = "Informe a data de saída."
            return

        permanencia = next((p for p in self.permanencias if p["id"] == permanencia_id), None)
        if not permanencia:
            self.mensagem = "Permanência não encontrada."
            return

        data_formatada = _normalizar_data_xano(data_fim)

        try:
            with httpx.Client(timeout=8.0) as client:
                res_perm = client.patch(
                    f"{XANO_ANIMAL_LAR_URL}/{permanencia_id}",
                    json={
                        "data_fim": data_formatada,
                        "observacoes": (permanencia["observacoes"] + f" | Saída: {self.observacoes_saida}").strip(" | "),
                    },
                )
                if res_perm.status_code == 200:
                    client.patch(
                        f"{XANO_ANIMAL_URL}/{permanencia['animal_id']}",
                        json={"status_atual": "Disponível"},
                    )
                    self.mensagem = "Saída registrada com sucesso!"
                    self.data_saida = ""
                    self.observacoes_saida = ""
                    self.carregar_dados()
                else:
                    self.mensagem = f"Erro ao registrar saída ({res_perm.status_code}): {res_perm.text}"
        except Exception as e:
            self.mensagem = f"Erro na chamada da API: {str(e)}"

    def on_load(self):
        self.carregar_dados()
        if self.lares and not self.lar_selecionado.get("id"):
            self.lar_selecionado = dict(self.lares[0])