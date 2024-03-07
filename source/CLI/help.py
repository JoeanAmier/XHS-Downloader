from click import Context

__all__ = ["help"]


def help(ctx: Context, *args, **kwargs):
    ctx.exit()
