import psycopg2
#importing for Proper date format
from datetime import datetime


# What are the most popular of three articles of all time?
data1 = ("What are the most popular of three articles of all time ?")
query1 = (
    "select articles.title, count(*) as views "
    "from articles inner join log on log.path "
    "like concat('%', articles.slug, '%') "
    "where log.status like '%200%' group by "
    "articles.title, log.path order by views desc limit 3")

# Who are the most popular of article authors of all time?
data2 = ("Who are the most popular of article authors of all time?")
query2 = (
    "select authors.name, count(*) as views from articles inner "
    "join authors on articles.author = authors.id inner join log "
    "on log.path like concat('%', articles.slug, '%') where "
    "log.status like '%200%' group "
    "by authors.name order by views desc")

# which days did more than 1% of requests lead to errors
data3 = ("which days did more than 1% of requests lead to errors?")
query3= (
    "select day, perc from ("
    "select day, round((sum(requests)/(select count(*) from log where "
    "substring(cast(log.time as text), 0, 11) = day) * 100), 2) as "
    "perc from (select substring(cast(log.time as text), 0, 11) as day, "
    "count(*) as requests from log where status like '%404%' group by day)"
    "as log_percentage group by day order by perc desc) as final_query "
    "where perc >= 1")


def connect(db_name="news"):
    """Connect or check database connection"""
    try:
        database = psycopg2.connect("dbname={}".format(db_name))
        cur = database.cursor()
        return database, cur
    except:
        print ("Unable to connect to the database")


def get_query_result(query):
    #Return results
    database, cur = connect()
    cur.execute(query)
    return cur.fetchall()
    database.close()


def print_query_result(query_result):
    print (query_result[1])
    for index, results in enumerate(query_result[0]):
        print ("\t"+str(index+1)+"."+str(results[0])+" - "+str(results[1])+" views")


def print_error_result(query_result):
    print (query_result[1])
    for results in query_result[0]:
        d= results[0]
        date_obj = datetime.strptime(d, "%Y-%m-%d")
        formatted_date = datetime.strftime(date_obj, "%B %d, %Y")        
        print ("\t"+str(formatted_date)+" - "+str(results[1]) + "% errors")


if __name__ == '__main__':
    # get results
    popular3_articles = get_query_result(query1), title1
    popular4_authors = get_query_result(query2), title2
    error_days = get_query_result(query3), title3

    # print results
    print_query_result(popular3_articles)
    print_query_result(popular4_authors)
    print_error_result(error_days)
