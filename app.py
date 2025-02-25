
import os
from flask import Flask, jsonify, render_template, request, session
import ephem
from datetime import datetime, timedelta, date
import calendar
from flask.cli import load_dotenv
import os
""" from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail """

app = Flask(__name__)
load_dotenv() 

app.secret_key = os.getenv('FLASK_SECRET_KEY')
# Define holidays on the simplified calendar test
holidays = {
    "HEAD OF THE YEAR/ Day of rememberance": {
        "month": 1, "days": [1],
        "description": "First day of the year , (Jubilees 6:23-29) And on the new moon of the first month, and on the new moon of the fourth month, and on the new moon of the seventh month, and on the new moon of the tenth month are the days of remembrance, and the days of the seasons in the four divisions of the year. These are written and ordained as a testimony for ever. And Noah ordained them for himself as feasts for the generations for ever, so that they have become thereby a memorial unto him. And on the new moon of the first month he was bidden to make for himself an ark, and on that (day) the earth became dry and he opened (the ark) and saw the earth. And on the new moon of the fourth month the mouths of the depths of the abyss beneath were closed. And on the new moon of the seventh month all the mouths of the abysses of the earth were opened, and the waters began to descend into them. And on the new moon of the tenth month the tops of the mountains were seen, and Noah was glad. And on this account he ordained them for himself as feasts for a memorial for ever, and thus are they ordained. And they placed them on the heavenly tablets, each had thirteen weeks; from one to another (passed) their memorial, from the first to the second, and from the second to the third, and from the third to the fourth."
    },
    "HEAD OF SUMMER/ Day of rememberance": {
        "month": 4, "days": [1],
        "description": "First day of summer , (Jubilees 6:23-29) And on the new moon of the first month, and on the new moon of the fourth month, and on the new moon of the seventh month, and on the new moon of the tenth month are the days of remembrance, and the days of the seasons in the four divisions of the year. These are written and ordained as a testimony for ever. And Noah ordained them for himself as feasts for the generations for ever, so that they have become thereby a memorial unto him. And on the new moon of the first month he was bidden to make for himself an ark, and on that (day) the earth became dry and he opened (the ark) and saw the earth. And on the new moon of the fourth month the mouths of the depths of the abyss beneath were closed. And on the new moon of the seventh month all the mouths of the abysses of the earth were opened, and the waters began to descend into them. And on the new moon of the tenth month the tops of the mountains were seen, and Noah was glad. And on this account he ordained them for himself as feasts for a memorial for ever, and thus are they ordained. And they placed them on the heavenly tablets, each had thirteen weeks; from one to another (passed) their memorial, from the first to the second, and from the second to the third, and from the third to the fourth."
    },
    "HEAD OF WINTER/ Day of rememberance": {
        "month": 10, "days": [1],
        "description": "First day of the Winter, , (Jubilees 6:23-29) And on the new moon of the first month, and on the new moon of the fourth month, and on the new moon of the seventh month, and on the new moon of the tenth month are the days of remembrance, and the days of the seasons in the four divisions of the year. These are written and ordained as a testimony for ever. And Noah ordained them for himself as feasts for the generations for ever, so that they have become thereby a memorial unto him. And on the new moon of the first month he was bidden to make for himself an ark, and on that (day) the earth became dry and he opened (the ark) and saw the earth. And on the new moon of the fourth month the mouths of the depths of the abyss beneath were closed. And on the new moon of the seventh month all the mouths of the abysses of the earth were opened, and the waters began to descend into them. And on the new moon of the tenth month the tops of the mountains were seen, and Noah was glad. And on this account he ordained them for himself as feasts for a memorial for ever, and thus are they ordained. And they placed them on the heavenly tablets, each had thirteen weeks; from one to another (passed) their memorial, from the first to the second, and from the second to the third, and from the third to the fourth."
    },
    "PASACH/ Passover": {
        "month": 1, "days": [14],
        "description": "These are the appointed feasts of 𐤉𐤄𐤅𐤄, the holy convocations, which you shall proclaim at the time appointed for them. In the first month, on the fourteenth day of the month at twilight, is 𐤉𐤄𐤅𐤄’s Passover.- Leviticus 23:4-5"
    },
    "Feast of Unleavened Bread Day 1": {
        "month": 1, "days": [15],
        "description": "And on the fifteenth day of the same month is the Feast of Unleavened Bread to 𐤉𐤄𐤅𐤄; for seven days you shall eat unleavened bread. On the first day you shall have a holy convocation; you shall not do any ordinary work. But you shall present a food offering to 𐤉𐤄𐤅𐤄 for seven days. On the seventh day is a holy convocation; you shall not do any ordinary work. - Leviticus 23:6-8"
    },
    "Feast of Unleavened Bread Day 2": {
        "month": 1, "days": [16],
        "description": "And on the fifteenth day of the same month is the Feast of Unleavened Bread to 𐤉𐤄𐤅𐤄; for seven days you shall eat unleavened bread. On the first day you shall have a holy convocation; you shall not do any ordinary work. But you shall present a food offering to 𐤉𐤄𐤅𐤄 for seven days. On the seventh day is a holy convocation; you shall not do any ordinary work. - Leviticus 23:6-8"
    },
    "Feast of Unleavened Bread Day 3": {
        "month": 1, "days": [17],
        "description": "And on the fifteenth day of the same month is the Feast of Unleavened Bread to 𐤉𐤄𐤅𐤄; for seven days you shall eat unleavened bread. On the first day you shall have a holy convocation; you shall not do any ordinary work. But you shall present a food offering to 𐤉𐤄𐤅𐤄 for seven days. On the seventh day is a holy convocation; you shall not do any ordinary work. - Leviticus 23:6-8"
    },
    # do for days 4-6
    "Feast of Unleavened Bread Day 4": {
        "month": 1, "days": [18],
        "description": "And on the fifteenth day of the same month is the Feast of Unleavened Bread to 𐤉𐤄𐤅𐤄; for seven days you shall eat unleavened bread. On the first day you shall have a holy convocation; you shall not do any ordinary work. But you shall present a food offering to 𐤉𐤄𐤅𐤄 for seven days. On the seventh day is a holy convocation; you shall not do any ordinary work. - Leviticus 23:6-8"
    },
    "Feast of Unleavened Bread Day 5": {
        "month": 1, "days": [19],
        "description": "And on the fifteenth day of the same month is the Feast of Unleavened Bread to 𐤉𐤄𐤅𐤄; for seven days you shall eat unleavened bread. On the first day you shall have a holy convocation; you shall not do any ordinary work. But you shall present a food offering to 𐤉𐤄𐤅𐤄 for seven days. On the seventh day is a holy convocation; you shall not do any ordinary work. - Leviticus 23:6-8"
    },
    "Feast of Unleavened Bread Day 6": {
        "month": 1, "days": [20],
        "description": "And on the fifteenth day of the same month is the Feast of Unleavened Bread to 𐤉𐤄𐤅𐤄; for seven days you shall eat unleavened bread. On the first day you shall have a holy convocation; you shall not do any ordinary work. But you shall present a food offering to 𐤉𐤄𐤅𐤄 for seven days. On the seventh day is a holy convocation; you shall not do any ordinary work. - Leviticus 23:6-8"
    },
    "Feast of Unleavened Bread Day 7": {
        "month": 1, "days": [21],
        "description": "And on the fifteenth day of the same month is the Feast of Unleavened Bread to 𐤉𐤄𐤅𐤄; for seven days you shall eat unleavened bread. On the first day you shall have a holy convocation; you shall not do any ordinary work. But you shall present a food offering to 𐤉𐤄𐤅𐤄 for seven days. On the seventh day is a holy convocation; you shall not do any ordinary work. - Leviticus 23:6-8"
    },
    "First fruits of Barley": {
        "month": 1, "days": [26],
        "description": "9 And 𐤉𐤄𐤅𐤄 spake unto Moses, saying, 10 Speak unto the children of Israel, and say unto them, When ye be come into the land which I give unto you, and shall reap the harvest thereof, then ye shall bring a sheaf of the firstfruits of your harvest unto the priest: 11 and he shall wave the sheaf before 𐤉𐤄𐤅𐤄, to be accepted for you: on the morrow after the sabbath the priest shall wave it. 15 And ye shall count unto you from the morrow after the sabbath, from the day that ye brought the sheaf of the wave offering; seven sabbaths shall be complete: 16 even unto the morrow after the seventh sabbath shall ye number fifty days; and ye shall offer a new meat offering unto 𐤉𐤄𐤅𐤄. Leviticus 23:9-11,15-16"
    },
    "Second Passover": {
        "month": 2, "days": [14],
        "description": "A second opportunity for those who were unable to participate in the Passover offering at its appointed time. Numbers 9:4-11, 4So Moses told the people to celebrate the Passover 5in the wilderness of Sinai as twilight fell on the fourteenth day of the month. And they celebrated the festival there, just as Yah had commanded Moses.6But some of the men had been ceremonially defiled by touching a dead body, so they could not celebrate the Passover that day. They came to Moses and Aaron that day 7and said, “We have become ceremonially unclean by touching a dead body. But why should we be prevented from presenting Yah’s offering at the proper time with the rest of the Israelites?”8Moses answered, “Wait here until I have received instructions for you from Yah.”9This was Yah’s reply to Moses. 10“Give the following instructions to the people of Israel: If any of the people now or in future generations are ceremonially unclean at Passover time because of touching a dead body, or if they are on a journey and cannot be present at the ceremony, they may still celebrate Yah’s Passover. 11They must offer the Passover sacrifice one month later, at twilight on the fourteenth day of the second month."
    },
    "FIRST FRUITS OF NEW WINE": {
        "month": 5, "days": [3],
        "description": "You shall beginning from the day when you bring the new grain offering to 𐤉𐤄𐤅𐤄, the bread of the First Fruits, seven weeks, seven full weeks, until the day after the seventh Sabbath. You are to count fifty days, then sacrifice new wine as a drink offering.Then the whole people, great and small, may begin to drink of the new wine and to eat grapes from the vines, whether ripe or unripe, for on this day they will make atonement for the wine.So the children of Israel are to rejoice before 𐤉𐤄𐤅𐤄, this being an eternal statute, from generation after generation, wherever they dwell. They shall rejoice this day in the festival of new wine to pour out a fermented drink offering, New Wine, upon the altar of 𐤉𐤄𐤅𐤄, an annual rite. (Temple Scroll – 11Q19-20 cols.19-21)" 
    },
    "FIRST FRUITS OF NEW OIL": {
        "month": 6, "days": [22],
        "description": "What is the Feast of New Oil? We usually see new oil referenced along with the the new grain and new wine as a part of the first fruits offering but the first time we actually see oil mentioned is in Genesis 28, after Jacob had his dream of 𐤉𐤄𐤅𐤄 speaking to him in a place where the heavenly connected with the earthly. When he awoke the next morning he anointed the rock where he laid his head. He called that place “the gate of the Heavens” and by pouring oil on top of it, he set it apart, just like the altar in the tabernacle. We see later it used in Exodus not only in service of the the House of 𐤉𐤄𐤅𐤄 for the sacrifices and fuel for the lamps but also for the service of the priests in order to consecrating them before they began their ministry. From there Israel is told to bring in these first fruits for the Levites and for their work. Because the levites were to work strictly in the tabernacle it was the duty of the nation to supply for them the materials for their service. In Deuteronomy 18:1-5 ESV"
    },
    "Pentecost/First Fruits": {
        "month": 3, "days": [15],
        "description": "9. And 𐤉𐤄𐤅𐤄 spake unto Moses, saying, 10. Speak unto the children of Israel, and say unto them, When ye be come into the land which I give unto you, and shall reap the harvest thereof, then ye shall bring a sheaf of the firstfruits of your harvest unto the priest: 11. and he shall wave the sheaf before 𐤉𐤄𐤅𐤄, to be accepted for you: on the morrow after the sabbath the priest shall wave it. 15. And ye shall count unto you from the morrow after the sabbath, from the day that ye brought the sheaf of the wave offering; seven sabbaths shall be complete: 16. even unto the morrow after the seventh sabbath shall ye number fifty days; and ye shall offer a new meat offering unto 𐤉𐤄𐤅𐤄. Leviticus 23:9-11,15-16"
    },
    
    "Feast of Trumpets/ HEAD OF AUTUMN/FALL / Day of rememberance": {
        "month": 7, "days": [1],
        "description": "23 And 𐤉𐤄𐤅𐤄 spake unto Moses, saying, 24 Speak unto the children of Israel, saying, In the seventh month, in the first day of the month, shall ye have a sabbath, a memorial of blowing of trumpets, an holy convocation. 25 Ye shall do no servile work therein: but ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄. Leviticus 23:23-25.(Jubilees 6:23-29) And on the new moon of the first month, and on the new moon of the fourth month, and on the new moon of the seventh month, and on the new moon of the tenth month are the days of remembrance, and the days of the seasons in the four divisions of the year. These are written and ordained as a testimony for ever. And Noah ordained them for himself as feasts for the generations for ever, so that they have become thereby a memorial unto him. And on the new moon of the first month he was bidden to make for himself an ark, and on that (day) the earth became dry and he opened (the ark) and saw the earth. And on the new moon of the fourth month the mouths of the depths of the abyss beneath were closed. And on the new moon of the seventh month all the mouths of the abysses of the earth were opened, and the waters began to descend into them. And on the new moon of the tenth month the tops of the mountains were seen, and Noah was glad. And on this account he ordained them for himself as feasts for a memorial for ever, and thus are they ordained. And they placed them on the heavenly tablets, each had thirteen weeks; from one to another (passed) their memorial, from the first to the second, and from the second to the third, and from the third to the fourth."
    },
    "Day of Atonement": {
        "month": 7, "days": [10],
        "description": "26 And 𐤉𐤄𐤅𐤄 spake unto Moses, saying, 27 Also on the tenth day of this seventh month there shall be a day of atonement: it shall be an holy convocation unto you; and ye shall afflict your souls, and offer an offering made by fire unto 𐤉𐤄𐤅𐤄 ,And ye shall do no work in that same day: for it is a day of atonement, to make an atonement for you before 𐤉𐤄𐤅𐤄 your Elohim. 32 It shall be unto you a sabbath of rest, and ye shall afflict your souls: in the ninth day of the month at even, from even unto even, shall ye celebrate your sabbath. Leviticus 23:26-28:32"
    },
    "Feast of Tabernacles Day 1": {
        "month": 7, "days": [15],
        "description": "33 And 𐤉𐤄𐤅𐤄 spake unto Moses, saying, 34 Speak unto the children of Israel, saying, The fifteenth day of this seventh month shall be the feast of tabernacles for seven days unto 𐤉𐤄𐤅𐤄, On the first day shall be an holy convocation: ye shall do no servile work therein . 36 Seven days ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: on the eighth day shall be an holy convocation unto you; and ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: it is a solemn assembly; and ye shall do no servile work therein. Leviticus 23:33-36"
    },
    "Feast of Tabernacles Day 2": {
        "month": 7, "days": [16],
        "description": "And 𐤉𐤄𐤅𐤄 spake unto Moses, saying, 34 Speak unto the children of Israel, saying, The fifteenth day of this seventh month shall be the feast of tabernacles for seven days unto 𐤉𐤄𐤅𐤄, On the first day shall be an holy convocation: ye shall do no servile work therein . 36 Seven days ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: on the eighth day shall be an holy convocation unto you; and ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: it is a solemn assembly; and ye shall do no servile work therein. Leviticus 23:33-36"
    },
    "Feast of Tabernacles Day 3": {
        "month": 7, "days": [17],
        "description": "And 𐤉𐤄𐤅𐤄 spake unto Moses, saying, 34 Speak unto the children of Israel, saying, The fifteenth day of this seventh month shall be the feast of tabernacles for seven days unto 𐤉𐤄𐤅𐤄, On the first day shall be an holy convocation: ye shall do no servile work therein . 36 Seven days ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: on the eighth day shall be an holy convocation unto you; and ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: it is a solemn assembly; and ye shall do no servile work therein. Leviticus 23:33-36"
    },
    "Feast of Tabernacles Day 4": {
        "month": 7, "days": [18],
        "description": "And 𐤉𐤄𐤅𐤄 spake unto Moses, saying, 34 Speak unto the children of Israel, saying, The fifteenth day of this seventh month shall be the feast of tabernacles for seven days unto 𐤉𐤄𐤅𐤄, On the first day shall be an holy convocation: ye shall do no servile work therein . 36 Seven days ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: on the eighth day shall be an holy convocation unto you; and ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: it is a solemn assembly; and ye shall do no servile work therein. Leviticus 23:33-36"
    },
    "Feast of Tabernacles Day 5": {
        "month": 7, "days": [19],
        "description": "And 𐤉𐤄𐤅𐤄 spake unto Moses, saying, 34 Speak unto the children of Israel, saying, The fifteenth day of this seventh month shall be the feast of tabernacles for seven days unto 𐤉𐤄𐤅𐤄, On the first day shall be an holy convocation: ye shall do no servile work therein . 36 Seven days ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: on the eighth day shall be an holy convocation unto you; and ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: it is a solemn assembly; and ye shall do no servile work therein. Leviticus 23:33-36"
    },
    "Feast of Tabernacles Day 6": {
        "month": 7, "days": [20],
        "description": "And 𐤉𐤄𐤅𐤄 spake unto Moses, saying, 34 Speak unto the children of Israel, saying, The fifteenth day of this seventh month shall be the feast of tabernacles for seven days unto 𐤉𐤄𐤅𐤄, On the first day shall be an holy convocation: ye shall do no servile work therein . 36 Seven days ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: on the eighth day shall be an holy convocation unto you; and ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: it is a solemn assembly; and ye shall do no servile work therein. Leviticus 23:33-36"
    },
    "Feast of Tabernacles Day 7": {
        "month": 7, "days": [21],
        "description": "And 𐤉𐤄𐤅𐤄 spake unto Moses, saying, 34 Speak unto the children of Israel, saying, The fifteenth day of this seventh month shall be the feast of tabernacles for seven days unto 𐤉𐤄𐤅𐤄, On the first day shall be an holy convocation: ye shall do no servile work therein . 36 Seven days ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: on the eighth day shall be an holy convocation unto you; and ye shall offer an offering made by fire unto 𐤉𐤄𐤅𐤄: it is a solemn assembly; and ye shall do no servile work therein. Leviticus 23:33-36"
    },
    "Day of Addition": {
        "month": 7, "days": [22],
        "description": "39 Also in the fifteenth day of the seventh month, when ye have gathered in the fruit of the land, ye shall keep a feast unto 𐤉𐤄𐤅𐤄 seven days: on the first day shall be a sabbath, and on the eighth day shall be a sabbath. Leviticus 23:39"
    },
}


