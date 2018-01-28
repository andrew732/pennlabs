from flask import Flask, request, jsonify
import json
from functools import wraps

app = Flask(__name__)


@app.route('/')
def main():
    return "Welcome to PennClubReview!"


@app.route('/api')
def api():
    return "Welcome to the PennClubReview API!"


@app.route('/api/clubs', methods=['GET'])
def get_clubs():
    with open('club_list.json') as j:
        clubs = json.load(j)
    j.close()
    return jsonify(clubs)


@app.route('/api/clubs', methods=['POST'])
def post_clubs():
    fields = {"name", "size"}
    if not request.json or not all(f in request.json for f in fields):
        return "ERROR 400 - Missing fields.", 400

    with open('club_list.json') as j:
        clubs = json.load(j)
    j.close()
    clubs.append(request.get_json())
    with open('club_list.json', 'w') as j:
        json.dump(clubs, j)
    j.close()
    return jsonify(request.get_json()), 201


@app.route('/api/rankings', methods=['GET'])
def get_rankings():
    with open('users.json') as j:
        user = json.load(j)
    j.close()
    return jsonify(user['1']['Ranking'])


@app.route('/api/rankings', methods=['POST'])
def update_rankings():
    fields = {'id', 'name', 'rank'}
    if not request.json or not all(f in request.json for f in fields):
        return 'ERROR 400 - Missing fields.', 400

    with open('users.json') as j:
        user = json.load(j)
    j.close()
    num = request.json['id']
    ranking = user[str(num)]['Ranking']
    ranking.remove(request.json['name'])
    ranking.insert(request.json['rank'] - 1, request.json['name'])
    with open('users.json', 'w') as j:
        json.dump(user, j)
    j.close()
    update()
    return jsonify(ranking)


def update():
    with open('club_rank.json') as j:
        club_rank = json.load(j)
    j.close()
    i = club_rank["Version"]
    i += 1
    club_rank.update({"Version": i})
    with open('club_rank.json', 'w') as j:
        json.dump(club_rank, j)
    j.close()


@app.route('/api/users', methods=['POST'])
def post_user():
    fields = {"Graduation Year", "Password", "PennId", "School", "last", "name", "Ranking"}
    if not request.json:
        return "ERROR 400 - No JSON entered.", 400

    with open('users.json') as j:
        users = json.load(j)
    j.close()
    total_users = len(users)

    # Take in an array of input users, insert one by one after checking validity
    for i in range(0, len(request.json)):
        if not all(f in request.json[i] for f in fields):
            return "ERROR 400 - Missing fields.", 400
        password = request.json[i]["Password"]
        hashed = hash_f(password)
        request.json[i].update({"ID": total_users + i + 1, "Password": hashed})
        users.update({total_users + i + 1: request.json[i]})
    with open('users.json', 'w') as j:
        json.dump(users, j)
    j.close()
    update()
    return jsonify(request.get_json()), 201


def validate(user, password):
    return user == 'pennlabs' and password == 'pennlabs'


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not validate(auth.username, auth.password):
            return "ERROR 404 - Incorrect credentials"
        return f(*args, **kwargs)
    return decorated


@app.route('/api/user/<int:id>', methods=['GET'])
@requires_auth
def get_user(id):
    print(request.view_args['id'])
    with open('users.json') as j:
        users = json.load(j)
    j.close()
    if request.view_args['id'] <= len(users):
        user = users[str(request.view_args['id'])]
        return jsonify(user)
    else:
        return "ERROR 400 - No such user."


@app.route('/api/clubs/<club>', methods=['GET'])
@requires_auth
def get_club_rank(club):
    total_people = 0
    total_rank = 0
    people = {}
    valid = False
    with open('club_list.json') as j:
        club_list = json.load(j)
    j.close()

    for i in range(0, len(club_list)):
        if club_list[i]["name"] == club:
            valid = True
    if not valid:
        return "ERROR 400 - No such club"

    with open('club_rank.json') as j:
        club_rank = json.load(j)
    j.close()
    data_version = club_rank["Version"]
    if club not in club_rank or club_rank[club]["Version"] != data_version:
        with open('users.json') as j:
            users = json.load(j)
        j.close()

        # Run through every user and determine their rank of the club
        for i in range(1, len(users) + 1):
            ranking = users[str(i)]["Ranking"]
            if club in ranking:
                rank = users[str(i)]["Ranking"].index(club) + 1
                total_rank += rank
                total_people += 1
                if rank in people:
                    temp = people.get(rank)
                    temp.append(users[str(i)]["name"] + " " + users[str(i)]["last"])
                    people.update({rank: temp})
                else:
                    people.update({rank: [users[str(i)]["name"] + " " + users[str(i)]["last"]]})
        if total_people > 0:
            return_json = {club: {"Average Rank": total_rank / total_people, "People by Rank": people,
                                  "Version": data_version}}
        else:
            return_json = {club: {"Average Rank": "N/A", "People by Rank": ["N/A"], "Version": data_version}}
        club_rank.update(return_json)
        with open('club_rank.json', 'w') as j:
            json.dump(club_rank, j)
        j.close()
    else:
        return_json = club_rank[club]
    return jsonify(return_json)


def hash_f(password):
    password = str(password)
    h = 13
    for i in range(0, len(password)):
        h = h * 31 + ord(password[i])
    return h


if __name__ == '__main__':
    app.run()
