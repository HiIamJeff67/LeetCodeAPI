from datetime import datetime
import json
import requests
from requests.exceptions import HTTPError
from typing import *
from abc import ABC, abstractmethod

from leetcode_queries import LeetCodeQueries


class LeetCodeQuestionFetcher():
    def __init__(
        self, 
        user_agent: str = None,
    ):
        self._GET_ALL_PROBLEMS_URL = "https://leetcode.com/api/problems/all/"
        self._GRAPHQL_URL = "https://leetcode.com/graphql"
        self.leetcode_query = LeetCodeQueries()   # initialize the class to get all the queries
        self.__HEADERS = {
            "Content-Type": "application/json",
            "User-Agent": "" if user_agent == None else user_agent, # use user_agent if it's provided
        }
        
    def _get_clean_json_string(
        self,
        data: json, 
        indent: int = 4,
    ) -> str:
        return json.dumps(data, indent=indent)

    def _get_all_question_jsons(
        self
    ) -> json:
        
        try:
            response = requests.get(self._GET_ALL_PROBLEMS_URL)
            response.raise_for_status()
        except HTTPError as http_error:
            print(f"HTTP error occurred: {http_error}")
        except Exception as error:
            print(f"Other error occurre: {error}")
            
        data = response.json()
        return data

    def _get_daily_challenge(
        self
    ) -> json:
        query = self.leetcode_query.daily_challenge_query
        
        try:
            response = requests.post(
                self._GRAPHQL_URL, 
                json={"query": query}, 
                headers=self.__HEADERS
            )
            response.raise_for_status()
        except HTTPError as http_error:
            print(f"HTTP error occurred: {http_error}")
        except Exception as error:
            print(f"Other error occurred: {error}")
        
        data = response.json()
        return data
    
    def _get_question_info_by_title(
        self,
        title: str, # required
    ) -> json:
        # note that the titleSlug in leetcode is in this form: two-sum(not: Two Sum),
        # since the url of 1. Two Sum is: https://leetcode.com/problems/two-sum/,
        # hence we have to adjust the title which user pass as a parameter
        titleSlug = title.lower().replace(" ", "-")
        query = self.leetcode_query.search_by_title_query
        
        try:
            response = requests.post(
                self._GRAPHQL_URL,
                json={
                    "operationName": "questionData",
                    "variables": { "titleSlug" : titleSlug},
                    "query": query,
                },
                headers=self.__HEADERS
            )
            response.raise_for_status()
        except HTTPError as http_error:
            print(f"HTTP error occurred: {http_error}")
        except Exception as error:
            print(f"Other error occurred: {error}")
            
        data = response.json()
        question_data = data["data"]["question"]
        return question_data
    
    def _get_question_info_by_id(
        self,
        id: int,    # required
    ):
        title: str = None # note that we still have to get the entire question by its title,
        question_json = None   # but we have to first find its title by id
        
        all_question_jsons = self._get_all_question_jsons()
        question_json = all_question_jsons["stat_status_pairs"]
        for data in question_json:
            if data["stat"]["question_id"] == id:
                title = data["stat"]["question__title"]
                break
        if (title == None):
            raise ValueError(f"\n\n\nquestion {id}. is not found, maybe try to search using its title.\n\n\n")
        question_data = self._get_question_info_by_title(title=title)
        return question_data
    
