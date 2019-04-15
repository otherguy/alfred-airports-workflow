# Q: What is a Dangerfile, anyway? A: See http://danger.systems/

# Sometimes it's a README fix, or something like that - which isn't relevant for
# including in a project's CHANGELOG for example
declared_trivial = github.pr_title.include? "#trivial"

# Check if PR is opened by @dependabot
is_dependabot = github.pr_author == "dependabot[bot]"

# Make it more obvious that a PR is a work in progress and shouldn't be merged yet
if github.pr_title.include? "[WIP]" or github.pr_title.include? "(WIP)"
    auto_label.wip=(github.pr_json["number"])
    fail("PR is classed as Work in Progress") if github.pr_title.include? "[WIP]" or github.pr_title.include? "(WIP)"
else
    auto_label.remove("WIP")
end

# Warn when there is a big PR
warn("Big PR, try to keep changes smaller if you can") if git.lines_of_code > 100

# Check commit message and disable the `subject_length` check
commit_lint.check disable: [:subject_length]

# PEP8 Linter
pep8.config_file = "./.flake8"
pep8.threshold = 10
pep8.lint(use_inline_comments = true)
pep8.count_errors(should_fail = true)

# Mainly to encourage writing up some reasoning about the PR, rather than just leaving a title
fail "Please provide a summary in the Pull Request description" if github.pr_body.length < 5 and not declared_trivial

# Only allow PRs to master
fail "Please re-submit this PR to `master`!" if github.branch_for_base != "master"

# Warn if the PR cannot be merged
can_merge = github.pr_json["mergeable"]
warn("This pull request cannot be merged yet due to merge conflicts. Please resolve them by [rebasing](https://help.github.com/articles/about-git-rebase/).", sticky: false) unless can_merge

# Warn if the PR has no assignees
warn "This PR does not have any assignees!" unless github.pr_json["assignee"]

# Message for edited requirements.txt
message "#{github.html_link("requirements.txt")} was edited!" if git.modified_files.include? "requirements.txt"

# Ensure a clean commit history
if git.commits.any? { |c| c.message =~ /^Merge branch '#{github.branch_for_base}'/ }
  message "It looks like you merged from `#{github.branch_for_base}` in this pull request. Please consider [rebasing](https://help.github.com/articles/about-git-rebase/) to get rid of the merge commits -- you may want to [rewind the `#{github.branch_for_base}` branch and rebase](https://publiclab.org/wiki/contributing-to-public-lab-software#Rewinding+the+master+branch) instead of merging in from `#{github.branch_for_base}`."
end

# Check for TODOs in the code
todo_markdown_string = "### There are TODOs left in your code\n| File/Line | Message |\n| ----- | ------- |\n"
todoist.todos.each do |row|
  todo_markdown_string << "| `#{row.file}:#{row.line_number}` | #{row.text.lines.first.chomp} |\n"
end

todoist.message = 'There are TODOs left in your code!'
todoist.fail_for_todos
markdown todo_markdown_string if todoist.todos.any?
