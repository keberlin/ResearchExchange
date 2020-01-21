from datetime import datetime
from flask import Flask, request, jsonify, abort

from books import Books
from users import Users
from subscriptions import Subscriptions

# Flask application
application = Flask(__name__)
application.debug = True

# Initialise the books data (from books.json)
books = Books()

# Initialise the list of users
users = Users()

# Initialise the list of subscriptions
subscriptions = Subscriptions()

# Route for api 'request' GET
@application.route("/request", methods=["GET"])
def request_get():
    id = request.args.get("id")

    if id is not None:
        id = int(id)
        user = users.find_by_id(id)
        if not user:
            abort(404, "user id '%d' not found" % (id))

        subs = subscriptions.find_by_user(id)

        ret = {
            "email": user.email,
            "titles": [books.find_by_id(x.book).title for x in subs],
            "id": user.id,
            "timestamp": datetime.utcnow(),
        }

    else:
        data = []
        for user in users.users:
            subs = subscriptions.find_by_user(user.id)

            data.append(
                {"email": user.email, "titles": [books.find_by_id(x.book).title for x in subs], "id": user.id,}
            )

        ret = {
            "users": data,
            "timestamp": datetime.utcnow(),
        }

    return jsonify(ret)


# Route for api 'request' POST
@application.route("/request", methods=["POST"])
def request_post():
    data = request.get_json()

    if data is None:
        abort(400, "no data specified")
    if "email" not in data:
        abort(400, "email not specified")
    if "title" not in data:
        abort(400, "title not specified")

    email = data["email"]
    title = data["title"]

    # Look up the book using its title
    book = books.find_by_title(title)
    if not book:
        abort(404, "book title '%s' not found" % (title))

    # See if the user has already registered
    user = users.find_by_email(email)
    if not user:
        user = users.create_new_user(email)

    subscriptions.create_new_subscription(user.id, book.id)

    ret = {
        "email": user.email,
        "title": title,
        "id": user.id,
        "timestamp": datetime.utcnow(),
    }

    return jsonify(ret)


# Route for api 'request' DELETE
@application.route("/request", methods=["DELETE"])
def request_delete():
    id = request.args.get("id")

    if id is None:
        abort(400, "id not specified")

    id = int(id)
    user = users.find_by_id(id)
    if not user:
        abort(404, "user id '%d' not found" % (id))

    # Remove all subscriptions for this user
    subs = subscriptions.find_by_user(id)
    subscriptions.delete_subscriptions(subs)

    # Remove this user
    users.delete_user(user)

    ret = {
        "id": id,
        "timestamp": datetime.utcnow(),
    }

    return jsonify(ret)


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=81)