def ephem_date_to_datetime(ephem_date):
    """
    Convert an ephem.Date object into a datetime.datetime object.
    
    Parameters:
    - ephem_date: The ephem.Date object to convert.
    
    Returns:
    - A datetime.datetime object representing the same point in time.
    """
    # Convert ephem.Date to a string and then parse it with datetime.strptime
    return datetime.strptime(str(ephem_date), '%Y/%m/%d %H:%M:%S')



def find_nearest_wednesday(year):
    """
    Find the nearest Wednesday to the vernal equinox for a given year.
    
    Parameters:
    - year: The year for which to find the vernal equinox.
    
    Returns:
    - A datetime.datetime object representing the nearest Wednesday.
    """
    equinox_date = ephem_date_to_datetime(ephem.next_vernal_equinox(str(year)))
    # Adjust for EDT or any other timezone if necessary. This example assumes UTC.
    days_until_wednesday = (2 - equinox_date.weekday()) % 7
    if days_until_wednesday > 3:
        days_until_wednesday -= 7
    nearest_wednesday = equinox_date + timedelta(days=days_until_wednesday)
    return nearest_wednesday




def generate_simplified_calendar_start_dates(start_year, end_year):
    start_dates = {}
    for year in range(start_year, end_year + 1):
        # Directly use find_nearest_wednesday to get the start date
        nearest_wednesday = find_nearest_wednesday(year)
        start_dates[year] = nearest_wednesday
    return start_dates



