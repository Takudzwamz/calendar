
import os
from flask import Flask, jsonify, make_response, render_template, request, session
import ephem
from datetime import datetime, timedelta, date
import calendar
from flask.cli import load_dotenv
import os


app = Flask(__name__)


# -------------------- MOON PHASE CALCULATION -------------------- #

def get_moon_phase(gregorian_date):
    """
    Calculate the moon phase for a given date using ephem.
    Returns a tuple of (phase_name, phase_emoji, illumination_percent)
    """
    if not gregorian_date:
        return None, None, None
    
    try:
        # Parse the date string (YYYY-MM-DD format)
        if isinstance(gregorian_date, str):
            date_obj = datetime.strptime(gregorian_date, '%Y-%m-%d')
        else:
            date_obj = gregorian_date
        
        # Create ephem date
        ephem_date = ephem.Date(date_obj)
        
        # Get moon illumination
        moon = ephem.Moon(ephem_date)
        illumination = moon.phase  # 0-100%
        
        # Find the nearest major phases
        prev_new = ephem.previous_new_moon(ephem_date)
        next_new = ephem.next_new_moon(ephem_date)
        prev_full = ephem.previous_full_moon(ephem_date)
        next_full = ephem.next_full_moon(ephem_date)
        prev_first_quarter = ephem.previous_first_quarter_moon(ephem_date)
        next_first_quarter = ephem.next_first_quarter_moon(ephem_date)
        prev_last_quarter = ephem.previous_last_quarter_moon(ephem_date)
        next_last_quarter = ephem.next_last_quarter_moon(ephem_date)
        
        # Calculate days since new moon (lunar age)
        lunar_age = ephem_date - prev_new
        lunar_cycle = next_new - prev_new
        phase_fraction = lunar_age / lunar_cycle
        
        # Determine phase name and emoji based on phase fraction
        # Lunar cycle: New -> Waxing Crescent -> First Quarter -> Waxing Gibbous -> 
        #              Full -> Waning Gibbous -> Last Quarter -> Waning Crescent -> New
        
        if phase_fraction < 0.0625:
            phase_name = "New Moon"
            phase_emoji = "🌑"
        elif phase_fraction < 0.1875:
            phase_name = "Waxing Crescent"
            phase_emoji = "🌒"
        elif phase_fraction < 0.3125:
            phase_name = "First Quarter"
            phase_emoji = "🌓"
        elif phase_fraction < 0.4375:
            phase_name = "Waxing Gibbous"
            phase_emoji = "🌔"
        elif phase_fraction < 0.5625:
            phase_name = "Full Moon"
            phase_emoji = "🌕"
        elif phase_fraction < 0.6875:
            phase_name = "Waning Gibbous"
            phase_emoji = "🌖"
        elif phase_fraction < 0.8125:
            phase_name = "Last Quarter"
            phase_emoji = "🌗"
        elif phase_fraction < 0.9375:
            phase_name = "Waning Crescent"
            phase_emoji = "🌘"
        else:
            phase_name = "New Moon"
            phase_emoji = "🌑"
        
        return phase_name, phase_emoji, round(illumination, 1)
    
    except Exception as e:
        return None, None, None
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

# -------------------- 1) 6-YEAR CYCLE CONSTANTS -------------------- #

EPOCH = datetime(2019, 3, 20)  # 20 March 2019 => Start of Zadok Year 2019
CYCLE_DAYS = 6 * 364 + 7       # 2191
DAYS_PER_YEAR = 364
PRIEST_OFFSET = 151  # So that 3/20/2019 => day 5 of Gamul's block


