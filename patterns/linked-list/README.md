# Linked List

## When to Use
題目操作 singly / doubly linked list，常見題型：
- 反轉、合併、分裂、deep copy
- cycle detection、找中點、找交點
- 用 list 結構模擬 stack / queue

Linked list 題的核心觀察：每個 node 有「**可寫的指標欄位**」，這是它與陣列最大的差別。許多看似需要額外 hashmap / stack 的問題，能透過暫時改寫指標欄位達成 O(1) 額外空間。

## Typical Complexity
**Time:** 多數操作 O(n) — 必須走過整條 list；無法 random access
**Space:** 可達 O(1)（in-place 操作）；遞迴解法是 O(n) stack

## General Template
```cpp
// dummy head：避免處理 head 變動的特例
ListNode dummy(0);
dummy.next = head;
ListNode* prev = &dummy;
ListNode* cur = head;
while (cur != nullptr) {
    // ... 操作 prev, cur, cur->next
    prev = cur;
    cur = cur->next;
}
return dummy.next;
```

`dummy` 是最常用的招數：當答案的 head 可能改變（刪頭、reverse、merge 等），用 dummy 避免「head 是不是就是它本身」的特例判斷。

## Common Variations
- [Deep Copy](deep-copy.md) — 複製含 random / 額外指標的 list，可用 hashmap 或 in-place interleaving
- [In-place Rewiring](in-place-rewiring.md) — 不開新 node、只重接 `next` 來改變結構（reverse / reorder / rotate / swap）
