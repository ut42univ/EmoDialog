#  クラス図一覧（2024/05/17）

---
ユーザー (User)
--------------------------------------------------------------
属性:
- userId: int
- userName: string
- password: string

メソッド:
- login(): ユーザーをログインさせる．
- logout(): ユーザーをログアウトさせる．

---
日記 (Diary)
--------------------------------------------------------------
属性:
- diaryId: int
- date: date
- content: string

メソッド:
- createDiary(content: string): 指定された内容の新しい日記を作成する．
- deleteDiary(diaryId: int): 指定されたIDの日記を削除する．
- viewDiaries(): すべての日記を表示する．
- editDiary(diaryId: int, newContent: string): 指定されたIDの日記の内容を編集する．

---
感情AI (EmotionAI)
--------------------------------------------------------------
属性:
- botId: int
- botName: string

メソッド:
- analyzeContent(content: string): 指定された内容の感情を分析する．
- generateResponse(query: string): ユーザーのクエリに対する応答を生成する．

---
分析結果 (AnalysisResult)
--------------------------------------------------------------
属性:
- analysisId: int
- responce: string
- emotion: string
- emotion_degree: 浮動小数点数
- date: date

---
会話 (Conversation)
--------------------------------------------------------------
属性:
- conversationId: int
- startTime: datetime
- endTime: datetime
- messages: メッセージのリスト

メソッド:
- startConversation(): 新しい会話を開始する．
- endConversation(): 会話を終了する．
- addMessage(message: Message): メッセージを会話に追加する．

---
メッセージ (Message)
--------------------------------------------------------------
属性:
- messageId: int
- content: string
- timestamp: datetime
- sender: string (ユーザーまたはEmotionAI)
