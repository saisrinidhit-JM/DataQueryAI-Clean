# QUESTION SCHEMA

| Field Name | Type | Required | Allowed Values / Reference | Description |
| --- | --- | --- | --- | --- |
| `surveyID` | ObjectId | — | `Survey` | Reference to the survey |
| `questionImage` | String | — | — | Question image (Only for Image questions) |
| `questionType` | String | Yes | `MCQ`, `MCQ_IMAGE`, `MCQ_EMOJI`, `MCQ_NUMBERS`, `DESCRIPTION`, `VIDEO_EMOJI`, `VIDEO_DESCRIPTION`, `VIDEO_RATING`, `VIDEO_LIST`, `IMAGE_EMOJI`, `IMAGE_DESCRIPTION`, `IMAGE_RATING`, `IMAGE_LIST`, `CONDITIONAL_MCQ`, `VIDEO_MCQ`, `MCQ_EXPLANATION`, `MCQ_WITH_OTHERS` | Question format/type |
| `question` | String | Yes | — | Question text |
| `choice` | Array | — | — | List of selectable choices |
| `multiple_answer` | Boolean | No | — | Allows multiple selections |
| `newQuestionType` | String | — | — | Extended/custom question type |
| `answerType` | String | — | — | Expected answer data type |
| `expectedAnswer` | String | — | — | Expected answer value (for validation/logic) |
| `child_question` | Boolean | No | — | Indicates if this is a child question |
| `child_questions` | ObjectId[] | — | `question` | References to child questions (Only for parent questions) |
| `rating_type.isEnabled` | Boolean | No | — | Enables rating-based question |
| `rating_type.low_rating_text` | String | — | — | Label for lowest rating |
| `rating_type.high_rating_text` | String | — | — | Label for highest rating |
| `idealTime` | Number | No | — | Ideal time to answer the question (seconds) |
| `validationQuestion` | Boolean | No | — | Marks this as a validation question |
| `subHeading` | String | — | — | Sub-heading text |
| `statementRankings` | Boolean | — | — | To show the rank in vertical ranking questions. |
| `panelCategoryId` | ObjectId | — | `PanelCategory` | Panel category mapping (Only for panel survey questions) |
| `createdAt` | Date | Auto | — | Question creation timestamp |
| `updatedAt` | Date | Auto | — | Last update timestamp |