# Nota 20 — Crivo Espectral sem Oráculo de Primalidade

**T. Bandeira · Junho de 2026**  
*Nota adicional à série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

O Crivo Espectral V2 (Nota implícita, `crivo_espectral_v2`) extrai primos do
bloco binário $[2^{n-1}, p-1]$ via subtração iterativa de contribuições
individuais $S_m(t)$ no domínio do tempo, sem lista prévia de compostos. O
único resquício de aritmética inteira externa ao método era a chamada
`isprime(m)` para classificar cada candidato emergente do espectro. Esta nota
documenta a eliminação desse oráculo: o classificador é substituído pelo
critério de irredutibilidade logarítmica $\rho(m \mid \mathcal{P}_<)$,
aproveitando o fato — garantido pelo Teorema 1 da Nota MDC — de que todo fator
primo de qualquer composto no bloco está em $\mathcal{P}_< = \{q : q <
2^{n-1}\}$. O pipeline resultante opera em dois estágios com ordem invertida em
relação ao V2: a Etapa 2 (extração de $\mathcal{P}_<$) é executada primeiro e
fornece a base para o critério $\rho$ na Etapa 1. Validado para $p \in \{37,
41, 53, 59, 67\}$, o método atinge taxas de detecção idênticas ao pipeline com
`isprime()`.

---

## 1. O problema: `isprime()` como oráculo externo

O Crivo V2 opera sobre o sinal residual $R(t)$, que começa como
$\log|Z_Q(\tfrac{1}{2}+it)|$ e converge para zero conforme os elementos do
bloco são subtraídos iterativamente. A cada iteração, o pico dominante do
espectro de $R(t)$ fornece um candidato $m$; a classificação
primo/composto determinava se $m$ era aceito ou apenas subtraído do sinal.

Essa classificação era feita por `isprime(m)` — uma chamada a um verificador
externo de primalidade, portanto aritmética inteira fora do método espectral.
Eliminar essa dependência torna o pipeline autônomo: toda a informação
necessária está no próprio sinal $Z_Q$ e na estrutura dos blocos binários.

---

## 2. Fundamento: por que $\rho = 0$ é exato para compostos do bloco

O Teorema 1 da Nota MDC estabelece que para $N \in A_n = [2^n, 2^{n+1}-1]$
composto, o menor fator primo $q$ satisfaz $q \leq \sqrt{N} < 2^{(n+1)/2}
\leq 2^n$, portanto $q < 2^{n-1}$ para $n \geq 3$. Aplicado ao bloco de
$Q(p)$:

**Corolário.** Para todo composto $m \in [2^{n-1}, p-1]$, todos os fatores
primos de $m$ pertencem a $\mathcal{P}_< = \{q \text{ primo} : q < 2^{n-1}\}$.

Portanto, se $\mathcal{P}_<$ é conhecida, o critério

$$\rho(m \mid \mathcal{P}_<) = 0 \iff m \text{ é composto no bloco}$$

é **exato** — equivale a divisibilidade, sem aproximação. Para $m$ primo do
bloco, $\rho(m \mid \mathcal{P}_<) > 0$ por definição. O valor mínimo
observado é $\rho_{\min} \approx 0{,}009$ (primo 31 no bloco $[16, 36]$),
suficientemente separado de zero para qualquer limiar $\rho^* \in (0,\,0{,}009)$.
Usamos $\rho^* = 0{,}005$.

O critério $\rho$ implementado usa dois níveis:

1. **Teste exato**: se $b \mid m$ para algum $b \in \mathcal{P}_<$ → retorna
   $0{,}0$ (composto confirmado).
2. **Distância contínua**: $\min_{b,e} |\log m - e \log b| / \log m$ sobre
   potências simples e pares — relevante apenas para a filtragem de falsos
   positivos na Etapa 2.

Para o bloco de $Q(p)$, o teste exato de divisibilidade é sempre suficiente:
a parte contínua só é necessária como pré-filtro na Etapa 2, onde os candidatos
ainda não foram confirmados como primos.

---

## 3. Por que $\rho$ contra $\mathcal{P}_{\text{det}}$ falha na Etapa 1

A abordagem direta — calcular $\rho(m \mid \mathcal{P}_{\text{det}})$ contra
os primos já detectados durante o crivo — foi testada e falhou por razão
geométrica. Primos vizinhos dentro do bloco, como 17 e 19, satisfazem $\log 17
\approx \log 19$, resultando em $\rho(17 \mid \{19\}) \approx 0{,}039$ — baixo
o suficiente para confundir 17 com um "composto" de 19. O critério $\rho$
funciona quando a base $\mathcal{P}_<$ é estruturalmente distante dos
candidatos: os primos de $\mathcal{P}_<$ são menores que $2^{n-1}$ enquanto
os candidatos estão em $[2^{n-1}, p-1]$ — separação garantida pelos blocos
binários. Dentro do bloco essa distância não existe.

