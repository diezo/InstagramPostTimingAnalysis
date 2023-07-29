from ensta import AutoHost
from time import time
import sys
import os

BLUE = "\033[94m"
GREEN ="\033[92m"
END = "\033[0m"

target = sys.argv[1]
load_following = len(sys.argv) > 2 and sys.argv[2] == "load"

login_username = "heysoniiii"
login_password = "7aczLPg$yBziAF3qqLa6xX&qDdf?YGf@5SM$DoQQ"

print(f"{BLUE}Authenticating as {login_username}...{END}")
host = AutoHost(login_username, login_password, file="session.txt")


def create_results_directory():
    if not os.path.exists("results") or not os.path.isdir("results"): os.mkdir("results")


if load_following and os.path.exists("./sorted-followings.txt"):
    print(f"{BLUE}Loading inspections...{END}")

    with open("./sorted-followings.txt", "r") as file:
        usernames = file.readlines()
        followings_list = []

        for each in usernames:
            followings_list.append((each.replace("\n", ""), None))
else:
    print()
    followings = host.followings(target)

    followings_list = []

    for following in followings:
        print(f"Inspecting {BLUE}{following.username}{END}...")
        profile = host.profile(following.username)
        followings_list.append((following.username, profile.total_post_count))

    followings_list.sort(key = lambda x:x[1])

    with open("./sorted-followings.txt", "w") as file:
        usernames = []

        for username, _ in followings_list:
            usernames.append(username + "\n")

        file.writelines(usernames)

print("\n")

result_storage = f"{str(time())}.txt"

total_searches = 0
total_likes = 0

for username, _ in followings_list:
    posts = host.posts(username)
    
    for post in posts:
        likers = post.likers().users
        liked = False

        for liker in likers:
            if liker.username == target:
                create_results_directory()
                with open(f"./results/{result_storage}", "a") as file:
                    file.write(post.share_url + "\n")

                liked = True
                total_likes += 1
        
        if liked:
            print(f"Searched {GREEN}{username}{END}: {post.share_url}")
        else:
            print(f"Searched {BLUE}{username}{END}: {post.share_url}")
        
        total_searches += 1

print(f"\nLikes: {str(total_likes)}/{str(total_searches)}")
