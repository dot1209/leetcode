# [2434] Using a Robot to Print the Lexicographically Smallest String
**Pattern:** [Greedy + Stack](../../patterns/greedy-stack.md)
**Complexity:** Time O(n), Space O(n)
**Link:** https://leetcode.com/problems/using-a-robot-to-print-the-lexicographically-smallest-string/

## Trigger Signals
- robot 的 `t`：「append 到尾、只能從尾移除」→ 這正是 stack（LIFO）的定義。一旦看出這點，就知道輸出順序受限、不能自由重排
- 要求 **lexicographically smallest** 輸出 → 逐位貪心：每一步吐出「當下能吐的最小字元」
- 「現在吐 top，還是再從 `s` 讀更多」這個決策只需比較 top 與「`s` 剩下的字元」→ 暗示 suffix-min 預處理

## Core Insight
`t` 是一個 stack。任何一刻，「下一個能寫到紙上的字元」的候選集合是：

```
{ stack 的 top } ∪ { s 中還沒 push 的所有字元 }
```

被壓在 top 底下的字元此刻取不出來，所以**不在**候選內。於是規則是：**當 `top ≤ s 剩餘字元的最小值` 時就 pop 並寫出**——因為此時沒有任何更小的字元還能冒出來，top 就是整個候選集合的最小值，現在吐它最優。把「`s` 剩餘字元的最小值」預先算成 **suffix-min**，每步比較降到 O(1)。

相等時也該 pop（用 `≤`）：再等下去不會更小，先吐掉這個一樣小的字元無損。

## Complexity Analysis
- **Time O(n)**：suffix-min 一次反向掃描 O(n)；主迴圈雖有巢狀 while，但每個字元一生只被 push 一次、pop 一次，while 的總執行次數 ≤ n → 攤還 O(n)。
- **Space O(n)**：suffix 陣列 O(n) + stack 最壞 O(n)（如 `"abc"` 一路壓著不 flush）。suffix 陣列可用 O(26) 計數陣列取代，但 stack 的 O(n) 無法避免。

## Solution Code
```cpp
class Solution {
public:
    string robotWithString(string s) {
        int n = s.size();
        // suf[i] = index of the smallest char in s[i..n-1]
        vector<int> suf(n, 0);
        int min_idx = n - 1;
        for (int i = n - 1; i >= 0; i--) {
            if (s[i] < s[min_idx]) min_idx = i;
            suf[i] = min_idx;
        }

        stack<char> st;
        string res;
        for (int i = 0; i < n; i++) {
            st.push(s[i]);
            // flush while top <= min of the still-unpushed part s[i+1..]
            while (st.size() && i + 1 < n && st.top() <= s[suf[i + 1]]) {
                res += st.top();
                st.pop();
            }
        }
        while (st.size()) {           // nothing left to read: drain the rest
            res += st.top();
            st.pop();
        }
        return res;
    }
};
```

## Pitfalls
- **flush 條件必須比 `st.top()`，且每 pop 後重新比新 top → 一定是 `while` 不是 `if`。** 第一版常見錯：把條件寫成「剛 push 的 `s[i]` 是否為 suffix 最小」（`suf[i] == i`），這既沒看 top，又在整個 while 中恆定不變 → 退化成「整個 stack 全倒、或完全不動」。
  - 反例 `s = "dac"`：正解 `"acd"`，錯版輸出 `"adc"`——吐 `a` 時把 `d` 一起倒掉，但 `c` 還沒來，`d` 該等。
- **比的是 `s[i+1..]` 不是 `s[i..]`。** index `i` 的字元已經 push 進 stack，suffix 最小值只能看「還沒 push 的部分」，否則把自己重複算進去 → off-by-one。
- **`≤` 不是 `<`。** 相等時該 pop（已經沒有更小的了）。
- **收尾 drain。** 最後一個字元 push 後 `i+1 == n`，內層 while 的 `i+1 < n` 短路掉，靠迴圈外的 drain 把 stack 倒完。替代寫法：把 suffix 設成 `sufMin[n] = CHAR_MAX` 的 sentinel，讓內層自然倒完，省掉外層 drain。

## Related Problems
- [316] / [1081] Remove Duplicate Letters / Smallest Subsequence — 同樣 greedy + stack 建字典序最小，但 flush 改用「維持單調 + 之後是否還會再出現」
- [402] Remove K Digits — greedy + stack 求最小數，flush 條件是「top > 下一位且還有刪除預算」
- [1673] Find the Most Competitive Subsequence — 幾乎是 402 的子序列版，monotonic flush + 剩餘長度預算
