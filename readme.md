### Presto Connect Whatsapp API Documentation
Welcome to the Presto API documentation! This guide provides an overview of the available endpoints, request formats, and response structures for interacting with the Presto API.
#### Base URL
All API requests are made to the following base URL:
```
https://connect.prestoghana.com
#### Authentication
To access the Presto API, you need to include an API key in the request headers.        
```
Header: X-api-presto-app YOUR_API_KEY
```
#### REST ENDPOINTS
1. **Send Message to Connect**
   - **Endpoint:** `/wa/send`
   - **Method:** POST
   - **Description:** Send Message to Connect.
   - **Parameters:**
     - `to` (path) - The ID of the user to retrieve.
     - 'text' (body) -  The message content to be sent.
       - **Response:**
         ```json
         {
           "response" : "Message sent successfully to {to}."
         }

            ```         


2. 


### Events
account.created, account.updatedpayment.created, payment.pending, payment.settled, payment.failed, payment.reversedtransfer.created, transfer.completedquote.created, trade.filled, trade.failedcard.authorization.request, card.authorization.approved, card.settlement.postedyield.deposit, yield.accrual, yield.withdrawalkyc.verified, kyc.review_requiredcompliance.alert


### 