# String

## When to Use
題目以字串為主要輸入，且操作集中在**字元層級**而非 array index 的隨機存取上：解析、模擬大數運算、模式比對、格式轉換等。

跟 [[array/README]] 的差別：array 題重點是「位置承載資訊」與 random access，string 題重點是「字元語意」與「逐字掃描狀態」。許多 string 題本質上就是字元上的小型狀態機。

## Typical Complexity
**Time:** 多數 O(n) 或 O(m·n)（兩字串交互處理）；模式比對類有 O(n+m)（KMP）或 O(n·m) brute force
**Space:** Brute force 常開額外 buffer 存中間結果（O(n) ~ O(m+n)）；follow-up 常要求把 buffer 壓掉，直接在輸出字串上累加

## General Template
String 題沒有單一 skeleton，依變體不同。核心原語：

```cpp
// 1. char ↔ int 轉換（處理數字字串時最常用）
int d = ch - '0';        // char → int
char c = '0' + d;        // int → char

// 2. 雙指針從尾巴往前掃（模擬筆算對齊）
int i = s1.size() - 1, j = s2.size() - 1;
while (i >= 0 || j >= 0 || carry) {
    int a = i >= 0 ? s1[i--] - '0' : 0;
    int b = j >= 0 ? s2[j--] - '0' : 0;
    // ...
}

// 3. 去前導零
size_t pos = s.find_first_not_of('0');
return pos == string::npos ? "0" : s.substr(pos);
```

## Common Variations
- [Simulation](simulation.md) — 字串上模擬筆算大數運算（multiply / add / plus one / atoi 等），核心是位數對齊與進位處理
