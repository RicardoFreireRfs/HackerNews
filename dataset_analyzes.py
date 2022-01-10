from csv import reader
import datetime as dt

# Open hacker_news.csv file
read_file = reader(open("hacker_news.csv"))
# hn is a list with the csv data
hn = list(read_file)
# The file's headers is saved at headers
headers = hn[0]
# updating the hn list deleting the header
del hn[0]

# creating lits with the asked, shown and other posts
ask_posts = []
show_posts =[]
other_posts = []

# updating the posts lists
for row in hn:
    title = row[1]
    if title != None and "ask hn" in title.lower():
        ask_posts.append(row)
    elif title != None and "show hn" in title.lower():
        show_posts.append(row)
    else:
        other_posts.append(row)
#print(ask_posts)

# calculating the average of comments
total_ask_comments = 0
total_show_comments = 0
for row in ask_posts:
    num_comments = row[4]
    total_ask_comments = int(num_comments) + total_ask_comments
avg_ask_comments = total_ask_comments/len(ask_posts)

for row in show_posts:
    num_comments = row[4]
    total_show_comments = int(num_comments) + total_show_comments
avg_show_comments = total_show_comments/len(show_posts)
#print(avg_ask_comments, avg_show_comments)

# starting the analyzes of comments over time
result_list = []
for row in ask_posts:
    created_at = row[6]
    n_comments = int(row[4])
    app_v = (created_at, n_comments)
    result_list.append(app_v)

#print(result_list)

# creating dictionaries to analyze comments frequency
counts_by_hour = {}
comments_by_hour = {}

for row in result_list:
    date_c = row[0]
    date_obj =  dt.datetime.strptime(date_c, "%m/%d/%Y %H:%M")
    date_hour = date_obj.hour
    #print(type(date_hour))
    if date_hour not in counts_by_hour:
        counts_by_hour[date_hour] = 1
        comments_by_hour[date_hour] = row[1]
    else:
        counts_by_hour[date_hour] += 1
        comments_by_hour[date_hour] = comments_by_hour[date_hour] + row[1]
        
print(counts_by_hour)
print(comments_by_hour)

avg_by_hour = []

for t in comments_by_hour:
    avg_by_hour.append([t, comments_by_hour[t]/counts_by_hour[t]])
    
print(avg_by_hour)

swap_avg_by_hour = []
for row in avg_by_hour:
    swap = [row[1],row[0]]
    swap_avg_by_hour.append(swap)
    
#print(swap_avg_by_hour)
sorted_swap = sorted(swap_avg_by_hour, reverse=True)
print("Top 5 Hours for Ask Posts Comments  \n", sorted_swap[:5])

for x in sorted_swap[:5]:
    time_t = dt.time(x[1],00)
    time_str = time_t.strftime("%H:%M")
    print("{0}: {1:.2f} average comments per post".format(time_str,x[0]))
