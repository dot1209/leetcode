# [1189] Maximum Number of Balloons
**Pattern:** [Frequency Counting](../../patterns/frequency-counting.md)
**Complexity:** Time O(n), Space O(1)
**Link:** https://leetcode.com/problems/maximum-number-of-balloons/

## Trigger Signals
- 給一袋字元 `text`，要**重複拼出固定單字** `balloon`，問最多能拼幾個 → 不在乎順序、只在乎每個字母**有幾個** → frequency counting。
- 目標字 `balloon` 內有**重複字母**（`l`、`o` 各 2 個）→ 是 bottleneck min 的標準訊號：答案卡在最稀缺的字母。

## Core Insight
先數出 `text` 裡每個字母出現幾次，然後答案 = 對 `balloon` 需要的每個字母，算「擁有量 ÷ 需要量」再取 **min**。能拼幾個 `balloon` 由**最稀缺的那個字母**決定（bottleneck）：`b`、`a`、`n` 各需要 1 份，`l`、`o` 各需要 2 份，所以 `l`、`o` 要用 `freq / 2` 才反映真正能供應的組數。

## Complexity Analysis
- **Time O(n)** — 建頻率表掃 `text` 一次，n = `text` 長度；最後的 `min({...})` 只比 5 個固定的值，是 O(1)。所以整體就是線性。
- **Space O(1)** — `freq[26]` 是固定 26 格的陣列，與輸入長度 n 無關。字母表大小是常數，不隨輸入增長。

## Solution Code
```cpp
class Solution {
public:
    int maxNumberOfBalloons(string text) {
        int freq[26] = {0};
        for (auto c : text) {
            freq[c - 'a']++;
        }
        // b: 1, a: 1, l: 2, o: 2, n: 1
        return min({freq['b' - 'a'] / 1, freq['a' - 'a'] / 1,
                    freq['l' - 'a'] / 2, freq['o' - 'a'] / 2,
                    freq['n' - 'a'] / 1});
    }
};
```

## Notes / 可改進處（不改你的 code，另記於此）
- **`/ 1` 是 no-op。** `b`、`a`、`n` 各除以 1 等於沒除，可以直接寫 `freq['b'-'a']`；留著只是對齊「每個字母都除以需要量」的心智模型，不影響正確性或複雜度。
- 這已經是**最佳解**：建表必須掃過每個字元至少一次，所以 O(n) 是下界；空間是固定 26 格的 O(1)。沒有更好的漸進複雜度。

## Pitfalls
- **`l`、`o` 一定要除以 2。** 它們在 `balloon` 裡各出現 2 次，忘了除會把能拼的組數**高估一倍**——這是這題唯一的陷阱。
- 用陣列 `freq[26]` 而不是 hash map：值域固定只有 26 個小寫字母，陣列更快更省。

## Follow-ups
**把目標字從寫死的 `balloon` 換成任意輸入單字 `target`。** 這時不能再手刻 `l/2`、`o/2`，要先對 `target` 也建一張 `need[26]` 頻率表，再對 `need[c] > 0` 的每個字母取 `min(have[c] / need[c])`：

```cpp
// generalized: how many copies of `target` can we build from `text`?
int have[26] = {0}, need[26] = {0};
for (char c : text)   have[c - 'a']++;
for (char c : target) need[c - 'a']++;
int ans = INT_MAX;
for (int i = 0; i < 26; i++)
    if (need[i] > 0) ans = min(ans, have[i] / need[i]);
return ans;
```

改變的關鍵假設：原題「每個字母需要幾份」是常數、可以寫死進 `min`；一般化後它變成資料、必須先數出來。這也正是 **[383] Ransom Note**（只問能不能拼 1 個 = 問 min ≥ 1）和 **[1160] Find Words That Can Be Formed by Characters** 的同一套路。

## Related Problems
- [383] Ransom Note — 同樣比對「擁有 vs 需要」的字母數，只是問能否拼出 1 份（每個字母 `have[c] >= need[c]`）。
- [1160] Find Words That Can Be Formed by Characters — 對每個候選字檢查 `have >= need`，累加能拼出的字長。
- [242] Valid Anagram — 兩張頻率表是否完全相等。
