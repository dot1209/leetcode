# Linked List — Deep Copy

## When to Use
- 要複製一條 list，且 node 帶有**額外指標**（如 `random`），不只是 `next`
- 額外指標可能指向 list 上任意位置，包含 nullptr 或回頭指向已走過的 node
- 題目要求「new list 的指標都指向 new node」，不能指回 old node

單純的 `next` deep copy（一條走到底就好）不算這個變體；關鍵在「**有非線性指標需要對應**」。

## Two Solutions

這個變體有兩個典型解法，**trade-off 是空間 vs in-place 修改**。

### 1. Hashmap 對應 — O(n) space
建一張 `old node → new node` 的 map。走 list 時對每個 node 確保 copy 已存在於 map，再接好 `next` / `random`。直觀好寫，但要多 O(n) 記憶體。

### 2. In-place Interleaving — O(1) space ⭐ follow-up
三 pass：
1. 把每個 copy `X'` 插在原 node `X` 後面 → `A → A' → B → B' → ...`
2. 接 random：`X'->random = X->random ? X->random->next : nullptr`（因為 old 的 random 的 copy 就在它隔壁）
3. 拆鏈：把 even/odd 拆回兩條獨立 list，順手還原原 list

核心觀察：**hashmap 的本質是「old → new 的 function」，當 key 是 input node 時，把 new 直接塞在 old 隔壁就能取代 hashmap**。

## Pitfalls
- **Hashmap 版**：lazy 建 copy（走到才建）會多很多特例；改成 two-pass（第一輪只建 node、第二輪只接線）最乾淨
- **Interleaving 版**：
  - Pass 2 的 random：`X->random` 可能是 nullptr，必須三元判斷
  - Pass 3 之前要 reset `cur = head`，前一個 pass 結束時 `cur == nullptr`
  - Pass 3 必須**同步還原原 list**，題目要求 original 不被修改
  - 最後一個 copy 的 `next` 可能殘留指向某個 old node，記得設 nullptr（即使 LC 上靠 pass 1 的副作用恰好正確，也建議顯式處理避免脆弱）

---

## Problems

### [[138] Copy List with Random Pointer](../../problems/linked-list/copy_list_with_random.md)
**Complexity:** Hashmap O(n) time / O(n) space；Interleaving O(n) time / O(1) extra space
- **Trigger:** Linked list 含 `random` 指標，要 deep copy；不能讓 new list 指回 old node
- **Insight:** hashmap 直觀；O(1) 解法把 copy 插在原 node 後當作 in-place 的 hashmap
- **Pitfall:** Interleaving pass 3 要 reset cursor、同步還原原 list、收尾 nullptr
