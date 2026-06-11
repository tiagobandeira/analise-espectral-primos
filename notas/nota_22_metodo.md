# Nota 22 — Método do Crivo Espectral Oracle-Free

**T. Bandeira · Junho de 2026**  
*Nota de método — complementar à Nota 21 (formalização teórica)*

---

## Resumo

Descrevemos o método do Crivo Espectral Oracle-Free de forma reproduzível e
agnóstica de linguagem. O método extrai os primos de um bloco binário
$[2^{n-1}, p-1]$ sem conhecimento prévio de primos e sem oráculo externo de
primalidade, usando apenas aritmética básica e transformada de Fourier discreta.
A justificativa teórica completa está na Nota 21; esta nota foca no algoritmo,
nos parâmetros e em critérios de qualidade verificáveis. Um leitor com acesso
a qualquer ambiente de computação numérica (Python, Julia, R, MATLAB, ou
equivalente) consegue reproduzir o método a partir desta descrição.

---

## 1. Contexto e fundamento teórico

O método repousa sobre três resultados da Nota 21:

**Teoremas 1 e 2** — compostos são logaritmicamente redutíveis (sua frequência
característica $f_m = \log(m)/(2\pi)$ é combinação linear inteira das
frequências de seus fatores); primos são irredutíveis.

**Teorema 3** — o operador de redução $\mathcal{R}_m$ remove a contribuição do
inteiro $m$ do sinal residual sem afetar as contribuições dos demais elementos,
no limite $T \to \infty$. Isso vale porque as funções $t \mapsto \cos(t \log m)$
são assintoticamente ortogonais no espaço de Dirichlet.

**Corolário** — aplicando $\mathcal{R}_m$ iterativamente sobre todos os
compostos de $\mathcal{B} = [2^{n-1}, p-1]$, os sinais sobreviventes
correspondem exatamente aos primos de $\mathcal{B}$.

A FFT não é objeto da teoria — é o instrumento que implementa o Corolário:
torna visíveis as frequências sobreviventes após a eliminação iterativa.

---

## 2. Definições operacionais

### 2.1 O sinal de um inteiro

Para $m \geq 2$ e parâmetro real $t > 0$, define-se:

$$S_m(t) = -\frac{1}{2} \log\!\left(1 - 2\,m^{-1/2}\cos(t \log m) + m^{-1}\right)$$

Esta função oscila principalmente na frequência $f_m = \log(m)/(2\pi)$
com amplitude aproximada $m^{-1/2}$.

### 2.2 O sinal do bloco

Para o conjunto $\mathcal{B} = \{2^{n-1}, 2^{n-1}+1, \ldots, p-1\}$:

$$Z_{\mathcal{B}}(t) = \sum_{m \in \mathcal{B}} S_m(t)$$

### 2.3 O critério de redutibilidade $\rho$

Dado um conjunto de primos base $P$ e um inteiro $m$:

$$\rho(m \mid P) = 0 \iff \exists\, b \in P : b \mid m$$

Quando $\rho(m \mid P) = 0$, $m$ é composto (redutível). Quando
$\rho(m \mid P) > 0$, $m$ é candidato a primo (irredutível).

Para filtragem de falsos positivos, usa-se também a distância logarítmica
contínua (ver Seção 4.2).

### 2.4 Notação de frequência

A frequência característica de $m$ é $f_m = \log(m)/(2\pi)$.
A inversão é $m = \mathrm{round}(\exp(2\pi f))$.
A resolução espectral é $\Delta f = 1/(N \cdot \Delta t)$, onde
$N$ é o número de amostras e $\Delta t$ o passo de amostragem.

---

## 3. Parâmetros do método

