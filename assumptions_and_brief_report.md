# Assumptions made:
1. A user has interests list containing more than one elements.
2. A user is looking for following things in the population to get matched with:
	1. one must be of opposite sex.
	2. one's age must be lower than the user's age + 5 years and greater than the user's age - 5 years.
	3. one resides in the same city as the user does.
	4. atleast two of the interests match.
3. Using soft delete method to delete a user by updating the status from "active" to "inactive".

# Brief explanation
## Add User Update Endpoint:
Endpoint : /users/{user_id}, HTTP METHOD : PUT and it is expecting updated user details in its payload.
It will update in the following steps:
1. When this API is triggered, firstly we are fetching the user details for the given user_id from the database.
2. then we are converting the existing_user details into dictionary and updating it from the payload we received from API.
3. then we are converting it into User object.
4. Finally we are updating the User object into the database and returning the updated user details to the API response.

## Add User Deletion Endpoint:
Endpoint : /users/{user_id}, HTTP METHOD : DELETE
We have introduced a new column named "status" to store if the user is "active" or "inactive".
1. When this API is triggered, firstly we are fetching the user details for the given user_id from the database.
2. then we update the user's status to "inactive" and save the changes into the database
3. finally, we are returning a success message that the user for the given id has been deleted.

## Find Matches for a User:
Endpoint : /get_potential_matches/{user_id}, HTTP METHOD : GET
1. When this API is triggered, firstly we are fetching the user details for the given user_id from the database.
2. Then we have generated a query using the assumptions we made to get the potential matches.
3. Then we extract all the users satisfying the given assumptions from the database by running the query.
4. Finally we will return all these potential matches to the user.

## Add Email Validation:
- To validate the email, we have exploited the in-built email validator [EmailStr] provided by pydantic and updated the schemas accordingly.