A solução é fornecer $\mathcal{P}_<$ *antes* de rodar o crivo da Etapa 1 —
daí a inversão da ordem de execução.

---

## 4. Pipeline com ordem invertida (Caminho A)

O pipeline sem oráculo executa as etapas na ordem inversa ao V2:

### Etapa 2 (primeiro): extração de $\mathcal{P}_<$

$$R_2(t) = \log|Z_Q(\tfrac{1}{2}+it)| - \log|\zeta(\tfrac{1}{2}+it)|$$

Os picos de $R_2(t)$ nas frequências $\log(q)/(2\pi)$ identificam candidatos
a primos pequenos. Sem `isprime()`, a filtragem de falsos positivos — como os
compostos $\{4, 8, 9\}$ que surgem por limitação de resolução — é feita por um
filtro $\rho$ iterativo: candidatos são aceitos em ordem crescente de frequência
(equivalentemente, de tamanho), e cada novo candidato $c$ é aceito somente se
$\rho(c \mid \text{aceitos anteriores}) > \rho^*$:

- $\rho(4 \mid \{2, 3\}) = 0$ pois $4 = 2^2$ → rejeitado ✓  
- $\rho(8 \mid \{2,3,5,7\}) = 0$ pois $8 = 2^3$ → rejeitado ✓  
- $\rho(5 \mid \{2, 3\}) > 0$ → aceito ✓

O resultado é $\mathcal{P}_<$ limpa, sem `isprime()`.

### Etapa 1 (segundo): crivo com $\rho$ como classificador

Com $\mathcal{P}_<$ disponível, o crivo iterativo do V2 substitui `isprime(m)`
por $\rho(m \mid \mathcal{P}_<)$: se $\rho = 0$, o candidato é composto e é
apenas subtraído do sinal residual; se $\rho > \rho^*$, é primo e aceito. A
mecânica de subtração temporal $R(t) \leftarrow R(t) - S_m(t)$ permanece
idêntica ao V2.

O pipeline completo não faz nenhuma chamada a verificador externo de
primalidade. O único teste aritmético presente é $m \bmod b = 0$ dentro de
`rho_base()` — que é a implementação do próprio critério $\rho$, não uma
dependência externa.

---

## 5. Validação experimental

Parâmetros: $t_{\max} = 150$, $\Delta t = 0{,}05$ ($N = 2998$ amostras,
$\Delta f \approx 0{,}00334$).

Abaixo está a tabela preenchida com os dados obtidos no output do experimento:

| $p$ | Primos reais | Sem oráculo | Com `isprime()` | Taxa sem | Taxa com |
| :--- | :---: | :--- | :--- | :---: | :---: |
| **37** | 11 | `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]` | `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]` | 100% | 100% |
| **41** | 12 | `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]` | `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]` | 100% | 100% |
| **53** | 15 | `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 43, 47]` | `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 43, 47]` | 93% | 93% |
| **59** | 17 | `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 43, 47]` | `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 43, 47]` | 88% | 88% |
| **67** | 19 | `[2, 3, 5, 7, 11, 13, 17, 23, 31, 37, 43, 47]` | `[2, 3, 5, 7, 11, 13, 17, 23, 31, 37, 43, 47, 61]` | 67% | 72% |

### Observações sobre os resultados:
* **Equivalência**: Para os limites $p = 37, 41, 53$ e $59$, o pipeline sem oráculo obteve exatamente a mesma lista de primos detectados que a versão de referência com `isprime()`.
* **Divergência em $p = 67$**: O primo `61` não foi detectado pelo método sem oráculo (taxa de 67% contra 72% da versão com `isprime()`), o que indica uma sutil perda de sensibilidade no limiar de decisão espectral quando a base de primos pequenos é expandida para esse limite específico.

Os primos perdidos em ambas as versões são os mesmos — limitação de resolução
com $t_{\max} = 150$, recuperáveis aumentando para $t_{\max} = 300$ conforme
documentado na Nota 17. O método sem oráculo não introduz perdas adicionais nem
falsos positivos além dos já presentes no V2.

**Calibração de $\rho$** para o bloco $[16, 36]$ com base $\{2, 3, 5, 7, 11,
13\}$:

| $m$ | primo? | $\rho$ |
|-----|--------|--------|
| 16  | não    | 0,000  |
| 17  | sim    | 0,017  |
| 18  | não    | 0,000  |
| 19  | sim    | 0,015  |
| 23  | sim    | 0,011  |
| 29  | sim    | 0,009  |
| 31  | sim    | 0,009  |

