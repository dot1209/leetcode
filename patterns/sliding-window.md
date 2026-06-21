# Sliding Window

Sliding Window 是用左右兩個指針框出 array / string 上一段**連續區間**,讓區間隨著掃描「滑動」而非每次重算的技巧。它存在的理由是:很多「連續子陣列 / 子字串滿足某條件」的問題,暴力解會對每個起點重新往後掃一遍(O(n²) 甚至 O(n²·σ)),但相鄰的兩個區間其實**只差頭尾一兩個元素**——把上一個區間的計算結果留著、只處理進出視窗的那幾個元素,就能把重算省掉。它改變的是問題量級:把「枚舉所有區間」壓成「每個元素被左右指針各碰一次」的線性掃描,代價只剩「視窗狀態怎麼增量維護」這一個重點。

## When to Use
- 問題針對 **連續** 的 subarray / substring(不連續就不是它,是 DP / 其他)
- 求「最長 / 最短 / 符合某條件的區間個數 / 是否存在」這類,且區間的合法性隨長度**單調**(視窗變長越容易/越難滿足條件)
- 暴力解是「對每個起點往後掃」的 O(n²),而相鄰區間的狀態只差頭尾元素 → 可增量維護
- 訊號詞:`longest/shortest substring`、`subarray with sum/at most K`、`contains all of...`、`permutation/anagram in string`

兩種形態:
- **Fixed window**:視窗大小固定 = k,右進一個就左出一個。
- **Variable window**:視窗大小浮動,典型節奏是「**右指針一直擴到滿足條件 → 左指針一直縮到剛好不滿足(過程中更新答案)→ 繼續擴**」。Minimum Window Substring 屬此類。

## Typical Complexity
**Time:** O(n)(+ 建表 O(m))— 關鍵在 `l`、`r` 各自**單調往右、一生只走過 n 次**,所以即使主迴圈裡有內層 while 縮放,內層**總**執行次數 ≤ n,是攤還 O(n),不是 O(n²)。前提是「視窗合法性檢查」本身是 O(1)。
**Space:** O(σ) — 視窗狀態通常是一個字元計數(map 或 `int[128]`),被字母表大小 σ 封頂。對固定字母表就是 **O(1)**,與 n 無關。

關鍵理解:把「每步 O(σ) 重掃整個視窗判斷合法」換成「進出元素時 O(1) 增量更新一個摘要值」,是這個 pattern 從「能過但常數肥」進化到「乾淨 O(n)」的核心——見下方 incremental counter。

## General Template
```cpp
// Variable window: grow r to satisfy, then shrink l while still satisfied.
int need[128] = {0}, win[128] = {0};
int required = 0;                          // distinct keys to satisfy
for (char c : t) { if (need[c] == 0) required++; need[c]++; }

int l = 0, formed = 0;                     // formed = #keys currently satisfied
int best_len = INT_MAX, best_l = 0;
for (int r = 0; r < (int)s.size(); r++) {
    char c = s[r];
    win[c]++;
    if (need[c] > 0 && win[c] == need[c]) formed++;   // exactly hit threshold -> +1
    while (formed == required) {                       // window valid: O(1) check
        if (r - l + 1 < best_len) { best_len = r - l + 1; best_l = l; }
        char cl = s[l];
        if (need[cl] > 0 && win[cl] == need[cl]) formed--;  // about to drop below -> -1
        win[cl]--;
        l++;
    }
}
```

### Incremental counter（這個 pattern 的靈魂)
與其每次都重掃整個視窗問「合法嗎」(O(σ)/步),不如維護一個**摘要整數**,只在「某元素剛好讓條件翻轉」的瞬間 O(1) 更新它:
- 「裝齊所有必要字元」→ 維護 `formed`(已達標的字元種數),`==required` 即合法。
- 「at most K distinct」→ 維護 `distinct`,字元數 `0→1` 時 `distinct++`、`1→0` 時 `distinct--`。

