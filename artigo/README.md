# Uma representação espectral da aritmética

Artigo autocontido em LaTeX: primos, compostos e crivos em frequência.

```
artigo/
  artigo.tex                    fonte (preamble + \input das seções)
  artigo.pdf                    compilado, 30 páginas
  secoes/                       01-intro … 10-perspectiva, apA-lean, apB-numeros
  figuras/                      f1…f6 em PDF vetorial (usadas pelo .tex)
                                e1…e5 em PNG (versão anterior)
  experimentos/
    figuras_artigo.py           gera as seis figuras PDF a partir das definições
    verificar_teoremas.py       verificações por força bruta e tabelas
    resultados.json             valores brutos
    verificacao_teoremas.{json,md}
  auditoria-e-correcoes.md      documento anterior: a auditoria das notas
```

Compilar:

```bash
cd artigo
pdflatex --enable-installer artigo.tex   # duas vezes, para as referências
```

(`--enable-installer` só é necessário na primeira vez, para o MiKTeX baixar os
pacotes ausentes.)

## O que o artigo contém

Um dicionário entre a aritmética multiplicativa e a reta real — produto vira
soma, suavidade vira pertencer a um reticulado, primalidade vira
irredutibilidade — e, sobre ele, três imagens do crivo.

| § | conteúdo | resultado central |
|---|---|---|
| 2 | o dicionário | Teorema 2.7: irredutível ⟺ primo |
| 3 | blocos binários | Lema 3.2 e Teorema 3.3 (crivo por blocos) |
| 4 | geometria do reticulado | **Teoremas 4.2 e 4.4**: `ρ(q) = log(1+1/q)/log q`, exato |
| 5 | o desenho | Figuras 1 e 2: os primos do bloco como picos isolados |
| 6 | resolução | **Teorema 6.4**: `τ(Seed_k) = Θ(2^k/k)`; Corolário 6.5 |
| 7 | contagem coerente | **Proposição 7.2**: a razão medida é exatamente `k` |
| 8 | assinatura de um par | Proposição 8.1: sinal `1`, fundo `O(q/T)` |
| 9 | verificação | tabela do que o Lean cobre |
| 10 | perspectiva | o dicionário em resumo, perguntas abertas |

Apêndice A: os enunciados verificados em Lean 4, em notação matemática.
Apêndice B: os dados numéricos completos.

## Relação com o resto do repositório

O artigo é autocontido: não cita as notas da série, e todos os resultados que usa
estão demonstrados nele. O repositório entra como material suplementar — código,
figuras, formalização — e como registro do percurso.

`auditoria-e-correcoes.md` é o documento anterior, de natureza diferente: ele
confronta as notas 16–40 com os cálculos e registra três correções (a lei de
`T_max` é linear em `p`; a rota de Baker é desnecessária; os "80,1%" medem
incompletude da busca). Fica aqui porque é útil a quem for mexer nas notas, mas
não faz parte do artigo.
