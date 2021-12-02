from typing import Optional, List
from server.configuration.environment import Environment
from server.repository.relacao_projeto_interesse_repository import RelacaoProjetoInteresseRepository
from server.models.relacao_projeto_interesse import RelacaoProjetoInteresseModel
from server.schemas.relacao_projeto_interesse_schema import RelacaoProjetoInteresseInput
from sqlalchemy import or_, and_


class RelacaoProjetoInteresseService():

    def __init__(self, rel_repo: Optional[RelacaoProjetoInteresseRepository] = None,
                 environment: Optional[Environment] = None):
        self.rel_proj_interesse_repo = rel_repo
        self.environment = environment

    async def get(self, id_projetos=None, id_interesses=None):
        if id_projetos == None and id_interesses == None:
            filtros = []
        else:
            filtros = [
                or_(
                    RelacaoProjetoInteresseModel.id_projetos == id_projetos,
                    RelacaoProjetoInteresseModel.id_interesses == id_interesses
                )]
        return await self.rel_proj_interesse_repo.find_rel_by_filtros(filtros=filtros)

    async def mult_insert(self, relacoes: List[RelacaoProjetoInteresseInput]):
        resp = []
        for relacao in relacoes:
            data = await self.create(relacao);
            resp.append(data)
        return resp

    async def mult_delete(self, relacoes):
        for relacao in relacoes:
            await self.delete(relacao.id_projetos, relacao.id_interesses);

    async def create(self, rel_proj_interesse_input):
        if type(rel_proj_interesse_input) is not dict:
            rel_proj_interesse_input = rel_proj_interesse_input.convert_to_dict()
        # Insere no banco de dados e retorna a relacao

        resp = await self.rel_proj_interesse_repo.insere_relacao(rel_proj_interesse_input)
        return resp

    async def delete(self, id_projetos: int, id_interesses: int):
        filtros = [
            and_(
                RelacaoProjetoInteresseModel.id_projetos == id_projetos,
                RelacaoProjetoInteresseModel.id_interesses == id_interesses
            )]
        await self.rel_proj_interesse_repo.delete_relacao_by_filtros(filtros=filtros)
