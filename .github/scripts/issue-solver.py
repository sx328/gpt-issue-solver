import os
import openai
from github import Github


def get_gpt4_response(prompt, max_tokens=50):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


openai.api_key = os.environ["OPENAI_API_KEY"]
github_token = os.environ["ACTION_KEY"]

github_client = Github(github_token)
repo = github_client.get_repo(os.environ["GITHUB_REPOSITORY"])

issue_number = int(os.environ["ISSUE_NUMBER"])
issue = repo.get_issue(number=issue_number)

prompt = f"Help me solve this GitHub issue:\nTitle: {issue.title}\nDescription: {issue.body}\n"
solution = get_gpt4_response(prompt)
issue.create_comment(solution)
print(f"Generated solution for issue {issue.number}: {solution}\n")
