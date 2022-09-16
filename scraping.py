import pandas as pd
import datetime as dt
import praw
from psaw import PushshiftAPI

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="",
)
api = PushshiftAPI(reddit)

titles = []
createds = []
scores = []
upvote_ratios = []
nums_comments = []

start = int(dt.datetime.now().timestamp())
for i in range(2):
    submissions_generator = api.search_submissions(before=start, subreddit='language_exchange', limit=1000)
    submissions = list(submissions_generator)
    j = 0
    for submission in submissions:
        titles.append(submission.title)
        scores.append(submission.score)
        upvote_ratios.append(submission.upvote_ratio)
        nums_comments.append(submission.num_comments)
        createds.append(dt.datetime.utcfromtimestamp(int(submission.created)).strftime('%Y-%m-%d %H:%M:%S'))

        j += 1
        #print(j)

    YYMMDD = createds[-1][:10].split("-")
    hhmmss = createds[-1][11:].split(":")
    print(YYMMDD)
    print(f"Page {i} done -----------------------------------------------------")

    start = int((dt.datetime(int(YYMMDD[0]), int(YYMMDD[1]), int(YYMMDD[2]), hour=(int(hhmmss[0])), minute=int(hhmmss[1]), second=(int(hhmmss[2]))) + dt.timedelta(seconds=-1)).timestamp())

df = pd.DataFrame({'created': createds, 'title': titles, 'score': scores, 'upvote_ratio': upvote_ratios, 'num_comments': nums_comments})
df.to_excel('lang_exchange_data.xlsx', index=False)