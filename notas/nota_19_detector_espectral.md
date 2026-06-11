# Nota 19 — Detector Espectral de Primalidade: da Razão $R(k)$ à Irredutibilidade Logarítmica

**T. Bandeira · Junho de 2026**  
*Nota adicional à série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

Investigamos três abordagens progressivamente refinadas para detecção espectral do próximo primo a partir de um primo $p$ conhecido, motivadas pela estrutura do extrator $Q(p)$ da Nota 17. A primeira abordagem — razão $R(k) = \log|Z_{Q(p+k)}| - \log|Z_{Q(p)}|$ — falhou por vazamento do sinal do intervalo base, mas produziu como subproduto uma tabela estendida de $t_{\min}$ para pares de primos gêmeos (Exp 1b, `fundamentos_teoricos_v2`), confirmando crescimento $\sim p/\log p$ até $p = 463$ com $t_{\min} = 1451{,}4$. A segunda — regressão linear entre sinais $S_m$ — falhou por ortogonalidade: sinais de frequências distintas são ortogonais sobre $[0, t_{\max}]$. A terceira reformulação, baseada na irredutibilidade de $\log m$ no reticulado gerado por $\{\log p_i\}$, produziu resultados concretos: critério exato com 100% de acurácia (equivalente à definição de primo), resíduo contínuo com 80,1% de separação sem aritmética inteira, e uma correlação negativa inesperada entre resíduo e distância ao primo mais próximo. Esses experimentos revelam uma geometria logarítmica dos primos que conecta diretamente à estrutura do bloco binário de $Q(p)$.

---

## 1. Motivação

A Nota 18 demonstrou que $Q(p)$ é o melhor extrator espectral entre os três testados. Uma questão natural emergiu: dado $p$ primo conhecido, é possível detectar o próximo primo $p'$ usando o mesmo maquinário espectral, sem oráculo externo de primalidade?

A questão tem interesse duplo. Praticamente, seria um detector autônomo. Teoricamente, qualquer critério espectral de primalidade que funcione estabeleceria uma conexão entre a estrutura de $Z_Q$ e a distribuição dos primos — potencialmente mais acessível que abordagens globais via $\zeta$.

Esta nota documenta três tentativas, seus diagnósticos de falha, e o resultado final.

---

## 2. Primeira abordagem: razão $R(k)$

### 2.1 Definição

Para cada candidato $p + k$ com $k = 2, 4, 6, \ldots$, definiu-se:

$$R(k) = \log|Z_{Q(p+k)}(\tfrac{1}{2}+it)| - \log|Z_{Q(p)}(\tfrac{1}{2}+it)|$$

A hipótese era que, se $p+k$ é primo, $R(k)$ exibiria um pico novo irredutível na frequência $f^* = \log(p+k)/(2\pi)$; se $p+k$ é composto, o pico em $f^*$ seria explicável pelos primos já presentes.

### 2.2 Resultados

Para $p \in \{29, 37, 41, 53\}$ com $t_{\max} = 150$, a taxa de acertos do critério foi **57,9%** — marginalmente acima do aleatório. A análise das amplitudes revelou o problema: amplitude média de $R$ na frequência alvo $f^*$ foi 252,6 para primos e 263,1 para compostos — praticamente indistinguíveis. O pico dominante de $R(k)$ estava sistematicamente na frequência do primo base $p$, não do candidato $p+k$.

### 2.3 Diagnóstico

$R(k) = \log|Z_{Q(p+k)}| - \log|Z_{Q(p)}|$ inclui a diferença de dois intervalos de tamanhos diferentes. Quando $p+k$ muda de bloco binário, toda a estrutura de $Z$ muda, não apenas a contribuição de $p+k$. O sinal do candidato fica enterrado no sinal do intervalo base.

### 2.4 Resultado colateral: $t_{\max}$ e gaps

O experimento produziu um resultado útil sobre a Questão 1 da Nota 18. O SNR (amplitude do primo / amplitude do composto na frequência alvo) ficou entre 1,22 e 1,77 para $t_{\max} \in [50, 300]$ — essencialmente estável. Aumentar $t_{\max}$ eleva as amplitudes proporcionalmente mas não melhora a discriminação. A separação é estrutural, não de resolução.

Adicionalmente, o $t_{\min}$ teórico necessário para separar primos gêmeos consecutivos cresce claramente com $p$. A tabela abaixo combina os casos originais com os dados do Exp 1b (`fundamentos_teoricos_v2`), cobrindo a faixa até $p = 463$:

| Par $(p, p')$ | Gap | $t_{\min} = 2\pi/(\log p' - \log p)$ | Status ($t_{\max}=150$) |
|---|---|---|---|
| $(29, 31)$ | 2 | 94,2 | OK |
| $(41, 43)$ | 2 | 131,9 | OK |
| $(59, 61)$ | 2 | 188,5 | **Insuficiente** |
| $(71, 73)$ | 2 | 226,2 | **Insuficiente** |
| $(97, 101)$ | 4 | 155,5 | **Insuficiente** |
| $(107, 109)$ | 2 | 339,3 | **Insuficiente** |
| $(137, 139)$ | 2 | 434,8 | **Insuficiente** |
| $(191, 193)$ | 2 | 607,2 | **Insuficiente** |
| $(239, 241)$ | 2 | 757,7 | **Insuficiente** |
| $(281, 283)$ | 2 | 891,2 | **Insuficiente** |
| $(311, 313)$ | 2 | 986,5 | **Insuficiente** |
| $(419, 421)$ | 2 | 1330,4 | **Insuficiente** |
| $(461, 463)$ | 2 | 1451,4 | **Insuficiente** |

Para gap fixo igual a 2, $t_{\min}$ cresce como $\sim p / \log p$ — confirmando empiricamente a Questão 1 da Nota 18: separação de primos gêmeos requer $t_{\max}$ crescente com $p$. O Exp 1b quantifica essa escala concretamente: para $p \approx 460$, separar o par gêmeo mais próximo já exige $t_{\max} > 1451$, um fator de $\approx 10 \times$ acima do padrão de $t_{\max} = 150$.

---

## 3. Segunda abordagem: regressão de $S_m$ nos fatores

### 3.1 Definição

Isolou-se o sinal de um único inteiro:

$$S_m(t) = -\frac{1}{2}\log\!\left(1 - 2m^{-1/2}\cos(t\log m) + m^{-1}\right)$$

A hipótese era que, para $m$ composto com fatores $p_1, \ldots, p_r$, o sinal $S_m$ seria aproximado por combinação linear $\sum_i c_i S_{p_i}$. Para $m$ primo, o erro de reconstrução seria alto (irredutível).

### 3.2 Resultados

Para $m \in [20, 70]$, os coeficientes da regressão foram todos $\approx 0.00$ — a regressão não encontrou combinação útil. O erro de reconstrução foi $\approx 1.0$ para todo mundo: primos com média 0.9998, compostos com média 0.9976. O limiar ótimo caiu em 1.0000, equivalendo a predizer "composto" para todos — daí os 78.4% de acertos, que é apenas a proporção de compostos na amostra.

### 3.3 Diagnóstico: ortogonalidade

$S_m(t)$ oscila na frequência $f_m = \log(m)/(2\pi)$. O sinal $S_{p_i}(t)$ oscila em $f_{p_i} = \log(p_i)/(2\pi)$. Como $f_m \neq f_{p_i}$ para qualquer $m \neq p_i$, os sinais têm frequências distintas e são aproximadamente ortogonais sobre $[0, t_{\max}]$:

$$\langle S_m, S_{p_i} \rangle \approx 0 \quad \text{para } m \neq p_i$$

A tabela de correlações de Pearson confirmou isso: valores entre $-0.04$ e $0.18$ para todos os pares, com o caso mais expressivo sendo $m = 49 = 7^2$ com correlação 0.18 com $q = 7$ — uma relação harmônica fraca. A regressão linear no espaço dos sinais não pode combinar frequências distintas para reconstruir outra frequência distinta.

### 3.4 A relação correta está no espaço logarítmico

O experimento revelou onde a estrutura real está. Para $m = p \cdot q$:

$$\log m = \log p + \log q \implies f_m = f_p + f_q$$

A frequência espectral de um composto é a **soma** das frequências dos seus fatores. Não é uma combinação linear dos sinais no tempo — é uma relação aditiva nas frequências. A reformulação correta não é no espaço dos sinais $S_m(t)$, mas no espaço dos logaritmos.

---

## 4. Terceira abordagem: irredutibilidade logarítmica

### 4.1 Formulação

Dado $m$ e o conjunto de primos conhecidos $\mathcal{P} = \{p_1, \ldots, p_k\}$ com $p_i < m$, o critério é:

> $m$ é primo $\iff$ $\log m$ não pode ser escrito como $\sum_i e_i \log p_i$ com $e_i \in \mathbb{Z}_{\geq 0}$ e $\sum_i e_i \geq 2$.