| Parâmetro | Notação | Papel | Valor típico |
|-----------|---------|-------|-------------|
| Extremo superior do intervalo de $t$ | $T_{\max}$ | Controla a ortogonalidade (Teorema 3) e a resolução espectral | $150$–$300$ |
| Passo de amostragem | $\Delta t$ | Define $N = T_{\max}/\Delta t$ amostras | $0{,}05$ |
| Limiar do critério $\rho$ | $\rho^*$ | Separa primos de compostos (Lema $\rho$, Nota 21) | $0{,}005$ |
| Altura relativa mínima de pico | $h$ | Filtra ruído de fundo na FFT | $0{,}03$ |
| Distância mínima entre picos | $d_f$ | Evita detecção dupla do mesmo pico | $0{,}008$ |

**Escolha de $T_{\max}$:** para separar dois primos consecutivos $q_1 < q_2$,
é necessário $T_{\max} > 2\pi / (\log q_2 - \log q_1)$. Para o par mais
próximo no bloco $[2^{n-1}, p-1]$, calcule esse valor e use-o como cota
inferior de $T_{\max}$. Para $p \leq 67$, $T_{\max} = 150$ é suficiente;
para $p \leq 200$, use $T_{\max} = 300$.

---

## 4. O algoritmo

O método opera em duas etapas executadas nesta ordem: primeiro a Etapa 2
(que extrai $\mathcal{P}_<$), depois a Etapa 1 (que criba o bloco usando
$\mathcal{P}_<$). A ordem é obrigatória — a Etapa 1 depende do resultado
da Etapa 2.

---

### Etapa 2 — Extração de $\mathcal{P}_<$

**Objetivo:** obter $\mathcal{P}_< = \{q \text{ primo} : q < 2^{n-1}\}$
sem oráculo de primalidade.

**Entrada:** $p$, parâmetros $T_{\max}$, $\Delta t$, $\rho^*$, $h$, $d_f$.

**Passo 2.1 — Calcular o sinal residual $R_2$**

$$R_2(t) = Z_{\mathcal{B}}(t) - \log|\zeta(\tfrac{1}{2}+it)|, \qquad t \in [T_{\min}, T_{\max}]$$

Para calcular $\log|\zeta(\tfrac{1}{2}+it)|$: usar uma biblioteca de precisão
arbitrária (ex: mpmath em Python, ArbLib em C, ou equivalente). Este é o único
passo que requer computação especial — $\zeta$ na linha crítica. O valor pode
ser cacheado para reutilização com os mesmos parâmetros.

$T_{\min} = 0{,}1$ evita a singularidade em $t = 0$.

**Passo 2.2 — Aplicar a FFT ao sinal $R_2$**

Centralizar o sinal (subtrair a média) antes da FFT. Calcular as amplitudes
$|{\rm FFT}(R_2)|$ e as frequências correspondentes $f_k = k/(N \Delta t)$.

**Passo 2.3 — Extrair picos candidatos**

Identificar os picos locais do espectro de amplitude com:
- altura $\geq h \cdot \max(\text{amplitude})$
- distância mínima entre picos $\geq d_f$ em unidades de frequência

Para cada pico em frequência $f$, calcular o candidato $c = \mathrm{round}(\exp(2\pi f))$.
Manter apenas candidatos $c \geq 2$.

**Passo 2.4 — Filtrar candidatos com o critério $\rho$ iterativo**

Ordenar os candidatos $c_1 < c_2 < \cdots$ em ordem crescente.
Inicializar $\mathcal{P}_< = \emptyset$.

Para cada candidato $c_i$:
- Se $\rho(c_i \mid \mathcal{P}_<) = 0$: descartar ($c_i$ é composto dado
  o que já foi aceito)
- Se $\rho(c_i \mid \mathcal{P}_<) > \rho^*$: aceitar, adicionar a $\mathcal{P}_<$

**Saída da Etapa 2:** $\mathcal{P}_< = \{q_1, q_2, \ldots\}$ — primos menores
que $2^{n-1}$, sem oráculo externo.

---

### Etapa 1 — Crivo do bloco $\mathcal{B}$

**Objetivo:** identificar os primos de $\mathcal{B} = [2^{n-1}, p-1]$.

