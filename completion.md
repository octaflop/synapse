# Completion

In order for this project to be up to my own standards, I would like to
ensure that the following features are implemented:

* Markdown with the following extensions:
	* RSS
	* Footnotes[^1]
	* Codeblocks
* MongoDB should have most of the dynamic site information
	* Markdown & and resultant html should be saved upon posting and putting.
* Markdown should be formatted immediately from the serve in the "editable
  area" fields

* There should also be fenced code, like this[^2]
~~~~{.python}
# python code
from markdown2 import markdown as markdown

def do_it(it):
    ret = {}
    return ret
~~~~

* Media uploads will be simply from the static folder; but scalability options should be available in the settings file.

[^1]: Like this one!

[^2]: Also be sure to do things with the CSS (pygments?)
