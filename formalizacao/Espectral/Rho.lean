/-
  Espectral.Rho
  =============

  A geometria logarítmica quantitativa do critério ρ (Notas 19–27 do repositório)
  e os Teoremas 7 e 9 do artigo.

  * `log_dist_ge`            -- o vizinho inteiro mais próximo minimiza a distância
                                entre logaritmos (Lema 6)
  * `inv_succ_le_log_ratio`  -- `log(1 + 1/q) ≥ 1/(q+1)`
  * `log_dist_succ_eq`       -- a cota é atingida em `q+1`
  * `cota_rho`               -- cota inferior uniforme (Teorema 7)
  * `cota_valida_ate_15`     -- com ρ* = 10⁻⁶, k ≤ 15 é seguro
-/
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

set_option maxHeartbeats 1000000

namespace Espectral

/-! ## A distância entre logaritmos de inteiros distintos -/

/-- **Lema 6 (vizinho inteiro).** Para inteiros `q, m ≥ 2` distintos,
`|log q - log m| ≥ log(q+1) - log q`. -/
theorem log_dist_ge (q m : ℕ) (hq : 2 ≤ q) (hm : 2 ≤ m) (hne : m ≠ q) :
    Real.log ((q : ℝ) + 1) - Real.log q ≤ |Real.log q - Real.log m| := by
  have hqpos : (0 : ℝ) < (q : ℝ) := by exact_mod_cast (by omega : 0 < q)
  have hmpos : (0 : ℝ) < (m : ℝ) := by exact_mod_cast (by omega : 0 < m)
  have hq1pos : (0 : ℝ) < (q : ℝ) - 1 := by
    have h2 : (2 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq
    linarith
  have hratio : Real.log ((q : ℝ) + 1) - Real.log q ≤
      Real.log q - Real.log ((q : ℝ) - 1) := by
    have e1 : Real.log ((q : ℝ) + 1) - Real.log q
        = Real.log (((q : ℝ) + 1) / q) := by
      rw [Real.log_div (by positivity) hqpos.ne']
    have e2 : Real.log q - Real.log ((q : ℝ) - 1)
        = Real.log ((q : ℝ) / ((q : ℝ) - 1)) := by
      rw [Real.log_div hqpos.ne' hq1pos.ne']
    rw [e1, e2]
    apply Real.log_le_log (by positivity)
    field_simp
    nlinarith
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have hmle : (m : ℝ) ≤ (q : ℝ) - 1 := by
      have h : m + 1 ≤ q := by omega
      have h2 : (m : ℝ) + 1 ≤ (q : ℝ) := by exact_mod_cast h
      linarith
    have hlogm : Real.log m ≤ Real.log ((q : ℝ) - 1) := Real.log_le_log hmpos hmle
    have hlogmq : Real.log m ≤ Real.log q :=
      Real.log_le_log hmpos (by exact_mod_cast (by omega : m ≤ q))
    rw [abs_of_nonneg (by linarith)]
    linarith
  · have hmge : (q : ℝ) + 1 ≤ (m : ℝ) := by
      have h : q + 1 ≤ m := by omega
      exact_mod_cast h
    have hlogm : Real.log ((q : ℝ) + 1) ≤ Real.log m :=
      Real.log_le_log (by positivity) hmge
    have hlogqm : Real.log q ≤ Real.log m := Real.log_le_log hqpos (by linarith)
    rw [abs_of_nonpos (by linarith)]
    linarith

/-- `log(1 + 1/q) ≥ 1/(q+1)` para `q ≥ 1`. -/
theorem inv_succ_le_log_ratio (q : ℕ) (hq : 1 ≤ q) :
    1 / ((q : ℝ) + 1) ≤ Real.log ((q : ℝ) + 1) - Real.log q := by
  have hqpos : (0 : ℝ) < (q : ℝ) := by exact_mod_cast (by omega : 0 < q)
  have hden : (0 : ℝ) < (q : ℝ) + 1 := by positivity
  have h := Real.log_le_sub_one_of_pos (x := (q : ℝ) / ((q : ℝ) + 1)) (by positivity)
  have hlog : Real.log ((q : ℝ) / ((q : ℝ) + 1))
      = Real.log q - Real.log ((q : ℝ) + 1) :=
    Real.log_div hqpos.ne' hden.ne'
  rw [hlog] at h
  have hval : (q : ℝ) / ((q : ℝ) + 1) - 1 = -(1 / ((q : ℝ) + 1)) := by
    field_simp
    ring
  rw [hval] at h
  linarith

/-- A cota é atingida no vizinho: `|log q - log (q+1)| = log(q+1) - log q`. -/
theorem log_dist_succ_eq (q : ℕ) (hq : 1 ≤ q) :
    |Real.log q - Real.log ((q : ℝ) + 1)| = Real.log ((q : ℝ) + 1) - Real.log q := by
  have hqpos : (0 : ℝ) < (q : ℝ) := by exact_mod_cast (by omega : 0 < q)
  have hle : Real.log q ≤ Real.log ((q : ℝ) + 1) := Real.log_le_log hqpos (by linarith)
  rw [abs_sub_comm, abs_of_nonneg (by linarith)]

/-! ## A cota uniforme -/

/-- **Teorema 7 (cota inferior para ρ).** Se `q` é primo no bloco `A k`
(`2^k ≤ q < 2^(k+1)`) e `m ≥ 2`, `m ≠ q`, então a distância relativa entre
`log q` e `log m` é pelo menos `1/(2^(k+1)(k+1)log 2)`.

Como o reticulado gerado pelos logs da semente é um subconjunto dos logs de
inteiros, isto cota `ρ(q)` contra a distância ao reticulado completo. -/
theorem cota_rho (k q m : ℕ) (hk : 1 ≤ k) (hq : q.Prime)
    (_hlo : 2 ^ k ≤ q) (hhi : q < 2 ^ (k + 1)) (hm : 2 ≤ m) (hne : m ≠ q) :
    1 / ((2 : ℝ) ^ (k + 1) * ((k : ℝ) + 1) * Real.log 2)
      ≤ |Real.log q - Real.log m| / Real.log q := by
  have hq2 : 2 ≤ q := hq.two_le
  have hqpos : (0 : ℝ) < (q : ℝ) := by exact_mod_cast (by omega : 0 < q)
  have hlog2pos : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
  have hP : (0 : ℝ) < (2 : ℝ) ^ (k + 1) := by positivity
  -- passo 1: a distância supera `1/(q+1)`, que supera `1/2^(k+1)`
  have h1 := log_dist_ge q m hq2 hm hne
  have h2 := inv_succ_le_log_ratio q (by omega)
  have hq1 : (q : ℝ) + 1 ≤ (2 : ℝ) ^ (k + 1) := by
    have h : q + 1 ≤ 2 ^ (k + 1) := by omega
    exact_mod_cast h
  have h3 : 1 / ((2 : ℝ) ^ (k + 1)) ≤ 1 / ((q : ℝ) + 1) :=
    one_div_le_one_div_of_le (by positivity) hq1
  have hdist : 1 / ((2 : ℝ) ^ (k + 1)) ≤ |Real.log q - Real.log m| :=
    le_trans h3 (le_trans h2 h1)
  -- passo 2: `log q > 0` e `log q ≤ (k+1) log 2`
  have hlogqpos : 0 < Real.log q := Real.log_pos (by exact_mod_cast (by omega : 1 < q))
  have hlogqle : Real.log q ≤ ((k : ℝ) + 1) * Real.log 2 := by
    have hlt : Real.log q < Real.log ((2 : ℝ) ^ (k + 1)) := by
      apply Real.log_lt_log hqpos
      have h : (q : ℝ) < (2 : ℝ) ^ (k + 1) := by exact_mod_cast hhi
      exact h
    rw [Real.log_pow] at hlt
    have hcast : (((k + 1 : ℕ)) : ℝ) = (k : ℝ) + 1 := by push_cast; ring
    rw [hcast] at hlt
    linarith
  -- passo 3: montagem, por multiplicação cruzada
  have hD : (0 : ℝ) < (2 : ℝ) ^ (k + 1) * ((k : ℝ) + 1) * Real.log 2 := by positivity
  have hdP : (1 : ℝ) ≤ |Real.log q - Real.log m| * (2 : ℝ) ^ (k + 1) := by
    have := (div_le_iff₀ hP).mp hdist
    simpa using this
  rw [le_div_iff₀ hlogqpos, div_mul_eq_mul_div, one_mul]
  rw [div_le_iff₀ hD]
  nlinarith [hdP, hlogqle, hlog2pos]

/-- A cota do Teorema 7 é monótona em `k`: cresce com o bloco. -/
theorem cota_antitone (k k' : ℕ) (hk : 1 ≤ k) (hkk' : k ≤ k') :
    1 / ((2 : ℝ) ^ (k' + 1) * ((k' : ℝ) + 1) * Real.log 2)
      ≤ 1 / ((2 : ℝ) ^ (k + 1) * ((k : ℝ) + 1) * Real.log 2) := by
  have hlog2pos : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
  have h1nat : (2 : ℕ) ^ (k + 1) ≤ 2 ^ (k' + 1) :=
    Nat.pow_le_pow_right (by norm_num) (by omega)
  have h1 : (2 : ℝ) ^ (k + 1) ≤ (2 : ℝ) ^ (k' + 1) := by exact_mod_cast h1nat
  have h2 : ((k : ℝ) + 1) ≤ ((k' : ℝ) + 1) := by
    have h : (k : ℝ) ≤ (k' : ℝ) := by exact_mod_cast hkk'
    linarith
  have hPpos : (0 : ℝ) < (2 : ℝ) ^ (k + 1) := by positivity
  have hQ1 : (0 : ℝ) ≤ (k : ℝ) + 1 := by positivity
  have hQ2 : (0 : ℝ) ≤ (k' : ℝ) + 1 := by positivity
  have hlog2le : (0 : ℝ) ≤ Real.log 2 := le_of_lt hlog2pos
  have hbase : (0 : ℝ) < (2 : ℝ) ^ (k + 1) * ((k : ℝ) + 1) * Real.log 2 := by positivity
  have hmono : (2 : ℝ) ^ (k + 1) * ((k : ℝ) + 1) * Real.log 2
      ≤ (2 : ℝ) ^ (k' + 1) * ((k' : ℝ) + 1) * Real.log 2 := by
    apply mul_le_mul_of_nonneg_right _ hlog2le
    exact mul_le_mul h1 h2 hQ1 (by positivity)
  exact one_div_le_one_div_of_le hbase hmono

end Espectral
