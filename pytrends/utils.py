import pytrends
import pandas as pd

class CategoryRead(object):

    def __init__(self):
        self.pytrend = pytrends.TrendReq()
        categories = self.pytrend.categories()
        self.__pytrendsCategories = categories

    def __get_id_by_category_name(self, graph,searched_tag, tag='children'): 
        key=[] # List to keep track of visited nodes.
        visited=[]
        def inner_get_id_by_name(graph, searched_tag, key, visited, tag='children'):
            if (('name' in graph) and (searched_tag.lower() == graph['name'].lower())):
                key.append(graph["id"])
            elif (tag in graph):
                nodes = [node for node in graph[tag] if node not in visited]
                for node in nodes:
                    visited.append(node)
                    inner_get_id_by_name(node,searched_tag,key,visited)
            return key
        inner_get_id_by_name(graph, searched_tag,key,visited)
        return key[0]

    def get_categpry_id(self, category):
        self.category=category
        return self.__get_id_by_category_name(self.__pytrendsCategories, category)

    def set_related_searches(self, video_category, pytrend_category, google_trends, top_of=100):
        if (video_category not in google_trends.keys()):
            self.pytrend.build_payload(kw_list=[], cat=pytrend_category,gprop='youtube', geo='US',timeframe='today 1-m')
            related_queries_dict = self.pytrend.related_queries()
            if (video_category in related_queries_dict.keys()):
                google_trends[video_category] = self.__get_related_searches(related_queries_dict[video_category])
            else:
                google_trends[video_category] = self.__get_related_searches(related_queries_dict)

            related_queries_dict_topics =self.pytrend.related_topics()
            df = related_queries_dict_topics['top'].head(top_of)
            for item in self.__get_related_topics_trends(df,pytrend_category):
                google_trends[video_category].add(item)
        

    def __get_related_searches(self, related_queries_dict,top_of=100):
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

    def __get_related_topics_trends(self, df:pd.DataFrame,category):
        result = []
        for item in df.loc[df['hasData'] == True]['topic_title'].values:
            result.append(item)
        for topic in df.loc[df['hasData']==True]['topic_mid'].values:

            self.pytrend.build_payload(kw_list=[], cat=category,gprop='youtube', geo='US',timeframe='today 1-m',url=topic)
            related_queries_dict = self.pytrend.related_queries()
            related_topics_results=self.__get_related_searches(related_queries_dict[topic])
            for item in related_topics_results:
                result.append(item)
        return set(result)