Equivalentemente: $m$ é primo $\iff$ $m$ não é divisível por nenhum $p_i \leq \sqrt{m}$ — a irredutibilidade de $\log m$ no reticulado $\mathbb{Z}$-gerado por $\{\log p_i\}$ é idêntica à definição clássica de primo. O valor da reformulação está na **versão contínua** do critério.

### 4.2 Resíduo contínuo

Define-se o resíduo normalizado como a distância mínima de $\log m$ ao reticulado, normalizada por $\log m$:

$$\rho(m) = \frac{\min_{p_i, e_i} \left|\log m - e_i \log p_i\right|}{\log m}$$

onde o mínimo é sobre todos os primos $p_i \leq \sqrt{m}$ e expoentes inteiros $e_i \geq 1$, e também sobre pares $(p_i, p_j)$ via $|\log m - \log p_i - \log p_j|/\log m$.

### 4.3 Resultados

Para $m \in [4, 149]$:

| Grupo | $\rho$ médio | $\rho$ mín | $\rho$ máx |
|-------|-------------|------------|------------|
| Primos | 0.01484 | 0.00162 | 0.11328 |
| Compostos | 0.00343 | 0.00000 | 0.06203 |

O critério exato (divisibilidade) atingiu 100% — trivialmente equivalente à definição. O resíduo contínuo com limiar ótimo $\rho^* = 0.01181$ atingiu **80,1% de acurácia sem aritmética inteira** — apenas medindo distâncias no espaço logarítmico.

A distribuição dos primos é mais espalhada e centrada em valores maiores; a dos compostos está concentrada perto de zero (decomposição exata) com cauda moderada.

### 4.4 O detector guiado não ajuda: resultado honesto

A hipótese era que ordenar candidatos a fator pelo menor $\rho$ aceleraria a busca pelo fator real de compostos. O resultado foi o oposto: o detector guiado usou **12,2% mais testes** em média que a ordem natural. O resíduo contínuo separa primo de composto em média, mas não aponta para qual primo é o fator específico de um composto dado.

Isso faz sentido em retrospecto: $\rho(m)$ mede a proximidade de $\log m$ ao reticulado como um todo, sem privilegiar nenhum gerador específico. O primo com menor resíduo parcial $|\log m - e \cdot \log p|$ não é necessariamente o fator — é apenas o primo cujo múltiplo logarítmico mais se aproxima de $\log m$ de forma contínua.

### 4.5 Resultado inesperado: correlação negativa com distância ao primo

A correlação de Pearson entre $\rho(m)$ e distância de $m$ ao primo mais próximo foi $-0.25$; a correlação de Spearman foi $-0.45$. A relação é **negativa**: compostos *perto* de um primo têm resíduo *maior*.

A interpretação geométrica é direta. Se $m$ está próximo de um primo $p$, então $\log m \approx \log p$ — mas $m \neq p$, logo nenhum divisor de $m$ tem $\log$ que aproxime bem $\log m$ por múltiplo inteiro. O composto $m$ está "encostado" num primo no espaço logarítmico, mas sua fatoração envolve primos menores cujos logs estão longe de $\log m$, resultando em resíduo alto. Já compostos como potências de 2 ($m = 2^k$) têm $\log m = k \log 2$ exatamente — resíduo zero e distância típica moderada ao primo mais próximo.

Essa correlação negativa revela que $\rho(m)$ mede a vizinhança de primos na reta, não a fatoração interna — são duas geometrias distintas que coincidem no critério exato mas divergem no contínuo.

---

## 5. Conexão com o pipeline de $Q(p)$

Os três experimentos, vistos em conjunto, iluminam por que o pipeline de $Q(p)$ funciona.

A Etapa 1 do extrator $Q(p)$ isola os primos do bloco $[2^{n-1}, p-1]$ subtraindo os compostos. Ela funciona porque, pelo Teorema 1 da Nota sobre blocos binários, todo composto $m \in [2^n, 2^{n+1}-1]$ tem todos os seus fatores primos em $[2^{n-1}, 2^n-1]$. Traduzido para a linguagem desta nota: a frequência $f_m = \log(m)/(2\pi)$ de todo composto do bloco é **redutível** — é soma de frequências de primos que já estão no bloco anterior. Os primos do bloco, por outro lado, têm frequências irredutíveis — não são somas de frequências menores.

