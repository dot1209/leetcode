# Google L4 — Practice Sessions

紀錄規則見 [README](README.md)。**Hint 等級與完成狀態要分開看**；下表是依已有對話可驗證的基線，未完成者不算正式通過。

| 日期（台灣） | 題目 | 解題獨立性／提示 | Code 狀態 | L4 品質 | 證據與需回訪項目 |
|---|---|---|---|---|---|
| 2026-11-11 | [[827] Making A Large Island](../problems/union-find/making_a_large_island.md) | Independent AC（使用者提供完整 Code；歷史提示量未完全核實） | 使用者回報 AC | Not Assessed（完整 Mock 未記錄） | DSU、重複 Root 去重；Follow-up 的 Stale Size／Union by Size 證明曾需修正。 |
| 2026-11-14 | [907] Sum of Subarray Minimums | Major Hint（核心 Contribution、Tie-breaking、Stack 規則經引導） | 本段對話中未確認最終 AC | Not Assessed（未完成完整 Coding Round） | Stack Top 時機、Previous ≤ 與 Next <、相同值歸屬、溢位；安排不同題變形驗證。 |
| 2026-11-15 | [[1590] Make Sum Divisible by P](../problems/prefix-sum/make_sum_divisible_by_p.md) | Major Hint（提供同餘條件、查找公式與核心迴圈） | 使用者回報 AC | Not Assessed（未完成完整 Mock） | 自行想到 Prefix Modulo、歷史 Index 查詢和保留最新位置。復盤：C++ 負餘數、`res == n` 排除整段、公式寫對但實作減法順序寫反。用陌生變形回訪。 |
| 2026-11-16 | [[1493] Longest Subarray of 1's After Deleting One Element](../problems/sliding-window/longest_subarray_of_1s_after_deleting_one_element.md) | Not Assessed（先討論任意整數變形，再實作二元版） | 使用者回報 AC | Not Assessed（未完成完整 Mock） | 自行提出滑窗、最多一個異值與視窗長度減一。任意整數版的合法條件經釐清，待實作驗證。 |

## 後續新增格式

每題完成後新增一列，必要時在下方補充：

- **Problem / Date / Cold or Revisit：** LeetCode 編號、日期、是否第一次接觸、若重複則檢查至少間隔 7 個完整日。
- **Initial Approach：** 使用者自己提出的第一個解法與 Time／Space。
- **Hints：** `None / Minor / Major`，以及實際揭露了什麼，不能因為最終 AC 就忘記提示。
- **Code & Proof：** 是否自行實作並 AC；Complexity、Correctness、Edge Cases 是否交代清楚。
- **L4 Quality：** `Strong / Borderline / Weak / Not Assessed`，簡潔列出原因。
- **Weaknesses：** 分別記 Conceptual Gap 與 Implementation Slip。
- **Next Verification：** 用另一道陌生變形驗證，不在 7 天內重複同題。
