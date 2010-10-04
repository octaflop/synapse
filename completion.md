# Completion

In order for this project to be up to my own standards, I would like to
ensure that the following features are implemented:

* Markdown with the following extensions:
	* <del>RSS</del>
	* <del>Footnotes[^1]</del>
	* <del>Codeblocks</del>[^code]

* <del>MongoDB should have most of the dynamic site information</st>
	* <del>Markdown & and resultant html should be saved upon posting and
          putting.</del>
*<del>Markdown should be formatted immediately from the serve in the "editable
  area" fields</del>

* There should also be fenced code, like this[^2]



* Media uploads will be simply from the static folder; but scalability options should be available in the settings file.


# right on

    #!/usr/bin/python
    from markdown import markdown as markdown
    extensions = ['footnotes', 'fenced_code', 'codehilite']
    text = open('completion.md', 'r').read()
    html = markdown(text, extensions)
    file = open('completion.html', 'w')
    file.write(html)
    file.close()



[^1]: Like this one!

[^2]: Also be sure to do things with the CSS (pygments?)

[^code]: word