# The 24 priests from 1 Chronicles 24
PRIESTS_24 = [
    "Yehoyariv",  # 1) יְהוֹיָרִיב
    "Yedayah",    # 2) יְדַעְיָה
    "Charim",     # 3) חָרִם
    "Seorim",    # 4) שְׂעוֹרִים
    "Malkiyah",   # 5) מַלְכִּיָּה
    "Miyamin",    # 6) מִיָּמִין
    "Haqqots",    # 7) הַקֹּץ  (sometimes “Haqqotz”)
    "Aviyah",     # 8) אֲבִיָּה
    "Yeshua",     # 9) יֵשׁוּעַ
    "Shekhanyah", # 10) שְׁכַנְיָה
    "Elyashiv",   # 11) אֶלְיָשִׁיב
    "Yakim",      # 12) יָקִים
    "Chuppah",    # 13) חוּפָּה
    "Yeshevav",  # 14) יְשֵׁבְאָב (sometimes “Yeshebeab”)
    "Bilgah",     # 15) בִּלְגָּה
    "Immer",      # 16) אִמֵּר
    "Chezir",     # 17) חֵזִיר
    "Hapitzetz",  # 18) הַפִּצֵּץ (sometimes “Happizzez”)
    "Petachyah",  # 19) פְּתַחְיָה
    "Yechezkel",  # 20) יְחֶזְקֵאל
    "Yakhin",     # 21) יָכִין
    "Gamul",      # 22) גָּמוּל
    "Delayah",    # 23) דְּלָיָה
    "Maazyah"     # 24) מַעַזְיָה
]




# -------------------- 2) HELPER: FIND CURRENT CYCLE -------------------- #
def find_current_cycle(gregorian_date):
    """
    Returns a tuple (current_year, cycle_start, next_cycle_start)
    where cycle_start is the Gregorian date for the start of the Zadok year 
    for the current cycle, and next_cycle_start is the start date of the next cycle.
    This works for both dates on/after and before EPOCH.
    """
    if gregorian_date >= EPOCH:
        current_year = 2019
        while get_zadok_year_start(current_year + 1) <= gregorian_date:
            current_year += 1
        return current_year, get_zadok_year_start(current_year), get_zadok_year_start(current_year + 1)
    else:
        # For dates before EPOCH, decrement until the start is <= gregorian_date.
        current_year = 2019 - 1
        while get_zadok_year_start(current_year) > gregorian_date:
            current_year -= 1
        return current_year, get_zadok_year_start(current_year), get_zadok_year_start(current_year + 1)

# -------------------- 3) COUNTED DAY CALCULATION -------------------- #
def get_priestly_day_count(gregorian_date):
    """
    Returns the 'counted' Zadok day offset from EPOCH (2019-03-20) if the date
    falls within the counted portion of a cycle.
    If the date falls within a leap week (non-counted days), returns None.
    Works for dates both after and before EPOCH.
    """
    current_year, cycle_start, next_cycle_start = find_current_cycle(gregorian_date)
    # Counted portion of the cycle runs for 364 days starting at cycle_start
    counted_end = cycle_start + timedelta(days=DAYS_PER_YEAR - 1)  # last counted day
    
    # If the date falls in the leap week (after counted days but before next cycle), no priest serves.
    if cycle_start <= gregorian_date <= counted_end:
        # Date is within counted days; proceed normally.
        offset_in_year = (gregorian_date - cycle_start).days
    elif gregorian_date > counted_end and gregorian_date < next_cycle_start:
        # Date is in the leap week.
        return None
    else:
        # For backward dates, similar check applies.
        if gregorian_date < cycle_start:
            offset_in_year = (gregorian_date - cycle_start).days  # will be negative
            # If date falls in the "reverse leap week" period, return None.
            # (Assuming symmetry: reverse leap week is the period between next_cycle_start of previous cycle and cycle_start.)
            prev_cycle_start = get_zadok_year_start(current_year)
            prev_counted_end = prev_cycle_start + timedelta(days=DAYS_PER_YEAR - 1)
            if gregorian_date > prev_counted_end and gregorian_date < cycle_start:
                return None
        else:
            offset_in_year = (gregorian_date - cycle_start).days

    # Now, count full cycles between EPOCH and cycle_start.
    if gregorian_date >= EPOCH:
        full_years = current_year - 2019  # each contributes 364 counted days
        base_count = full_years * DAYS_PER_YEAR
    else:
        full_years = 2019 - current_year
        base_count = - (full_years * DAYS_PER_YEAR)

    return base_count + offset_in_year

