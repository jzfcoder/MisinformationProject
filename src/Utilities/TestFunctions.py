class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# print(bcolors.OKCYAN + "Early bird gets the worm... What about the worm? He gets up early and is eaten alive D:" + bcolors.ENDC)

'''
def test_main():
    convert(lst)
'''

def convert(lst): 
      
    return ' '.join(lst) 
      
# Driver code 
lst = ['geeks', 'for', 'geeks'] 
print(convert(lst)) 

'''
if __name__ == "__main__":
    print(bcolors.OKCYAN + "OVERSEE is functional...")
    test_main()
'''