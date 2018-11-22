User Details for Doctor and User are stored in individual tables.
UserModel and DoctorModel are both derived from a superclass AppUser.

The password of the user is saved in a hashed format.
To log in the user, we need to hash the input and compare with the saved value in the database.

After validating the password at the time of sign in, a session token is generated which is saved to the database.
This session token is sent with each request from the browser and the user details are derived using the Session Token table based on the session token.
SessionTokenModel stores reference to user of type AppUser.

To log out the user, we simply delete this session token.