def generate_month_data_with_intervals(start_date, days_in_month, month_number):
    month_data = []
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    padding_days = (start_date.weekday() + 1) % 7
    month_data += [{'simplified_date': '', 'gregorian_date': '', 'weekday': None, 'holiday': None, 'description': None} for _ in range(padding_days)]
    
    end_date = start_date + timedelta(days=days_in_month - 1)  # Calculate end date of the month
    month_interval = f"{month_names[start_date.month-1]}-{month_names[end_date.month-1]}"
    
    for day in range(1, days_in_month + 1):
        holiday_name, holiday_description = None, None
        # Determine if the day is a Sabbath (Saturday) by checking if it's the 7th day of the week in the Zadok calendar
        is_sabbath = (start_date.weekday() == 5)  # Sabbath is the 7th day (0-based index for Sunday is 0)
        for holiday, details in holidays.items():
            if month_number == details["month"] and day in details["days"]:
                holiday_name, holiday_description = holiday, details["description"]
                break
        month_data.append({
            'simplified_date': f"{day:02}",
            'gregorian_date': start_date.strftime('%Y-%m-%d'),
            'weekday': (start_date.weekday() + 1) % 7,
            'holiday': holiday_name,
            'description': holiday_description,
            'month_interval': month_interval,  # Add month_interval to each day's data
            'is_sabbath': is_sabbath  # Mark Sabbath days
        })
        start_date += timedelta(days=1)
    
    while len(month_data) % 7 != 0:
        month_data.append({'simplified_date': '', 'gregorian_date': '', 'weekday': None, 'holiday': None, 'description': None, 'is_sabbath': False})
    return month_data, month_interval

