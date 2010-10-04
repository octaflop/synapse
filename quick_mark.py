import markdown
md = markdown.Markdown(
        extensions = ['extra', 'codehilite'],
        output_format ='html4'
)
md.convertFile(input="completion.md", output="completion.html", encoding="utf8")

