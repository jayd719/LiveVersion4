def userInfo(requests):
    printFunction = True
    if printFunction:
        print(f"{requests.get_full_path()}:{requests.get_host()}:{requests.user.first_name}:{requests.user.password}")