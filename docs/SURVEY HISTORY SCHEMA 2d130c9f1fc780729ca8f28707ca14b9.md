# SURVEY HISTORY SCHEMA

| Field Name | Type | Default | Allowed Values / Reference | Description |
| --- | --- | --- | --- | --- |
| `userId` | ObjectId | — | `User` | Reference to the user |
| `surveyId` | ObjectId | — | `Survey` | Reference to the survey |
| `totalQuestions` | Number | — | — | Total number of questions in the survey |
| `answeredQuestions` | Number | — | — | Number of questions answered |
| `answeredQuestionsId` | ObjectId[] | — | `Question` | List of answered question IDs |
| `type` | String | — | `bumper`, `normal`, `multipart` | Survey type |
| `status` | String | — | `started`, 
`progress`, `completed`, `abandoned`, `suspended` | Survey participation status |
| `treeOfLifeStatus` | String | — | `completed`, `suspended` | Survey participation status |
| `reason` | String | — | — | Reason for Termination. (Not mandatory) |
| `surveySource` | ObjectId | — | `Business` | Where the user answered the survey from. |
| `userSource` | ObjectId | — | `Business` | Where the user was onboarded from. |
| `panelId` | ObjectId | — | `Panel` | Panel reference |
| `location` | Object | — | — | Stores location data if the survey requires it. |
| `verificationStatus` | String | — | `started`, `pending`, `approved`, `rejected` | Stores the verification status if the survey requires verification. |
| `verifyAttemptCount` | Number | — | — | Stores the count of how many times the user tried to verify the survey. |
| `createdAt` | Date | Auto | — | Record creation time |
| `updatedAt` | Date | Auto | — | Last update time |