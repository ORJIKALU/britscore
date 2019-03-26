from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABckz8Q44fJteqGcpfljbecJLHfUoQOa3k-nZF7O8GxPUki-_mWwhj4hC7xug-1SIu-njhDmuyVtIOl9vF2v5eKuC87-C7BUsdOF2p3koqgTaa41FqwWE9mO2chdLOQJrTJj5VAgXKiXw3-vI84UVWA3kE_s_epP6LisgvhoMAv0VWbG9wnl0b-fuWsOyYJOCiQJ9Zx'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
