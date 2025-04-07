## A SIMPLE LOAN MANAGEMENT SYSTEM API.
User can register, login, request for loan, repay loan, update profile, logout with django simplejwt
Admin can approve, reject loan
User can request for multiple loans only if outstanding loan has been paid and loan status has been changed to paid by the admin

##Endpoints
# register user
http://127.0.0.1:8000/api/register/
![image](https://github.com/user-attachments/assets/7b9a77fd-4d1e-40b9-8ac0-9f5eafd8c8e1)


#login user
[image](https://github.com/user-attachments/assets/5361e7cd-e9c0-43dd-a9bf-24bf282ca28d)

# Get user details
http://127.0.0.1:8000/api/profile/
![image](https://github.com/user-attachments/assets/67b0a2c8-8acb-47b8-a7cc-9ca3dc945905)

# Update User profile
# Before
![image](https://github.com/user-attachments/assets/c8d97a65-fb47-4763-b8e6-4add2aac6676)
# After
![image](https://github.com/user-attachments/assets/3134d6f3-30b4-4eb1-8f1a-65624c627e19)

# Request for loan
http://127.0.0.1:8000/api/request-loan/
![image](https://github.com/user-attachments/assets/0e3e1d87-c313-480b-8950-09ff9c014760)

# view loan details before admin approval
http://127.0.0.1:8000/api/loan-details/
![image](https://github.com/user-attachments/assets/b0504b91-0701-470d-af86-148a9fca45d2)
# Admin view
![image](https://github.com/user-attachments/assets/c48d005d-7f5d-4393-9ddd-a052773e1b21)
# Admin approves
![image](https://github.com/user-attachments/assets/4c99ef69-3e35-4028-98c6-5c8e6731b7fc)

# user loan status changes from pending to approved
![image](https://github.com/user-attachments/assets/cc99aa71-6613-4398-baff-b3f25a5f4470)

# User repays part of the loan
http://127.0.0.1:8000/api/repay-loan/
![image](https://github.com/user-attachments/assets/27984e0f-b770-4f2a-bf26-eb4b11351aa1)

# If user try to request for another loan without full payment of the existence loan, an error occurs
![image](https://github.com/user-attachments/assets/23798992-cd8d-4021-a9f7-f425f97c9bcf)

# check loan balance to see outstanding payment
![image](https://github.com/user-attachments/assets/ce3fa4be-0831-4ccd-8934-91c8d8410bba)
# User makes full payment
![image](https://github.com/user-attachments/assets/978ac224-da54-4f4d-999a-a20cd5892f0c)
# Loan status automatically changes to paid
![image](https://github.com/user-attachments/assets/77c216e4-ffd9-4373-9e15-868cefc376d6)

# User logs out
http://127.0.0.1:8000/api/logout/
![image](https://github.com/user-attachments/assets/9bd93ca8-081c-498a-8d12-31a6a62c83ef)











