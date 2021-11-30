from typing import Optional
from server.configuration.environment import Environment
from server.repository.relacao_projeto_entidade_repository import RelacaoProjetoEntidadeRepository
from server.models.relacao_projeto_entidade import RelacaoProjetoEntidadeModel
from sqlalchemy import or_, and_


class RelacaoProjetoEntidadeService():

    def __init__(self, rel_repo: Optional[RelacaoProjetoEntidadeRepository] = None, environment: Optional[Environment] = None):
        self.rel_proj_entidade_repo = rel_repo
        self.environment = environment

    async def get(self, id_projetos=None, id_entidade=None):
        if id_projetos == None and id_entidade == None:
            filtros = []
        else:
            filtros = [
                or_(
                    RelacaoProjetoEntidadeModel.id_projetos == id_projetos,
                    RelacaoProjetoEntidadeModel.id_entidade == id_entidade
                )]
        return await self.rel_proj_entidade_repo.find_rel_by_filtros(filtros=filtros)

    async def mult_insert(self, relacoes):
        resp = []
        for relacao in relacoes:
            data = await self.create(relacao);
            resp.append(data)
        return resp

    async def mult_delete(self, relacoes):
        for relacao in relacoes:
            await self.delete(relacao.id_projetos, relacao.id_entidade);

    async def create(self, rel_proj_entidade_input):
        novo_rel_proj_entidade_dict = rel_proj_entidade_input.convert_to_dict()
        # Insere no banco de dados e retorna a relacao

        resp = await self.rel_proj_entidade_repo.insere_relacao(novo_rel_proj_entidade_dict)
        return resp


    async def delete(self, id_projetos: int, id_entidade: int):
        filtros = [
            and_(
                RelacaoProjetoEntidadeModel.id_projetos == id_projetos,
                RelacaoProjetoEntidadeModel.id_tags == id_entidade
            )]
        await self.rel_proj_entidade_repo.delete_relacao_by_filtros(filtros=filtros)