**Entrada:** $\mathcal{P}_<$ (da Etapa 2), $\mathcal{B}$, parâmetros.

**Passo 1.1 — Inicializar o sinal residual**

$$R(t) \leftarrow Z_{\mathcal{B}}(t), \qquad t \in [T_{\min}, T_{\max}]$$

**Passo 1.2 — Loop de eliminação iterativa**

Enquanto o sinal $R(t)$ tiver picos detectáveis:

1. Aplicar FFT ao sinal $R(t)$ centralizado
2. Identificar o pico dominante em frequência $f^*$
3. Calcular o candidato $m = \mathrm{round}(\exp(2\pi f^*))$
4. Classificar $m$ usando o critério $\rho$:
   - Se $\rho(m \mid \mathcal{P}_<) = 0$: $m$ é **composto** — subtrair
     $S_m(t)$ do resíduo e continuar
   - Se $\rho(m \mid \mathcal{P}_<) > \rho^*$: $m$ é **primo** — registrar
     em $\mathcal{P}_{\text{int}}$ e subtrair $S_m(t)$ do resíduo
5. Atualizar: $R(t) \leftarrow R(t) - S_m(t)$

**Critério de parada:** quando a amplitude máxima do espectro de $R(t)$
cair abaixo de $h \cdot \text{amp\_inicial}$, ou quando todos os elementos
de $\mathcal{B}$ tiverem sido processados.

**Saída da Etapa 1:** $\mathcal{P}_{\text{int}}$ — primos de $\mathcal{B}$.

---

### Resultado final

$$\text{Primos}(p) = \mathcal{P}_< \cup \mathcal{P}_{\text{int}}$$

O conjunto completo de primos menores que $p$, sem uso de oráculo de
primalidade em nenhuma etapa.

---

## 5. Pseudocódigo completo

```
função CRIVO_ORACLE_FREE(p, T_max, Δt, ρ*, h, d_f):

  # Configuração
  n     ← floor(log2(p))
  B     ← {2^{n-1}, ..., p-1}
  t_arr ← {T_min, T_min + Δt, ..., T_max}    # grade de amostragem
  N     ← |t_arr|

  # Pré-calcular sinais
  Z_B   ← Σ_{m ∈ B} S_m(t_arr)               # sinal do bloco
  ζ_arr ← log|ζ(½ + i·t_arr)|               # via biblioteca de precisão

  # ── ETAPA 2: extrair P< ─────────────────────────────────────────

  R2 ← Z_B - ζ_arr
  candidatos ← EXTRAIR_PICOS(FFT(R2 - média(R2)), h, d_f)
  candidatos ← ORDENAR_CRESCENTE(candidatos)

  P_lt ← []
  para cada c em candidatos:
    se ρ(c | P_lt) > ρ*:
      P_lt ← P_lt ∪ {c}

  # ── ETAPA 1: crivar bloco B ─────────────────────────────────────

  R ← Z_B
  P_int ← []
  amp0 ← max(|FFT(R - média(R))|)

  enquanto max(|FFT(R - média(R))|) > h · amp0:
    f*  ← frequência do pico dominante de FFT(R - média(R))
    m   ← round(exp(2π · f*))
    R   ← R - S_m(t_arr)                     # operador ℛ_m (Teorema 3)
    se ρ(m | P_lt) > ρ*:
      P_int ← P_int ∪ {m}

  # ── Resultado ──────────────────────────────────────────────────

  retornar P_lt ∪ P_int


função S_m(t_arr):
  # Sinal do inteiro m (Seção 2.1)
  a ← m^{-1/2}
  retornar -½ · log(1 - 2a·cos(t_arr · log m) + a²)
  # Nota: operações são vetorizadas sobre t_arr


função EXTRAIR_PICOS(espectro, h, d_f):
  # Picos locais com altura ≥ h·max e distância mínima d_f
  amp_max ← max(espectro)
  picos ← picos_locais(espectro, altura_min = h · amp_max, dist_min = d_f)
  retornar [round(exp(2π · f_k)) para cada pico k]


função ρ(m, P):
  # Critério de redutibilidade (Seção 2.3)
  para cada b em P:
    se m mod b = 0: retornar 0.0
  # Se nenhum elemento de P divide m, m é irredutível dado P
  retornar 1.0    # valor > ρ* indica aceitação
```

