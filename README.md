# Documentation

## Note to reviewers
I provided the API calls below and some comments about how I implemented them. The feature that I decided to make
was an API call to api/users to allow people to add multiple users to the system. I also made an API call to 
clubs/<club> for clubs to see statistics about their own club. This API call requires basic auth, and when provided with
valid credentials, the api call will return the average rank of the club by students, and a list of students by how
they ranked the club. I felt like this was a good feature to implement because clubs can see how they're faring
in students' rankings, and also get to know which students want to join their club the most, so during the application 
process, they can favor students who want to join their club more. 

I was very unfamiliar with Flask and learned a lot throughout the process; in particular, I referenced 
http://flask.pocoo.org/snippets/8/ when learning how to use basic auth in Flask. Additionally, I used the Postman
tool for testing APIs.

## List of files
1. club_list.json
This is a json with the list of clubs.
2. club_rank.json
This is a json for the clubs/<club> API. It contains a field, updated, which says if there were any users added or any
updates to students' rankings. If updated, the API can simply just use the data present; otherwise, it must re-parse
the users to see what the updated information is. It contains the last accessed data for each club.
3. fun.py
This is the program for step 10.
4. index.py
This is the program for the API calls.
5. users.json
This is a json that contains every user, indexed by their unique id.

## List of API calls
1. GET /api/clubs
    1. Function: Get club information
    2. Input: None
    3. Output: JSON of all the clubs
    4. Notes: None
2. POST /api/clubs
    1. Function: Add new club
    2. Input: JSON with fields "name" and "size", 
        i.e. {"name": "Penn Tech Review", "size": 30}
    3. Output: input JSON
    4. Notes: None
3. GET /api/rankings
    1. Function: Get Jennifer's ranking
    2. Input: N/A
    3. Output: JSON of Jennifer's club ranking
    4. Notes: Can be easily extended to get any user's rankings.
4. POST /api/rankings
    1. Function: Update anyone's ranking
    2. Input: JSON with fields "name" and "size", 
        i.e. {"id": "1", "name": "Penn Tech Review", "rank": 3}
    3. Output: JSON of Jennifer's club ranking
    4. Notes: If you want to update Jennifer's rankings, set "id" to 1
5. POST /api/users
    1. Function: Add a list of new users
    2. Input: LIST of JSONs with fields "Graduation Year", "Password", "PennId", "School", "last", "name", "Ranking",
        where "Ranking" is a list of clubs in their rank 
        i.e.[
              {
                "name": "Jennifer",
                "last": "Song",
                "PennId": "20870823",
                "Graduation Year": "2020",
                "School": "SEAS",
                "Password": "ilovearun6789",
                "Ranking": [
                  "Penn Labs",
                  "Penn Coffee Clubs",
                  "Penn Tech Review",
                  "Totally Not a Frat",
                  "Dining Philosophers",
                  "Hack4Impact"
                ]
              }
            ]
    3. Output: input JSON
    4. Notes: The function will check if all fields are present, and terminate at the first instance of an invalid JSON.
6. GET /api/user/<int:id>
    1. Function: Get a specific user with id: <id>
    2. Input: N/A
    3. Output: JSON of user's information
    4. Notes: You need valid credentials to access this page; username = "pennlabs", password = "pennlabs". I
        implemented this since it is a security concern if everyone has access to this API call. It will return an error
        if no user exists with the id.
7. GET /api/clubs/<club>
    1. Function: Get club information with name: <club>
    2. Input: N/A
    3. Output: JSON of club's information (average rank by user, list of users by rank)
    4. Notes: You need valid credentials to access this page; username = "pennlabs", password = "pennlabs". I
        implemented this since it is a security concern if everyone has access to this API call. This API call also 
        "caches" the most recently visited data. If the version of the data is up to date with the current version,
        it will simply extract the data. Otherwise, if a user has been added/rankings have been updated, it will
        reparse the student database for new data. If the club does not exist, this will return N/A.