# -------------------- 4) PRIEST ASSIGNMENT -------------------- #
def get_priest_for_date(gregorian_date):
    """
    Returns (priest_name, day_in_7) for the given date.
    If the date is within a leap week (non-counted), returns (None, None).
    """
    day_count = get_priestly_day_count(gregorian_date)
    if day_count is None:
        return None, None  # No priest during the leap week.
    cyclePos = (day_count + PRIEST_OFFSET) % (24 * 7)  # 168-day cycle
    priest_index = cyclePos // 7
    day_in_block = (cyclePos % 7) + 1
    return PRIESTS_24[priest_index], day_in_block


# -------------------- TODAY'S SUMMARY & HOLIDAY COUNTDOWN -------------------- #

def get_todays_summary(gregorian_date, zadok_year_start):
    """
    Returns a summary of today including:
    - Current Tsadak date (month/day)
    - Priest serving
    - Moon phase
    - Is it a Sabbath?
    - Is it a holiday?
    - Days until next Sabbath
    """
    if isinstance(gregorian_date, str):
        gregorian_date = datetime.strptime(gregorian_date, '%Y-%m-%d').date()
    
    # Ensure zadok_year_start is a date object
    if hasattr(zadok_year_start, 'date'):
        zadok_year_start = zadok_year_start.date()
    
    # Calculate Tsadak date
    days_since_start = (gregorian_date - zadok_year_start).days
    
    # Calculate which month and day in Tsadak calendar
    tsadak_month = 1
    tsadak_day = days_since_start + 1
    
    for month in range(1, 13):
        days_in_month = 31 if month in [3, 6, 9, 12] else 30
        if tsadak_day <= days_in_month:
            tsadak_month = month
            break
        tsadak_day -= days_in_month
    
    # Get priest info - convert date to datetime for get_priest_for_date
    gregorian_datetime = datetime.combine(gregorian_date, datetime.min.time())
    priest_name, priest_day = get_priest_for_date(gregorian_datetime)
    
    # Get moon phase
    moon_phase, moon_emoji, moon_illumination = get_moon_phase(gregorian_date.strftime('%Y-%m-%d'))
    
    # Check if Sabbath (Saturday)
    is_sabbath = gregorian_date.weekday() == 5
    
    # Check if holiday
    holiday_name = None
    for hname, details in holidays.items():
        if tsadak_month == details["month"] and tsadak_day in details["days"]:
            holiday_name = hname
            break
    
    # Days until next Sabbath
    current_weekday = gregorian_date.weekday()
    if current_weekday == 5:  # Saturday
        days_until_sabbath = 0
    elif current_weekday == 6:  # Sunday
        days_until_sabbath = 6
    else:
        days_until_sabbath = 5 - current_weekday
    
    return {
        'tsadak_month': tsadak_month,
        'tsadak_day': tsadak_day,
        'priest_name': priest_name,
        'priest_day': priest_day,
        'moon_phase': moon_phase,
        'moon_emoji': moon_emoji,
        'moon_illumination': moon_illumination,
        'is_sabbath': is_sabbath,
        'holiday_name': holiday_name,
        'days_until_sabbath': days_until_sabbath,
        'gregorian_date': gregorian_date.strftime('%Y-%m-%d')
    }


