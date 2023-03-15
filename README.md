# Basketball2023
For basketball project team winter 2023

Contents:
* main.py: runs the model on a given .csv file
* project_marchmadness_scraping.py: scrapes data from the given year on basketball reference
* CSV_Merger.ipynb: merges two .csv files if their 'Team' column is identical
* Json_format.ipynb: converts a .csv into a more easily readable .json file
* merger.py: merges two .csv files using 'Team' column with an outer join
* Module1.bas: Finds and changes many names in an Excel file, creating a column with the changed values
* A variety of other data files and versions

## Download

Download main.py and call it on an ranked .csv file formatted with combined data in the same directory to train the model.
Then input an unranked combined .csv of teams in a March Madness bracket to rank those teams on how well it believes they will do in the tournament.

.csv Input Indexes

0. Num
1. Rk
2. Team
3. Conf
4. W/L
5. AdjEM
6. AdjO
7. AdjD
8. AdjT
9. Luck
10. AdjEM.1
11. OppO
12. OppD
13. AdjEM.2
14. FG
15. FGA
16. FGpct
17. 2PT
18. 2PTA
19. 2PTpct
20. 3PT
21. 3PTA
22. 3PTpct
23. FT
24. FTA
25. FTpct
26. ORB
27. DRB
28. TRB
29. AST
30. STL
31. BLK
32. TOV
33. PF
34. PTS
35. FG_RANK
36. FGA_RANK
37. FGpct_RANK
38. 2PT_RANK
39. 2PTA_RANK
40. 2PTpct_RANK
41. 3PT_RANK
42. 3PTA_RANK
43. 3PTpct_RANK
44. FT_RANK
45. FTA_RANK
46. FTpct_RANK
47. ORB_RANK
48. DRB_RANK
49. TRB_RANK
50. AST_RANK
51. STL_RANK
52. BLK_RANK
53. TOV_RANK
54. PF_RANK
55. PTS_RANK
56. OPP_FG
57. OPP_FGA
58. OPP_FGpct
59. OPP_2PT
60. OPP_2PTA
61. OPP_2PTpct
62. OPP_3PT
63. OPP_3PTA
64. OPP_3PTpct
65. OPP_FT
66. OPP_FTA
67. OPP_FTpct
68. OPP_ORB
69. OPP_DRB
70. OPP_TRB
71. OPP_AST
72. OPP_STL
73. OPP_BLK
74. OPP_TOV
75. OPP_PF
76. OPP_PTS
77. OPP_FG_RANK
78. OPP_FGA_RANK
79. OPP_FGpct_RANK
80. OPP_2PT_RANK
81. OPP_2PTA_RANK
82. OPP_2PTpct_RANK
83. OPP_3PT_RANK
84. OPP_3PTA_RANK
85. OPP_3PTpct_RANK
86. OPP_FT_RANK
87. OPP_FTA_RANK
88. OPP_FTpct_RANK
89. OPP_ORB_RANK
90. OPP_DRB_RANK
91. OPP_TRB_RANK
92. OPP_AST_RANK
93. OPP_STL_RANK
94. OPP_BLK_RANK
95. OPP_TOV_RANK
96. OPP_PF_RANK
97. OPP_PTS_RANK
98. Rank (only in ranked datasets)
99. Round (only in ranked datasets)

And easily scalable to more data.
