# Monotonic Stack

Monotonic Stack 是用一個數值單調的 stack 存住**還在等答案的元素**，等第一個打破單調性的新元素出現時一次結算它們。它存在的理由是：很多題目要對每個元素問「右邊第一個比我大／小的在哪」，暴力是 O(n²)，但這些查詢高度重疊——如果 `a` 被後來的 `b` 擋住，那 `a` 對更右邊的元素就永遠不可能是答案，可以直接丟掉。Stack 就是「還沒被擋住的候選清單」，單調性只是這條丟棄規則的副產物。

真正的心法是 **pop 的那一刻就是答案定案的那一刻**。不要想「走到 `i` 時，用 stack 算出 `res[i]`」，要反過來想「`i` 把 `j` 彈掉了，所以 `j` 的答案現在確定了」。答案寫進 `res[j]`，對齊自然成立，不需要事後配對——一旦拖到迴圈外再想回頭配對，`(j, i)` 這組對應關係已經不存在了。

## When to Use
- 對每個元素問「左／右第一個比它大（小）的元素是誰／在哪／差多遠」→ next greater / next smaller
- 需要「以某元素為極值，所能延伸的最大區間」→ 邊界 + 寬度類（柱狀圖矩形、子陣列貢獻）
- 訊號詞：`next greater element`、`next smaller`、`daily temperatures`、「要等幾天」、「下一個更便宜的」、`largest rectangle`、「以 X 為最小值的所有子陣列」
- 暴力寫法長成「對每個 `i` 往右掃找第一個滿足條件的 `j`」→ 幾乎必定可以攤平成 monotonic stack

反例（不要誤用）：
- 要**建構字典序最佳的輸出序列** → 是 [Greedy + Stack](greedy-stack.md)，多一層 flush 決策與守門條件
- **固定長度視窗**內取極值 → 是 monotonic **deque**（LC 239），因為左端也要淘汰
- 可以自由重排、沒有「第一個」這種方向性 → 直接 sort 或 heap

## Typical Complexity
**Time:** O(n) — 主迴圈內雖然有巢狀 `while`，但每個 index 一生只被 push 一次、pop 一次，所以 `while` 的**總**執行次數 ≤ n，是攤還 O(n) 不是 O(n²)。這跟 two pointers、greedy + stack 是同一種攤還論證。
**Space:** O(n) — stack 最壞存下全部元素（輸入嚴格遞增時完全不 pop）。若答案是逐位置的陣列，輸出另計 O(n)。

## Template Code
```cpp
// The stack holds INDICES of elements still waiting for their answer.
// Invariant: values in the stack are monotonic from bottom to top.
vector<int> st;
for (int i = 0; i < n; i++) {
    while (!st.empty() && breaks_monotonicity(a[i], a[st.back()])) {
        int j = st.back();
        st.pop_back();
        // right boundary -> i
        // left  boundary -> st.back()   <-- only correct AFTER the pop
        settle(j, i);
    }
    st.push_back(i);
}
```

需要左邊界時，改用哨兵版，省掉所有 `empty()` 分支：

```cpp
// Sentinel form: -1 at the bottom stands for "no smaller element to the left",
// and a virtual element at index n flushes whatever is still waiting.
vector<int> st {-1};
for (int i = 0; i <= n; i++) {
    int cur = (i == n) ? SENTINEL_VALUE : a[i];
    while (st.back() != -1 && breaks_monotonicity(cur, a[st.back()])) {
        int j = st.back();
        st.pop_back();
        settle(j, st.back(), i);          // left = st.back(), right = i
    }
    st.push_back(i);
}
```

---

## 四個設計決策

骨架永遠一樣，逐題要決定的只有這四件事。面試時把這四題自問一遍，基本不會寫錯。

### 1. pop 的當下算什麼？（決定題型）

| 寫什麼 | 得到 | 例題 |
|---|---|---|
| `res[j] = a[i]` | 下一個更大／更小元素的**值** | [496] Next Greater Element |
| `res[j] = i - j` | 下一個更大元素的**距離** | [739] Daily Temperatures |
| `res[j] = a[j] - a[i]` | 兩者的**差** | [1475] Final Prices |
| `a[j] * (i - st.back() - 1)` | 以 j 為極值能延伸的**最大區間** | [84] Largest Rectangle |
| `a[j] * (j - L) * (R - j)` | 以 j 為最小值的**子陣列數量／貢獻** | [907] Sum of Subarray Minimums |

### 2. 需不需要左哨兵？

看 pop 之後那行公式**有沒有讀 `st.back()`**：

- 只用到 `i` 和 `j` → 不需要，`!st.empty()` 就夠（496 / 739 / 1475）
- 讀了左邊界 → 需要一個虛擬元素頂替「不存在的左邊界」（84 / 907）

哨兵能成立的前提是：**你想得出一個假元素，放進去不改變答案，但讓公式繼續正確**。選值的原則是取該運算的單位元／極值（求 min 用 `+∞`、求 max 用 `-∞`、求和用 `0`）。

反例：LC 42 接雨水的 stack 解**不能**用哨兵——水需要一道真實的牆，硬塞高度 0 的虛擬牆會讓 `min(left,right) - h` 算出錯的值，只能老實 `if (st.empty()) break;`。

