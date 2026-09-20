# [84] Largest Rectangle in Histogram
**Pattern:** [Monotonic Stack](../../patterns/monotonic-stack.md)
**Complexity:** Time O(n), Space O(n)
**Link:** https://leetcode.com/problems/largest-rectangle-in-histogram/

## Trigger Signals
- 要找「最大矩形」，而矩形的高度必然等於它涵蓋範圍內**最矮**的那根柱子 → 問題轉成「對每根柱子問：以它為高，最寬能延伸多遠」
- 「最寬能延伸多遠」= 左右各找**第一根比它矮**的柱子 → next smaller element，兩側都要
- 暴力是對每個 `l` 往右掃並維護 min，O(n²) → 典型可攤平成 monotonic stack 的形狀

## Core Insight
枚舉的單位是「**以哪根柱子當最矮**」：任何一個最大矩形一定貼齊它涵蓋範圍內最矮的那根（不然還能再往上長），所以對每根柱子 `j` 算一次「以 `heights[j]` 為高的最大矩形」，取 max 就是答案。

關鍵是 **pop 掉 `j` 的那一刻，左右邊界同時到齊**：

- **右邊界**：觸發 pop 的 `i`，定義上就是 `j` 右邊第一根比它矮的 → 矩形右端最多到 `i - 1`
- **左邊界**：pop 掉 `j` 之後的新 `st.back()`。因為 stack 單調，`j` 底下那個元素正是 `j` 左邊第一根比它矮的 → 矩形左端最早從 `st.back() + 1` 開始

合法區間是**開區間** `(st.back(), i)`，index 從 `st.back()+1` 到 `i-1`，所以

```
width = (i - 1) - (st.back() + 1) + 1 = i - st.back() - 1
```

那個 `-1` 就是從「兩個閉區間端點」換算成「中間有幾格」多出來的一格。

為什麼 `st.back()` 真的是左邊界：stack 中**相鄰兩個元素之間被 pop 掉的所有柱子，高度都 ≥ 上面那個元素**。因為 `j` 被 push 時已經把所有比它高的彈掉了，而 `j` 與它底下的 `k` 之間那些柱子，全是被「不高於 `j` 的東西」踢掉的。

## Complexity Analysis
- **Time O(n)**：外層迴圈跑 `n+1` 次；內層 `while` 看起來像巢狀迴圈，但每個 index 一生只被 push 一次、pop 一次，所以 `while` 的**總**執行次數 ≤ `n` → 攤還 O(n)，不是 O(n²)。
- **Space O(n)**：stack 最壞存下全部 index（輸入嚴格遞增時完全不 pop，例如 `[1,2,3,4,5]`）。除了 stack 沒有其他輔助空間。

## Solution Code
```cpp
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int res = 0;
        vector<int> st {-1};
        int n = heights.size();
        for (int i = 0; i <= n; i++) {
            int h = (i == n) ? 0 : heights[i];
            while (st.back() != -1 && h < heights[st.back()]) {
                int j = st.back();
                st.pop_back();
                // left boundary -> st.back()
                // right boundary -> i
                res = max(res, ((i - st.back() - 1) * heights[j]));
            }
            st.push_back(i);
        }

        return res;
    }
};
```

隨機壓測 400000 筆（長度 1~9、值域 0~4、大量重複值）對照暴力解：全數通過，且輸入 vector 未被改動。

### 兩個哨兵各自在幹嘛
- **`st {-1}`（左哨兵）**：代表「左邊沒有更矮的柱子」。這時矩形應該從 index 0 開始，寬度 `i - 0`，而公式給出 `i - (-1) - 1 = i` → 自動成立，不用寫 `if (st.empty())`。
- **`(i == n) ? 0 : heights[i]`（右哨兵）**：用一根虛擬的 0 高度柱子把 stack 清空。沒有它，留在 stack 裡（右邊沒有更矮的）的柱子永遠不會被 pop，答案會漏掉——而那些恰恰是能一路延伸到 `n-1` 的大矩形。