---

## 6. Verificação da implementação

Antes de usar o método para $p$ novos, verifique a implementação com os
casos documentados:

**Caso de referência: $p = 37$**

- $n = 5$, $\mathcal{B} = [16, 36]$
- $\mathcal{P}_< = \{2, 3, 5, 7, 11, 13\}$ (esperado da Etapa 2)
- $\mathcal{P}_{\text{int}} = \{17, 19, 23, 29, 31\}$ (esperado da Etapa 1)
- Resultado completo: $\{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31\}$

**Checklist de sanidade:**

1. $Z_{\mathcal{B}}(t)$ deve ser positivo para todo $t$ (por construção de $S_m$)
2. O espectro de $Z_{\mathcal{B}}$ deve ter picos visíveis em $f_q = \log(q)/(2\pi)$
   para os primos $q \in \mathcal{B}$ — verificar antes de rodar a Etapa 1
3. $\rho(m \mid \mathcal{P}_<) = 0$ para todo composto $m \in \mathcal{B}$ —
   verificar para todos os compostos do caso de referência
4. Após a Etapa 2, $\mathcal{P}_<$ deve conter apenas primos — verificar
   com um teste de primalidade pontual (não é oráculo do método, é checagem
   de implementação)
5. O sinal residual $R(t)$ deve ter amplitude decrescente a cada iteração
   da Etapa 1

**Falsos positivos esperados na Etapa 2:** os compostos $\{4, 8, 9\}$ podem
aparecer como candidatos antes de serem filtrados pelo critério $\rho$ iterativo.
Se aparecerem, verifique que o filtro os rejeita corretamente:
$\rho(4 \mid \{2, 3\}) = 0$, $\rho(8 \mid \{2,3,5,7\}) = 0$,
$\rho(9 \mid \{2,3,5,7\}) = 0$.

---

## 7. Limitações conhecidas e como lidar com elas

**L1 — Primo perdido por resolução insuficiente**

*Causa:* dois primos consecutivos $q_1 < q_2$ com $T_{\max} < 2\pi/(\log q_2 - \log q_1)$
não são separados espectralmente.

*Diagnóstico:* o primo ausente tem sempre um vizinho próximo no bloco.
Calcule $T_{\min}$ para o par mais próximo e verifique se $T_{\max}$ é suficiente.

*Solução:* aumentar $T_{\max}$. O primo 41 (perdido para $p = 53$ com
$T_{\max} = 150$) é recuperado com $T_{\max} = 300$.

**L2 — Custo de $\zeta$**

*Causa:* $\log|\zeta(\tfrac{1}{2}+it)|$ requer biblioteca de precisão e é
$O(t \log t)$ por ponto via algoritmos padrão.

*Mitigação:* calcular uma única vez para a grade $(T_{\min}, T_{\max}, \Delta t)$
e cachear. Para experimentos com múltiplos $p$ no mesmo bloco $n$, o cache
é reutilizado integralmente.

*Nota teórica:* tentativas de substituir $\zeta$ por produtos sobre blocos
finitos foram testadas e mostraram-se inviáveis por obstrução estrutural
(Nota 20, Seção 7). $\zeta$ é o único denominador limpo disponível sem
conhecimento prévio de primos.

**L3 — Parâmetro $\rho^*$ para $p$ grandes**

*Causa:* o gap mínimo entre $\rho$ de primos e compostos do bloco pode
variar com $p$.

*Diagnóstico:* calcular $\rho_{\min} = \min_{q \in \mathcal{B}_{\text{int}}} \rho(q \mid \mathcal{P}_<)$
para o bloco de interesse e verificar que $\rho_{\min} > \rho^*$.

