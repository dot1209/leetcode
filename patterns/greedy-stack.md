# Greedy + Stack

Greedy + Stack 是用一個 stack 當「暫存區」、配合一條 **flush 規則**逐步建構**字典序最佳（最小／最大）序列**的技巧。它存在的理由是：當輸出順序受 LIFO 限制——元素一旦被壓在別人下面就拿不出來——你沒辦法把輸入直接 sort 成答案，只能在「現在就吐出 stack top」與「再多讀進幾個元素」之間做**局部最優決策**。它改變的是問題的量級：把「在所有可達排列裡找字典序最小」這個看似要爆搜的問題，壓成一次線性掃描（每個元素一生 push / pop 各一次），代價只剩下「flush 條件怎麼設計」這一個重點。

## When to Use
- 要建構**字典序最小／最大**的字串或子序列，而輸出順序受某種 LIFO / 單向消費規則限制（不能自由重排）
- 元素被壓在 stack 下面就無法越過上面的元素取出 → sort 不可行
- 決策只是「吐出 top，還是再讀入更多」，且這個決策**只需比較 top 與剩餘元素的某個極值或下一個讀入元素**
- 訊號詞：`lexicographically smallest/largest`、`remove k digits`、`remove duplicate letters`、`most competitive subsequence`、用某種裝置／機器人逐步吐字

兩種 flush 條件（決定本家題目分流的關鍵）：

1. **Suffix-min/max flush**（如 2434）：當 top 已經是「剩下不可能再更好」時就 pop——即 `top ≤ 剩餘所有元素的最小值`。需要預先算 **suffix-min**。
2. **Monotonic flush**（如 316 / 402 / 1673）：當 top 比「即將讀入的元素」差時 pop，以維持 stack 單調；通常再配一個守門條件（刪除預算、之後是否還會再出現）。

反例：若可以自由重排（沒有 LIFO 限制）→ 直接 sort；若只是查 next greater / smaller 的位置而非建構輸出 → 純 monotonic stack 即可，不需 greedy 吐字。

## Typical Complexity
**Time:** O(n) — 每個元素最多被 push 一次、pop 一次。雖然主迴圈內有巢狀 while，但「一生只 pop 一次」保證 while 的**總**執行次數 ≤ n，所以是攤還 O(n)，不是 O(n²)。Suffix-min 版另加一次 O(n) 反向掃描。
**Space:** O(n) — stack 最壞存下全部元素（如遞增輸入無法 flush）。Suffix-min 版另開 O(n) 陣列，或用 O(σ) 計數陣列取代（σ 為字元集大小，小寫字母 σ=26）。輸出本身 O(n)。

關鍵理解：巢狀 while 看起來像 O(n²)，但攤還是 O(n)——這跟 monotonic stack、two pointers 是同一種「每個元素只進出一次」的攤還論證。

## General Template
```cpp
// Flavor A — suffix-min flush: build lexicographically smallest output.
// Pop the top once nothing smaller can ever surface from the unread part.

int n = s.size();
vector<char> sufMin(n + 1, CHAR_MAX);          // sufMin[n] = sentinel: nothing left
for (int i = n - 1; i >= 0; i--)
    sufMin[i] = min(s[i], sufMin[i + 1]);

stack<char> st;
string res;
for (int i = 0; i < n; i++) {
    st.push(s[i]);
    // flush while top can't be beaten by the best of what is still unread
    while (!st.empty() && st.top() <= sufMin[i + 1]) {
        res += st.top();
        st.pop();
    }
}
// the sentinel makes the final iteration drain the stack automatically
```

```cpp
// Flavor B — monotonic flush: pop while the top is worse than the incoming
// element, guarded by a budget (e.g. "remove k") or an "appears later" check.

stack<char> st;
for (char c : s) {
    while (!st.empty() && st.top() > c && budget > 0) {
        st.pop();
        budget--;
    }
    st.push(c);
}
```

## Pitfalls
- **flush 條件比的是 `st.top()`，且每 pop 後要重新比新的 top → 必須是 `while`，不能是 `if`。** 最常見的 bug 是把條件寫成「剛 push 的那個元素」的性質而非 top 的性質——那種條件在整個 while 中恆定不變，會退化成「要嘛整個 stack 全倒、要嘛完全不動」。
- **Suffix-min 比的是「還沒 push」的部分 `s[i+1..]`，不是 `s[i..]`。** index `i` 已經在 stack 上了，把它算進剩餘極值會 off-by-one。
- **`≤` vs `<`。** 相等時通常該 flush（再等也不會更小）——用 `≤`；寫成 `<` 在有重複元素時可能多留不必要的元素。逐題確認。
- **收尾要 drain。** Suffix-min 版最後一段沒有「剩餘元素」，要嘛靠迴圈外補 drain、要嘛用 sentinel 讓內層自然倒完。
- **Monotonic flush 版別漏掉守門條件**（預算 / 計數 / 之後是否再出現），否則會過度刪除。

---

## Problems

### [[2434] Using a Robot to Print the Lexicographically Smallest String](../problems/greedy-stack/robot_print_smallest_string.md)
**Complexity:** Time O(n), Space O(n)
- **Trigger:** robot 的 t 只能 append / remove 尾端 = stack；要求字典序最小輸出
- **Insight:** 可寫候選 = `{top} ∪ {s 剩餘未讀字元}`；當 `top ≤ suffix-min(剩餘)` 就 pop 寫出
- **Pitfall:** flush 要比 top 且用 while 重評估；比 `s[i+1..]`（非 `s[i..]`）；用 `≤` 非 `<`
