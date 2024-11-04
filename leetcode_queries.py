class LeetCodeQueries():
    def __init__(
        self,
    ):
        self.__SEARCH_BY_TITLE_QUERY = """
            query questionData($titleSlug: String!) {
                question(titleSlug: $titleSlug) {
                    questionId
                    questionFrontendId
                    boundTopicId
                    title
                    titleSlug
                    content
                    translatedTitle
                    translatedContent
                    isPaidOnly
                    difficulty
                    likes
                    dislikes
                    isLiked
                    similarQuestions
                    contributors {
                        username
                        profileUrl
                        avatarUrl
                        __typename
                    }
                    langToValidPlayground
                    topicTags {
                        name
                        slug
                        translatedName
                        __typename
                    }
                    companyTagStats
                    codeSnippets {
                        lang
                        langSlug
                        code
                        __typename
                    }
                    stats
                    hints
                    solution {
                        id
                        canSeeDetail
                        __typename
                    }
                    status
                    sampleTestCase
                    metaData
                    judgerAvailable
                    judgeType
                    mysqlSchemas
                    enableRunCode
                    enableTestMode
                    envInfo
                    libraryUrl
                    __typename
                }
            }
        """
        self.__DAILY_CHALLENGE_QUERY = """
            {
                activeDailyCodingChallengeQuestion {
                    date
                    question {
                        title
                        questionId
                        questionFrontendId
                        difficulty
                        content
                        codeSnippets {
                            lang
                            langSlug
                            code
                            __typename
                        }
                        acRate
                        topicTags {
                            name
                        }
                        stats
                    }
                }
            }
        """
        
    # since we assigned the below two as property,
    # so if we want to call them: just do LeetCodeQueries.search_by_title_query,
    # same as others, just do LeetCodeQueries.daily_question_query, without '()'
    @property
    def search_by_title_query(self) -> str:
        return self.__SEARCH_BY_TITLE_QUERY
    @property
    def daily_challenge_query(self) -> str:
        return self.__DAILY_CHALLENGE_QUERY