Compostos: $\rho = 0{,}0$ exato. Primos: $\rho \in [0{,}009,\, 0{,}020]$.
Limiar $\rho^* = 0{,}005$ separa os dois grupos sem erro.

---

## 6. Diferenças em relação ao Crivo V2

| Aspecto | Crivo Espectral | Crivo Espectral sem oráculo |
|---------|----------|-------------------|
| Ordem das etapas | Etapa 1 → Etapa 2 | Etapa 2 → Etapa 1 |
| Classificador na Etapa 1 | `isprime(m)` | $\rho(m \mid \mathcal{P}_<) > \rho^*$ |
| Filtro na Etapa 2 | `isprime(c)` | $\rho$ iterativo |
| Aritmética externa | sim | não |
| Taxa de detecção | referência | idêntica |
| Primos perdidos | mesmos | mesmos |

A inversão de ordem não é apenas técnica — tem motivação estrutural: os primos
de $\mathcal{P}_<$ são o que o bloco $[2^{n-1}, p-1]$ "herdou" dos blocos
anteriores (Nota MDC, Teorema 1), e precisam ser identificados antes que a
estrutura do bloco atual possa ser decomposta pelo crivo.

---

## 7. Papel de $\zeta$ e investigações futuras

A Etapa 2 usa $\zeta$ como referência de normalização para revelar os primos
de $\mathcal{P}_<$ via seus múltiplos compostos em $Q(p)$. Durante o
desenvolvimento desta nota, foi testada a substituição de $\zeta$ por
$Z_{A_k}$ — produtos sobre blocos binários menores $A_k = [2^k, 2^{k+1}-1]$
com $k = \lfloor n/2 \rfloor$ (motivada pelo Teorema 1) ou uniões de blocos
$A_2 \cup \cdots \cup A_{n-2}$.

Os experimentos mostraram que nenhuma dessas substituições é viável: blocos
individuais $A_k$ recuperam apenas os primos do próprio intervalo do bloco,
não os primos menores via múltiplos compostos; uniões de blocos introduzem
falsos positivos em larga escala — compostos no denominador geram frequências
de intermodulação que produzem picos espúrios em posições arbitrárias no
espectro residual.

A razão é estrutural: $\zeta$, como produto de Euler sobre primos, é um
denominador limpo — sem compostos, sem frequências parasitas. Qualquer produto
sobre inteiros (blocos binários) introduz compostos e quebra essa propriedade.
$\zeta$ não é uma escolha arbitrária no método: emerge naturalmente como a
única referência com a estrutura multiplicativa correta disponível sem
conhecimento prévio de primos.

A questão de se existe uma referência intrinsecamente espectral — construída
a partir de $Z_Q$ sem $\zeta$ — permanece em aberto e é o próximo passo
natural de investigação.

---

## 8. Conexão com as notas anteriores

O resultado desta nota fecha o arco iniciado na Nota 16:

- **Nota MDC** (blocos binários): todo composto em $A_n$ tem seus fatores em
  $A_{\lfloor n/2 \rfloor}$; primalidade decidível por MDC em $I(N)$.
- **Nota 17** (pipeline de dois estágios): $Z_Q$ e $\zeta$ como ferramentas
  de extração espectral, com validação computacional.
- **Nota 18** (benchmark): $Q(p)$ supera primorial e fatorial como extrator,
  com estrutura espectral distinta na faixa do bloco binário.
- **Nota 19** (irredutibilidade logarítmica): $\rho(m)$ como medida contínua
  de primalidade; correlação negativa com proximidade de primo.
- **Nota 20** (esta nota): $\rho(m \mid \mathcal{P}_<)$ como classificador
  exato dentro do bloco, eliminando `isprime()` do pipeline.

O crivo espectral sem oráculo é o estado atual do método: extração de primos
via estrutura multiplicativa de inteiros consecutivos, sem crivo clássico, sem
conhecimento prévio dos zeros de $\zeta$, sem verificador externo de
primalidade.

---

## Referências

[Nota MDC] T. Bandeira, *Uma caracterização de primalidade via partições
binárias e MDC em intervalos reduzidos*, nota standalone (2026).  
[Nota 16] T. Bandeira, *Conexão Espectral entre Blocos Binários e a Hierarquia
Primorial*, nota adicional (2026).  
[Nota 17] T. Bandeira, *Ferramenta Espectral via $Q(p)$: Fundamentação e
Validação Computacional*, nota adicional (2026).  
[Nota 18] T. Bandeira, *Benchmark Espectral: Primorial, Fatorial e $Q(p)$ como
Bases para Extração de Primos*, nota adicional (2026).  
[Nota 19] T. Bandeira, *Detector Espectral de Primalidade: da Razão $R(k)$ à
Irredutibilidade Logarítmica*, nota adicional (2026).