O pipeline espectral está, portanto, implementando implicitamente o critério de irredutibilidade logarítmica: a FFT detecta as frequências irredutíveis como picos não explicáveis pelos outros picos presentes. A diferença entre o extrator $Q(p)$ e o detector desta nota é que $Q(p)$ opera no domínio do produto (via $Z_Q$) enquanto o detector opera diretamente no espaço dos logaritmos — mas ambos exploram a mesma estrutura fundamental.

---

## 6. Questões abertas

**Questão 1 — Crescimento do resíduo contínuo com $p$** *(com evidência adicional).*
Os dados mostram resíduo médio dos primos em 0.01484 para $m \in [4, 149]$. A tabela estendida de $t_{\min}$ (Seção 2.4, Exp 1b) fornece evidência indireta: $t_{\min}$ cresce como $\sim p/\log p$ para pares gêmeos, implicando que a separabilidade espectral *entre dois primos consecutivos* exige recursos crescentes. O resíduo $\rho(p)$ no espaço logarítmico e o $t_{\min}$ espectral medem estruturas complementares da mesma geometria — um no espaço dos logs, outro no tempo de observação. A questão precisa — se $\rho(p) \to \infty$ ou estabiliza — permanece em aberto, mas os dados do Exp 4b (Nota 20) mostram que $\rho_{\min}$ dos primos do bloco *decai* com $p$, sugerindo que primos grandes são logaritmicamente mais próximos do reticulado dos primos menores, não mais distantes.

**Questão 2 — Separabilidade assintótica.**
Com 80,1% de acurácia em $[4, 149]$, o resíduo contínuo já é informativo sem aritmética inteira. Essa acurácia cresce, decresce ou estabiliza em faixas maiores? A sobreposição entre as distribuições de $\rho$ para primos e compostos diminui com $m$?

**Questão 3 — Interpretação da correlação negativa.**
A correlação $\rho \times \text{dist\_primo} = -0.45$ (Spearman) é robusta. Existe uma formulação precisa: para compostos $m$ com primo mais próximo $p^*$, $\rho(m)$ é uma função monótona de $|m - p^*|/\log m$? Isso conectaria a geometria logarítmica dos primos à distribuição de gaps.

**Questão 4 — Reticulado logarítmico e crivo espectral.**
O crivo de Eratóstenes pode ser reformulado como construção incremental do reticulado $L_n = \mathbb{Z}_{\geq 0}\text{-span}\{\log p_1, \ldots, \log p_n\}$: a cada passo, $m$ é primo se e somente se $\log m \notin L_{n}$ para todo $p_n \leq \sqrt{m}$. Existe uma versão espectral desse crivo — um operador que, a partir de $Z_{Q(p)}$, produz $Z_{Q(p')}$ onde $p'$ é o próximo primo, usando apenas propriedades de $Z$ sem divisibilidade explícita?

---

## 7. Conclusão

Os três experimentos estabelecem uma progressão clara. A abordagem por razão $R(k)$ falhou por vazamento do intervalo base, mas produziu evidência empírica de que $t_{\max} \sim O(p)$ para primos gêmeos. A abordagem por regressão de sinais falhou por ortogonalidade, mas revelou que a relação entre $S_m$ e $S_{p_i}$ não é linear no tempo — é aditiva nas frequências. A abordagem por irredutibilidade logarítmica conectou as duas falhas numa formulação coerente e produziu 80,1% de separação sem aritmética inteira.

O resultado mais rico não é a taxa de acerto, mas a correlação negativa entre $\rho(m)$ e proximidade de primo: ela mostra que o resíduo contínuo captura a topologia dos primos na reta, não sua fatoração. São duas estruturas distintas — multiplicativa e aditiva — que coincidem no critério exato e divergem no contínuo. Essa divergência é, em si, informativa sobre a natureza dos primos.

---

## Referências

[Nota 17] T. Bandeira, *Ferramenta Espectral via $Q(p)$: Fundamentação e Validação Computacional*, nota adicional (2026).  
[Nota 18] T. Bandeira, *Benchmark Espectral: Primorial, Fatorial e $Q(p)$ como Bases para Extração de Primos*, nota adicional (2026).  
[Nota 20] T. Bandeira, *Crivo Espectral sem Oráculo de Primalidade*, nota adicional (2026).  
[Nota 1] T. Bandeira, *Uma caracterização de primalidade via partições binárias e MDC em intervalos reduzidos*, nota standalone (2026).  
[Exp 1b] T. Bandeira, `fundamentos_teoricos_v2.ipynb` — $t_{\min}$ para pares de primos gêmeos até $p = 463$, Junho de 2026.