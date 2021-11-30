from typing import Optional
from server.configuration.environment import Environment
from server.repository.relacao_projeto_tag_repository import RelacaoProjetoTagRepository
from server.models.relacao_projeto_tag import RelacaoProjetoTagModel
from sqlalchemy import or_, and_


class RelacaoProjetoTagService():

    def __init__(self, tag_repo: Optional[RelacaoProjetoTagRepository] = None, environment: Optional[Environment] = None):
        self.rel_proj_tag_repo = tag_repo
        self.environment = environment

    async def get(self, id_projetos=None, id_tags=None):
        if id_projetos == None and id_tags == None:
            filtros = []
        else:
            filtros = [
                or_(
                    RelacaoProjetoTagModel.id_projetos == id_projetos,
                    RelacaoProjetoTagModel.id_tags == id_tags
                )]
        return await self.rel_proj_tag_repo.find_rel_by_filtros(filtros=filtros)

    async def mult_insert(self, relacoes):
        resp = []
        for relacao in relacoes:
            data = await self.create(relacao);
            resp.append(data)
        return resp

    async def mult_delete(self, relacoes):
        for relacao in relacoes:
            await self.delete(relacao.id_projetos, relacao.id_tags);

    async def create(self, rel_proj_tag_input):
        novo_rel_proj_tag_dict = rel_proj_tag_input.convert_to_dict()
        # Insere no banco de dados e retorna a relacao

        resp = await self.rel_proj_tag_repo.insere_relacao(novo_rel_proj_tag_dict)
        return resp


    async def delete(self, id_projetos: int, id_tags: int):
        filtros = [
            and_(
                RelacaoProjetoTagModel.id_projetos == id_projetos,
                RelacaoProjetoTagModel.id_tags == id_tags
            )]
        await self.rel_proj_tag_repo.delete_relacao_by_filtros(filtros=filtros)
