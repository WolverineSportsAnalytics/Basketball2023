Attribute VB_Name = "Module1"
Function MassReplace(InputRng As Range, FindRng As Range, ReplaceRng As Range) As Variant()
  Dim arRes() As Variant 'array to store the results
  Dim arSearchReplace(), sTmp As String 'array where to store the find/replace pairs, temporary string
  Dim iFindCurRow, cntFindRows As Long 'index of the current row of the SearchReplace array, count of rows
  Dim iInputCurRow, iInputCurCol, cntInputRows, cntInputCols As Long 'index of the current row in the source range, index of the current column in the source range, count of rows, count of columns

  cntInputRows = InputRng.Rows.Count
  cntInputCols = InputRng.Columns.Count
  cntFindRows = FindRng.Rows.Count

  ReDim arRes(1 To cntInputRows, 1 To cntInputCols)
  ReDim arSearchReplace(1 To cntFindRows, 1 To 2) 'preparing the array of find/replace pairs

  For iFindCurRow = 1 To cntFindRows
    arSearchReplace(iFindCurRow, 1) = FindRng.Cells(iFindCurRow, 1).Value
    arSearchReplace(iFindCurRow, 2) = ReplaceRng.Cells(iFindCurRow, 1).Value
  Next
  
  'Searching and replacing in the source range
  For iInputCurRow = 1 To cntInputRows
  For iInputCurCol = 1 To cntInputCols
    sTmp = InputRng.Cells(iInputCurRow, iInputCurCol).Value
    'Replacing all find/replace pairs in each cell
    For iFindCurRow = 1 To cntFindRows
      sTmp = Replace(sTmp, arSearchReplace(iFindCurRow, 1), arSearchReplace(iFindCurRow, 2))
    Next
    arRes(iInputCurRow, iInputCurCol) = sTmp
    Next
  Next

  MassReplace = arRes
End Function
