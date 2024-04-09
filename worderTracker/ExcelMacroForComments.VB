Sub FitComments()
Dim xComment As Comment
For Each xComment In Application.ActiveSheet.Comments
    xComment.Shape.TextFrame.AutoSize = True
    With xComment.Shape.TextFrame.Characters.Font
        .Size = 23
      End With
    
Next
End Sub
