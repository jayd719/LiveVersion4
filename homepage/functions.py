def userInfo(requests):
    printFunction = True
    if printFunction:
        print(f"{requests.get_full_path()}:{requests.META['REMOTE_ADDR']}:{requests.user.first_name}:{requests.user.password}")