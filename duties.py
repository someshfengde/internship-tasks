from duty import duty


@duty
def docs(ctx):
    ctx.run("mkdocs build", title="Building documentation")
