# [1475] Final Prices With a Special Discount in a Shop
**Pattern:** [Monotonic Stack](../../patterns/monotonic-stack.md)
**Complexity:** Time O(n), Space O(n)
**Link:** https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/

## Trigger Signals
- 題目定義直接就是 next smaller-or-equal element：「第一個 `j > i` 且 `prices[j] <= prices[i]`」
- 每個 index 各要一個答案，而答案只依賴「右邊第一個滿足條件的元素」
- 暴力是對每個 `i` 往右掃到第一個更便宜的，O(n²) → 標準可攤平形狀
- 有「找不到就維持原價」的預設值 → 暗示留在 stack 裡的元素不用特別處理

## Core Insight
折扣條件在「拿 `prices[i]` 跟 `st.back()` 比大小」的當下就已經成立了，所以**當場扣掉就沒問題**。

`st` 存的是「還在等折扣、尚未找到答案」的 index。走到 `i` 時若 `prices[i] <= prices[st.back()]`，代表 `i` 正是 `st.back()` 要找的那個更便宜的商品——這一刻就把 `res[st.back()] -= prices[i]` 寫掉再 pop。因為是寫進 `res[j]`（`j` 是被 pop 的下標），**對齊是自動成立的，不需要事後配對**。

迴圈結束後仍留在 stack 的 index，代表右邊沒有更便宜的 → 不打折 → 維持原價。把 `res` 初始化成 `prices` 就免掉末尾 flush。

## Complexity Analysis
- **Time O(n)**：每個 index 只被 push 一次、pop 一次，內層 `while` 的總執行次數 ≤ `n` → 攤還 O(n)。
- **Space O(n)**：stack 最壞存下全部 index（價格嚴格遞增時完全不 pop，例如 `[1,2,3,4,5]`）。輸出陣列另計 O(n)，但那是題目要求的回傳值。

## Solution Code
```cpp
class Solution {
public:
    vector<int> finalPrices(vector<int>& prices) {
        vector<int> res = prices;
        vector<int> st;
        for (int i = 0; i < prices.size(); i++) {
            while (!st.empty() && prices[i] <= prices[st.back()]) {
                res[st.back()] -= prices[i];
                st.pop_back();
            }
            st.push_back(i);
        }
        return res;
    }
};
```

隨機壓測 400000 筆（長度 1~9、值域 1~5、大量重複值）對照暴力解：全數通過，輸入未被改動。
`[8,4,6,2,3] → [4,2,4,2,3]`、`[5,5,5] → [0,0,5]`、`[10,1,1,6] → [9,0,1,6]`。

### 第一版錯在哪（值得記住的三個坑）
最初的寫法是「先用 stack 記下下一個更小的 index，最後再另外一個迴圈把答案配對回來」，結果卡在**沒辦法對齊減回來**。三個問題：

1. **`while (prices[i] <= prices[st.back()])` 少了 `!st.empty()`** → stack 被清空後繼續 `st.back()` 是 UB。
2. **pop 的瞬間就是答案成立的瞬間，卻直接 `pop_back()` 沒寫回去** → 資訊在那一行消失了。
3. **收尾迴圈把 index 當 value 用**：`res[i] = prices[i] - st[i]`，`st[i]` 是下標不是價格；而且 `st` 剩下的元素跟 `i` 沒有任何對應關係。

第 3 點是第 2 點的必然後果——**一旦拖到迴圈外再想回頭配對，`(j, i)` 這組關係已經不存在了**。修正的關鍵不是改公式，是把「寫答案」這件事搬回 pop 的那一行。

## Pitfalls
- **答案必須寫在 pop 的同一個地方**，不能等迴圈跑完再配對。這是整個 monotonic stack 最核心的一條。
- **`<=` 不是 `<`。** 題目寫的是 `prices[j] <= prices[i]`，等價也算折扣，所以等值要 pop。寫成 `<` 會讓等價的商品拿不到折扣（`[5,5,5]` 會得到 `[5,5,5]` 而非 `[0,0,5]`）。
- **`res` 初始化成 `prices` 而不是 `vector<int>(n)`。** 這一步同時承擔了「找不到就原價」的預設值，省掉末尾 flush；初始化成 0 會讓沒打折的商品變成 0。
- **stack 存 index 不存 value。** 要寫回 `res[st.back()]`，只有 index 拿得到位置。
- **別把 index 當 value 相減。** 比大小和做算術前都要包一層 `prices[...]`。
- `int i` 跟 `prices.size()` 比較會有 sign-compare warning（`int` vs `size_t`），不影響正確性，但先存 `int n` 比較乾淨。

## Related Problems
- [496] Next Greater Element I — 同骨架，pop 當下寫的是 `res[j] = nums[i]`（值而非差）
- [739] Daily Temperatures — 同骨架，pop 當下寫的是 `res[j] = i - j`（距離）；留在 stack 的預設 0
- [901] Online Stock Span — 同骨架但改成串流輸入，pop 時把被吃掉的 span 累加起來
- [84] Largest Rectangle in Histogram — 同骨架但**兩側**邊界都要，因此需要左哨兵與末尾 flush