class LeetCodeDailyChallengeInfoFetcher(LeetCodeQuestionFetcher):
    def __init__(
        self,
        user_agent: str = None,
    ):
        super().__init__(user_agent=user_agent)
        # only fetch daily challenge once at the beginning
        self.daily_challenge_json = self._get_daily_challenge()
    
    def get_daily_challenge_title(self) -> str:
        if (self.daily_challenge_json is None): self.daily_challenge_json = self._get_daily_challenge()
        title = self.daily_challenge_json["data"]["activeDailyCodingChallengeQuestion"]["question"]["title"]
        return title
    
    def get_daily_challenge_content(self) -> str:
        if (self.daily_challenge_json is None): self.daily_challenge_json = self._get_daily_challenge()
        content = self.daily_challenge_json["data"]["activeDailyCodingChallengeQuestion"]["question"]["content"]
        return content
    
    def get_daily_challenge_id(self) -> int:
        if (self.daily_challenge_json is None): self.daily_challenge_json = self._get_daily_challenge()
        id = self.daily_challenge_json["data"]["activeDailyCodingChallengeQuestion"]["question"]["questionFrontendId"]
        return int(id)
    
    def get_daily_challenge_difficulty(self) -> str:
        if (self.daily_challenge_json is None): self.daily_challenge_json = self._get_daily_challenge()
        difficulty = self.daily_challenge_json["data"]["activeDailyCodingChallengeQuestion"]["question"]["difficulty"]
        return difficulty
    
    def get_daily_challenge_date(self) -> str:
        if (self.daily_challenge_json is None): self.daily_challenge_json = self._get_daily_challenge()
        date = self.daily_challenge_json["data"]["activeDailyCodingChallengeQuestion"]["date"]
        return date
    
    def get_daily_challenge_url(self) -> str:
        daily_challenge_title = self.get_daily_challenge_title()
        daily_challenge_title_slug = daily_challenge_title.replace(" ", "-").lower()
        url = f"https://leetcode.com/problems/{daily_challenge_title_slug}/"
        return url
    
    def get_daily_challenge_code_snippets(self) -> List[dict]:
        if (self.daily_challenge_json is None): self.daily_challenge_json = self._get_daily_challenge()
        default_code_snippets = self.daily_challenge_json["data"]["activeDailyCodingChallengeQuestion"]["question"]["codeSnippets"]
        
        default_solutions = {}
        for snippet in default_code_snippets:
            code_map = {
                "lang": snippet["lang"],
                "code": snippet["code"],
            }
            default_solutions[snippet["langSlug"]] = code_map
        
        return default_solutions
    
class LeetCodeQuestionFetcherAbstractClass(ABC):
    """
        Note that all the inherited fetcher should overwrite:
        __init__(self, search_key_word, user_agent): super().__init__(user_agent),
        get_question_title(self) -> str,
        get_question_content(self) -> str,
        get_question_id(self) -> str,
        get_question_difficulty(self) -> str,
        get_today(self) -> str,
        get_question_url(self) -> str,
        get_question_code_snippets(self) -> str
    """
    @abstractmethod
    def __init__(self, search_key_word: Union[int, str], user_agent: str = None): pass
    
    @abstractmethod
    def get_question_title(self) -> str: pass
    
    @abstractmethod
    def get_question_content(self) -> str: pass
    
    @abstractmethod
    def get_question_id(self) -> str: pass
    
    @abstractmethod
    def get_question_difficulty(self) -> str: pass
    
    @abstractmethod
    def get_today(self) -> str: pass
    
    @abstractmethod
    def get_question_url(self) -> str: pass
    
    @abstractmethod
    def get_question_code_snippets(self) -> str: pass
    
