from typing import Tuple

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from linkedin_lookup_agent import linkedin_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scraper_user_tweets
from twitter_lookup_agent import twitter_lookup_agent
from output_parsers import summary_parser,Summary

information = """
Elon Reeve Musk (/ˈiːlɒn mʌsk/; born June 28, 1971) is a businessman known for his key roles in the space company SpaceX and the automotive company Tesla, Inc. 
He is also known for his ownership of X Corp.
 (the company that operates the social media platform X, formerly Twitter), 
 and his role in the founding of the Boring Company, xAI, Neuralink, and OpenAI. 
 Musk is the wealthiest individual in the world; as of January 2025, Forbes estimates his net worth to be US$421 billion.[2]

"""

def ice_break_with(name:str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scraper_user_tweets(username=twitter_username)

    summary_template = """
        given the information about a person from linkedin {information},
        and twitter posts {twitter_posts} I want you to create:
        1. a short summary
        2. two interesting facts about them

        Use both information from twitter and Linkedin
        \n{format_instructions}
"""

    summary_prompt_template = PromptTemplate(input_variables=["information","twitter_posts"],template=summary_template,
        partial_variables={"format_instructions":summary_parser.get_format_instructions()})

    llm = ChatOpenAI(temperature=0,model_name="gpt_3.5-turbo")

    chain = summary_prompt_template | llm | summary_parser

    linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/eden-marco/")

    res:Summary = chain.invoke(input={"information":linkedin_data,"twitter_posts":tweets})

    return res, linkedin_data.get("profile_pic_url")

if __name__ == '__main__':
    
#     print("Hello LangChain")
    
#     summary_template = """
#         given the {information} about a person from I want you to create:
#         1. a short summary
#         2. two interesting facts about them
# """

# summary_prompt_template = PromptTemplate(input_variables=["information"],template=summary_template)

# #llm = ChatOpenAI(temperature=0,model_name="gpt_3.5-turbo")
# llm = ChatOllama(model="llama3")

# chain = summary_prompt_template | llm | StrOutputParser()

# linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/eden-marco/")

# res = chain.invoke(input={"information":linkedin_data})

# print(res)
    print("Ice Breaker Enter")

    ice_break_with(name="Eden Marco")