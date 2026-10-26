# Decisões metodológicas

O registro separa as regras **adotadas** (validadas nas etapas de diagnóstico) das **pendentes**, que ainda dependem de aprovação. A classificação de evidência usa sempre:
- **COMPROVADO:** registrado num evento.
- **INFERIDO:** depende de uma premissa.
- **INDETERMINADO:** não determinável com os dados.

## Regras adotadas

### Gerais
1. **Unidade primária = projeto.** Os indicadores são calculados por projeto; a consolidação é uma segunda camada (efeito fixo ou multinível de projeto) e só ocorre entre workflows compatíveis.
2. **Período principal:** eventos com T0 ≥ 2020-01-01; fim da observação em 2026-10-25 (snapshot).
   - **Motivo:** a coleta só traz issues anteriores a 2020 que estavam abertas ou foram atualizadas depois de 2020. Isso gera viés de seleção: 49,7% de abertas entre as anteriores a 2020, contra 22,3% entre as posteriores.
   - **Registros anteriores:** são mantidos para contexto e relacionamentos (ex.: intervalo entre releases).
3. **Sprints fora do escopo.**
4. **Horas de worklog não medem esforço.** 99,84% dos registros vêm da integração automática com o GitHub.
5. **Prioridade ≠ severidade.** Nenhum campo de severidade tem cobertura suficiente.
6. **Pseudonimização.** Pessoas aparecem só como hash com sal local. Não há rankings individuais.

### Releases × Bugs (Objetivo 1)
7. **Vínculo explícito.** Affects Version por **ID de versão** e no mesmo projeto. Não há atribuição por proximidade temporal: 72% das releases têm outra release do mesmo projeto em 90 dias.
8. **Classes temporais.** Data UTC de criação do bug × `releaseDate`:
   - **A:** antes da release.
   - **B:** no mesmo dia.
   - **C:** depois da release.
   - **D:** data insuficiente.

   A contagem de "bugs após a release" usa **só a classe C**. A classe A indica uso do campo para a linha em desenvolvimento e é analisada à parte.
9. **Multiplicidade.** Um bug conta uma vez por versão; não há soma entre versões nem escolha de uma versão principal.
10. **Releases sem bugs vinculados** são classificadas, não lidas como "sem defeitos":
    - zero vinculado em projeto com Affects Version ≥ 50%;
    - projeto com baixa cobertura;
    - dados insuficientes (< 30 bugs);
    - acompanhamento incompleto.
11. **Nível de evidência do vínculo** (reconstrução reversa do campo Version):
    - **COMPROVADO:** evento de inclusão.
    - **INFERIDO COM CORROBORAÇÃO** (`RECONSTRUIDO`): presente na criação, com reverso e cadeia de status consistentes.
    - **INFERIDO SEM CORROBORAÇÃO:** issue sem histórico ou com cadeia de status quebrada.
    - **INDETERMINADO:** issue movida ou reverso inconsistente.
12. **Limitação declarada.** A exclusão ou mescla de versões no Jira altera as issues **sem evento**: 969 issues têm reverso inconsistente, e 1.173 de 1.202 inconsistências envolvem versões inexistentes. A presença "desde a criação" continua sendo inferência.
13. **Versões modulares** (≥ 30% dos nomes com prefixo de módulo; ex.: SLING, FELIX, FLINK) são tratadas à parte e ficam fora do modelo agrupado principal.
14. **Projetos elegíveis:** associação verificável, ou seja, Affects Version em ≥ 50% dos bugs desde 2020 e ≥ 30 bugs.

### Tempo de correção (Objetivo 2)
15. **Indicadores:**
    - **B1:** primeira resolução (evento `resolution` não vazio).
    - **B2:** primeiro fechamento (primeira entrada em status de categoria `done`; **não** "Closed").
    - **B3:** primeira correção (evento `resolution = Fixed`).

    Duplicate, Invalid, Won't Fix e similares são "encerrado sem Fixed", não correção.
16. **Sem datas inventadas.** Bugs abertos são censurados. Para classificação, usa-se horizonte fixo com acompanhamento completo. "Não corrigido em 90 d" não significa "nunca corrigido".
17. **Faixas no horizonte de 90 d:** ≤ 7 d, 8–30 d, 31–90 d, > 90 d ou não Fixed.

### Reaberturas (Objetivo 5, exploratório)
18. **Reabertura** é a transição de status de categoria `done` → `new`/`indeterminate`.
    - **Critério:** a categoria vem do Jira, não do nome do status. Resolved → Closed não é reabertura.
    - **Papel da Resolution:** a limpeza do campo é corroboração, não requisito.
    - **Concordância:** 4.163 de 4.556 bugs.
    - **Divergências:** 100% explicadas por workflow (reabre sem limpar a Resolution, ou fecha sem Resolution).
19. **Reaberturas rápidas (≤ 5 min)** são sinalizadas, nunca excluídas automaticamente.
20. **Estabilidade:** ausência de reabertura em 30/90 d após o primeiro fechamento ou o primeiro Fixed, só com acompanhamento completo.

### Modelagem
21. **Variáveis em T0.** Só variáveis disponíveis em T0, reconstruídas pelo changelog (prioridade e responsável na abertura, componentes na criação, composição da release em T0). Nunca o estado atual.
22. **Split cronológico comum:**
    - **Treino:** T0 em 2020–2023.
    - **Teste:** T0 ≥ 2024 com o horizonte completamente observado.
23. **Técnicas ensinadas no MBA:** começar por baseline e um modelo comprovadamente ensinado.
    - **H2:** regressão logística multinomial.
    - **H1:** regressão Binomial Negativa.
    - **Demais técnicas:** citadas apenas como possibilidade futura.

## Decisões pendentes (não aprovadas)

| ID | Decisão | Valor provisório usado nesta versão |
|---|---|---|
| D1 | Nível de evidência da contagem principal de bugs após a release | **Ampliado** (COMPROVADO + RECONSTRUÍDO); conservador e máximo reportados como sensibilidade |
| D2 | Limite de vínculos INDETERMINADOS para excluir um projeto | Nenhum projeto excluído por esse critério |
| D3 | Incluir releases do 2º semestre de 2019 numa sensibilidade (truncamento à esquerda) | Não incluídas |
| D4 | Estabilidade oficial com ou sem re-encerramentos ≤ 1 h com outra Resolution | Todas as reaberturas (versão a) |
| D5 | Critério de "lote suspeito" de reaberturas | Não aplicado; casos documentados (BEAM, CELEBORN) |
| D6 | Janela definitiva pós-release (30/90/180 d) | 180 d no modelo; 30/90 d descritivos |
| D7 | Critérios mínimos para modelo individual por projeto | Regra de bolso de ~10 eventos por variável (`projetos_resumo.json`) |
| D8 | Tratamento dos 26 projetos com série interrompida | Mantidos no treino agrupado; sem avaliação individual |
| — | `releaseDate` como data real de publicação | **NÃO DEMONSTRADO**; tratada como a data registrada no Jira |