def calculate_current_zadok_year_interval():
    today = datetime.now()
    current_year = today.year
    
    # Find nearest Wednesday to the vernal equinox for the current and next year
    nearest_wednesday_this_year = find_nearest_wednesday(current_year)
    nearest_wednesday_next_year = find_nearest_wednesday(current_year + 1)
    
    # Determine the correct year interval based on today's date
    if today < nearest_wednesday_this_year:
        # If today is before this year's nearest Wednesday to the equinox
        year_interval = f"{current_year - 1}-{current_year}"
    elif today >= nearest_wednesday_this_year and today < nearest_wednesday_next_year:
        # If today is after this year's equinox but before the next year's
        year_interval = f"{current_year}-{current_year + 1}"
    else:
        # If today is after the next year's equinox (should rarely happen, but included for completeness)
        year_interval = f"{current_year + 1}-{current_year + 2}"
    
    return year_interval

def calculate_year_interval_for_requested_year(requested_year):
    nearest_wednesday_this_year = find_nearest_wednesday(requested_year)
    nearest_wednesday_next_year = find_nearest_wednesday(requested_year + 1)
    
    # Determine the correct year interval based on the requested year
    if datetime.now() < nearest_wednesday_this_year:
        year_interval = f"{requested_year - 1}-{requested_year}"
    elif datetime.now() >= nearest_wednesday_this_year and datetime.now() < nearest_wednesday_next_year:
        year_interval = f"{requested_year}-{requested_year + 1}"
    else:
        year_interval = f"{requested_year + 1}-{requested_year + 2}"
    
    return year_interval



