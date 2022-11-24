import os

with open("IPs.txt") as file:
    park = file.read()
    park = park.splitlines()
    print(" {park}  \n")
    # ping for each ip in the file
for ip in park:
    response = os.popen(f"ping -c 4 {ip} ").read()
    # Pinging each IP address 4 times

    # saving some ping output details to output file
    if ("Request timed out." or "unreachable") in response:
        print(response)
        f = open("ip_output.txt", "a")
        f.write(str(ip) + " link is down" + "\n")
        f.close()
    else:
        print(response)
        f = open("ip_output.txt", "a")
        f.write(str(ip) + " is up " + "\n")
        f.close()
    # print output file to screen
with open("ip_output.txt") as file:
    output = file.read()
    f.close()
    print(output)
with open("ip_output.txt", "w") as file:
    pass