更新時機要抓「跨門檻那一刻」:加用 `== need`(剛好達標才 +1)、減在 `== need` 時(即將跌破才 -1)。這招不限 sliding window——union-find 的連通分量數、括號平衡計數都是同一個精神。

## 記錄與縮放的兩個旋鈕
滑動視窗的寫法差異幾乎都落在兩個**獨立**的選擇上,拆開來看就不用硬背。

**旋鈕一:先記答案還是先縮?——由「縮的 while 條件」決定。**
記錄一定發生在「視窗處於你要的合法狀態」那一刻,而 while 條件決定那一刻在縮之前還是之後:
- `while (不合法) 縮`:縮完跳出迴圈才剛恢復合法 → **記錄寫在迴圈外、縮之後**(求最長、at most K 計數)。
- `while (合法) 縮`:一縮就可能不合法,得趁還合法先記 → **記錄寫在迴圈內、縮之前**(求最短,如 LC76)。

**旋鈕二:用 `while` 還是 `if` 縮?——看「一次右移後左指針最多要追幾步」。**
- 一步就夠 → `if`。固定大小視窗每次只超一格,縮一次就回去(如 LC30,以詞為單位、超一個詞縮一個詞)。
- 可能要好幾步 → `while`。變動視窗加一個元素可能要連縮多格才恢復(如 LC3、LC76)。
- `while` 是安全預設(該 `if` 的地方用 `while` 也只跑一次);`if` 用錯(該 `while` 卻 `if`)會留下不合法視窗 → bug。**不確定就 `while`。**

## Pitfalls
- **`unordered_map::operator[]` 會偷插 key**:`if (cnt[c] == need[c])` 裡若 `c` 不存在,`need[c]` 會被插入一個 0,讓 `need.size()` 莫名變大。若你拿 `need.size()` 當判斷基準(`formed == need.size()`),它會一路膨脹導致條件永遠不成立 → WA。解法:(a) 用 `int[128]` 陣列(沒有「key 不存在」這回事),或 (b) 開頭就把 `required = need.size()` 存起來、之後別再讀 `.size()`,查詢用 `.count()` / `.find()`。
- **`formed++` 用 `==` 不是 `>=`**:只有「剛好達標」那一次才 +1,否則同字元多進來會重複加。
- **縮放時先判斷再減**:`if (win[cl] == need[cl]) formed--;` 必須在 `win[cl]--` **之前**,抓「即將跌破」的時刻。
- **答案先記 index、迴圈結束再 `substr` 一次**:在內層 while 裡每次都 `res = s.substr(...)` 會反覆配置字串(常數很肥);改成記 `best_l` / `best_len`,最後才 substr。
- **內外指針都要單調**:`l` 只進不退才有攤還 O(n)。若某種寫法會讓 `l` 回頭,複雜度就崩了。

---

## Problems

### [[76] Minimum Window Substring](../problems/sliding-window/minimum_window_substring.md)
**Complexity:** Time O(S+T), Space O(σ)=O(1)
- **Trigger:** 找 `s` 中**最短**、能涵蓋 `t` 所有字元(含重複次數)的連續子字串 → variable window
- **Insight:** 右指針擴到「裝齊 t」,左指針縮到「剛好還合法」並更新答案;用 `formed` 計數器把合法性檢查降到 O(1)
- **Pitfall:** `need[c]` 用 `operator[]` 會汙染 `need.size()`(改用陣列或先存 `required`);substr 留到最後一次

### [[30] Substring with Concatenation of All Words](../problems/sliding-window/substring_with_concatenation_of_all_words.md)
**Complexity:** Time O(S·word_len + W), Space O(S+W)
- **Trigger:** 找所有起點,使子字串剛好是一組**等長** words 的任意串接 → 以「詞」為單位的 fixed window
- **Insight:** 起點按 `start mod word_len` 分成 word_len 條獨立「詞格線」各跑一次;`formed` 計數同 LC76,只是 key 從字元換成詞
- **Pitfall:** 每個 offset 要重置 `window`/`formed`/`l`(共用會跨格線污染,且 `len≥10` 才暴露);時間別漏算每步 substr 的 O(word_len) 因子
