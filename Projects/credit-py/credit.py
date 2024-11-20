
def LuhnsAlgorithm(cardNumber):
    digits = len(cardNumber)
    sum = 0
    isSecond = False

    for i in range(digits - 1, -1, -1):
        d = ord(cardNumber[i]) - ord('0')


        if(isSecond == True):
            d*= 2

        sum+= d//10
        sum+= d%10
        isSecond = not isSecond

    if(sum % 10 == 0):
        return True
    else:
        return False


def masterCard(cardNumber):
    return len(cardNumber) == 16 and (cardNumber.startswith(("51", "52", "53", "54", "55")))


def visa(cardNumber):
    return len(cardNumber) in [13, 16] and cardNumber.startswith("4")


def amex(cardNumber):
    return len(cardNumber) == 15 and (cardNumber.startswith("34") or cardNumber.startswith("37"))


if __name__ == "__main__":
    cardNumber = input("Number: ")

    if(LuhnsAlgorithm(cardNumber)):
        if masterCard(cardNumber):
            print("MASTERCARD")
        elif visa(cardNumber):
            print("VISA")
        elif amex(cardNumber):
            print("AMEX")
        else:
            print("INVALID")
    else:
        print("INVALID")