def get_next_holiday(gregorian_date, zadok_year_start):
    """
    Returns the next upcoming holiday with days remaining.
    """
    if isinstance(gregorian_date, str):
        gregorian_date = datetime.strptime(gregorian_date, '%Y-%m-%d').date()
    
    # Ensure zadok_year_start is a date object
    if hasattr(zadok_year_start, 'date'):
        zadok_year_start = zadok_year_start.date()
    
    # Calculate current Tsadak position
    days_since_start = (gregorian_date - zadok_year_start).days
    
    # Build a list of all holidays with their absolute day position in the year
    holiday_list = []
    for hname, details in holidays.items():
        month = details["month"]
        for day in details["days"]:
            # Calculate absolute day position
            abs_day = 0
            for m in range(1, month):
                abs_day += 31 if m in [3, 6, 9, 12] else 30
            abs_day += day
            
            # Get a simpler name for display (first part before /)
            display_name = hname.split('/')[0].strip() if '/' in hname else hname
            # Remove "Day X" suffixes for multi-day feasts
            if "Day " in display_name and display_name.split()[-1].isdigit():
                display_name = ' '.join(display_name.split()[:-2])
            
            holiday_list.append({
                'name': display_name,
                'full_name': hname,
                'month': month,
                'day': day,
                'abs_day': abs_day
            })
    
    # Sort by absolute day
    holiday_list.sort(key=lambda x: x['abs_day'])
    
    # Remove duplicates (keep first occurrence of each feast)
    seen_names = set()
    unique_holidays = []
    for h in holiday_list:
        if h['name'] not in seen_names:
            seen_names.add(h['name'])
            unique_holidays.append(h)
    
    # Current day in year (1-indexed)
    current_day_in_year = days_since_start + 1
    
    # Find next holiday
    for holiday in unique_holidays:
        if holiday['abs_day'] > current_day_in_year:
            days_until = holiday['abs_day'] - current_day_in_year
            return {
                'name': holiday['name'],
                'full_name': holiday['full_name'],
                'month': holiday['month'],
                'day': holiday['day'],
                'days_until': days_until
            }
    
    # If no holiday found this year, get first holiday of next year
    # Calculate days remaining in current year
    total_days_in_year = sum(31 if m in [3, 6, 9, 12] else 30 for m in range(1, 13))
    days_remaining = total_days_in_year - current_day_in_year
    
    if unique_holidays:
        first_holiday = unique_holidays[0]
        days_until = days_remaining + first_holiday['abs_day']
        return {
            'name': first_holiday['name'],
            'full_name': first_holiday['full_name'],
            'month': first_holiday['month'],
            'day': first_holiday['day'],
            'days_until': days_until
        }
    
    return None


# -------------------- 5) YEAR START CALCULATION -------------------- #
def divmod_6(delta):
    cycles, remainder = divmod(delta, 6)
    return cycles, remainder

def get_zadok_year_start(gregorian_year):
    """
    Returns the Gregorian date for the start of the Zadok year labeled 'gregorian_year'
    based on the 6-year cycle (each cycle: 2191 real days = 2184 counted days + 7 leap days).
    This works for both years >= 2019 and years < 2019.
    """
    delta = gregorian_year - 2019
    cycles, remainder = divmod_6(delta)
    total_days = cycles * CYCLE_DAYS + remainder * DAYS_PER_YEAR
    return EPOCH + timedelta(days=total_days)


# -------------------- 2) GENERATE START DATES  -------------------- #

def generate_simplified_calendar_start_dates(start_year, end_year):
    """
    For each 'year' in [start_year..end_year], compute the Zadok year start date
    using the 6-year cycle approach, including years before 2019.
    """
    start_dates = {}
    for year in range(start_year, end_year + 1):
        start_dates[year] = get_zadok_year_start(year)
    return start_dates