*Solução:* se $\rho_{\min}$ aproximar-se de $\rho^*$, usar
$\rho^* = \rho_{\min}/2$ como margem de segurança.

**L4 — Comportamento para $p$ muito grandes**

O método foi validado para $p \leq 67$ (Notas 17–20) e investigado
empiricamente para $p \leq 499$ (Nota 21). Para $p$ maiores, o comportamento
assintótico do SNR e de $\rho_{\min}$ não está formalmente estabelecido
(ver Conjecturas A5 e A7, Nota 21). Use os resultados experimentais do
bloco de interesse como verificação antes de confiar nos resultados.

---

## 8. Relação com o Teorema 3 e o limite $T \to \infty$

O Teorema 3 (Nota 21) é exato no limite $T_{\max} \to \infty$. Para
$T_{\max}$ finito, o operador $\mathcal{R}_m$ deixa um resíduo de ordem
$O(T_{\max}^{-1})$ nas componentes de $m' \neq m$. As consequências práticas:

- A subtração $R \leftarrow R - S_m$ na Etapa 1 não é perfeitamente limpa:
  há vazamento de amplitude de $m$ para frequências vizinhas, decrescente
  com $T_{\max}$
- Esse vazamento é a causa dos falsos positivos de resolução finita
- Para $T_{\max}$ suficientemente grande (ver Passo de escolha de $T_{\max}$
  na Seção 3), o vazamento é inferior ao limiar $h$ e não gera falsos positivos

Não existe valor universal de $T_{\max}$ — ele depende do par de primos
mais próximo no bloco. O método é correto para qualquer $T_{\max}$ que
satisfaça a condição de separação da Seção 3.

---

## 9. Resumo em uma página

```
CRIVO ESPECTRAL ORACLE-FREE — RESUMO DO MÉTODO

Entrada: primo p
Saída:   todos os primos menores que p

Blocos:
  n ← floor(log2(p))
  B ← [2^{n-1}, p-1]

Sinal:
  S_m(t) = -½ log(1 - 2·m^{-½}·cos(t·log m) + m^{-1})
  Z_B(t) = Σ_{m ∈ B} S_m(t)

ETAPA 2 — obter primos menores que 2^{n-1}:
  1. R2(t) = Z_B(t) - log|ζ(½+it)|
  2. FFT(R2) → picos → candidatos c_1 < c_2 < ...
  3. Aceitar c_i se ρ(c_i | aceitos anteriores) > ρ* = 0.005
  → P_lt = primos aceitos

ETAPA 1 — obter primos do bloco B:
  1. R(t) = Z_B(t)
  2. Loop:
       m ← pico dominante de FFT(R)
       R ← R - S_m(t)
       se ρ(m | P_lt) > ρ*: registrar m como primo
  → P_int = primos do bloco

Resultado: P_lt ∪ P_int

Parâmetros: T_max > 2π/(log q₂ - log q₁) para par mais próximo
            Δt = 0.05,  ρ* = 0.005,  h = 0.03
```

---

## Referências

[Nota 21] T. Bandeira, *Formalização do Crivo Espectral Oracle-Free* (2026)
— contém as provas dos Teoremas 1, 2 e 3 e do Corolário.

[Nota 20] T. Bandeira, *Crivo Espectral sem Oráculo de Primalidade* (2026)
— experimentos de validação e o Lema $\rho$.

[Nota 17] T. Bandeira, *Ferramenta Espectral via $Q(p)$* (2026)
— pipeline original e cache de $\zeta$.

[Nota MDC] T. Bandeira, *Uma caracterização de primalidade via partições
binárias e MDC em intervalos reduzidos* (2026) — Teorema 1 e Corolário
que fundamentam o Lema $\rho$.

[Notebooks] Implementações de referência em Python disponíveis nos repositórios
associados à série: `crivo_sem_oraculo.ipynb`, `crivo_espectral_v2.ipynb`.