早期版本是寫 `heights.push_back(0)`，效果一樣但會**改動 caller 的 vector**（參數是 `vector<int>&`）。改成迴圈多跑一格、用區域變數 `h` 之後就沒有這個 side effect 了。

### 這版用 `<`，所以等高時「最左邊」那根拿到完整寬度
pop 條件是嚴格小於，等高不 pop，所以等高的柱子會並存在 stack 裡。`[4,4]` 的走法：

- `i=1`：`4 < 4` 為 false → 不 pop，兩根並存
- `i=2`（哨兵 0）：pop `j=1` → `st.back()=0` → 寬 `2-0-1=1` → 面積 4
- 繼續 pop `j=0` → `st.back()=-1` → 寬 `2-(-1)-1=2` → 面積 **8** ✓

換成 `<=` 也對，只是變成**最右邊**那根拿到完整寬度。求 max 的題目兩種都可以；但同樣的選擇到了 [907] 求和就不能亂換。

## Pitfalls
- **左邊界必須是 pop *之後* 的 `st.back()`。** pop 之前 `st.back()` 就是 `j` 自己，寫成 `i - j - 1` 等於在數「`j` 和 `i` 之間有幾根柱子」——但單調性保證那些柱子早就被 pop 光了，所以結果幾乎恆為 0。
  - 實測：`[3,9,8,7,4]` 正解 21 → 錯版只得 12；`[2,3]` 正解 4 → 錯版只得 2。
- **也不能用 `j` 當左邊界（寬度寫成 `i - j`）。** 那算的是「以 `j` 為**最左端**」的矩形，涵蓋 `[j, i-1]`——是一個真實存在的矩形（所以永遠不會高估），但少了往左延伸的那段，會漏掉最佳解。
  - 實測：`[1,3,2]` 正解 4（index 1~2，高 2 寬 2）→ 此版只得 3，因為 index 2 那根必須往左吃掉比它高的 index 1。最短反例是 `[4,4]`：正解 8 → 此版 4。
- **錯在語意不在算術**：`i - j` 把「`j` 是這個矩形的**最矮柱子**」偷換成「`j` 是這個矩形的**最左端**」。枚舉的前提是前者。
- **哨兵值 0 在這裡是「剛好沒事」。** 因為用的是嚴格 `<`，高度 0 的柱子不會被哨兵 0 彈掉，會留在 stack 裡——幸好它們面積是 0，不影響答案。若題目允許負高度就要改用 `INT_MIN`。
- **溢位邊界很近**：`(i - st.back() - 1) * heights[j]` 是 `int * int`，本題上限 `10^5 × 10^4 = 10^9`，而 `INT_MAX ≈ 2.147×10^9`，剛好夠用。面試時主動說一句「範圍再大我會轉 `long long`」會加分。
- `int i` 跟 `heights.size()` 比較會有 sign-compare warning，先存 `int n` 就沒事（這版已經這樣寫）。

## Follow-ups
**[85] Maximal Rectangle** — 輸入換成 0/1 的二維矩陣，求全為 1 的最大矩形。做法是逐列把「每一行往上連續有幾個 1」累積成一個直方圖，對每一列跑一次本題 → O(rows × cols)。本題就是它的一維核心，破的假設是「輸入只有一排柱子」。

## Related Problems
- [85] Maximal Rectangle — 二維版，每列建直方圖後套用本題
- [42] Trapping Rain Water — 同樣要左右邊界，但求的是**凹陷**不是凸起；注意它**不能**用哨兵（水需要真實的牆，stack 空掉時只能直接 break）
- [907] Sum of Subarray Minimums — 同樣是「以 j 為最小值能延伸多遠」，但目標從 max 換成 sum，因此等值時**必須**非對稱破平手，否則同一個子陣列被算兩次
- [1475] Final Prices With a Special Discount — 同骨架但只需右邊界，pop 當下直接相減
