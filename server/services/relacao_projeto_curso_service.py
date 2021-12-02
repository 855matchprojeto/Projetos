from typing import Optional, List
from server.configuration.environment import Environment
from server.repository.relacao_projeto_curso_repository import RelacaoProjetoCursoRepository
from server.models.relacao_projeto_curso import RelacaoProjetoCursoModel
from server.schemas.relacao_projeto_curso_schema import RelacaoProjetoCursoInput
from sqlalchemy import or_, and_


class RelacaoProjetoCursoService():

    def __init__(self, rel_repo: Optional[RelacaoProjetoCursoRepository] = None,
                 environment: Optional[Environment] = None):
        self.rel_proj_curso_repo = rel_repo
        self.environment = environment

    async def get(self, id_projetos=None, id_cursos=None):
        if id_projetos == None and id_cursos == None:
            filtros = []
        else:
            filtros = [
                or_(
                    RelacaoProjetoCursoModel.id_projetos == id_projetos,
                    RelacaoProjetoCursoModel.id_cursos == id_cursos
                )]
        return await self.rel_proj_curso_repo.find_rel_by_filtros(filtros=filtros)

    async def mult_insert(self, relacoes: List[RelacaoProjetoCursoInput]):
        resp = []
        for relacao in relacoes:
            data = await self.create(relacao);
            resp.append(data)
        return resp

    async def mult_delete(self, relacoes):
        for relacao in relacoes:
            await self.delete(relacao.id_projetos, relacao.id_cursos);

    async def create(self, rel_proj_curso_input):
        if type(rel_proj_curso_input) is not dict:
            rel_proj_curso_input = rel_proj_curso_input.convert_to_dict()
        # Insere no banco de dados e retorna a relacao

        resp = await self.rel_proj_curso_repo.insere_relacao(rel_proj_curso_input)
        return resp

    async def delete(self, id_projetos: int, id_cursos: int):
        filtros = [
            and_(
                RelacaoProjetoCursoModel.id_projetos == id_projetos,
                RelacaoProjetoCursoModel.id_cursos == id_cursos
            )]
        await self.rel_proj_curso_repo.delete_relacao_by_filtros(filtros=filtros)