### 3. 需不需要末尾 flush？

看迴圈跑完還留在 stack 裡的元素，**它們的答案是什麼**：

- 是一個「什麼都沒發生」的預設值 → 不用 flush，把 `res` 初始化成那個值即可（739 預設 0、1475 預設原價、496 預設 -1）
- 仍需要實際計算 → **必須** flush（84 留下的柱子代表「右邊沒有更矮的，可以一路延伸到 n-1」，那是貨真價實的候選答案）

三種等價寫法：迴圈多跑一格用虛擬值（推薦，不動輸入）、在資料尾端 `push_back` 哨兵、主迴圈後再跑一輪 drain。

### 4. 等值時用 `<` 還是 `<=`？

兩者都能得到正確的極值，差別在「等值群組中誰拿到完整區間」：

| pop 條件 | stack 性質 | 等值群組中誰拿到完整寬度 |
|---|---|---|
| `a[i] <= a[st.back()]`（等值也 pop） | 嚴格單調 | **最右邊**那個 |
| `a[i] < a[st.back()]`（等值不 pop） | 非嚴格單調（等值並存） | **最左邊**那個 |

**求 max / min 的題目兩種都對**，因為被「少算」的那些是較小的合法候選，會被 max 自然淘汰。**但求和／計數的題目必須非對稱破平手**，否則同一個子陣列會被兩個等值元素各認領一次。

## 證明義務（面試最常被追問的地方）

「有沒有重複算到」是個好直覺，但它是不是義務要看目標：

| 目標 | Soundness（不高估） | Completeness（不漏） | Uniqueness（不重複） |
|---|---|---|---|
| max / min（84、42） | ✓ | ✓ | **✗ —— `max(a,a)=a`，重複無害** |
| sum / count（907、2104） | ✓ | ✓ | **✓ —— 等值必須非對稱破平手** |
| 逐位置答案（739、1475、496） | ✓ | ✓ | ✗ —— 每個 j 只被 pop 一次，天然唯一 |

很多人卡住是把求和題的直覺套到求極值題上，自己嚇自己。

- **Soundness**：左邊界 `L` 是左邊第一個更小的、右邊界 `i` 是右邊第一個更小的 → 由定義，`[L+1, i-1]` 內每個元素都 `>= a[j]` → 算出來的一定是真實存在的區間。
- **Completeness**：設最佳區間為 `[l, r]`、極值 `m`。區間內等於 `m` 的元素可能不只一個，**取最右邊那個**當 `j`（用 `<` 版時則取最左邊）。由最佳性 `a[r+1] < m`、`a[l-1] < m`，於是 pop 時機恰好 `i = r+1`、左邊界恰好 `L = l-1` → 那次 pop 算出的正是最佳答案。

## Pitfalls
- **`while` 條件一定要先檢查 `!st.empty()`（或哨兵）再讀 `st.back()`**，否則 stack 被清空後繼續存取是 UB。
- **答案必須寫在 pop 的同一個地方。** 拖到迴圈外再配對 → `(j, i)` 的對應關係已經消失。
- **左邊界是 pop *之後* 的 `st.back()`，不是 pop 之前的。** pop 前的 `st.back()` 就是 `j` 自己——寫成 `i - j - 1` 會算成「j 和 i 之間有幾個元素」，而那些元素早就被 pop 光了，結果幾乎恆為 0。
- **別把 index 當成 value 用。** stack 存的是下標，要比大小或相減時記得包一層 `a[...]`。
- **別用 `j` 當左邊界（`i - j`）。** 那算出的是「以 j 為**最左端**」的區間，而不是「以 j 為**極值**」的最大區間——永遠是合法的下界，但會漏掉最佳解。
- **`int i < v.size()` 會觸發 sign-compare warning**（`int` vs `size_t`）。先存 `int n = v.size();` 比較乾淨。

---

## Problems

### [[84] Largest Rectangle in Histogram](../problems/monotonic-stack/largest_rectangle_in_histogram.md)
**Complexity:** Time O(n), Space O(n)
- **Trigger:** 要求「以某根柱子為高度所能延伸的最大矩形」→ 每根柱子都要左右各一個「第一個更矮的」邊界
- **Insight:** pop 掉 j 的瞬間左右邊界同時到齊——右邊界是觸發 pop 的 `i`、左邊界是 pop *之後* 的 `st.back()`，寬度 `i - st.back() - 1`
- **Pitfall:** 左邊界必須是 pop 之後的 `st.back()`；用 pop 前的 top（`i-j-1`）或用 j 自己（`i-j`）都會低估

### [[1475] Final Prices With a Special Discount in a Shop](../problems/monotonic-stack/final_prices_with_discount.md)
**Complexity:** Time O(n), Space O(n)
- **Trigger:** 「右邊第一個 `prices[j] <= prices[i]`」——題目直接把 next smaller-or-equal element 寫進定義裡
- **Insight:** 折扣條件在「拿 `prices[i]` 跟 `st.back()` 比大小」的當下就成立了，所以當場 `res[st.back()] -= prices[i]` 再 pop，對齊自動成立
- **Pitfall:** 答案要在 pop 當下寫入；留在 stack 的元素不打折 → 把 `res` 初始化成 `prices` 就免掉末尾 flush
