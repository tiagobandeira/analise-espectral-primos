# Nota 25 — Critério ρ sem Aritmética Inteira: Separabilidade Logarítmica e Limites de Escala

**T. Bandeira · 2026**  
*Nota adicional à série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

O critério ρ_B usado no pipeline das Notas 20–24 contém um único uso de
aritmética inteira: o teste de divisibilidade `m % b == 0`. Esta nota
investiga se esse teste pode ser eliminado, substituindo-o pela versão
puramente contínua ρ_cont, que mede a distância de log(m) ao reticulado
gerado por {log(b) : b na base}. Os experimentos (Exp D, `exp_d_rho_continuo.ipynb`)
mostram que a separação é perfeita para blocos k ≤ 5 — rho_max dos compostos
fica na ordem de 10^{-16} (erro de ponto flutuante) enquanto rho_min dos
primos fica acima de 10^{-3}. Para k ≥ 6, a separação colapsa: compostos
com muitas potências de primos pequenos (ex: 96 = 2^5 × 3) produzem
rho_cont da mesma ordem que primos do bloco, causando falsos positivos.
O padrão dos escapados revela a causa: a busca de combinações logarítmicas
precisa de expoentes crescentes com k, enquanto a implementação usa um teto
fixo. A nota propõe uma correção incremental — restringir os expoentes ao
intervalo possível para cada bloco — como questão aberta, e conclui que a
aritmética inteira é o algoritmo ótimo para o critério de irredutibilidade
no regime de n grande, não uma dependência conceitual.

---

## 1. Contexto

O critério ρ_B, introduzido na Nota 19 e usado como classificador nas Notas
20–24, tem dois componentes:

1. **Teste de divisibilidade:** `m % b == 0` para algum b na base → retorna 0.0 exato.
2. **Distância contínua:** mínimo de `|log(m) - combinação de logs da base| / log(m)`.

O componente 1 é aritmética inteira pura. O componente 2 é puramente analítico.
A questão desta nota: o componente 1 é necessário, ou o componente 2 sozinho
é suficiente para separar primos de compostos em todos os blocos?

A motivação é conceitual: se o critério de irredutibilidade logarítmica é
puramente geométrico — distância de log(m) ao reticulado dos logs da base —
idealmente sua implementação também seria puramente analítica.

---

## 2. O critério ρ_cont

Define-se a versão puramente contínua:

```
ρ_cont(m, base) = min{ |log(m) - Σ e_i * log(b_i)| / log(m) }
```

onde o mínimo é tomado sobre:
- **Singles:** e * log(b) para b na base, e = 1, 2, ..., e_max
- **Pares:** e1 * log(b1) + e2 * log(b2) para b1, b2 na base, e1, e2 = 1..4
- **Triplos:** e1*log(b1) + e2*log(b2) + e3*log(b3), e1,e2,e3 = 1..2

Para compostos m = prod p_i^{e_i} com p_i na base, a igualdade
log(m) = Σ e_i * log(p_i) é matematicamente exata. O único erro é
de ponto flutuante (float64 ~ 10^{-15}), portanto ρ_cont dos compostos
deveria ser da ordem de 10^{-15} / log(m) — essencialmente zero.

Para primos m do bloco, nenhuma combinação inteira dos logs da base
iguala log(m) pelo Teorema Fundamental da Aritmética — portanto ρ_cont > 0.

---

## 3. Resultados experimentais (Exp D)

### 3.1 Separabilidade por bloco

| k | A[k] | rho_min primos | rho_max compostos | Gap | Separável |
|---|------|---------------|-------------------|-----|-----------|
| 2 | [4,7]     | 6.86e-02 | 1.24e-16 | 6.86e-02 | ✓ |
| 3 | [8,15]    | 2.89e-02 | 9.64e-17 | 2.89e-02 | ✓ |
| 4 | [16,31]   | 9.25e-03 | 1.54e-16 | 9.25e-03 | ✓ |
| 5 | [32,63]   | 3.96e-03 | 1.24e-16 | 3.96e-03 | ✓ |
| 6 | [64,127]  | 1.62e-03 | 2.29e-03 | -6.75e-04 | ✗ |
| 7 | [128,255] | 7.20e-04 | 1.97e-03 | -1.25e-03 | ✗ |
| 8 | [256,511] | 3.16e-04 | 1.32e-03 | -1.00e-03 | ✗ |

Para k ≤ 5 a margem de separação é de 10^{13} a 10^{14} — completamente
fora de qualquer ambiguidade numérica. Para k ≥ 6 o gap inverte de sinal:
alguns compostos têm ρ_cont maior que alguns primos.