def generate_month_data_with_intervals(start_date, days_in_month, month_number):
    """
    Builds day-by-day data for a Zadok month. Unchanged from your code.
    """
    month_data = []
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    padding_days = (start_date.weekday() + 1) % 7
    month_data += [
        {'simplified_date': '', 'gregorian_date': '', 'weekday': None,
         'holiday': None, 'description': None, 'moon_phase': None, 'moon_emoji': None, 'moon_illumination': None}
        for _ in range(padding_days)
    ]
    
    end_date = start_date + timedelta(days=days_in_month - 1)
    month_interval = f"{month_names[start_date.month - 1]}-{month_names[end_date.month - 1]}"
    
    for day in range(1, days_in_month + 1):
        holiday_name, holiday_description = None, None
        is_sabbath = (start_date.weekday() == 5)  # Saturday=5
        
        # Now figure out which priest is serving
        priest_name, priest_day = get_priest_for_date(start_date)
        
        # Get moon phase for this date
        gregorian_date_str = start_date.strftime('%Y-%m-%d')
        moon_phase, moon_emoji, moon_illumination = get_moon_phase(gregorian_date_str)
        
        # Check if it's a holiday
        for hname, details in holidays.items():
            if month_number == details["month"] and day in details["days"]:
                holiday_name, holiday_description = hname, details["description"]
                break
        month_data.append({
            'simplified_date': f"{day:02}",
            'gregorian_date': gregorian_date_str,
            'weekday': (start_date.weekday() + 1) % 7,
            'holiday': holiday_name,
            'description': holiday_description,
            'month_interval': month_interval,
            'is_sabbath': is_sabbath,
             # Store the priest info
            'priest_name': priest_name,
            'priest_day': priest_day,
            # Store moon phase info
            'moon_phase': moon_phase,
            'moon_emoji': moon_emoji,
            'moon_illumination': moon_illumination
        })
        start_date += timedelta(days=1)
    
    while len(month_data) % 7 != 0:
        month_data.append({
            'simplified_date': '',
            'gregorian_date': '',
            'weekday': None,
            'holiday': None,
            'description': None,
            'is_sabbath': False,
            'priest_name': None,
            'priest_day': None,
            'moon_phase': None,
            'moon_emoji': None,
            'moon_illumination': None
        })
    return month_data, month_interval


# -------------------- 3) YEAR INTERVAL CALCULATIONS -------------------- #

def calculate_current_zadok_year_interval():
    """
    Finds which Zadok year 'today' belongs to, returning e.g. "2018-2019" or "2025-2026".
    We do a small local search near the current Gregorian year to find
    the largest Zadok year whose start <= today < next year's start.
    """
    today = datetime.now().date()
    current_greg_year = today.year

    # We'll search a small range around 'current_greg_year'
    possible_years = [current_greg_year - 1, current_greg_year, current_greg_year + 1, current_greg_year + 2]
    # Build (year, start_date)
    year_starts = [(y, get_zadok_year_start(y).date()) for y in possible_years]
    # Sort by the start date
    year_starts.sort(key=lambda tup: tup[1])

    zadok_year = None
    for (y, sdate) in year_starts:
        if sdate <= today:
            zadok_year = y
    if zadok_year is None:
        # fallback if not found
        zadok_year = current_greg_year

    return f"{zadok_year}-{zadok_year + 1}"


def calculate_year_interval_for_requested_year(requested_year):
    """
    If user says ?year=2015, we produce "2015-2016" (Zadok year 2015).
    """
    return f"{requested_year}-{requested_year + 1}"


# -------------------- 4) FLASK ROUTES -------------------- #