""" message = Mail(
    from_email='info@sputniktech.co',
    to_emails='mupanesuret48@gmail.com',
    subject='Sending with Twilio SendGrid is Fun', 
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message) """

@app.route('/set-date')
def set_date():
    
    local_date = request.args.get('date')
    # You can store the local date in the session to use it in other routes
    session['local_date'] = local_date
    return jsonify({"message": "Local date received", "date": local_date})


@app.route('/')
def home():
    # Extract the requested year from the query parameter, if present
    requested_year = request.args.get('year', default=None, type=int)

    # Determine the current or requested year interval
    if requested_year:
        year_interval = calculate_year_interval_for_requested_year(requested_year)
    else:
        year_interval = calculate_current_zadok_year_interval()

    start_year, end_year = map(int, year_interval.split('-'))
    today = datetime.now().date()
    start_dates = generate_simplified_calendar_start_dates(start_year, start_year)
    start_date = start_dates[start_year]

    # Retrieve the local date from the session or default to today
    local_date = session.get('local_date', today.strftime('%Y-%m-%d'))
    # Convert stored local_date to a date object for comparison
    stored_date = datetime.strptime(local_date, '%Y-%m-%d').date()

    # If the stored date is before today, update it
    if stored_date < today:
        local_date = today.strftime('%Y-%m-%d')
        session['local_date'] = local_date

    months_data, month_intervals = {}, {}
    for month_number in range(1, 13):
        days_in_month = 31 if month_number in [3, 6, 9, 12] else 30
        month_data, month_interval = generate_month_data_with_intervals(start_date, days_in_month, month_number)
        months_data[month_number] = month_data
        month_intervals[month_number] = month_interval  # Store month intervals
        start_date += timedelta(days=days_in_month)

    return render_template('calendar.html', 
                           months_data=months_data, 
                           month_intervals=month_intervals, 
                           year_interval=year_interval, 
                           local_date=local_date,
                           today=today.strftime('%Y-%m-%d'))


