import os
from dotenv import load_dotenv
from typing import *
from pathlib import Path
from bs4 import BeautifulSoup
from get_questions import LeetCodeQuestionInfoByFrontendIdFetcher, LeetCodeQuestionInfoByTitleFetcher, LeetCodeQuestionFetcherAbstractClass

class QuestionByTitleSetter():
    def __init__(
        self,
        init_search_key_word: Union[int, str],
        fetcher: Union[any, None] = None,
        user_agent: str = "",
    ):
        self.fetcher = fetcher(
            search_key_word = init_search_key_word,
            user_agent = user_agent
        )
        self.question_directory_name = None
        
    def get_question_dir_name(self):
        today = self.fetcher.get_today()
        todayWithoutYear = today[4:]
        formatted_date_today = todayWithoutYear.replace("-", "")
        questionId = self.fetcher.get_question_id()
        title = self.fetcher.get_question_title()
        daily_challenge_dir_name = formatted_date_today + "-" + str(questionId) + "_" + title
        
        return daily_challenge_dir_name
    
    def make_question_directory(
        self,
        path_to_target_folder: str, # required
    ) -> bool:
        # get the name of target folder, which should be this form: MMDD-Id_title
        # MM: month, DD: day, Id: question id, title: question title
        folder_name = self.get_question_dir_name()
        self.question_directory_name = folder_name
        
        try:
            # make sure the we don't have double '/' for folder_path
            if path_to_target_folder[-1] == "/": 
                path_to_target_folder = path_to_target_folder[:-1]
            # create the daily challenge code directory with the given path
            folder_path = Path(path_to_target_folder + "/" + folder_name)
            folder_path.mkdir(parents=True, exist_ok=False) # we don't allow to override exist file, so exist_ok=False
            
            return True
        except FileExistsError as error:
            print(f"The folder name: {folder_name} has exist at {path_to_target_folder}: {error}")
            return False
        
    def get_parser_html_text(
        self,
        html_content: str = "",
    ) -> str:
        def format_text_content(text_content: str) -> str:
            text_content = text_content.replace(".", ".\n\n")
            text_content = text_content.replace(":", ":\n")
            text_content = text_content.replace(" Exmaple 1:", "Example 1:")
            text_content = text_content.replace(" Exmaple 2:", "Example 2:")
            text_content = text_content.replace("Input:", "\n - Input:")
            text_content = text_content.replace("Output:", "\n - Output:")
            text_content = text_content.replace("Explanation:", "\n - Explanation:")
            return text_content
        
        soup = BeautifulSoup(html_content, "html.parser")
        text_content = soup.get_text(separator=" ", strip=True)
        text_content = format_text_content(text_content)
        return text_content
    
    def make_question_by_title_solution_file(
        self,
        path_to_target_folder: str,
        question_text_file_name = "question.txt",
        solution_file_types: List[str] = ["cpp"],   # place all the type of the solution file which are needed
    ) -> bool:
        question_text_file_path = path_to_target_folder + "/" + self.question_directory_name + "/" + question_text_file_name
        question_url = self.fetcher.get_question_url()
        try:
            with open(question_text_file_path, "x") as file:
                question_html = self.fetcher.get_question_content()
                question_text = self.get_parser_html_text(question_html)
                file.write(question_text)
        except FileExistsError as error:
            print(f"Expect not to override exist file {question_text_file_name} at {path_to_target_folder}: {error}")
            return False
        
        default_solution_code_map = self.fetcher.get_question_code_snippets()
        for file_type in solution_file_types:
            solution_file_name = path_to_target_folder + "/" + self.question_directory_name + "/Solution." + file_type
            try:
                with open(solution_file_name, "x") as file:    # we use "x" mode to write, but only for not exist file
                    if (file_type == "cpp"):
                        with open("leetcode_solution_cpp_form.txt", "r") as form_file:
                            default_solution_file_content = form_file.read()
                            default_solution_file_content = default_solution_file_content.replace(
                                "place_your_solution_class_here", 
                                default_solution_code_map[file_type]["code"]
                            ).replace(
                                "place_your_question_url_here",
                                question_url
                            )
                            file.write(default_solution_file_content)
                    # the other programing language will be done in the future
            except FileExistsError as error:
                print(f"Expect not to override exist file {solution_file_name} at {path_to_target_folder}: {error}")
                return False
                
        return True

def entire_process(
    question_search_key_word: Union[int, str] = "Two Sum",
    leetcode_fetcher: LeetCodeQuestionFetcherAbstractClass = LeetCodeQuestionInfoByTitleFetcher,
    path_to_target_folder: str = "",
    question_text_file_name: str = "question.txt",
    solution_file_types: List[str] = ["cpp"],   # place all the type of the solution file which are needed
):
    setter = QuestionByTitleSetter(
        init_search_key_word=question_search_key_word, 
        fetcher=leetcode_fetcher,
        user_agent=os.getenv("_USER_AGNET")
    ) 
    setter.make_question_directory(path_to_target_folder)
    setter.make_question_by_title_solution_file(
        path_to_target_folder=path_to_target_folder,
        question_text_file_name=question_text_file_name,
        solution_file_types=solution_file_types
    )


def main():
    # set this variable to fetch the specific question
    question_title = "Course Schedule"
    question_id = 1
    
    # some variable will change along the time
    _path_to_target_folder: str = "../ExamsAndSolutions2024"
    _question_text_file_name: str = "question.txt"
    _solution_file_types: List[str] = [
        "cpp",
        # "c"
        # "java",
        # "python",
        # "python3",
        # "csharp",
        # "javascript",
        # "typescript",
        # "php",
        # "swift",
        # "kotlin",
        # "dart",
        # "golang",
        # "ruby",
        # "scala",
        # "rust",
        # "racket",
        # "erlang",
        # "elixir"
    ]
    
    # initially, load our dotenv file
    load_dotenv()
    
    # run the entire process to generate leetcode Exams and Solutions file into new directory
    entire_process(
        question_search_key_word=question_title,
        leetcode_fetcher=LeetCodeQuestionInfoByTitleFetcher,
        path_to_target_folder=_path_to_target_folder,
        question_text_file_name=_question_text_file_name,
        solution_file_types=_solution_file_types
    )

if __name__ == "__main__":
    main()