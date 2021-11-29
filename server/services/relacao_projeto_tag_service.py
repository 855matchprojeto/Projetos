from typing import Optional
from server.configuration.environment import Environment
from server.repository.relacao_projeto_tag_repository import RelacaoProjetoTagRepository
from server.models.relacao_projeto_tag import RelacaoProjetoTagModel
from sqlalchemy import or_, and_


class RelacaoProjetoTagService():

    def __init__(self, tag_repo: Optional[RelacaoProjetoTagRepository] = None, environment: Optional[Environment] = None):
        self.rel_proj_tag_repo = tag_repo
        self.environment = environment

    async def mult_insert(self, relacoes):
        resp = []
        for relacao in relacoes:
            data = await self.create(relacao);
            resp.insert(data)
        return data

    async def mult_delete(self, relacoes):
        for relacao in relacoes:
            await self.delete(relacao['id_projeto'], relacao['id_tag']);

    async def create(self, rel_proj_tag_input):
        novo_rel_proj_tag_dict = rel_proj_tag_input.convert_to_dict()
        # Insere no banco de dados e retorna a relacao

        resp = await self.rel_proj_tag_repo.insere_relacao(novo_rel_proj_tag_dict)
        return resp


    async def delete(self, id_projeto: int, id_tag: int):
        filtros = [
            and_(
                RelacaoProjetoTagModel.id_projetos == id_projeto,
                RelacaoProjetoTagModel.id_tags == id_tag
            )]
        return await self.rel_proj_tag_repo.delete_relacao_by_filtros(filtros=filtros)