### 3.2 Padrão dos compostos que escapam

Os compostos que produzem ρ_cont erroneamente alto têm um padrão claro —
todos possuem muitas potências de primos pequenos:

```
k=6: m=96  = 2^5 × 3     rho_cont = 2.29e-3
     m=120 = 2^3 × 3 × 5 rho_cont = 1.73e-3

k=7: m=192 = 2^6 × 3     rho_cont = 1.97e-3
     m=210 = 2 × 3 × 5 × 7 rho_cont = 8.93e-4

k=8: m=270 = 2 × 3^3 × 5 rho_cont = 1.32e-3
     m=96  = 2^5 × 3     rho_cont = 6.78e-4  (reaparece como herdado)
```

A causa é direta: `log(96) = 5*log(2) + log(3)` exige e=5 no par (2,3),
mas a implementação de ρ_cont usa e1, e2 ≤ 4 para pares. O expoente
necessário excede o teto fixo da busca.

### 3.3 Recursão com ρ_cont: zero falsos negativos, muitos falsos positivos

Rodando a recursão C1 com ρ_cont e rho* = 1e-6:

| n_alvo | Primos reais | TP | FP | FN |
|--------|-------------|----|----|-----|
| 5 | 11 | 11 | 7  | 0 |
| 6 | 18 | 18 | 15 | 0 |
| 7 | 31 | 31 | 29 | 0 |
| 8 | 54 | 54 | 64 | 0 |

Nenhum primo é perdido — a irredutibilidade logarítmica genuína dos primos
garante ρ_cont > 0 independente da profundidade da busca. O problema são
os compostos com expoente alto que "fingem" ser irredutíveis por limitação
da busca.

---

## 4. Por que os primos grandes são mais fáceis de separar

A observação empírica — separação perfeita para k ≤ 5, colapso para k ≥ 6
— tem uma explicação geométrica direta.

Para um primo grande q próximo de 2^k, log(q) está perto de k * log(2).
Para que algum composto m tenha log(m) próximo de log(q), m precisaria
de muitos fatores pequenos com expoentes altos — ou seja, m seria uma
potência alta de 2 ou 3, que está longe do bloco A[k]. Os compostos
*dentro* do bloco têm log(m) distribuído em toda a faixa [k*log(2), (k+1)*log(2)],
e suas fatorações envolvem combinações de primos menores que,
por construção da base S_k, estão todas presentes. O sinal geométrico
é limpo.

Para os primos pequenos da base — o problema desta nota — o cenário é
inverso. Um primo pequeno p tem log(p) << k*log(2). Para um composto m
do bloco A[k] com fator p, a relação `log(m) ≈ e*log(p) + log(cofator)`
envolve um expoente e que pode ser grande (e ~ k*log(2)/log(p)).
Quando e excede o teto da busca, ρ_cont não encontra a combinação
e reporta um valor erroneamente alto.

Já os primos do bloco têm `rho_min` que decresce com k porque o espaçamento
relativo entre primos consecutivos diminui — `(log(q+2) - log(q)) / log(q) ~ 2/q`.
Assim, à medida que k cresce, rho_min dos primos cai, e os compostos
escapados ficam cada vez mais próximos do limiar.

---

## 5. Correção incremental por bloco (questão aberta)

A causa do problema é precisa: o expoente máximo necessário para decompor
um composto m ∈ A[k] com fator primo p é:

```
e_max(p, k) = floor(k * log(2) / log(p))
```

Para p=2, k=6: e_max = floor(6 * 0.693 / 0.693) = 6.
Para p=3, k=8: e_max = floor(8 * 0.693 / 1.099) = 5.

Uma implementação de ρ_cont adaptativa usaria e_max(p, k) em vez de um
teto fixo. Isso garantiria cobertura exata para qualquer composto do bloco
sem aritmética inteira, ao custo de uma busca proporcional a k por elemento.

**Ideia de correção incremental:** em vez de subtrair a contribuição de log(p)
sozinho, subtrair a contribuição de p elevado ao seu maior expoente possível
para o bloco — `e_max(p,k) * log(p)`. Isso "desconta" do sinal logarítmico
de m não apenas a presença de p, mas sua contribuição máxima possível.
O resíduo `log(m) - e_max(p,k)*log(p)` seria menor para compostos com fator p
do que para primos do bloco, potencialmente restaurando a separação.

Formalmente, define-se:

```
ρ_adapt(m, base, k) = min_{p in base} |log(m) - e_max(p,k)*log(p)| / log(m)
```

