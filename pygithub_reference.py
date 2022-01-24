from github import Github, UnknownObjectException

github_object = Github('GITHUB_API_TOKEN')
repository = github_object.get_user().get_repo('coronasafe_plotly_map_urls')

# path in the repository
filename = 'us_case_map_url2.txt'
content = 'boob1'
# create with commit message
# file = repository.create_file(filename, "edit_file via PyGithub", content)

try:
    file = repository.get_contents(filename)
    
    # read file
    file_text = file.decoded_content.decode()
    # print(file_text)
    
    # update file syntax: repository.update_file(path, message, content, sha, branch=NotSet, committer=NotSet, author=NotSet)
    repository.update_file(file.path, "update file test", content, file.sha, branch="main")
# Error raised: github.GithubException.UnknownObjectException: 404 {"message": "Not Found", "documentation_url": "https://docs.github.com/rest/reference/repos#get-repository-content"}
except UnknownObjectException:
    file = repository.create_file("state_maps/" + filename, "create_file via PyGithub", content)

# delete file
# repo.delete_file(file.path, "remove test", file.sha, branch="main")