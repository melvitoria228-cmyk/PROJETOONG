import reflex as rx
import httpx
from typing import List, Dict, Any

# URLs dos endpoints do Xano
URL_GET_PROCESSOS = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/processo_adocao"
URL_POST_PROCESSO = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/processo_adocao"
URL_PATCH_PROCESSO = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/processo/adocao/update"
URL_GET_TUTORES = "https://x8ki-letl-twmt.n7.xano.io/api:Ad2Yak5N/admin/tutor_adotante"


class AdocoesState(rx.State):
    """Estado do Módulo de Adoções integrado ao Xano."""

    # --- MÉTRICAS ---
    variacao_total: str = "+12%"

    # --- FILTROS ---
    filtro_texto: str = ""
    filtro_status: str = "Todos"
    opcoes_status: List[str] = [
        "Todos",
        "Em análise",
        "Mais informações necessárias",
        "Aprovada",
        "Adoção efetivada",
        "Não aprovada",
    ]

    # --- DADOS DAS SOLICITAÇÕES ---
    solicitacoes: List[Dict[str, str]] = []
    solicitacao_selecionada: Dict[str, str] = {"id": ""}

    # Lista de tutores do Xano
    tutores: List[Dict[str, Any]] = []

    # Estado de carregamento
    is_loading: bool = False
    error_message: str = ""

    # --- CARREGAMENTO INICIAL DIRETO ---
    async def on_load(self):
        """Carrega os dados dos endpoints do Xano ao abrir a página."""
        self.is_loading = True
        self.error_message = ""

        async with httpx.AsyncClient() as client:
            try:
                res_proc = await client.get(URL_GET_PROCESSOS)

                if res_proc.status_code == 200:
                    raw_data = res_proc.json()

                    normalizados = []
                    for item in raw_data:
                        animal = item.get("_animal_1") or item.get("_animal") or {}
                        tutor = item.get("_tutor_adotante") or {}

                        # Ignora registros vazios/incompletos
                        if not animal and not tutor.get("nome"):
                            continue

                        foto_pet = (
                            animal.get("foto_url")
                            or "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400"
                        )

                        especie = str(animal.get("especie") or "").strip()
                        raca = str(animal.get("raca") or "").strip()
                        especie_raca = " • ".join(p for p in (especie, raca) if p) or "Não informado"

                        porte = str(animal.get("porte") or "").strip()
                        sexo = str(animal.get("sexo") or "").strip()
                        porte_sexo = " • ".join(p for p in (porte, sexo) if p) or "Não informado"

                        alergias = str(animal.get("alergias") or "").strip()
                        restricoes = str(animal.get("restricoes_clinicas") or "").strip()
                        cuidados = " | ".join(
                            p for p in (alergias, restricoes)
                            if p and p.lower() not in ("nenhuma", "nenhuma conhecida")
                        ) or "Sem restrições"

                        normalizados.append({
                            "id": str(item.get("id", "")),
                            "nome_tutor": str(tutor.get("nome") or "Tutor Desconhecido"),
                            "cpf": str(tutor.get("cpf") or "Não informado"),
                            "telefone": str(tutor.get("telefone") or "Não informado"),
                            "email": str(tutor.get("email") or "Não informado"),
                            "endereco": str(tutor.get("endereco") or "Não informado"),
                            "data": str(item.get("data_inicio") or item.get("data_solicitacao") or "N/A"),
                            "status": str(item.get("status_processo") or "Em análise"),
                            "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100",
                            "foto_detalhe": str(foto_pet),

                            # Dados reais vindos do Add-on _animal_1
                            "pet_nome": str(animal.get("nome") or "Sem Nome"),
                            "pet_status": str(animal.get("status_atual") or "Disponível"),
                            "pet_especie": especie_raca,
                            "pet_detalhes": porte_sexo,
                            "pet_saude": str(animal.get("condicao_saude") or "Saudável"),
                            "pet_descricao": str(animal.get("descricao") or "Sem descrição registrada"),
                            "pet_cuidados": cuidados,

                            "exp_animal": "Sim",
                            "lar_tipo": str(tutor.get("tipo_residencia") or "Casa"),
                            "lar_familia": "Não informado",
                            "lar_tempo": "Livre",
                            "check_cerca": "Sim",
                            "check_espaco": "Sim",
                            "check_outros": "Não",
                        })

                    self.solicitacoes = normalizados
                    if self.solicitacoes:
                        self.solicitacao_selecionada = dict(self.solicitacoes[0])
                else:
                    self.error_message = f"Erro Xano ({res_proc.status_code})"

                res_tutores = await client.get(URL_GET_TUTORES)
                if res_tutores.status_code == 200:
                    self.tutores = res_tutores.json()

            except Exception as e:
                self.error_message = f"Falha na conexão: {str(e)}"
            finally:
                self.is_loading = False

    # --- ATUALIZAÇÃO DE STATUS NO XANO ---
    async def alterar_status(self, novo_status: str):
        sol_id = self.solicitacao_selecionada.get("id", "")
        if not sol_id:
            return

        payload = {
            "processo_adocao_id": int(sol_id),
            "status_processo": novo_status,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.patch(URL_PATCH_PROCESSO, json=payload)
                if response.status_code == 200:
                    atualizadas: List[Dict[str, str]] = []
                    for item in self.solicitacoes:
                        if item["id"] == sol_id:
                            novo_pet_status = (
                                "Adotado"
                                if novo_status == "Adoção efetivada"
                                else item["pet_status"]
                            )
                            item = {
                                **item,
                                "status": novo_status,
                                "pet_status": novo_pet_status,
                            }
                            self.solicitacao_selecionada = dict(item)
                        atualizadas.append(item)
                    self.solicitacoes = atualizadas
                else:
                    self.error_message = f"Erro ao atualizar no backend: {response.text}"
            except Exception as e:
                self.error_message = f"Erro na requisição: {str(e)}"

    # --- SETTERS E SELEÇÃO ---
    def set_filtro_texto(self, valor: str):
        self.filtro_texto = valor

    def set_filtro_status(self, valor: str):
        self.filtro_status = valor

    def selecionar_solicitacao(self, item_id: str):
        for item in self.solicitacoes:
            if item["id"] == item_id:
                self.solicitacao_selecionada = dict(item)
                break

    # --- VARS CALCULADAS ---
    @rx.var
    def solicitacoes_filtradas(self) -> List[Dict[str, str]]:
        resultado = self.solicitacoes
        if self.filtro_status != "Todos":
            resultado = [
                item
                for item in resultado
                if item["status"].lower() == self.filtro_status.lower()
            ]
        if self.filtro_texto:
            termo = self.filtro_texto.lower()
            resultado = [
                item
                for item in resultado
                if termo in item["nome_tutor"].lower()
                or termo in item["pet_nome"].lower()
            ]
        return resultado

    @rx.var
    def total_adocoes(self) -> int:
        return len(self.solicitacoes)

    @rx.var
    def pendentes_aprovacao(self) -> int:
        return len([
            s for s in self.solicitacoes
            if s["status"].lower() in ("aguardando aprovação", "em análise", "em processo")
        ])

    @rx.var
    def aguardando_info(self) -> int:
        return len([
            s for s in self.solicitacoes
            if s["status"].lower() in ("revisão pendente", "mais informações necessárias")
        ])

    @rx.var
    def em_processo(self) -> int:
        return len([
            s for s in self.solicitacoes
            if s["status"].lower() in (
                "aguardando aprovação",
                "em análise",
                "em processo",
                "revisão pendente",
                "mais informações necessárias",
            )
        ])

    @rx.var
    def aprovadas(self) -> int:
        return len([
            s for s in self.solicitacoes
            if s["status"].lower() in ("aprovada", "adoção efetivada", "realizado")
        ])

    @rx.var
    def recusadas(self) -> int:
        return len([
            s for s in self.solicitacoes
            if s["status"].lower() in ("recusada", "não aprovada")
        ])

    @rx.var
    def tem_muitas_solicitacoes(self) -> bool:
        return len(self.solicitacoes_filtradas) > 3