como pré-filtro antes da busca de combinações. Se ρ_adapt ≈ 0 para algum p,
m é composto com aquele fator dominante. A questão empírica — se esse
pré-filtro restaura a separação sem introduzir novos falsos negativos —
está em aberto.

---

## 6. Aritmética inteira como algoritmo ótimo

A análise acima permite uma conclusão mais precisa sobre o papel da
aritmética inteira no critério ρ_B.

A aritmética inteira não é uma dependência conceitual — é o algoritmo
ótimo para computar o critério de irredutibilidade quando a base é
composta de inteiros. O teste `m % b == 0` verifica em O(1) se
`log(m) - log(b) - log(m/b) = 0` exatamente, sem busca de expoentes.
É a implementação direta da propriedade multiplicativa dos inteiros
na linguagem da divisibilidade.

A versão contínua ρ_cont tenta aproximar essa verificação via busca
no espaço logarítmico. Para blocos pequenos funciona porque os expoentes
necessários são pequenos e o ruído de ponto flutuante é desprezível.
Para blocos grandes, a busca precisa ser mais profunda — e o custo
cresce enquanto a aritmética inteira permanece O(|base|).

A tabela comparativa de custo por candidato:

| Método | Custo | Exatidão | Escala com k |
|--------|-------|----------|--------------|
| `m % b` (aritmética inteira) | O(|base|) | Exato | Constante |
| ρ_cont com e_max fixo | O(|base|² × e_max) | Aproximado | Degrada |
| ρ_cont com e_max(p,k) adaptativo | O(|base|² × k) | Exato | Linear |

O ponto central: a aritmética inteira não conflita com a natureza
analítica do método — ela é o mesmo critério, implementado de forma
ótima para inteiros.

---

## 7. Questões em aberto

**Questão 1 — ρ_adapt restaura a separação?**
A correção incremental proposta na Seção 5 — usar e_max(p,k) em vez de
teto fixo — é testável diretamente. O Exp D pode ser estendido com
ρ_adapt e verificar se a separação é restaurada para k ≥ 6 sem novos
falsos negativos.

**Questão 2 — Limite teórico da separação contínua.**
Existe um k* acima do qual nenhuma implementação contínua com profundidade
polinomial em k consegue separar primos de compostos? Ou a separação
é sempre restaurável aumentando e_max? A resposta envolve a distribuição
dos gaps `rho_min(primos) - rho_max(compostos)` como função de k.

**Questão 3 — Conexão com aproximação diofantina.**
O problema de encontrar `e` inteiro tal que `|log(m) - e*log(p)|` é pequeno
é um problema de aproximação diofantina. Para p=2, isso é equivalente a
encontrar potências de 2 próximas de m — bem estudado. Para combinações de
múltiplos primos, a teoria de formas lineares em logaritmos (Baker) fornece
cotas inferiores para `|Σ e_i * log(p_i) - log(m)|` quando m não é divisível
pelos p_i. Essas cotas conectariam ρ_cont dos primos a resultados clássicos
de teoria dos números transcendentes.

---

## 8. Conclusão

A separação entre primos e compostos via ρ_cont é estruturalmente real —
não é artefato da implementação — mas exige profundidade de busca crescente
com k. Para k ≤ 5, float64 é suficiente e a separação é perfeita com teto
fixo. Para k ≥ 6, compostos com expoentes altos de primos pequenos escapam,
produzindo falsos positivos mas nunca falsos negativos. A aritmética inteira
resolve o problema em O(|base|) com exatidão garantida, e é o algoritmo
ótimo para o critério quando a base é inteira. A correção incremental por
bloco — restringir a busca ao expoente máximo possível para cada primo em
cada bloco — é a direção natural para uma implementação contínua exata,
e permanece como questão aberta.

---

## Referências

[Nota 19] T. Bandeira, *Detector Espectral de Primalidade: da Razão R(k) à
Irredutibilidade Logarítmica*, nota adicional (2026).  
[Nota 20] T. Bandeira, *Crivo Espectral sem Oráculo de Primalidade*, nota
adicional (2026).  
[Nota 23] T. Bandeira, *Extração Recursiva de Primos via Blocos Binários:
Substituição de ζ na Etapa 2*, nota adicional (2026).  
[Nota 24] T. Bandeira, *Pré-limpeza Espectral: Fechando a Equivalência com
a Versão com ζ*, nota adicional (2026).  
[Exp D] T. Bandeira, `exp_d_rho_continuo.ipynb` — Separabilidade de ρ_cont
para k=2..8, Junho de 2026.  
A. Baker, *Transcendental Number Theory*, Cambridge University Press (1975).
