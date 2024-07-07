import requests


def search_specific_worksheet(roll, sem, sub, week):
    pdf_url = f"https://iare-data.s3.ap-south-1.amazonaws.com/uploads/STUDENTS/{roll}/LAB/SEM{sem}/{sub}/{roll}_week{week}.pdf"
    res = requests.head(pdf_url)
    if res.status_code == 200:
        return pdf_url
    else:
        return None


def next_roll(roll):
    is_number = roll[8:].isdigit()

    if is_number and int(roll[8:]) < 99:
        return roll[:8] + str(int(roll[8:]) + 1).zfill(2)
    elif is_number and int(roll[8:]) == 99:
        return roll[:8] + "A0"
    elif int(roll[9]) < 9:
        return roll[:9] + str(int(roll[9]) + 1)
    elif roll[9] == "9" and roll[8] != "Z":
        return roll[:8] + chr(ord(roll[8]) + 1) + "0"
    elif roll[8] == "Z":
        return roll[:8] + "00"


def bulk_rolls(from_roll, to_roll):
    from_roll = from_roll.upper()
    to_roll = to_roll.upper()
    roll = []
    current_roll = from_roll

    while current_roll != next_roll(to_roll) and len(roll) <= 80:
        roll.append(current_roll)
        current_roll = next_roll(current_roll)

    return roll


def search_bulk_worksheet(rolls, sem, sub, week):
    pdf_urls = []
    for roll in rolls:
        print(roll)
        pdf_url = search_specific_worksheet(roll, sem, sub, week)
        if pdf_url:
            pdf_urls.append([roll, pdf_url])
        else:
            pdf_urls.append([roll, "Not found"])
    if len(pdf_urls) == 0:
        return None
    else:
        return pdf_urls
