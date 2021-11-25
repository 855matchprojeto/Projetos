from sqlalchemy import or_, and_
from typing import Optional

from server.configuration.environment import Environment
from server.models.historico_projetos_model import HistoricoProjetoModel
from server.repository.historico_projetos_repository import HistoricoProjetoRepository


class HistoricoProjetosService():

    def __init__(self, proj_repo: Optional[HistoricoProjetoRepository] = None,
                 environment: Optional[Environment] = None):
        self.proj_repo = proj_repo
        self.environment = environment

    async def get(self, id=None, guid=None):
        if id is None and guid == None:
            filtros = []
        else:
            filtros = [
                or_(
                    HistoricoProjetoModel.id == id,
                    HistoricoProjetoModel.guid == guid
                )]

        projects_history = await self.proj_repo.find_projetos_by_ids()  # filtros=filtros
        for project_history in projects_history:
            entidades = [historico_projeto_entidade.entidade_externa for historico_projeto_entidade in project_history.historico_projeto_entidade]
            tags = [historico_projeto_tag.tag for historico_projeto_tag in project_history.historico_projeto_tag]
            project_history.entidades = entidades
            project_history.tags = tags

        return projects_history