# @app.route('/')
# def home():
#     # Extract the requested year from the query parameter, if present
#     requested_year = request.args.get('year', default=None, type=int)

#     # Determine the current or requested year interval
#     if requested_year:
#         year_interval = calculate_year_interval_for_requested_year(requested_year)
#     else:
#         year_interval = calculate_current_zadok_year_interval()

#     start_year, end_year = map(int, year_interval.split('-'))
#     today = datetime.now().date()
#     start_dates = generate_simplified_calendar_start_dates(start_year, start_year)
#     start_date = start_dates[start_year]
    
    
#     # Retrieve the local date from the session
#     local_date = session.get('local_date', datetime.now().strftime('%Y-%m-%d'))

#     months_data, month_intervals = {}, {}
#     for month_number in range(1, 13):
#         days_in_month = 31 if month_number in [3, 6, 9, 12] else 30
#         month_data, month_interval = generate_month_data_with_intervals(start_date, days_in_month, month_number)
#         months_data[month_number] = month_data
#         month_intervals[month_number] = month_interval  # Store month intervals
#         start_date += timedelta(days=days_in_month)

#     # Pass the calculated year_interval to your template
#     return render_template('calendar.html', months_data=months_data, month_intervals=month_intervals, year_interval=year_interval, local_date=local_date,today=today.strftime('%Y-%m-%d'))

def calculate_year_interval_for_requested_year(requested_year):    
    return f"{requested_year}-{requested_year + 1}"

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)
