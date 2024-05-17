### User

- userId: int
- userName: string
- password: string

#### Methods

- login()
- logout()

---

### Diary

- diaryId: int
- date: date
- content: string

#### Methods

- createDiary(content: string)
- deleteDiary(diaryId: int)
- viewDiaries()
- editDiary(diaryId: int, newContent: string)

---

### EmotionAI

- botId: int
- botName: string

#### Methods

- analyzeContent(content: string): AnalysisResult
- generateResponse(query: string): string

---

### AnalysisResult

- analysisId: int
- emotion: string
- emotion_degree: float
- date: date

---

### Conversation

- conversationId: int
- startTime: datetime
- endTime: datetime
- messages: list[Message]

#### Methods

- startConversation()
- endConversation()
- addMessage(message: Message)

---

### Message

- messageId: int
- content: string
- timestamp: datetime
- sender: string  // "User" or "EmotionAI"
