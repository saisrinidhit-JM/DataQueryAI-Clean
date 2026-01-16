# ANSWER SCHEMA

| Field Name | Type | Required | Reference / Allowed Values | Description |
| --- | --- | --- | --- | --- |
| `userId` | ObjectId | — | `User` | Reference to the user who submitted the answer |
| `questionId` | ObjectId | — | `question` | Reference to the Question |
| `surveyId` | ObjectId | — | `Survey` | Reference to the Survey |
| `panelCategoryId` | ObjectId | — | `PanelCategory` | Optional panel category reference. (Only for panel surveys) |
| `answer` | String | Yes | — | User’s answer content |
| `rankId` | Number | — | — | Integer Rank value of selected option. (Only for vertical ranking questions) |
| `rank` | String | — | — | Store the label for the vertical ranking questions. (Only for vertical ranking questions) |
| `mediaLinks` | Array | — | — | Links of user uploaded media. |
| `description` | String | — | — | Stores the explanation for a single option. |
| `parentqId` | ObjectId | — | `question` | Reference to parent question (for multipart questions) |
| `phone` | String | — | — | User phone number (Only for scheduler survey) |
| `fromDate` | Date | — | — | Start date for time-based answers. (Only for scheduler survey) |
| `toDate` | Date | — | — | End date for time-based answers. (Only for scheduler survey) |
| `date` | Date | — | — | To store Date type response(Only for scheduler survey) |
| `time` | String | — | — | To store time type response(Only for scheduler survey) |
| `location` | Boolean | — | — | Stores location data if the question requires it. (Boolean) |
| `location_details` | Object | — | — | Stores location data if the question requires it. |
| `city` | String | — | — | City of the user or answer origin |
| `link` | String | — | — | Link of question media |
| `createdAt` | Date | Auto | — | Document creation timestamp |
| `updatedAt` | Date | Auto | — | Document last update timestamp |