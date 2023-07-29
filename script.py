from datetime import datetime
from ensta import AutoHost
from matplotlib import pyplot
import numpy

# Constants
MAX_INDIVIDUAL_POST = 40
MAX_INDIVIDUAL_USER = 100

# Welcome Text
input('''Welcome!
This script helps you analyse your follower list to find the best suitable time for your posts!

Press ENTER key to start analysing...''')

# Authentication
user_credentials = ["heysoniiii", "7aczLPg$yBziAF3qqLa6xX&qDdf?YGf@5SM$DoQQ"]
print(f"Authenticating as \"{user_credentials[0]}\"")
host = AutoHost(user_credentials[0], user_credentials[1], file="session-data.txt")
print()

# Fetch Profile Information
profile = host.profile(user_credentials[0])
if profile is None: raise Exception("Unable to fetch profile to get follower count.")

# Fetch Follower List
followers = host.followers(user_credentials[0], 0)

weights: dict[int, int] = {}

for i, follower in enumerate(followers):
    if follower is None: raise Exception("Unable to fetch own follower list.")

    posts = host.posts(follower.username, 0)  # Fetch Individual Posts

    for j, post in enumerate(posts):
        if post is None: raise Exception("Unable to fetch posts.")
        print(f"User {i + 1}: Post {j + 1};  Total Users: {profile.follower_count}")

        # Taken Timings
        timing = datetime.fromtimestamp(post.taken_at)
        hour = timing.hour if timing.minute <= 30 else timing.hour + 1

        # Increment Weight
        if hour in weights: weights[hour] += 1
        else: weights[hour] = 1

        if j + 1 >= MAX_INDIVIDUAL_POST != 0: break

    if i + 1 >= MAX_INDIVIDUAL_USER != 0: break

    print()

# Calculate X & Y
x = numpy.array(list(weights.keys()))
y = numpy.array(list(weights.values()))

# Log Information
print("Weights: ", end="")
print(weights)
print("X: ", end="")
print(x)
print("Y: ", end="")
print(y)

# Plot Graph
print("Plotting graph...")
pyplot.bar(x, y, width=0.4)
pyplot.show()
