# [3517] Smallest Palindromic Rearrangement I
**Pattern:** [Frequency Counting](../../patterns/frequency-counting.md)
**Complexity:** Time O(n), Space O(n) — `half`/`rev` 兩個中間 buffer 隨 n 成長;可壓到 auxiliary O(1)(見「其他解法」)
**Link:** https://leetcode.com/problems/smallest-palindromic-rearrangement-i/

## Trigger Signals
- 輸入保證是**回文**,要重排成「**字典序最小**的回文」→ 只在乎每個字母有幾個、不在乎原順序 → frequency counting。
- 「回文」這個限制 → 頂多一個字母出現奇數次(放正中間),其餘都成對 → 建 freq 表就能直接推出結構。

## Core Insight
**答案 = 「每個字母取一半、由 `a→z` 升序排」構成前半段,奇數次的字母放正中間,後半段是前半段的鏡射。**

因為 `s` 是回文,最多只有一個字母是奇數次。整個回文的後半段被前半段完全決定(鏡射)、中間字元也固定(唯一的奇數字母),所以字典序**只由前半段決定** → 要最小就把小字母盡量往前放,也就是把每個字母的「一半份數」按 `a→z` 依序 append(greedy:每個位置放當下可用的最小字母)。

## Complexity Analysis
- **Time O(n)** — 掃 freq 是 O(n);組 `half`、`rev`、最後串接 `half + mid + rev` 每步都線性。
- **Space O(n)** — 這是重點,別誤標 O(1):`half` 和 `rev` 各 ⌊n/2⌋ 個字元,是**隨 n 成長**的 auxiliary buffer;`freq[26]` 才是 O(1)。加上 output 也是 O(n)。只盯著 `freq` 固定陣列就標 O(1) 是錯的。

## Solution Code
```cpp
class Solution {
public:
    string smallestPalindrome(string s) {
        int freq[26] = {0};
        for (auto c: s) {
            freq[c-'a']++;
        }
        string half, mid;
        // greedly append char in alphabetic order
        for (int i = 0; i < 26; i++) {
            half.append(freq[i]/2, i+'a');
            // valid palindrome only has one odd frequency char, and it must in the mid pos
            if (freq[i] & 1) {
                mid = i+'a';
            }
        }
        string rev(half.rbegin(), half.rend());
        return half + mid + rev;
    }
};
```
> 已用 brute-force(`next_permutation` 取第一個回文)對拍,even / odd / 全同字元 / 單字元皆通過。

## 為什麼「升序排前半段」給出字典序最小
- 後半段是前半段的鏡射、中間字元是唯一的奇數字母 —— 兩者都不是自由變數,所以整個回文的字典序**只取決於前半段**。
- 要前半段字典序最小 → 越小的字母越往前 → 把每個字母的一半份數按 `a→z` 依序放。這是標準 greedy:每個位置都填「當下還有庫存的最小字母」,不會有更好的選擇。

## 其他解法 / 複雜度優化(不改上面的 code)
- **真・O(1) auxiliary:** 別另外 materialize `half` 和 `rev`,而是先把 output buffer 開好(`string res(n, ' ')`),再從兩端對稱往中間填,只用 `freq[26]`。(這剛好呼應下面 Pitfalls:字串**先 `resize` 撐長度**,`res[i]` 直接寫才合法。)已對拍驗證通過:
  ```cpp
  string smallestPalindrome(string s) {
      int freq[26] = {0};
      for (char c : s) freq[c - 'a']++;
      int n = s.size();
      string res(n, ' ');              // output sized once; index writes now valid
      int l = 0, r = n - 1;
      for (int i = 0; i < 26; i++) {
          for (int k = 0; k < freq[i] / 2; k++) {
              res[l++] = 'a' + i;      // fill left half
              res[r--] = 'a' + i;      // mirror to right half
          }
          if (freq[i] & 1) res[n / 2] = 'a' + i;   // middle char (odd n)
      }
      return res;
  }
  ```
- **面試取捨:** `half + mid + rev` 版可讀性明顯更好,一眼就懂;這題 n 頂多 1e5,O(n) vs O(1) auxiliary 無關痛癢。優先寫清楚的,被追問再提「可以就地填省一半空間」。

## Pitfalls
- **`reserve` 只改 capacity、不改 size。** 想用 `res[i]` 直接寫某個位置,必須先 `resize(n)` 把 `size` 撐出來(`reserve` 不行);否則 index ≥ `size` 就是越界 UB。這是本題最容易踩的雷 —— 第一版就是 `reserve` 完直接 `res[pos]=...`,結果字串長度根本沒長、越界又只回傳半條答案。
- **複雜度別只看固定陣列。** `half`/`rev` 這種隨 n 成長的中間 buffer 也要算進 space → 是 **O(n)** 不是 O(1)。
- **中間字元只有 odd n 才有。** 回文保證頂多一個奇數字母;even n 沒有中間字元,`mid` 留空字串,`half + "" + rev` 剛好正確。

## 概念補充(這題連帶學到的)
- **`reserve` vs `resize` vs `capacity`:** `reserve(n)` 只確保 capacity ≥ n(預留 buffer、避免 reallocation),**size 不變**;`resize(n)` 才會改 size(新字元 value-initialize 成 `'\0'`)。`operator[]` 的合法範圍由 `size()` 決定,跟 capacity 無關。
- **SSO(Small String Optimization)是 library 技巧,不是 compiler optimization。** `std::string` 的實作在物件內部塞一個小 buffer,短字串(libstdc++ ≤ 15、libc++ ≤ 22)直接存在裡面、不碰 heap,所以空字串 `capacity()` 天生就是 15、對小字串 `reserve` 常常看似無效。它寫死在 STL 原始碼裡,`-O0` 照樣有;換 STL 實作才會變(換 compiler / 調 `-O` 不變)。

## Follow-ups
**[3518] Smallest Palindromic Rearrangement II —— 求第 k 小的回文重排。** 這時不能只 greedy 排最小,要用 combinatorics 逐位定位:對每個位置,計算「固定這個字母後、剩下字母能組成幾種前半排列」(multinomial `(剩餘一半總數)! / ∏(各字母剩餘一半)!`),用 k 去判斷該跨過這個分支還是鑽進去 —— 本質是「k-th permutation」的字母多重集版本。關鍵假設變化:原題只要最小(前半升序即可),II 要按序數精準定位第 k 個,得會算「還剩多少種排法」並小心大數 / overflow。

## Related Problems
- [266] Palindrome Permutation — 判斷字串能否重排成回文(奇數次字母 ≤ 1),正是本題成立的前提條件。
- [267] Palindrome Permutation II — 列出**所有**回文重排(不是最小):一樣建半段,再對半段做 backtracking 全排列。
- [409] Longest Palindrome — 同樣數 freq:成對的全用、最多留一個奇數字母當中間,求最長回文長度。
- [2384] Largest Palindromic Number — 反向求**最大**回文(還要處理前導零),同樣 freq → 半段 → 鏡射的骨架。
