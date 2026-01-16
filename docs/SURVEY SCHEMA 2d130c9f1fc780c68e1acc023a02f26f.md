# SURVEY SCHEMA

| Field Name | Type | Default | Allowed Values / Reference | Description |
| --- | --- | --- | --- | --- |
| `name` | String | — | — | Name of the survey |
| `description` | String | — | — | Survey description |
| `surveyCategory` | String | — | — | Category of the survey(Not mandatory) |
| `businessName` | String | — | — | Name of the business that created this survey (Not mandatory) |
| `researchGoal` | String | — | — | Goal of the Survey |
| `expiryDate` | Date | — | — | Survey expiry date |
| `surveyType` | String | — | `bumper`, `normal`, `multipart`, `multipart_child`, `flash_survey` | Type of survey (bumper, multipart, and flash surveys are not currently used) |
| `rewardType` | String | — | `coupon`, `reward` | Type of reward provided for the survey.
If the type is ‘coupon’, check the `instantGc` field. If `instantGc` is true, it is an instant gift card survey.
`reward` ⇒ Cash reward |
| `image` | String | — | — | Survey card preview image |
| `staticDataId` | ObjectId | — | `SurveyStaticData` | Static survey data reference.
(Check SurveyStaticData documentation for more details) |
| `Coupon` | ObjectId[] | — | `Coupon` | IDs of coupons provided for the survey. |
| `Reward` | ObjectId | — | `Reward` | ID of Reward provided for the survey. |
| `businessId` | ObjectId | — | `Business` | ID of business that created the survey. |
| `tag` | String | — | `VIDEO_FIRST_WATCH`, `IMAGE_FIRST_WATCH`, `NORMAL` | This field indicates the type of survey.
`VIDEO_FIRST_WATCH` /`IMAGE_FIRST_WATCH`⇒ Watch video/Image first and answer the survey |
| `videoLink` | String | — | — | Video URL for `VIDEO_FIRST_WATCH` surveys |
| `imageLink` | String | — | — | Image URL for `IMAGE_FIRST_WATCH` surveys |
| `rank` | Number | — | — | Rank of the survey.
Displays the survey on the home screen based on rank. |
| `isPaid` | Boolean | `false` | — | Paid survey flag (Not mandatory) |
| `filters.age` | Number[] | — | — | Target age range |
| `filters.gender` | String[] | — | — | Target gender |
| `filters.place` | String[] | — | — | Target locations |
| `reward_amount` | Number | `0` | — | Reward amount for the survey |
| `status` | Boolean | `false` | — | Survey active/inactive |
| `isDeleted` | Boolean | `false` | — | Soft delete flag |
| `businessIds` | Array | — | — | Based on the businessIds, the survey will be pushed to platforms such as App, Web, IRCTC, and ISKCON. |
| `limit` | Number | `10000` | — | Max responses allowed. |
| `campaignType` | String | — | — | Campaign type |
| `campaignBy` | String | — | — | Campaign owner |
| `surveyPerformance.completed` | Number | `0` | — | Survey Completed count |
| `surveyPerformance.abandoned` | Number | `0` | — | Survey Abandoned count |
| `instantGc` | Boolean | `false` | — | Instant gift card (Value will be true if it is an instant gift card survey) |
| `brandSurvey` | Boolean | `false` | — | To identify the survey is created for jupitermeta or other business.
(Value will be false for daily surveys) |
| `hercules` | Boolean | — | — | Hercules flag |
| `nsSurveyImages` | Object | — | — | Survey preview Image urls |
| `survey_status` | String | `scheduled` | `scheduled`, `live`, `completed` | Survey lifecycle status |
| `versions` | Object[] | — | Embedded schema | Survey version history |
| `versions.type` | String | `created` | — | Version event type |
| `versions.reason` | String | `Survey Created` | — | Reason for version change |
| `versions.time` | Date | — | — | Version timestamp |
| `duration` | String | `1 minute` | — | Estimated time to complete the survey. |
| `validationSurvey` | Boolean | `false` | — | To identify whether it is a validation survey. |
| `newDesign` | Boolean | `true` | — | To change the front end design for the survey. |
| `panelId` | ObjectId | — | `Panel` | Panel survey reference |
| `startTime` | Date | — | — | Survey start time (Only for panel surveys) |
| `endTime` | Date | — | — | Survey end time (Only for panel surveys) |
| `isVerification` | Boolean | — | — | To identify whether it is a verification survey. (Value is true if the survey needs verification.) |
| `createdAt` | Date | Auto | — | Document creation time |
| `updatedAt` | Date | Auto | — | Last update time |