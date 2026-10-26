# Decisões metodológicas

O registro reúne as regras **adotadas** (validadas nas etapas de diagnóstico) e as decisões **D1–D8, aprovadas em 25/10/2026**. Para cada decisão aprovada, o status de implementação diz o que já foi executado e o que é só formalização ou trabalho futuro. A classificação de evidência usa sempre:
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

## Decisões D1–D8 (aprovadas)

**Status de implementação:**
- **Já implementada:** o notebook executado segue a decisão.
- **Apenas formalizada:** o critério está definido, mas não foi aplicado no código desta execução.
- **Sensibilidade ainda não executada:** a análise complementar está prevista, mas não foi calculada.
- **Alteração futura necessária:** o experimento executado difere da decisão; o ajuste exige recalcular e **não** foi feito nesta versão.

| ID | Decisão aprovada | Status | Observações sobre a implementação atual |
|---|---|---|---|
| **D1** Evidência do Affects Version | Estimativa **ampliada** (COMPROVADO + INFERIDO COM CORROBORAÇÃO) como principal; **conservadora** (só COMPROVADO) como limite inferior; **máxima** (+ INFERIDO SEM CORROBORAÇÃO) como sensibilidade. Evidência observada e inferência permanecem distintas. | **Já implementada** | Cap. 9.2. A direção e a ordem de grandeza do efeito do tamanho da release se mantêm (IRR 1,45 / 1,40 / 1,39), mas as contagens absolutas diferem muito (média observada no teste: 1,27 / 8,20 / 8,42 bugs por release). Os cenários **não** são equivalentes. |
| **D2** Vínculos indeterminados | Projeto elegível só com **≤ 10%** de vínculos temporalmente INDETERMINADOS, **além** dos critérios já usados (Affects Version em ≥ 50% dos bugs e ≥ 30 bugs desde 2020) | **Apenas formalizada** + **alteração futura necessária** | O limite não foi aplicado no código. Entre os 133 projetos verificáveis, 2 o ultrapassam: HTTPCORE (12,9%), que **está** na população do modelo H1, e MSKINS, já excluído por versionamento modular. Aplicar a regra removeria HTTPCORE do H1; o efeito **não foi recalculado**. |
| **D3** Releases anteriores a 2020 | Análise principal a partir de 2020; releases anteriores só como contexto (ex.: intervalo entre releases); 2019 fora da modelagem principal | **Já implementada** (análise principal); **sensibilidade ainda não executada** (opcional) | A perda nas janelas é de 93 / 578 / 1.617 vínculos (30 / 90 / 180 d), cerca de 5% dos vínculos de 180 d. Há risco de truncamento à esquerda caso o 2º semestre de 2019 seja incluído numa sensibilidade. |
| **D4** Reaberturas rápidas | Indicador principal com **todas** as reaberturas válidas por transição de status; Resolution como evidência complementar; reaberturas rápidas sinalizadas e **nunca** excluídas automaticamente | **Já implementada** (indicador principal e sinalização ≤ 5 min); **sensibilidade ainda não executada** | A versão sem re-encerramentos ≤ 1 h com outra Resolution não foi calculada. Esses re-encerramentos são 209 das 636 reaberturas ≤ 5 min. |
| **D5** Possíveis operações em lote | Sinalização **exploratória** de concentrações de **≥ 20 reaberturas no mesmo projeto e dia**; sem exclusão automática; sem afirmar natureza administrativa sem evidência | **Apenas formalizada** | O critério está definido, mas **a sinalização não foi calculada** nesta versão. Os casos de BEAM e CELEBORN foram observados só entre as divergências status × Resolution (etapa de validação). |
| **D6** Janela pós-release | Horizonte principal de **180 d**; complementar de **90 d**; 30 d só descritivo; acompanhamento completo exigido em cada horizonte; só informação disponível em T0 | **Já implementada** (180 d); **sensibilidade ainda não executada** (modelo com 90 d) | Os 90 d e 30 d aparecem só nas estatísticas descritivas (Cap. 5). |
| **D7** Modelagem por projeto | **Modelo principal conjunto** com controle das diferenças entre projetos (efeito fixo de projeto); modelos individuais **complementares e exploratórios**, só com observações suficientes, classes representadas, estimação viável, convergência e teste válido. A regra de ~10 eventos por variável **não** garante viabilidade. | **Já implementada** (modelo principal); individuais **exploratórios** | Na H2, os modelos individuais foram **ajustados para os 22 projetos** que passaram no filtro inicial. Superaram o baseline em 21 e o modelo conjunto em só **6**, o que reforça o modelo conjunto como principal. Não houve modelo individual na H1. Não há promessa de modelo individual para todos os projetos. |
| **D8** Séries interrompidas | Podem contribuir para o **treino conjunto**; sem avaliação individual quando não há observações de teste; separação cronológica preservada; ausência de issues recentes **não** prova encerramento do projeto | **H1: já implementada**. **H2: alteração futura necessária**. | **H1:** projetos com treino entram no ajuste, e a avaliação usa só os que têm releases de teste. **H2:** a população exige bugs no treino **e** no teste, então projetos sem observações de teste (ex.: ARROW, BEAM, NETBEANS, que param em 2022) ficaram fora **também do treino**. Isso difere da decisão aprovada, e o ajuste não foi recalculado. Projetos com série interrompida que ainda têm teste (ex.: HUDI, MNG) foram avaliados normalmente. A exclusão desses projetos do treino é uma sensibilidade futura. |

**Ponto ainda em aberto (não é D1–D8):** `releaseDate` como data real de publicação continua **NÃO DEMONSTRADO**. Nesta versão, ela é tratada como a data registrada no Jira.

### Análises de sensibilidade e ajustes pendentes

1. **H1 com horizonte de 90 d (D6).**
2. **H1 sem projetos acima de 10% de vínculos indeterminados (D2):** exclui HTTPCORE.
3. **H2 incluindo no treino os projetos sem observações de teste (D8):** é um ajuste para conformidade com a decisão.
4. **H1/H2 excluindo do treino os projetos com série interrompida (D8):** sensibilidade.
5. **Estabilidade sem re-encerramentos ≤ 1 h com outra Resolution (D4).**
6. **Sinalização de possíveis lotes de reaberturas (D5).**
7. **Releases do 2º semestre de 2019 (D3):** opcional.
