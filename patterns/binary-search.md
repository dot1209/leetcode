# Binary Search on Answer

## When to Use

不是搜尋陣列位置，而是像「用二分搜來搜可能的 cost」一樣，直接搜尋答案的數值。

- 題目要求最小可行容量、速度、上限，或最大可行下限。
- 直接找最佳解很難，但給定一個限制後，能有效判斷「可不可以」。
- 可行性具有單調性：限制放寬後，原本合法的方案依然合法。
- 先設計判定函式與證明，再套二分搜尋；`feasible` 不一定靠 greedy，也可能靠 DP、計數或其他演算法。

## Typical Complexity

**Time:** O(Tcheck · log(W + 1)) — 每輪執行一次判定，搜尋寬度約減半；`W = r - l` 是答案值域的初始寬度，不是輸入長度。初始化成本另計。

**Space:** O(Scheck) — 二分搜尋自身只用 O(1) 空間，整題空間由判定函式決定。

## Template Code

搜尋第一個可行整數。前提是所有小於初始 l 的值都不可行，初始 r 已知可行，且數值差可由選用型別表示。

`[l, r)` 是尚待搜尋的值；r 保留為已知可行的邊界。最佳答案可以等於 r，所以不能寫成「答案永遠在 `[l, r)`」。

```cpp
template <class Predicate>
long long firstFeasible(long long l, long long r, Predicate feasible) {
    // Search unresolved values in [l, r).
    // Values below l are infeasible; r is feasible.
    while (l < r) {
        long long mid = l + (r - l) / 2;
        if (feasible(mid)) {
            r = mid;
        } else {
            l = mid + 1;
        }
    }
    return r;
}
```

## 判定函式與搜尋本身要分開證明

證明分成兩件事：`feasible(cap)` 是否真的等價於存在合法方案，以及其真假是否隨 cap 單調變化。Greedy 的正確性與二分搜尋的單調性不是同一個證明；有負數等條件變更時，判定方法可能失效，而可行性的單調性仍然成立。

若某個方案在 cap 下可行，同一個方案在更大的 cap 下仍可行。因此小的值不可行、大的值可行，存在一個由不可行轉為可行的邊界。

## 半開搜尋區間的更新與收斂

| 判定結果 | 更新 | 原因 |
|---|---|---|
| `feasible(mid)` 為真 | `r = mid` | 保留這個可行邊界，繼續尋找更小的可行值。 |
| `feasible(mid)` 為假 | `l = mid + 1` | 單調性保證 mid 與更小的值都不可行。 |

`l < r` 時，向下取整的 mid 滿足 `l <= mid < r`，兩種更新都讓區間縮小。最後 `l == r`：該值可行，而所有更小值都不可行，因此是第一個可行值。

初始右界可以直接是已知可行值，也可以是搜尋值域之外的可行 sentinel。`sum + 1` 是一種初始化選擇，並非這個模板一律要求加一。

## Pitfalls

- 沒有證明判定函式，就以為外層二分搜尋能修正錯誤判定。
- 把二分次數寫成 `log n`；這裡搜尋的是答案值域，不能直接寫 O(n log n)。
- 忘記初始 r 必須可行，或沒有處理根本不存在可行值的情況。
- 把右界排除於尚待搜尋的區間，就誤認為答案不能等於右界。
- 型別只放大邊界，卻忘記判定中的加總、乘法也可能溢位。
- 改成最大化最小值時，要重新確認可行性的方向，不能照抄最小上限的更新規則。

---

## Problems

### [[410] Split Array Largest Sum](../problems/binary-search/split_array_largest_sum.md)

**Complexity:** Time O(n log(S - M + 2)), Space O(1)

- **Trigger:** 非負陣列切成剛好 k 個連續非空組，最小化最大組的總和；固定 cost 後可用線性 greedy 判定。
- **Insight:** 「用二分搜來搜可能的 cost」；每組能放就繼續放，超過 cap 才切，得到最少組數，再以 `groups <= k` 判定。
- **Pitfall:** groups 不等於切刀數；下界用最大元素，並區分半開區間中尚待搜尋的值與可行右界；S 是總和、M 是最大元素。