@app.route('/export-calendar')
def export_calendar():
    """
    Generate an .ics file with all holidays for the current Tsadak year.
    """
    requested_year = request.args.get('year', default=None, type=int)
    
    if requested_year:
        year_interval = calculate_year_interval_for_requested_year(requested_year)
    else:
        year_interval = calculate_current_zadok_year_interval()
    
    start_year, end_year = map(int, year_interval.split('-'))
    
    # Get the Zadok year start date
    start_dates = generate_simplified_calendar_start_dates(start_year, start_year)
    zadok_start = start_dates[start_year]
    
    # Build ICS content
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Tsadak Calendar//Biblical Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:Tsadak Calendar {year_interval}",
    ]
    
    # Add each holiday
    for holiday_name, details in holidays.items():
        month = details["month"]
        for day in details["days"]:
            # Calculate the Gregorian date for this holiday
            days_offset = 0
            for m in range(1, month):
                days_offset += 31 if m in [3, 6, 9, 12] else 30
            days_offset += day - 1
            
            holiday_date = zadok_start + timedelta(days=days_offset)
            date_str = holiday_date.strftime('%Y%m%d')
            
            # Create unique ID
            uid = f"{date_str}-{holiday_name.replace(' ', '-').replace('/', '-')}@tsadakcalendar"
            
            # Clean description for ICS (escape special chars)
            description = details["description"].replace('\n', '\\n').replace(',', '\\,').replace(';', '\\;')
            
            ics_lines.extend([
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTART;VALUE=DATE:{date_str}",
                f"DTEND;VALUE=DATE:{(holiday_date + timedelta(days=1)).strftime('%Y%m%d')}",
                f"SUMMARY:{holiday_name}",
                f"DESCRIPTION:{description[:500]}",  # Limit description length
                "STATUS:CONFIRMED",
                "TRANSP:TRANSPARENT",
                "END:VEVENT",
            ])
    
    ics_lines.append("END:VCALENDAR")
    ics_content = "\r\n".join(ics_lines)
    
    response = make_response(ics_content)
    response.headers["Content-Type"] = "text/calendar; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename=tsadak-calendar-{year_interval}.ics"
    return response


@app.route('/set-date')
def set_date():
    local_date = request.args.get('date')
    session['local_date'] = local_date
    return jsonify({"message": "Local date received", "date": local_date})


@app.route('/sitemap.xml')
def sitemap():
    year_interval = calculate_current_zadok_year_interval()
    current_date = date.today().isoformat()
    sitemap_xml = render_template('sitemap_template.xml', year_interval=year_interval, current_date=current_date)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@app.route('/robots.txt')
def robots_txt():
    return app.send_static_file('robots.txt')


@app.route('/')
def home():
    requested_year = request.args.get('year', default=None, type=int)

    if requested_year:
        year_interval = calculate_year_interval_for_requested_year(requested_year)
    else:
        year_interval = calculate_current_zadok_year_interval()

    start_year, end_year = map(int, year_interval.split('-'))
    today = datetime.now().date()

    # Generate the start date for 'start_year'
    start_dates = generate_simplified_calendar_start_dates(start_year, start_year)
    start_date = start_dates[start_year]
    zadok_new_year_str = start_date.strftime('%Y-%m-%d')
    zadok_year_start = start_date  # Keep as date object for calculations

    # Retrieve or set local_date
    local_date = session.get('local_date', today.strftime('%Y-%m-%d'))
    stored_date = datetime.strptime(local_date, '%Y-%m-%d').date()

    if stored_date < today:
        local_date = today.strftime('%Y-%m-%d')
        session['local_date'] = local_date

    # Get today's summary and next holiday countdown using ACTUAL current year
    # (not the selected/viewed year)
    current_year_interval = calculate_current_zadok_year_interval()
    current_start_year = int(current_year_interval.split('-')[0])
    current_year_start_dates = generate_simplified_calendar_start_dates(current_start_year, current_start_year)
    current_zadok_year_start = current_year_start_dates[current_start_year]
    
    todays_summary = get_todays_summary(today, current_zadok_year_start)
    next_holiday = get_next_holiday(today, current_zadok_year_start)

    months_data, month_intervals = {}, {}
    for month_number in range(1, 13):
        days_in_month = 31 if month_number in [3, 6, 9, 12] else 30
        month_data, month_interval = generate_month_data_with_intervals(
            start_date, days_in_month, month_number
        )
        months_data[month_number] = month_data
        month_intervals[month_number] = month_interval
        start_date += timedelta(days=days_in_month)

    return render_template(
        'calendar.html',
        months_data=months_data,
        month_intervals=month_intervals,
        year_interval=year_interval,
        local_date=local_date,
        today=today.strftime('%Y-%m-%d'),
        zadok_new_year=zadok_new_year_str,
        todays_summary=todays_summary,
        next_holiday=next_holiday,
        start_year=start_year,
        end_year=end_year
    )


@app.route('/instructions')
def instructions():
    return render_template('instructions.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