class LeetCodeQuestionInfoByFrontendIdFetcher(LeetCodeQuestionFetcherAbstractClass, LeetCodeQuestionFetcher):
    def __init__(
        self,
        search_key_word: int = 1,
        user_agent: str = None
    ):
        LeetCodeQuestionFetcherAbstractClass.__init__(
            self=self,  # I know is weird, but we have to provided self to abc
            search_key_word=search_key_word,
            user_agent=user_agent
        )
        LeetCodeQuestionFetcher.__init__(self=self, user_agent=user_agent)  # same as other parent class
        # only specify the id and fetch the question once at the beginning
        self.id = search_key_word
        self.question_json = self._get_question_info_by_id(id=self.id)
        
    def get_question_title(self) -> str:
        if (self.question_json is None):
            self.question_json = self._get_question_info_by_id(id=self.id)
        title = self.question_json["title"]
        return title
    
    def get_question_content(self) -> str:
        if (self.question_json is None):
            self.question_json = self._get_question_info_by_id(id=self.id)
        content = self.question_json["content"]
        return content
    
    def get_question_id(self) -> int:
        return self.id
    
    def get_question_difficulty(self) -> str:
        if (self.question_json is None):
            self.question_json = self._get_question_info_by_id(id=self.id)
        difficulty = self.question_json["difficulty"]
        return difficulty
    
    def get_today(self) -> str: # instead of question date, we usually have to specify today
        now = datetime.now()
        current_year, current_month, current_day = now.year, now.month, now.day
        return str(current_year) + "-" + \
            (str(current_month) if current_month >= 10 else "0" + str(current_month)) + "-" + \
            (str(current_day) if current_day >= 10 else "0" + str(current_day))
            
    def get_question_url(self) -> str:
        question_title_slug = self.get_question_title()
        question_title_slug = question_title_slug.replace(" ", "-").lower()
        url = f"https://leetcode.com/problems/{question_title_slug}/"
        return url
    
    def get_question_code_snippets(self) -> List[str]:
        if (self.question_json is None): 
            self.question_json = self._get_question_info_by_id(id=self.id)
        default_code_snippets = self.question_json["codeSnippets"]
        
        default_solutions = {}
        for snippet in default_code_snippets:
            code_map = {
                "lang": snippet["lang"],
                "code": snippet["code"],
            }
            default_solutions[snippet["langSlug"]] = code_map
        
        return default_solutions
    
class LeetCodeQuestionInfoByTitleFetcher(LeetCodeQuestionFetcherAbstractClass, LeetCodeQuestionFetcher):
    def __init__(
        self,
        search_key_word: str = "Two Sum",
        user_agent: str = None,
    ):
        LeetCodeQuestionFetcherAbstractClass.__init__(
            self=self,  # I know is weird, but we have to provided self to abc
            search_key_word=search_key_word,
            user_agent=user_agent
        )
        LeetCodeQuestionFetcher.__init__(self=self, user_agent=user_agent)  # same as other parent class
        # only specify the title and fetch the question once at the beginning
        self.title = search_key_word
        self.question_json = self._get_question_info_by_title(title=self.title)
        
        
    def get_question_title(self) -> str:
        return self.title

    def get_question_content(self) -> str:
        if (self.question_json is None): 
            self.question_json = self._get_question_info_by_title(title=self.title)
        content = self.question_json["content"]
        return content

    def get_question_id(self) -> int:
        if (self.question_json is None): 
            self.question_json = self._get_question_info_by_title(title=self.title)
        id = self.question_json["questionFrontendId"]
        return id
    
    def get_question_difficulty(self) -> str:
        if (self.question_json is None): 
            self.question_json = self._get_question_info_by_title(title=self.title)
        difficulty = self.question_json["difficulty"]
        return difficulty
    
    def get_today(self) -> str: # instead of question date, we usually have to specify today
        now = datetime.now()
        current_year, current_month, current_day = now.year, now.month, now.day
        return str(current_year) + "-" + \
            (str(current_month) if current_month >= 10 else "0" + str(current_month)) + "-" + \
            (str(current_day) if current_day >= 10 else "0" + str(current_day))
    
    def get_question_url(self) -> str:
        question_title_slug = self.title
        question_title_slug = question_title_slug.replace(" ", "-").lower()
        url = f"https://leetcode.com/problems/{question_title_slug}/"
        return url
    
    def get_question_code_snippets(self) -> List[str]:
        if (self.question_json is None): 
            self.question_json = self._get_question_info_by_title(title=self.title)
        default_code_snippets = self.question_json["codeSnippets"]
        
        default_solutions = {}
        for snippet in default_code_snippets:
            code_map = {
                "lang": snippet["lang"],
                "code": snippet["code"],
            }
            default_solutions[snippet["langSlug"]] = code_map
            
        print(default_code_snippets)
        print(default_solutions)
        
        return default_solutions
