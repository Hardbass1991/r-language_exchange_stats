import pandas as pd
import datetime as dt
import praw
from psaw import PushshiftAPI
import re

def includes_age_and_sex(text):
    a = re.search(r"([fmFM][1-9][0-9])", text)
    b = re.search(r"([1-9][0-9][fmFM])", text)
    if a:
        return 1, a.group(1)[-2:] + a.group(1)[:1].upper()
    if b:
        return 1, b.group(1)[:2] + b.group(1)[-1].upper()
    return 0, "NA"

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="",
)
api = PushshiftAPI(reddit)

titles = []
createds = []
texts = []
age_sexs = []
#2022-08-30 (40 pages)
#2019-07-21
start = int((dt.datetime(2019, 7, 21, hour=4, minute=54, second=25) + dt.timedelta(seconds=-1)).timestamp())
for i in range(7):
    submissions_generator = api.search_submissions(before=start, subreddit='language_exchange', limit=1000)
    submissions = list(submissions_generator)
    j = 0
    for submission in submissions:
        title_as = includes_age_and_sex(submission.title)
        selftext_as = includes_age_and_sex(submission.selftext)
        if (title_as[0] + selftext_as[0]):
            titles.append(submission.title)
            createds.append(dt.datetime.utcfromtimestamp(int(submission.created)).strftime('%Y-%m-%d %H:%M:%S'))
            #texts.append(submission.selftext)
            if (title_as[0]):
                age_sexs.append(title_as[1])
            elif (selftext_as[0]):
                age_sexs.append(selftext_as[1])
            j += 1
        #print(j)

    YYMMDD = createds[-1][:10].split("-")
    hhmmss = createds[-1][11:].split(":")
    print(YYMMDD)
    print(f"Page {i + 1} done -----------------------------------------------------")

    start = int((dt.datetime(int(YYMMDD[0]), int(YYMMDD[1]), int(YYMMDD[2]), hour=(int(hhmmss[0])), minute=int(hhmmss[1]), second=(int(hhmmss[2]))) + dt.timedelta(seconds=-1)).timestamp())

df = pd.DataFrame({'created': createds, 'title': titles, 'age_sex': age_sexs})
df.to_excel('lang_exchange_agesex.xlsx', index=False)