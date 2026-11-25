#!/usr/bin/env python3
"""
verificar_teoremas.py -- Auditoria numerica das afirmacoes matematicas do repo.

Verifica, para blocos binarios A_k = [2^k, 2^(k+1)-1]:

  V1  Lema do bloco: todo composto m em A_k tem fator primo < 2^k.
  V2  rho_min(k) = log(1 + 1/q_max)/log(q_max)  [Teorema 3 do artigo]
      comparando com a distancia ao reticulado COMPLETO (numeros S_k-suaves).
  V3  O expoente e*(p,k) = floor(k log2 / log p) da Nota 26 e insuficiente
      (contra-exemplos) e e*(p,k) = floor((k+1) log2 / log p) e suficiente.
  V4  rho_impl (singles + pares, como implementado) coincide com rho_full.
  V5  Algoritmo final (Nota 29) extrai exatamente os primos < p.

Saida: relatorio em texto + verificacao_teoremas.json
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
LOG2 = math.log(2.0)


# ---------------------------------------------------------------- utilidades
def sieve(n: int) -> np.ndarray:
    """Crivo booleano: True sse i e primo, para i <= n."""
    if n < 2:
        return np.zeros(n + 1, dtype=bool)
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i :: i] = False
    return s


def smallest_prime_factor(n: int) -> np.ndarray:
    """spf[i] = menor fator primo de i (spf[1] = 1)."""
    spf = np.arange(n + 1, dtype=np.int64)
    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:  # i primo
            segment = spf[i * i :: i]
            segment[segment == np.arange(i * i, n + 1, i)] = i
    return spf


def largest_prime_factor_table(n: int, spf: np.ndarray) -> np.ndarray:
    """lpf[i] = maior fator primo de i (lpf[1] = 1)."""
    lpf = np.ones(n + 1, dtype=np.int64)
    for i in range(2, n + 1):
        p = spf[i]
        rest = i // p
        lpf[i] = max(int(p), int(lpf[rest]))
    return lpf


def block(k: int) -> range:
    return range(2**k, 2 ** (k + 1))


# ---------------------------------------------------------------- V1
def V1_lema_bloco(ks) -> dict:
    rows = []
    ok = True
    for k in ks:
        n = 2 ** (k + 1) - 1
        spf = smallest_prime_factor(n)
        primos = set(np.nonzero(sieve(n))[0].tolist())
        ruins = []
        for m in block(k):
            if m in primos:
                continue
            q = int(spf[m])
            if not (q < 2**k and m % q == 0):
                ruins.append(m)
        ok &= not ruins
        rows.append({"k": k, "compostos": len(block(k)) - len([m for m in block(k) if m in primos]),
                     "violacoes": ruins[:5]})
    return {"ok": ok, "rows": rows}


# ---------------------------------------------------------------- V2
def V2_rho_min(ks, kmax_full=20) -> dict:
    """rho_min(k) exato contra o reticulado completo (S_k-suaves)."""
    rows = []
    ok_at_max = True
    ok_formula = True
    for k in ks:
        n = 2 ** (k + 1)  # limite superior; q+1 <= 2^(k+1)
        spf = smallest_prime_factor(n)
        lpf = largest_prime_factor_table(n, spf)
        is_prime = sieve(n)
        limite_base = 2**k
        primos = [q for q in block(k) if is_prime[q]]
        # indices dos numeros S_k-suaves (todos os fatores primos < 2^k)
        suaves = np.array([m for m in range(2, n + 1) if lpf[m] < limite_base],
                          dtype=np.int64)
        log_suaves = np.log(suaves.astype(float))
        melhor_q, melhor_valor = None, None
        detalhe = {}
        for q in primos:
            d = np.abs(log_suaves - math.log(q)) / math.log(q)
            d[suaves == q] = np.inf  # excluir o proprio q (nao ocorre: q nao e S_k-suave)
            i = int(np.argmin(d))
            val = float(d[i])
            detalhe[q] = (val, int(suaves[i]))
            if melhor_valor is None or val < melhor_valor:
                melhor_q, melhor_valor = q, val
        qmax = max(primos)
        formula = math.log1p(1.0 / qmax) / math.log(qmax)
        # distancia ao inteiro mais proximo (cota inferior universal)
        vizinho = min(math.log(qmax / (qmax - 1)), math.log((qmax + 1) / qmax)) / math.log(qmax)
        at_max = (melhor_q == qmax)
        ok_at_max &= at_max
        ok_formula &= abs(melhor_valor - formula) < 1e-12 and abs(formula - vizinho) < 1e-12
        rows.append({
            "k": k,
            "q_max": qmax,
            "argmin": melhor_q,
            "rho_min_medido": melhor_valor,
            "rho(q_max)": formula,
            "1/(q_max log q_max)": 1.0 / (qmax * math.log(qmax)),
            "cota_2^k": 1.0 / (2 ** (k + 1) * (k + 1) * LOG2),
            "razao_cota": melhor_valor / (1.0 / (2 ** (k + 1) * (k + 1) * LOG2)),
            "vizinho_mais_proximo": int(detalhe[qmax][1]),
        })
    return {"ok": ok_at_max and ok_formula, "ok_argmin_qmax": ok_at_max,
            "ok_formula_exata": ok_formula, "rows": rows}


# ---------------------------------------------------------------- V3
def rho_singles_cobertura(k: int, expoente: str):
    """Testa se a busca de potencias simples com teto e* cobre todo composto de A_k."""
    n = 2 ** (k + 1) - 1
    spf = smallest_prime_factor(n)
    is_prime = sieve(n)
    base = [p for p in range(2, 2**k) if is_prime[p]]
    escapados = []
    for m in block(k):
        if is_prime[m]:
            continue
        coberto = False
        for p in base:
            if expoente == "nota26":
                e_star = int(math.floor(k * LOG2 / math.log(p)))
            else:  # corrigido
                e_star = int(math.floor((k + 1) * LOG2 / math.log(p)))
            if e_star < 1:
                continue
            # existe e <= e* com p^e | m ?
            pe = p
            e = 1
            while e <= e_star and pe <= m:
                if m % pe == 0:
                    coberto = True
                    break
                e += 1
                pe *= p
            if coberto:
                break
        if not coberto:
            escapados.append((m, int(spf[m])))
    return escapados


def V3_expoente(ks) -> dict:
    rows = []
    for k in ks:
        a = rho_singles_cobertura(k, "nota26")
        b = rho_singles_cobertura(k, "corrigido")
        rows.append({
            "k": k,
            "escapados_nota26": a[:6],
            "n_escapados_nota26": len(a),
            "escapados_corrigido": b[:6],
            "n_escapados_corrigido": len(b),
        })
    return {"ok": all(r["n_escapados_corrigido"] == 0 for r in rows), "rows": rows}


# ---------------------------------------------------------------- V4
def rho_singles_pares(m: int, base, k: int):
    """rho como implementado nas Notas 26-27: singles + pares com e <= e*(p,k)."""
    lm = math.log(m)
    melhor = math.inf
    e_star = {p: int(math.floor((k + 1) * LOG2 / math.log(p))) for p in base}
    for p in base:
        for e in range(1, e_star[p] + 1):
            melhor = min(melhor, abs(lm - e * math.log(p)))
    for i, p1 in enumerate(base):
        for p2 in base[i:]:
            for e1 in range(1, e_star[p1] + 1):
                l1 = e1 * math.log(p1)
                if l1 >= lm:
                    break
                for e2 in range(1, e_star[p2] + 1):
                    val = abs(lm - l1 - e2 * math.log(p2))
                    if val < melhor:
                        melhor = val
    return melhor / lm


def V4_impl_vs_full(ks) -> dict:
    rows = []
    ok = True
    for k in ks:
        n = 2 ** (k + 1)
        spf = smallest_prime_factor(n)
        lpf = largest_prime_factor_table(n, spf)
        is_prime = sieve(n)
        base = [p for p in range(2, 2**k) if is_prime[p]]
        primos = [q for q in block(k) if is_prime[q]]
        difs = []
        for q in primos:
            full = math.log1p(1.0 / q) / math.log(q)  # vizinho q+1 e q-1 suaves? nao em geral
            # valor "full" real: distancia ao suave mais proximo
            suaves = [m for m in range(2, n + 1) if lpf[m] < 2**k and m != q]
            full = min(abs(math.log(q) - math.log(m)) for m in suaves) / math.log(q)
            impl = rho_singles_pares(q, base, k)
            difs.append((q, full, impl, abs(full - impl)))
        pior = max(difs, key=lambda t: t[3])
        ok &= pior[3] < 1e-9
        rows.append({"k": k, "pior_q": pior[0], "full": pior[1], "impl": pior[2],
                     "max_abs_dif": pior[3]})
    return {"ok": ok, "rows": rows}


# ---------------------------------------------------------------- V5
def extrair_primos(p: int):
    """Algoritmo final da Nota 29, sem isprime, sem zeta, sem FFT."""
    n = int(math.floor(math.log(p, 2)))
    P_less = []
    for m in range(2, 2 ** (n - 1)):
        primo = True
        for b in P_less:
            if b * b > m:
                break
            if m % b == 0:
                primo = False
                break
        if primo:
            P_less.append(m)
    do_bloco = []
    for m in range(2 ** (n - 1), p):
        primo = True
        for b in P_less:
            if b * b > m:
                break
            if m % b == 0:
                primo = False
                break
        if primo:
            do_bloco.append(m)
    return P_less + do_bloco


def V5_algoritmo(ps) -> dict:
    rows = []
    ok = True
    for p in ps:
        got = extrair_primos(p)
        is_prime = sieve(p)
        want = [q for q in range(2, p) if is_prime[q]]
        ok &= got == want
        rows.append({"p": p, "n": int(math.floor(math.log(p, 2))),
                     "primos": len(want), "detectados": len(got), "exato": got == want})
    return {"ok": ok, "rows": rows}


# ---------------------------------------------------------------- main
def main():
    rel = {}

    print("V1  Lema do bloco binario ...", flush=True)
    rel["V1"] = V1_lema_bloco(range(2, 19))
    print("    ok =", rel["V1"]["ok"], flush=True)

    print("V2  rho_min(k) exato ...", flush=True)
    rel["V2"] = V2_rho_min(range(2, 19))
    print("    ok =", rel["V2"]["ok"], flush=True)

    print("V3  expoente adaptativo e* ...", flush=True)
    rel["V3"] = V3_expoente(range(2, 15))
    print("    ok (versao corrigida) =", rel["V3"]["ok"], flush=True)

    print("V4  rho implementado vs reticulado completo ...", flush=True)
    rel["V4"] = V4_impl_vs_full(range(2, 13))
    print("    ok =", rel["V4"]["ok"], flush=True)

    print("V5  algoritmo final ...", flush=True)
    rel["V5"] = V5_algoritmo([37, 67, 131, 257, 503, 1009, 2003, 4001, 8009, 16381])
    print("    ok =", rel["V5"]["ok"], flush=True)

    with open(OUT / "verificacao_teoremas.json", "w", encoding="utf-8") as f:
        json.dump(rel, f, indent=1, ensure_ascii=False, default=float)

    # ------------------------------------------------------------- relatorio
    L = []
    L.append("# Relatorio de verificacao dos teoremas\n")
    L.append("\n## V1 - Lema do bloco (todo composto em A_k tem fator primo < 2^k)\n")
    L.append(f"**Veredito: {'CONFIRMADO' if rel['V1']['ok'] else 'REFUTADO'}** "
             f"(k = 2..18)\n")
    L.append("\n## V2 - rho_min(k) = log(1+1/q_max)/log(q_max)\n")
    L.append(f"\n`q_max` realiza o minimo: {rel['V2']['ok_argmin_qmax']}; "
             f"formula exata: {rel['V2']['ok_formula_exata']}\n\n")
    L.append("| k | q_max | argmin | rho_min medido | rho(q_max) | 1/(q_max log q_max) | cota 2^k | razao |\n")
    L.append("|---:|---:|---:|---:|---:|---:|---:|---:|\n")
    for r in rel["V2"]["rows"]:
        L.append("| {k} | {q_max} | {argmin} | {rho_min_medido:.4e} | {rho(q_max):.4e} | "
                 "{1/(q_max log q_max):.4e} | {cota_2^k:.4e} | {razao_cota:.6f} |\n".format(**r))
    L.append("\n## V3 - Expoente adaptativo e*(p,k)\n")
    L.append("\n| k | escapados com e* = floor(k log2/log p) | escapados com e* = floor((k+1)log2/log p) |\n")
    L.append("|---:|---|---|\n")
    for r in rel["V3"]["rows"]:
        L.append(f"| {r['k']} | {r['n_escapados_nota26']} {r['escapados_nota26']} | "
                 f"{r['n_escapados_corrigido']} {r['escapados_corrigido']} |\n")
    L.append("\n## V4 - rho implementado (singles+pares) vs reticulado completo\n")
    L.append(f"**Veredito: {'IDENTICOS' if rel['V4']['ok'] else 'DIVERGEM'}**\n\n")
    L.append("| k | pior q | rho_full | rho_impl | max dif |\n|---:|---:|---:|---:|---:|\n")
    for r in rel["V4"]["rows"]:
        L.append("| {k} | {pior_q} | {full:.4e} | {impl:.4e} | {max_abs_dif:.2e} |\n".format(**r))
    L.append("\n## V5 - Algoritmo final (Nota 29)\n")
    L.append(f"**Veredito: {'CONFIRMADO' if rel['V5']['ok'] else 'REFUTADO'}**\n\n")
    L.append("| p | n | primos reais | detectados | exato |\n|---:|---:|---:|---:|---|\n")
    for r in rel["V5"]["rows"]:
        L.append("| {p} | {n} | {primos} | {detectados} | {exato} |\n".format(**r))

    txt = "".join(L)
    with open(OUT / "verificacao_teoremas.md", "w", encoding="utf-8") as f:
        f.write(txt)
    print("\n" + txt)
    print("\nRelatorio salvo em", OUT)


if __name__ == "__main__":
    sys.exit(main())
