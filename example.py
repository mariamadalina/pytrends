import pytrends as pytrends
import pandas as pd
import numpy as np
# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = pytrends.TrendReq()

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
# pytrend.build_payload(kw_list=[], cat=71,gprop='youtube', geo='US',timeframe='today 1-m', url='/m/07c_l')

# Interest Over Time
# interest_over_time_df = pytrend.interest_over_time()
# print(interest_over_time_df.head())

# # Interest by Region
# interest_by_region_df = pytrend.interest_by_region()
# print(interest_by_region_df.head())

# Related Queries, returns a dictionary of dataframes
# related_queries_dict = pytrend.related_queries()
# print(related_queries_dict)

# Get Google Hot Trends data
# trending_searches_df = pytrend.trending_searches()
# print(trending_searches_df.head())

# Get Google Hot Trends data
# today_searches_df = pytrend.today_searches()
# print(today_searches_df.head())

# # Get Google Top Charts
# top_charts_df = pytrend.top_charts(2018, hl='en-US', tz=300, geo='GLOBAL')
# print(top_charts_df.head())

# Get Google Keyword Suggestions
# suggestions_dict = pytrend.suggestions(keyword='pizza')
# print(suggestions_dict)
# result =pytrend.related_topics()
# print(result)


def get_related_searches(related_queries_dict,top_of=100):
  result = []
  if (related_queries_dict['top'] is not None):

      top5 = related_queries_dict['top'].head(top_of)['query'].values
      for item in top5:
        result.append(item)
  # if (related_queries_dict['rising'] is not None):
  #     top5 = related_queries_dict['rising'].head(top_of)['query'].values
  #     for item in top5:
  #       result.append(item)
  return set(result)
def get_related_topics_trends(df:pd.DataFrame,category):
  result = []
  for item in df.loc[df['hasData'] == True]['topic_title'].values:
      result.append(item)
  for topic in df.loc[df['hasData']==True]['topic_mid'].values:
    pytrend = pytrends.TrendReq()
    pytrend.build_payload(kw_list=[], cat=category,gprop='youtube', geo='US',timeframe='today 1-m',url=topic)
    related_queries_dict = pytrend.related_queries()
    related_topics_results=get_related_searches(related_queries_dict[topic])
    for item in related_topics_results:
        result.append(item)
  return set(result)

# category='Food'
# pytrend = pytrends.TrendReq()
# pytrend.build_payload(kw_list=[], cat=71,gprop='youtube', geo='US',timeframe='today 1-m')
# related_queries_dict_topics =pytrend.related_topics()
# df = related_queries_dict_topics['top'].head(10)
# items = get_related_topics_trends(df,71)
# print(items)


# pytrend = pytrends.TrendReq()
# categories = pytrend.categories()
# top_of=500

# def get_id_by_category_name(graph,searched_tag, tag='children'): 
#   visited = [] # List to keep track of visited nodes.

#   def inner_get_id_by_name(visited,graph,searched_tag,tag='children'):
#     if (tag in graph):
#       nodes = graph[tag]
#       not_viseted = [node for node in nodes if node not in visited]
#       for node in not_viseted:
#         visited.append(node)
#         if (searched_tag.lower() == node['name'].lower()):
#           return node["id"]
#         else:
#           inner_get_id_by_name(visited,node,searched_tag)

#   return inner_get_id_by_name(visited, graph, searched_tag, tag)

# search_category_car =get_id_by_category_name(categories,'Food & Drink')
category_identifier = pytrends.utils.CategoryRead()
categoryId = category_identifier.get_categpry_id('Wildlife')
print('Category',categoryId )
google_trends = {}
category_identifier.set_related_searches("Food", categoryId, google_trends, top_of=100)
print(len(google_trends['Food']))

